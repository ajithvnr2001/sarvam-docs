---
url: https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription/
title: Live Video Transcription | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:30.438995+00:00
---

# Live Video Transcription | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription/

Skip to navigation

On this page

  * Overview
  * Business Value
  * How It Works
  * 1\. Prerequisites
  * 2\. Clone and Install
  * 3\. Configure Environment Variables
  * 4\. Run It
  * 5\. Pipeline Walkthrough
  * Step 1: Capture and encode audio in the browser
  * Step 2: One persistent connection per mode
  * Step 3: Relay results back to the browser
  * Step 4: Socket.IO event wiring
  * Available Options
  * Source Language
  * Output Modes
  * Customization
  * Tune voice activity detection
  * Add speech start/end signals
  * Transcribe a live microphone instead of a video file
  * Change the chunk interval
  * Tips & Best Practices
  * Error Handling
  * Additional Resources
  * Final Notes



Scroll to top

[Cookbook](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)[Guides](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)

# Live Video Transcription

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription.md "View this page as plain text")|More actions

This page is for Model APIs.

## **Overview**

This cookbook builds a real-time transcription and translation demo. Play or upload any video with speech in the browser, and watch a live transcript and English translation appear as it plays, powered by Sarvam’s **Streaming Speech-to-Text API** over a persistent WebSocket connection.

**What you’ll build:**

  * A browser page that captures a playing video’s audio and streams it to a server, no file upload round-trip required
  * A Flask-SocketIO server that keeps one persistent Sarvam streaming connection open per client per mode
  * Live transcription in the source language, running concurrently with live translation to English
  * Results pushed back to the browser over WebSocket as each speech segment finalizes



[View on GitHubBrowse the full source for this app in the sarvam-ai-cookbook repo.](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/examples/Live_Video_Transcription)[Run Code LocallyJump to Clone and Install to set this demo up on your machine.](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription#2-clone-and-install)

### Business Value

  * Live captions for lectures, webinars, and internal recordings
  * Real-time subtitling for video content in a viewer’s own language
  * Accessibility support for hearing-impaired viewers watching pre-recorded or live video



###### EdTech

###### Media & Broadcast

###### Enterprise

Caption recorded lectures live as students watch, with an English translation running alongside the original-language transcript.

## **How It Works**

[1](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription#capture-audio-in-the-browser)

### Capture audio in the browser

The browser reads the video element’s audio track via the Web Audio API, resamples it to 16kHz mono, and encodes it as WAV, entirely client-side, no server upload of the raw video file.

[2](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription#stream-1-second-frames-over-socketio)

### Stream ~1 second frames over Socket.IO

Every second, the buffered audio is packaged into one WAV chunk, base64-encoded, and emitted to the Flask server over a Socket.IO event.

[3](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription#forward-into-a-persistent-sarvam-connection)

### Forward into a persistent Sarvam connection

For each client, the server opens one long-lived Sarvam streaming connection per active mode (transcribe and/or translate) and forwards incoming frames into it as they arrive.

[4](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription#relay-results-back-live)

### Relay results back live

Sarvam emits a finalized transcript or translation as each speech segment completes. The server relays it back to the same browser tab over Socket.IO, and it’s appended to the transcript panel immediately.

Transcription and translation run as two independent streaming connections, so you can start one, both, or switch between them without interrupting the other.

## **1\. Prerequisites**

  * Python 3.8 or higher
  * A Sarvam API key, sign up on the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/) to get one
  * A modern browser (Web Audio API and `HTMLMediaElement.captureStream()` support)
  * A video file with speech to try it on



## **2\. Clone and Install**

###### macOS/Linux

###### Windows
    
    
    git clone https://github.com/sarvamai/sarvam-ai-cookbook.git
    
    cd sarvam-ai-cookbook/examples/Live_Video_Transcription
    
    python -m venv venv
    
    source venv/bin/activate
    
    pip install -r requirements.txt

## **3\. Configure Environment Variables**

Create a `.env` file in the project root:
    
    
    SARVAM_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx

`config.py` reads this key and also holds a few settings worth knowing about before you run the app:

Setting| Default| Meaning  
---|---|---  
`HOST` / `PORT`| `127.0.0.1` / `5001`| Where the Flask server binds  
`API_LANGUAGE`| `"unknown"`| Source language passed to the transcription stream; `"unknown"` auto-detects. Set to a specific code (e.g. `"hi-IN"`) for more consistent accuracy on a known language  
`CORS_ALLOWED_ORIGINS`| `"*"`| Fine for local testing; restrict this before deploying anywhere public  
  
## **4\. Run It**
    
    
    python app.py

Open [http://localhost:5001](http://localhost:5001/), upload a video with speech, then click **Start Transcription** and/or **Start Translation**. Text appears in the corresponding panel as each segment finalizes.

## **5\. Pipeline Walkthrough**

### Step 1: Capture and encode audio in the browser

`templates/index.html` pulls the audio track off the `<video>` element with `captureStream()`, buffers raw samples from a `ScriptProcessorNode`, and every second resamples the buffer to 16kHz and encodes it as WAV before sending it over Socket.IO:
    
    
    const stream = video.captureStream();
    
    mediaStreamSource = audioContext.createMediaStreamSource(stream);
    
    processor = audioContext.createScriptProcessor(4096, 1, 1);
    
    processor.onaudioprocess = function(event) {
    
        const audioData = event.inputBuffer.getChannelData(0);
    
        const int16Array = new Int16Array(audioData.length);
    
        for (let i = 0; i < audioData.length; i++) {
    
            int16Array[i] = audioData[i] * 32767;
    
        }
    
        transcriptionChunks.push(int16Array);
    
        // ...every ~1s: resample to 16kHz, encode as WAV, base64, and emit
    
    };

Streaming endpoints only accept WAV or raw PCM audio, not MP3, AAC, or other compressed formats. Encoding to WAV client-side, as this demo does, is what makes the captured browser audio acceptable to the API.

### Step 2: One persistent connection per mode

`app.py` defines a `StreamingSession` class that opens a Sarvam streaming connection and keeps it alive in a dedicated background thread with its own asyncio event loop, one instance per `(client, mode)` pair:
    
    
    async def _session(self):
    
        client = AsyncSarvamAI(api_subscription_key=SARVAM_API_KEY)
    
        conn = client.speech_to_text_streaming.connect(
    
            language_code=config.API_LANGUAGE,
    
            model="saaras:v4",
    
            mode="transcribe" if self.mode == "transcribe" else "translate",
    
        )
    
        async with conn as ws:
    
            receiver = asyncio.create_task(self._receive(ws))
    
            try:
    
                while True:
    
                    audio_b64 = await self.queue.get()
    
                    if audio_b64 is None:
    
                        break
    
                    await ws.transcribe(audio=audio_b64)
    
                await ws.flush()
    
                await asyncio.sleep(2)  # let the receiver drain remaining transcripts
    
            finally:
    
                receiver.cancel()

Both modes go through the same unified `speech_to_text_streaming` endpoint here, the `mode` parameter (`"transcribe"` vs `"translate"`) picks the behavior, and both still call `ws.transcribe()` to send audio. See [Streaming Speech-to-Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api#key-differences-stt-vs-sttt) for the full comparison.

Audio frames arrive from the browser on Flask-SocketIO’s own thread and get handed off to the session’s asyncio loop through a queue (`asyncio.run_coroutine_threadsafe`), since the WebSocket connection itself must be driven from a single event loop.

`_session()` runs inside `_run()`, the background thread’s entry point, which wraps the whole coroutine in a try/except. Any failure, a rejected connection, an auth error, a dropped socket, is caught, logged, and relayed to the browser as an `error` event so the client isn’t left waiting on a connection that’s already dead:
    
    
    def _run(self):
    
        asyncio.set_event_loop(self.loop)
    
        try:
    
            self.loop.run_until_complete(self._session())
    
        except Exception as e:
    
            logger.error(f"[{self.mode}] session loop error: {e}")
    
            self._stopped = True
    
            streaming_sessions.pop((self.sid, self.mode), None)
    
            with app.app_context():
    
                socketio.emit(
    
                    "error",
    
                    {"message": f"Failed to start {self.mode} stream: {e}"},
    
                    to=self.sid,
    
                )
    
        finally:
    
            self.loop.close()

Sarvam’s role: This is where the actual transcription and translation happen. The `AsyncSarvamAI` client opens a live WebSocket to Sarvam’s Streaming Speech-to-Text API (Saaras v3), and everything downstream of that, voice activity detection, segmenting continuous audio into utterances, language handling, and the transcription/translation inference itself, runs on Sarvam’s side. The app’s only job here is to keep the connection open and feed it audio frames as they arrive.

### Step 3: Relay results back to the browser

A second task on the same connection continuously calls `ws.recv()` and emits each finalized result back to the originating client:
    
    
    async def _receive(self, ws):
    
        try:
    
            while True:
    
                resp = await ws.recv()
    
                text = _extract_text(resp)
    
                if text and text.strip():
    
                    emit_streaming_result(self.sid, self.mode, text.strip())
    
        except asyncio.CancelledError:
    
            pass
    
        except Exception as e:
    
            logger.info(f"[{self.mode}] receiver ended: {e}")

Sarvam’s role: Sarvam produces every `resp` this loop reads. Each one is a finalized transcript or translation segment that Sarvam decided was complete, based on its own voice-activity detection and segmentation, not something the app computes. This step only relays that already-finished text back over Socket.IO.

### Step 4: Socket.IO event wiring

Client and server agree on a small set of events to open, feed, and tear down each streaming session:

Event| Direction| Purpose  
---|---|---  
`start_stream` / `stop_stream`| Client → Server| Open or close a persistent streaming session for `{ mode: "transcribe" | "translate" }`  
`audio_chunk` / `translation_chunk`| Client → Server| Forward one WAV audio frame, `{ audio: "<base64>" }`  
`transcription_result` / `translation_result`| Server → Client| A finalized piece of text, `{ text: "..." }`  
`status` / `error`| Server → Client| Connection status and error messages  
  
## **Available Options**

### Source Language

`API_LANGUAGE` in `config.py` accepts any Saaras v3 BCP-47 language code, or `"unknown"` to auto-detect. See [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/specify-language-codes) for the full list of supported codes.

### Output Modes

This demo only wires up `transcribe` and `translate`, but the underlying Streaming API also supports `verbatim`, `translit`, and `codemix`. See [Streaming Speech-to-Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api#supported-modes-saaras-v3) for what each mode returns.

## **Customization**

### Tune voice activity detection

Pass `high_vad_sensitivity=True` when opening the connection in `StreamingSession._session` for a shorter silence boundary (~64ms instead of 1s at 16kHz), which makes segments finalize faster at a small cost to context:
    
    
    conn = client.speech_to_text_streaming.connect(
    
        language_code=config.API_LANGUAGE,
    
        model="saaras:v4",
    
        high_vad_sensitivity=True,
    
    )

### Add speech start/end signals

Pass `vad_signals=True` to receive `START_SPEECH` / `END_SPEECH` events alongside transcripts, useful if you want to show a “listening” indicator in the UI rather than only finalized text. See [Streaming Speech-to-Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api#response-types) for the message shapes.

### Transcribe a live microphone instead of a video file

Swap `video.captureStream()` in `templates/index.html` for `navigator.mediaDevices.getUserMedia({ audio: true })`. The rest of the pipeline, resampling, WAV encoding, and the Socket.IO events, stays the same, since it already operates on a generic `MediaStream`.

### Change the chunk interval

The browser buffers and sends audio roughly once a second (`currentTime - lastChunkTime >= 1000` in `templates/index.html`). Shorter intervals lower latency at the cost of more frequent small requests; longer intervals do the opposite.

## **Tips & Best Practices**

  * **Keep the sample rate consistent** : The demo resamples to 16kHz before encoding, matching the rate it passes to `connect()`. If you change one, change the other, mismatched sample rates degrade transcription quality.
  * **One connection per mode, not per chunk** : `StreamingSession` opens a single long-lived connection and streams every frame into it. Opening a new connection per audio chunk would add connection-setup latency to every single frame.
  * **Independent buffers per mode** : Transcription and translation each keep their own `audioChunks` buffer in the browser, so running both at once doesn’t mean one mode steals frames meant for the other.
  * **Handle disconnects** : This demo doesn’t automatically reconnect on a dropped WebSocket. For production use, add reconnect-with-backoff on close codes `1006`/`1011`, see [Handling Disconnects](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api#handling-disconnects).
  * **Restrict CORS before deploying** : `CORS_ALLOWED_ORIGINS = "*"` in `config.py` is fine for local testing only.



## **Error Handling**

You may encounter these errors while using the underlying API:

  * **403 Forbidden** (`invalid_api_key_error`), invalid API key. Use a valid key from the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/).
  * **429 Too Many Requests** (`rate_limit_exceeded_error`), too many concurrent streaming connections or requests. Check [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits) for streaming concurrency limits.
  * **WebSocket close`1006` / `1011`**, abnormal closure or server error. Reconnect with exponential backoff rather than retrying immediately, see [Handling Disconnects](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api#handling-disconnects).
  * **WebSocket close`4xxx`**, application-specific, usually auth or quota. Read the close reason before retrying; blind-retrying an auth failure will just fail again.



For the full error-code table and SDK exception reference, see [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting).

## **Additional Resources**

  * **Documentation** : [docs.sarvam.ai](https://docs.sarvam.ai/)
  * **Related APIs** : [Streaming Speech-to-Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api) · [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/specify-language-codes)
  * **Full source** : [Live_Video_Transcription on GitHub](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/examples/Live_Video_Transcription)
  * **Community** : [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



## **Final Notes**

  * Keep your API key secure, prefer environment variables over hardcoding.
  * This demo keeps one persistent connection per client per mode rather than reconnecting per audio chunk. That’s what keeps latency low.
  * Add reconnect logic and restrict CORS before taking this beyond local experimentation.



**Keep Building!** 🚀

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)[Podcast GeneratorNext](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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

    * Developer Tools

  * Cookbook

    * Guides
      * [Call Analytics Pipeline](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)
      * [Live Video Transcription](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)
      * [Podcast Generator](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator)
      * [WhatsApp Bot](https://docs.sarvam.ai/api/cookbook/guides/whats-app-bot)
      * [Example Projects on GitHub](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/examples "Example Projects on GitHub")

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


