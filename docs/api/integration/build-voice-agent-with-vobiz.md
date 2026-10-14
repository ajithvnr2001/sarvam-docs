---
url: https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz/
title: Build a Voice Agent using Vobiz | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:41.503150+00:00
---

# Build a Voice Agent using Vobiz | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz/

Skip to navigation

On this page

  * Overview
  * What You’ll Build
  * Quick Overview
  * Quick Start
  * 1\. Prerequisites
  * 2\. Install Dependencies
  * 3\. Create Environment File
  * 4\. Write the Sarvam Client
  * 5\. Write the Call Session
  * 6\. Write the FastAPI Server
  * 7\. Configure Vobiz to Reach Your Agent
  * 8\. Run and Test Your Agent
  * Audio Formats
  * Customization Examples
  * Hindi Voice Agent
  * Multilingual Agent (Auto-detect)
  * Available Language Codes
  * Speaker Voices (Bulbul v3)
  * Understanding the Call Flow
  * Pro Tips
  * Troubleshooting
  * Additional Resources
  * Need Help?



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

# Build a Voice Agent using Vobiz

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz.md "View this page as plain text")|More actions

This page is for Model APIs.

Want a production voice agent without assembling the stack yourself? [Sarvam Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents) is a managed platform with speech recognition, reasoning, Indian-language voices, telephony, testing, and analytics included, from ₹3 per minute. This guide shows how to build your own pipeline on the APIs instead.

## Overview

This guide shows you how to build a **real-time voice agent that answers phone calls** , using **Vobiz** for telephony and **Sarvam AI** for everything else: speech-to-text, the LLM, and text-to-speech. Unlike the other integration guides in this section, this one doesn’t use Pipecat. Vobiz’s bidirectional media stream is a plain JSON-over-WebSocket protocol, so a small FastAPI server talking to Sarvam’s REST API directly is all you need.

## What You’ll Build

A voice agent that can:

  * Answer inbound phone calls on a Vobiz number
  * Listen to callers speaking, in multiple Indian languages
  * Understand and process what they say, with barge-in support
  * Respond back in a natural-sounding voice, over the phone, sentence by sentence as the reply streams in



## Quick Overview

  1. Get an API key (Sarvam). Vobiz needs no API credentials for this flow.
  2. Install packages: `pip install fastapi httpx python-dotenv python-multipart "uvicorn[standard]"`
  3. Create a `.env` file with your API key and public URL
  4. Write a FastAPI server that speaks Vobiz’s WebSocket media protocol and calls Sarvam directly
  5. Create a Vobiz application pointing at your server, and attach your number to it
  6. Call your Vobiz number



* * *

## Quick Start

### 1\. Prerequisites

  * Python 3.9 or higher
  * [ngrok](https://ngrok.com/download), to expose your local server during development
  * A [Vobiz](https://vobiz.ai/) account with a provisioned voice number
  * A [Sarvam AI](https://dashboard.sarvam.ai/) API key from your dashboard



Vobiz doesn’t need an account SID, auth token, or any credentials in your agent code for this flow. It fetches your **Answer URL** as plain HTTP when a call comes in, and everything it needs to route the call, including the stream and call identifiers, arrives over the WebSocket itself, just like Exotel’s Voicebot Applet.

### 2\. Install Dependencies

###### macOS/Linux

###### Windows
    
    
    pip install fastapi httpx python-dotenv python-multipart "uvicorn[standard]"

This guide talks to Sarvam over plain `httpx` calls rather than the `sarvamai` SDK or Pipecat, so the whole pipeline has one HTTP dependency and one authentication header (`api-subscription-key`). That also means audio format handling, including resampling, WAV wrapping, and container stripping, is your responsibility here, unlike the Pipecat-based guides where the transport and Sarvam services handle it for you.

### 3\. Create Environment File

Create a file named `.env` in your project folder:
    
    
    SARVAM_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx
    
    SARVAM_STT_MODEL=saaras:v4
    
    SARVAM_LLM_MODEL=sarvam-105b
    
    SARVAM_TTS_MODEL=bulbul:v4-flash
    
    PUBLIC_URL=https://your-tunnel.example.com
    
    HTTP_PORT=8000
    
    AGENT_LANGUAGE=en-IN
    
    TTS_SPEAKER=anand
    
    # Vobiz sends caller audio as mu-law at 8 kHz or Linear16 at 16 kHz.
    
    STREAM_CONTENT_TYPE=audio/x-mulaw;rate=8000
    
    OUTBOUND_SAMPLE_RATE=8000

Replace `SARVAM_API_KEY` with your real key from the [Sarvam dashboard](https://dashboard.sarvam.ai/), and `PUBLIC_URL` with your ngrok URL once you have one (Step 5).

`sarvam-30b` has been deprecated. `sarvam-105b` is now the only supported chat model, and the `/v1/chat/completions` API rejects the `model="sarvam-30b"` value. If you have existing agents pinned to `sarvam-30b`, update them to `sarvam-105b` before it stops responding entirely.

`sarvam-105b` reasons before replying, and that reasoning is billed against `max_tokens`. Budget at least 1500 tokens per turn. Set it too low, and the API returns a valid response with empty content, which would otherwise strand the caller in silence.

### 4\. Write the Sarvam Client

Create `sarvam.py`, a thin async wrapper over the three Sarvam endpoints the agent needs: speech-to-text, chat, and text-to-speech.
    
    
    import base64
    
    import io
    
    import json
    
    import os
    
    import wave
    
    from typing import AsyncIterator
    
    import httpx
    
    BASE_URL = "https://api.sarvam.ai"
    
    STT_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v4")
    
    LLM_MODEL = os.getenv("SARVAM_LLM_MODEL", "sarvam-105b")
    
    TTS_MODEL = os.getenv("SARVAM_TTS_MODEL", "bulbul:v4-flash")
    
    SAMPLE_WIDTH_BYTES = 2
    
    class SarvamError(RuntimeError):
    
        pass
    
    def pcm_to_wav(pcm_audio: bytes, sample_rate: int) -> bytes:
    
        """Wrap raw mono Linear16 samples in a WAV container for the STT upload."""
    
        buffer = io.BytesIO()
    
        with wave.open(buffer, "wb") as wav_file:
    
            wav_file.setnchannels(1)
    
            wav_file.setsampwidth(SAMPLE_WIDTH_BYTES)
    
            wav_file.setframerate(sample_rate)
    
            wav_file.writeframes(pcm_audio)
    
        return buffer.getvalue()
    
    def raw_linear16(audio: bytes, expected_rate: int) -> bytes:
    
        """Vobiz playAudio needs container-free samples; Sarvam TTS may return a WAV."""
    
        if audio.startswith(b"RIFF"):
    
            with wave.open(io.BytesIO(audio), "rb") as wav_file:
    
                audio = wav_file.readframes(wav_file.getnframes())
    
        return audio
    
    class SarvamClient:
    
        def __init__(self, api_key: str) -> None:
    
            self._headers = {"api-subscription-key": api_key}
    
            self._http = httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)
    
        async def aclose(self) -> None:
    
            await self._http.aclose()
    
        async def transcribe(self, pcm_audio: bytes, sample_rate: int, language_code: str) -> str:
    
            wav_audio = pcm_to_wav(pcm_audio, sample_rate)
    
            response = await self._http.post(
    
                "/speech-to-text",
    
                headers=self._headers,
    
                files={"file": ("caller.wav", wav_audio, "audio/wav")},
    
                data={"model": STT_MODEL, "mode": "codemix", "language_code": language_code},
    
            )
    
            response.raise_for_status()
    
            return (response.json().get("transcript") or "").strip()
    
        async def stream_reply(
    
            self, messages: list[dict[str, str]], max_tokens: int = 2000
    
        ) -> AsyncIterator[str]:
    
            """Yield only reply text. These models also stream a private
    
            ``reasoning_content`` field that must never reach the caller's ear."""
    
            payload = {
    
                "model": LLM_MODEL,
    
                "messages": messages,
    
                "max_tokens": max_tokens,
    
                "stream": True,
    
            }
    
            async with self._http.stream(
    
                "POST", "/v1/chat/completions", headers=self._headers, json=payload
    
            ) as response:
    
                response.raise_for_status()
    
                async for line in response.aiter_lines():
    
                    if not line.startswith("data:"):
    
                        continue
    
                    data = line[len("data:"):].strip()
    
                    if data in ("", "[DONE]"):
    
                        continue
    
                    for choice in json.loads(data).get("choices", []):
    
                        delta = (choice.get("delta") or {}).get("content")
    
                        if delta:
    
                            yield delta
    
        async def synthesize(self, text: str, language_code: str, speaker: str, sample_rate: int) -> bytes:
    
            response = await self._http.post(
    
                "/text-to-speech",
    
                headers=self._headers,
    
                json={
    
                    "text": text,
    
                    "target_language_code": language_code,
    
                    "speaker": speaker,
    
                    "model": TTS_MODEL,
    
                    "speech_sample_rate": sample_rate,
    
                    "output_audio_codec": "linear16",
    
                },
    
            )
    
            response.raise_for_status()
    
            audios = response.json().get("audios") or []
    
            if not audios:
    
                raise SarvamError("Sarvam TTS returned no audio")
    
            return raw_linear16(base64.b64decode("".join(audios)), sample_rate)

`raw_linear16()` strips a WAV header if Sarvam returns one. Vobiz’s `playAudio` message requires raw, container-free Linear16 samples: sending it a WAV file (with its 44-byte header) produces a burst of noise at the start of every utterance.

### 5\. Write the Call Session

Create `agent.py`. This holds the per-call pipeline: a simple energy-based VAD (voice activity detector) over inbound audio, then speech-to-text, the chat model, and text-to-speech, streamed back to the caller sentence by sentence:
    
    
    import asyncio
    
    import audioop
    
    import base64
    
    import json
    
    import os
    
    import re
    
    from typing import Any
    
    from sarvam import SarvamClient
    
    OUTBOUND_SAMPLE_RATE = int(os.getenv("OUTBOUND_SAMPLE_RATE", "8000"))
    
    SAMPLE_WIDTH_BYTES = 2
    
    AGENT_LANGUAGE = os.getenv("AGENT_LANGUAGE", "en-IN")
    
    TTS_SPEAKER = os.getenv("TTS_SPEAKER", "anand")
    
    SYSTEM_PROMPT = (
    
        "You are a Sarvam AI voice assistant speaking with a caller on a phone "
    
        "line. You understand English and Indian languages, including code-mixed "
    
        "speech. Keep every reply to one or two short spoken sentences. Never use "
    
        "markdown, bullet points, emoji, or symbols, because your reply is read aloud."
    
    )
    
    GREETING = "Namaste! I am your Sarvam AI assistant. How can I help you today?"
    
    # Split streamed LLM text on sentence enders, including the Devanagari danda,
    
    # so the caller hears sentence one while the model is still writing sentence two.
    
    SENTENCE_END = re.compile(r"[.!?|।॥]+[\s\"')\]]*|\n+")
    
    MIN_TTS_CHARS = 24
    
    SILENCE_THRESHOLD = 250       # RMS energy that counts as speech
    
    END_OF_SPEECH_MS = 700        # trailing silence that ends an utterance
    
    MIN_SPEECH_MS = 200           # shorter utterances are treated as noise
    
    class CallSession:
    
        def __init__(self, websocket: Any) -> None:
    
            self.websocket = websocket
    
            self.stream_id: str | None = None
    
            self.input_sample_rate = 8000
    
            self.input_encoding = "audio/x-mulaw"
    
            self.sarvam = SarvamClient(os.getenv("SARVAM_API_KEY", ""))
    
            self.conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
    
            self._audio = bytearray()
    
            self._speech_ms = 0.0
    
            self._silence_ms = 0.0
    
            self._speech_active = False
    
            self._playback_active = False
    
            self._tasks: set[asyncio.Task] = set()
    
        async def handle_message(self, raw_message: str) -> None:
    
            data = json.loads(raw_message)
    
            event = data.get("event")
    
            if event == "start":
    
                await self._handle_start(data)
    
            elif event == "media":
    
                await self._handle_media(data)
    
            elif event in {"playedStream", "clearedAudio"}:
    
                self._playback_active = False
    
        async def _handle_start(self, data: dict) -> None:
    
            start = data.get("start") or {}
    
            self.stream_id = data.get("streamId") or start.get("streamId")
    
            # Trust the negotiated format rather than assuming a rate: Vobiz sends
    
            # mu-law at 8 kHz or Linear16 at 16 kHz depending on <Stream contentType>.
    
            media_format = start.get("mediaFormat") or {}
    
            self.input_sample_rate = int(media_format.get("sampleRate", 8000))
    
            self.input_encoding = str(media_format.get("encoding", "audio/x-mulaw"))
    
            self._spawn(self._speak(GREETING))
    
        async def _handle_media(self, data: dict) -> None:
    
            media = data.get("media") or {}
    
            payload = media.get("payload")
    
            if not payload:
    
                return
    
            raw = base64.b64decode(payload)
    
            pcm = audioop.ulaw2lin(raw, 2) if self.input_encoding == "audio/x-mulaw" else raw
    
            chunk_ms = len(pcm) * 1000 / (self.input_sample_rate * SAMPLE_WIDTH_BYTES)
    
            rms = audioop.rms(pcm, SAMPLE_WIDTH_BYTES)
    
            if rms >= SILENCE_THRESHOLD:
    
                if self._playback_active:
    
                    await self._clear_audio()  # barge-in
    
                self._speech_active = True
    
                self._speech_ms += chunk_ms
    
                self._silence_ms = 0
    
                self._audio.extend(pcm)
    
            elif self._speech_active:
    
                self._silence_ms += chunk_ms
    
                self._audio.extend(pcm)
    
            if self._speech_active and self._silence_ms >= END_OF_SPEECH_MS:
    
                utterance, speech_ms = bytes(self._audio), self._speech_ms
    
                self._audio.clear()
    
                self._speech_ms = self._silence_ms = 0
    
                self._speech_active = False
    
                if speech_ms >= MIN_SPEECH_MS:
    
                    self._spawn(self._process_utterance(utterance))
    
        async def _process_utterance(self, pcm_audio: bytes) -> None:
    
            transcript = await self.sarvam.transcribe(pcm_audio, self.input_sample_rate, AGENT_LANGUAGE)
    
            if not transcript:
    
                return
    
            self.conversation.append({"role": "user", "content": transcript})
    
            pending = ""
    
            async for delta in self.sarvam.stream_reply(self.conversation):
    
                pending += delta
    
                match = SENTENCE_END.search(pending)
    
                if match and match.end() >= MIN_TTS_CHARS:
    
                    sentence, pending = pending[:match.end()].strip(), pending[match.end():]
    
                    if sentence:
    
                        await self._speak(sentence)
    
            if pending.strip():
    
                await self._speak(pending.strip())
    
        async def _speak(self, text: str) -> None:
    
            pcm = await self.sarvam.synthesize(text, AGENT_LANGUAGE, TTS_SPEAKER, OUTBOUND_SAMPLE_RATE)
    
            await self._play(pcm)
    
        async def _play(self, pcm_audio: bytes) -> None:
    
            chunk_size = OUTBOUND_SAMPLE_RATE * SAMPLE_WIDTH_BYTES * 20 // 1000  # 20 ms chunks
    
            self._playback_active = True
    
            for offset in range(0, len(pcm_audio), chunk_size):
    
                await self.websocket.send_text(json.dumps({
    
                    "event": "playAudio",
    
                    "streamId": self.stream_id,
    
                    "media": {
    
                        "contentType": "audio/x-l16",
    
                        "sampleRate": OUTBOUND_SAMPLE_RATE,
    
                        "payload": base64.b64encode(pcm_audio[offset:offset + chunk_size]).decode(),
    
                    },
    
                }))
    
            await self.websocket.send_text(json.dumps({"event": "checkpoint", "streamId": self.stream_id, "name": "tts"}))
    
        async def _clear_audio(self) -> None:
    
            await self.websocket.send_text(json.dumps({"event": "clearAudio", "streamId": self.stream_id}))
    
            self._playback_active = False
    
        def _spawn(self, coroutine) -> None:
    
            task = asyncio.create_task(coroutine)
    
            self._tasks.add(task)
    
            task.add_done_callback(self._tasks.discard)
    
        async def close(self) -> None:
    
            for task in list(self._tasks):
    
                task.cancel()
    
            await self.sarvam.aclose()

The chat model’s streamed reply is split into sentences with `SENTENCE_END` and spoken as each one completes, rather than waiting for the full reply. This is what keeps turn latency down: the caller hears sentence one while the model is still generating sentence two.

Barge-in works by watching inbound RMS energy during playback: if the caller starts talking while the agent is still speaking, the session sends `clearAudio` and starts listening for a new utterance. This energy-based VAD can’t distinguish speech from background noise, so on noisy phone lines you may need to raise `SILENCE_THRESHOLD` or disable barge-in entirely.

### 6\. Write the FastAPI Server

Create `server.py`, exposing the Answer URL Vobiz fetches when a call comes in, and the WebSocket it streams audio over:
    
    
    import html
    
    import os
    
    from pathlib import Path
    
    import uvicorn
    
    from dotenv import load_dotenv
    
    from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
    
    from fastapi.responses import Response
    
    from agent import CallSession
    
    load_dotenv(Path(__file__).resolve().parent / ".env")
    
    PUBLIC_URL = os.getenv("PUBLIC_URL", "").rstrip("/")
    
    STREAM_CONTENT_TYPE = os.getenv("STREAM_CONTENT_TYPE", "audio/x-mulaw;rate=8000")
    
    app = FastAPI()
    
    def websocket_url(public_url: str) -> str:
    
        if public_url.startswith("https://"):
    
            return "wss://" + public_url.removeprefix("https://") + "/ws"
    
        return "ws://" + public_url.removeprefix("http://") + "/ws"
    
    @app.api_route("/answer", methods=["GET", "POST"])
    
    async def answer(request: Request) -> Response:
    
        """The XML Vobiz executes once the call is answered."""
    
        base_url = html.escape(PUBLIC_URL, quote=True)
    
        ws_url = html.escape(websocket_url(PUBLIC_URL), quote=False)
    
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    
    <Response>
    
        <Stream bidirectional="true"
    
                audioTrack="inbound"
    
                keepCallAlive="true"
    
                contentType="{html.escape(STREAM_CONTENT_TYPE, quote=True)}"
    
                statusCallbackUrl="{base_url}/stream-status"
    
                statusCallbackMethod="POST">
    
            {ws_url}
    
        </Stream>
    
        <Hangup/>
    
    </Response>"""
    
        return Response(content=xml, media_type="application/xml")
    
    @app.websocket("/ws")
    
    async def websocket_endpoint(websocket: WebSocket) -> None:
    
        await websocket.accept()
    
        session = CallSession(websocket)
    
        try:
    
            async for message in websocket.iter_text():
    
                await session.handle_message(message)
    
        except WebSocketDisconnect:
    
            pass
    
        finally:
    
            await session.close()
    
    @app.post("/stream-status")
    
    async def stream_status(request: Request) -> Response:
    
        await request.form()
    
        return Response(status_code=204)
    
    @app.post("/hangup")
    
    async def hangup(request: Request) -> Response:
    
        await request.form()
    
        return Response(status_code=204)
    
    if __name__ == "__main__":
    
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("HTTP_PORT", "8000")))

`<Record>` and `<Stream>` are siblings under `<Response>`, not nested inside one another. If you add call recording later with `<Record recordSession="true" .../>`, place it as its own top-level element alongside `<Stream>`. Nesting `<Stream>` inside `<Record>`, or letting a Record callback return `<Hangup/>`, ends the call before the agent WebSocket ever starts.

### 7\. Configure Vobiz to Reach Your Agent

**Start ngrok:**
    
    
    ngrok http 8000

ngrok prints a forwarding URL that looks like `https://xxxx.ngrok-free.app`. Put that exact URL, unchanged, into `PUBLIC_URL` in your `.env` file. The server derives the `wss://` WebSocket URL from it automatically.

Free ngrok URLs change every time you restart ngrok. If your agent stops receiving calls, update `PUBLIC_URL` in `.env` to match the URL ngrok is currently printing, and restart `server.py`.

**Create an application and point it at the server:**

The Answer and Hangup URLs live on a Vobiz **application** , not directly on the number. You create the application first, then attach your number to it.

  1. In the Vobiz dashboard, go to **Applications**
  2. Create a new application
  3. Set the **Answer URL** to `https://xxxx.ngrok-free.app/answer` (method: `POST`)
  4. Set the **Hangup URL** to `https://xxxx.ngrok-free.app/hangup` (method: `POST`)
  5. Save the application
  6. Go to your number’s settings and attach it to the application you just created



Step 6 is easy to miss but required. Without a number attached to the application, calls have nowhere to route to, even if the application itself is configured correctly.

### 8\. Run and Test Your Agent
    
    
    python server.py

Call your Vobiz number from any phone. Vobiz fetches `/answer`, opens the WebSocket at `/ws`, and your agent greets the caller.

* * *

## Audio Formats

The two directions of a Vobiz call are independent and configured separately.

**Vobiz → your agent** , set by `<Stream contentType>`:

Format| Use  
---|---  
`audio/x-mulaw;rate=8000`| 8 kHz inbound (default in this guide)  
`audio/x-l16;rate=16000`| 16 kHz inbound  
  
**Your agent → Vobiz** , set per `playAudio` message: Linear16 at 8000, 16000, or 24000 Hz. 24 kHz applies to playback only, not inbound audio.

`playAudio` payloads must be raw mono little-endian Linear16, Base64-encoded, with **no WAV header**. Declaring a `sampleRate` in the `playAudio` message does not resample the bytes you send. If you declare 24000 while the payload is actually 8 kHz audio, the caller hears distorted, sped-up “chipmunk” audio. `raw_linear16()` in Step 4 strips a WAV container if Sarvam happens to return one, but it doesn’t resample.

Read `start.mediaFormat` on the `start` event rather than assuming a rate, as this guide’s `_handle_start` does. Vobiz tells you the exact encoding and sample rate it negotiated for each call.

* * *

## Customization Examples

### Hindi Voice Agent
    
    
    AGENT_LANGUAGE = "hi-IN"
    
    TTS_SPEAKER = "simran"  # or: priya, ishita, kavya, aditya, anand, rohan

### Multilingual Agent (Auto-detect)
    
    
    AGENT_LANGUAGE = "unknown"  # Sarvam auto-detects the caller's spoken language
    
    TTS_SPEAKER = "anand"

Use `AGENT_LANGUAGE = "unknown"` for support lines where callers might speak any of several languages. Sarvam detects the spoken language per utterance, so the same agent can handle a Hindi caller followed by a Tamil caller without any code changes.

### Available Language Codes

Language| Code  
---|---  
English (India)| `en-IN`  
Hindi| `hi-IN`  
Bengali| `bn-IN`  
Tamil| `ta-IN`  
Telugu| `te-IN`  
Gujarati| `gu-IN`  
Kannada| `kn-IN`  
Malayalam| `ml-IN`  
Marathi| `mr-IN`  
Punjabi| `pa-IN`  
Odia| `od-IN`  
Auto-detect| `unknown`  
  
### Speaker Voices (Bulbul v3)

**Male:** Anand (default here), Aditya, Rahul, Rohan, Amit, Dev, Ratan, Varun, Manan, Sumit, Kabir, Aayan, Ashutosh, Advait, Tarun, Sunny, Mani, Gokul, Vijay, Mohit, Rehan, Soham, Shubh

**Female:** Ritu, Priya, Neha, Pooja, Simran, Kavya, Ishita, Shreya, Roopa, Tanya, Shruti, Suhani, Kavitha, Rupali

Speakers are model-specific. v3 short names (e.g. `shubh`) are rejected by `bulbul:v4-flash`; use persona IDs from the v4 catalog. `bulbul:v2` voices such as `anushka` are rejected by v3/v4. Check that the speaker you pick is valid for the `SARVAM_TTS_MODEL` you’re using.

* * *

## Understanding the Call Flow

  1. **Caller dials your Vobiz number.** Vobiz fetches your **Answer URL** , and executes the returned `<Stream>` XML, opening a bidirectional WebSocket to your agent.
  2. **`start` event:** Vobiz sends the stream ID and negotiated audio format. Your agent speaks a greeting.
  3. **`media` events:** Caller audio arrives as base64-encoded chunks. An energy-based VAD buffers speech and detects when the caller has stopped talking.
  4. **STT:** The buffered utterance is sent to Sarvam’s Saaras model for transcription.
  5. **LLM:** The transcript is added to the conversation and streamed through a Sarvam chat model.
  6. **TTS:** Each completed sentence of the reply is synthesized with Sarvam’s Bulbul and sent back as `playAudio` events, so playback starts before the whole reply is ready.
  7. **Barge-in:** If the caller speaks while the agent is still playing audio, a `clearAudio` event stops playback and a new utterance begins.



* * *

## Pro Tips

  * Use `AGENT_LANGUAGE = "unknown"` to auto-detect the caller’s language on multilingual support lines.
  * Sarvam’s models understand code-mixing, so your agent can naturally handle Hinglish, Tanglish, and other mixed languages common on real support calls.
  * Keep the system prompt explicit about reply length and formatting. Since the reply is read aloud, ask the model to avoid markdown, bullet points, and emoji.
  * If a chat completion ever returns empty content (the model spent its whole token budget reasoning), have the agent speak a fallback line instead of going silent.



Log every transcript and reply to a file or database for post-call analytics. It’s cheap and doesn’t slow down the live pipeline.

* * *

## Troubleshooting

**Call connects but there’s no audio.** Confirm `PUBLIC_URL` in `.env` matches your current ngrok URL exactly, and that the Answer URL configured on your Vobiz application points at `/answer` on that same URL.

**Call doesn’t reach your agent at all.** Confirm your number is actually attached to the application, not just that the application has the right URLs. A number with no application attached has nowhere to route an incoming call.

**Choppy or chipmunk-pitched audio.** Check that `OUTBOUND_SAMPLE_RATE` and the `sampleRate` you declare in each `playAudio` message match the actual bytes you’re sending. Declaring a rate that doesn’t match the payload distorts pitch and speed without erroring.

**Playback has a burst of noise at the start.** Sarvam TTS occasionally returns a WAV-wrapped file instead of raw PCM. Make sure `raw_linear16()` runs on every synthesized chunk before it’s sent as `playAudio`.

**API key errors.** Make sure `SARVAM_API_KEY` is in your `.env` file and that the file sits next to `server.py`.

**Empty or truncated replies.** `sarvam-105b` spends tokens on internal reasoning before writing the reply. Raise `max_tokens` on the chat request; 1500 to 2000 is a safe starting point.

**Barge-in doesn’t trigger, or triggers on background noise.** The VAD here is a simple RMS energy threshold, not real speech detection. Raise `SILENCE_THRESHOLD` on noisy lines, or set it high enough to ignore ambient noise from the caller’s environment.

* * *

## Additional Resources

  * [Sarvam AI Documentation](https://docs.sarvam.ai/)
  * [Vobiz Documentation](https://vobiz.ai/)



* * *

## Need Help?

  * Sarvam Support: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Community: [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



* * *

**Happy Building!**

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)[Build Your First Voice Agent using VapiNext](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
    * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
    * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
    * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
    * [Models](https://docs.sarvam.ai/api/getting-started/models)

    * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
    * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
    * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
    * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
    * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
    * Account & Billing

  * API Guides & Tutorials

    * Large Language Models

    * Speech to Text

    * Text to Speech

    * Text Processing

    * Document Intelligence

    * Document Translation

    * Dubbing

    * Instant Voice CloningBeta

  *     * Integration
      * [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)
      * [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)
      * [Twilio](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio)
      * [Exotel](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)
      * [Vobiz](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)
      * [Vapi](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)
      * [n8n](https://docs.sarvam.ai/api/integration/n8n)
      * [Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)
      * [LangChain](https://docs.sarvam.ai/api/integration/langchain)
      * Best Practices

    * Developer Tools

  * Cookbook

    * Guides

    * Example Voice Agents

  * Self-Hosted Deployments

    * Overview

    * AWS SageMaker

  *     * Migrations




  * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
  * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
  * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
  * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
  * [Models](https://docs.sarvam.ai/api/getting-started/models)
  * [Saaras](https://docs.sarvam.ai/api/getting-started/models/saaras)
  * [Bulbul](https://docs.sarvam.ai/api/getting-started/models/bulbul)
  * [Sarvam 105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)
  * [Open-Weight Models](https://docs.sarvam.ai/api/getting-started/models/openweight)
  * [GLM-5.3](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)
  * [Gemma 4 31B](https://docs.sarvam.ai/api/getting-started/models/openweight/gemma-4-31b)
  * [DeepSeek V4.1 Flash](https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash)
  * [Mayura](https://docs.sarvam.ai/api/getting-started/models/mayura)
  * [Sarvam Translate](https://docs.sarvam.ai/api/getting-started/models/sarvam-translate)
  * [Sarvam Vision](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)
  * [Sarvam 30B (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/sarvam-30b)
  * [Sarvam M (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/sarvam-m)
  * [Saarika (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/saarika)
  * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
  * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
  * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
  * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
  * [Organisations & workspaces](https://docs.sarvam.ai/api/platform/organisations-and-workspaces)
  * [Create an organisation](https://docs.sarvam.ai/api/platform/create-an-organisation)
  * [Create a workspace](https://docs.sarvam.ai/api/platform/create-a-workspace)
  * [Invite your team](https://docs.sarvam.ai/api/platform/invite-your-team)
  * [Billing & payments](https://docs.sarvam.ai/api/platform/billing)
  * [Platform FAQ](https://docs.sarvam.ai/api/platform/faq)
  * [Chat Completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * [Responses API](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/responses-api)
  * [List your chat messages](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/list-your-chat-messages)
  * [Control response randomness](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-response-randomness)
  * [Control response diversity](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-response-diversity)
  * [Adjust the model's thinking level](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/adjust-the-models-thinking-level)
  * [Encourage new topics in response](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/encourage-new-topics-in-response)
  * [Reduce repetition words or phrases in response](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/reduce-repetition-words-or-phrases-in-response)
  * [Get repeatable results](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/get-repeatable-results)
  * [Control the response length](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-the-response-length)
  * [Control where the model stops](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-where-the-model-stops)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)
  * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
  * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)
  * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
  * [Realtime Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming)
  * [Best Practices](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/best-practices)
  * [FAQs](https://docs.sarvam.ai/api/speech-to-text/faq)
  * [Select Output Mode](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/select-output-mode)
  * [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/specify-language-codes)
  * [Enable Speaker Diarization](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/enable-speaker-diarization)
  * [Keyterm Prompting](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/keyterms)
  * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/ivr-contact-center)
  * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/bfsi-voice-bots)
  * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
  * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services)
  * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/agri-rural)
  * [Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)
  * [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)
  * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/which-api-to-use)
  * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)
  * [HTTP Stream](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream)
  * [WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket)
  * [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
  * [Best Practice Guide for Bulbul v4 Flash](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices)
  * [Best Practices (Bulbul v3)](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices)
  * [Set the Language](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-the-language)
  * [Change the Speaker Voice](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/change-the-speaker-voice)
  * [Adjust the Tone](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-tone)
  * [Adjust the Speed](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-speed)
  * [Adjust the Loudness](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-loudness)
  * [Set the Sample rate](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-the-sample-rate)
  * [Enable Text Preprocessing](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/enable-text-preprocessing)
  * [Set audio format for output](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-audio-format-for-output)
  * [Set bitrate for output](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-bitrate-for-output)
  * [Set maximum length for sentence splitting](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-maximum-length-for-sentence-splitting)
  * [Set buffer size to start processing](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-buffer-size-to-start-processing)
  * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/ivr-contact-center)
  * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/bfsi-voice-bots)
  * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
  * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/government-services)
  * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview)
  * [Text Translation](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/translation)
  * [Transliteration](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/transliteration)
  * [Language Detection](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/language-detection)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview)
  * [Get your config_id](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/how-to/get-your-config-id)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)
  * [Set Style Guidelines](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/style-guidelines)
  * [Pick a Genre](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/genre-and-model-tier)
  * [Use Native Numerals](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/native-numerals)
  * [Poll Status and Export Results](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/poll-and-export)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/faq)
  * [Use Cases](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/use-cases)
  * [Translate a PDF](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/guides/translate-a-pdf)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)
  * [Job Lifecycle](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle)
  * [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/specify-language-codes)
  * [Control Translation Tone](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/control-translation-tone)
  * [Choose a Voice](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice)
  * [Choose Export Formats](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/faq)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview)
  * [Prepare Reference Audio](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/prepare-reference-audio)
  * [Clone Across Languages](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/clone-across-languages)
  * [Choose Audio Formats](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/choose-audio-formats)
  * [Use Quality Control](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/use-quality-control)
  * [HTTP Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/http-streaming)
  * [WebSocket Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/websocket-streaming)
  * [Supported Languages](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/supported-languages)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/faq)
  * [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)
  * [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)
  * [Twilio](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio)
  * [Exotel](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)
  * [Vobiz](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)
  * [Vapi](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)
  * [n8n](https://docs.sarvam.ai/api/integration/n8n)
  * [Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)
  * [LangChain](https://docs.sarvam.ai/api/integration/langchain)
  * [LiveKit in Production](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)
  * [Pipecat in Production](https://docs.sarvam.ai/api/integration/pipecat-production-guide)
  * [MCP Server](https://docs.sarvam.ai/api/developer-tools/mcp)
  * [Markdown & llms.txt](https://docs.sarvam.ai/api/developer-tools/llms-txt)
  * [Context7](https://docs.sarvam.ai/api/developer-tools/context7)
  * [Agent Skills](https://docs.sarvam.ai/api/developer-tools/agent-skills)
  * [Call Analytics Pipeline](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)
  * [Live Video Transcription](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)
  * [Podcast Generator](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator)
  * [WhatsApp Bot](https://docs.sarvam.ai/api/cookbook/guides/whats-app-bot)
  * [Collection Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/collection-agent)
  * [Government Scheme Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent)
  * [Tutor Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/tutor-agent)
  * [Loan Advisory Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/loan-advisory-agent)
  * [Introduction](https://docs.sarvam.ai/api/self-hosted/introduction)
  * [Managed vs Self-Hosted](https://docs.sarvam.ai/api/self-hosted/hosted-vs-self-hosted)
  * [How it works](https://docs.sarvam.ai/api/self-hosted/architecture)
  * [Get started](https://docs.sarvam.ai/api/self-hosted/sagemaker/get-started)
  * [Speech-to-Text (Saaras v3)](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-saaras)
  * [Sarvam Vision](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-vision)
  * [Text-to-Speech (Bulbul v3)](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-bulbul)
  * [Deploy with Terraform](https://docs.sarvam.ai/api/self-hosted/sagemaker/terraform)
  * [Speech-to-Text](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-saaras)
  * [Sarvam Vision](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-vision)
  * [Text-to-Speech](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-bulbul)
  * [Error handling](https://docs.sarvam.ai/api/self-hosted/sagemaker/errors)
  * [Configure & tune](https://docs.sarvam.ai/api/self-hosted/sagemaker/configure)
  * [Operations](https://docs.sarvam.ai/api/self-hosted/sagemaker/operations)
  * [Limitations](https://docs.sarvam.ai/api/self-hosted/sagemaker/limitations)
  * [Troubleshooting](https://docs.sarvam.ai/api/self-hosted/sagemaker/troubleshooting)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text)
  * [Instant Voice Cloning](https://docs.sarvam.ai/api/migrations/from-elevenlabs/voice-cloning)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-cartesia/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-cartesia/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-cartesia/speech-to-text)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-deepgram/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-deepgram/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-deepgram/speech-to-text)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-gemini/overview)
  * [Chat Completion](https://docs.sarvam.ai/api/migrations/from-gemini/chat-completion)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-gemini/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-gemini/speech-to-text)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


