---
url: https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming/
title: Realtime Streaming Speech-to-Text API | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:19.564571+00:00
---

# Realtime Streaming Speech-to-Text API | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming/

Skip to navigation

On this page

  * Overview
  * How this differs from the legacy Streaming API
  * Connection parameters
  * Stream types
  * Getting started
  * Turn detection
  * Language support
  * Message reference
  * Live config updates
  * Error handling
  * Best practices



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Speech to Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)

# Realtime Streaming Speech-to-Text API

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming.md "View this page as plain text")|More actions

This page is for Model APIs.

## Overview

Sarvam’s WebSocket streaming models for voice agents and live transcription: real interim (partial) transcripts as the user speaks, plus millisecond-based VAD tuning. `saaras:v3-realtime` is the default; `saaras:v4` is also available on this endpoint and accepts the same connection parameters and message protocol described below.

### How this differs from the legacy Streaming API

| Realtime Streaming (`saaras:v3-realtime` / `saaras:v4`)| Streaming API (Legacy, `saaras:v3`)  
---|---|---  
Endpoint| `GET /speech-to-text-realtime/ws`| `GET /speech-to-text/ws`  
Interim results| Real `transcript.partial` events throughout the utterance| None; only a final transcript per utterance  
VAD tuning| 3 parameters, in milliseconds (`threshold`, `silence_duration_ms`, `min_speech_duration_ms`)| 10+ parameters, in frame counts  
Mid-call reconfiguration| Yes, via `config.update` over the open socket| No, reconnect required to change parameters  
Manual turn control| `endpointing="manual"` with client-sent `speech_start` / `speech_end` / `flush`| `flush_signal` only  
Audio message format| `{"event": "audio_input", "audio": "<base64>"}`| `{"audio": {"data": ..., "sample_rate": ..., "encoding": ...}}`  
Language detection| `language_code="auto"`, detected language on every partial/final| `language_code="unknown"`, `language_probability` on final only  
Errors| Structured `error` events (`code`, `is_fatal`, `message`) + documented close codes| Close code only, no structured error event  
  
## Connection parameters

Sent as query parameters on the WebSocket URL (or the matching keyword argument on `connect()` in the Python SDK).

Parameter| Type| Default| Description  
---|---|---|---  
`language_code`| string| **required**|  BCP-47 code of the input audio, or `auto` for adaptive language detection.  
`model`| string| `saaras:v3-realtime`| `saaras:v3-realtime` (default) or `saaras:v4`.  
`stream_type`| string| `balanced`| Latency/accuracy tradeoff for partials. See [Stream types](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming#stream-types) below.  
`mode`| string| `transcribe`| Task applied to the **final** transcript only: `transcribe`, `translate`, `verbatim`, `translit`, `codemix`. Partials are always plain transcription.  
`endpointing`| string| `vad`| `vad` (server auto-detects turn boundaries) or `manual` (client sends `speech_start`/`speech_end`).  
`encoding`| string| `linear16`| `linear16`, `linear32`, `mulaw`, or `alaw`. Mono only.  
`sample_rate`| integer| `16000`| `8000` or `16000` only; any other value closes the connection (code `4000`).  
`threshold`| float| `0.3`| VAD sensitivity (0.0-1.0). Only applies when `endpointing=vad`.  
`silence_duration_ms`| integer| `500`| Silence (ms) marking end-of-turn. Only applies when `endpointing=vad`.  
`min_speech_duration_ms`| integer| `250`| Minimum speech duration (ms) to count as an utterance. Only applies when `endpointing=vad`.  
`return_timestamps`| boolean| `false`| Adds `start_s`/`end_s` to `transcript.final` when `true`.  
`prompt`| string|  _(none)_|  Optional terminology hint applied to the final transcript.  
`keyterms`| string (JSON array)| _(none)_|  JSON-encoded list of up to 50 keyterms (64 characters each) to bias recognition. **`saaras:v4` only.**  
  
### Stream types

`stream_type` controls the tradeoff between partial-transcript latency and accuracy:

Value| Partials| Use when  
---|---|---  
`fast`| Lowest latency| Conversational voice agents where snappy barge-in matters most  
`balanced` (default)| Slightly slower, more accurate| General live transcription and captioning  
`simulated`| None emitted at all| You only need the final transcript per utterance  
  
## Getting started

PythonJavaScriptcURL
    
    
    import asyncio
    
    import base64
    
    from sarvamai import AsyncSarvamAI, RealtimeAudioInput, RealtimeEnd
    
    API_KEY = "YOUR_SARVAM_API_KEY"
    
    async def transcribe(audio_chunks):
    
        """audio_chunks: an async iterator yielding raw linear16 PCM bytes."""
    
        client = AsyncSarvamAI(api_subscription_key=API_KEY)
    
        async with client.speech_to_text_realtime_streaming.connect(
    
            language_code="hi-IN",
    
            stream_type="fast",
    
        ) as ws:
    
            async def send_audio():
    
                async for chunk in audio_chunks:
    
                    await ws.send_realtime_audio_input(
    
                        RealtimeAudioInput(audio=base64.b64encode(chunk).decode("utf-8"))
    
                    )
    
                await ws.send_realtime_end(RealtimeEnd())
    
            async def receive_events():
    
                async for message in ws:
    
                    if message.event == "transcript.partial":
    
                        print(f"partial: {message.text}")
    
                    elif message.event == "transcript.final":
    
                        print(f"final: {message.text}")
    
                        return  # one-shot script: stop after the first utterance's final
    
                    elif message.event == "error":
    
                        print(f"error ({message.code}): {message.message}")
    
                        if message.is_fatal:
    
                            return
    
            await asyncio.gather(send_audio(), receive_events())
    
    async def pcm_chunks_from_file(path, chunk_size=3200):
    
        """Yields raw linear16 PCM chunks (~100ms each at 16kHz mono 16-bit)."""
    
        with open(path, "rb") as f:
    
            while chunk := f.read(chunk_size):
    
                yield chunk
    
                await asyncio.sleep(0.1)  # pace it like real-time audio
    
    if __name__ == "__main__":
    
        asyncio.run(transcribe(pcm_chunks_from_file("path/to/audio.pcm")))

To try the latest model, pass `model="saaras:v4"` when connecting. Connection parameters and message events are identical to `saaras:v3-realtime`, and `model="saaras:v4"` additionally supports `keyterms` — see [Keyterm Prompting](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/keyterms).

## Turn detection

  * **`vad`** (default): the server runs its own VAD and emits `vad.speech_start`/`vad.speech_end` automatically. Tune with `threshold`, `silence_duration_ms`, `min_speech_duration_ms`.
  * **`manual`** : the client delimits turns itself by sending `{"event": "speech_start"}` and `{"event": "speech_end"}`. VAD parameters have no effect. A `{"event": "flush"}` message force-finalizes buffered audio without waiting for `speech_end`.



## Language support

`language_code` is **required**. 24 values are accepted, including adaptive auto-detection:

Language| Code| | Language| Code  
---|---|---|---|---  
Auto-detect| `auto`| | Urdu| `ur-IN`  
English| `en-IN`| | Nepali| `ne-IN`  
Hindi| `hi-IN`| | Konkani| `kok-IN`  
Bengali| `bn-IN`| | Kashmiri| `ks-IN`  
Kannada| `kn-IN`| | Sindhi| `sd-IN`  
Malayalam| `ml-IN`| | Sanskrit| `sa-IN`  
Marathi| `mr-IN`| | Santali| `sat-IN`  
Odia| `or-IN`| | Manipuri| `mni-IN`  
Punjabi| `pa-IN`| | Bodo| `brx-IN`  
Tamil| `ta-IN`| | Maithili| `mai-IN`  
Telugu| `te-IN`| | Dogri| `doi-IN`  
Gujarati| `gu-IN`| | Assamese| `as-IN`  
  
**Odia’s code changed.** The legacy Streaming API uses `od-IN` for Odia; this endpoint uses `or-IN`.

With `language_code="auto"`, `transcript.partial` and `transcript.final` include a detected `language` field (`transcript.final` also adds `language_confidence`). With a specific `language_code`, neither field is present.

## Message reference

**Client to server:** `audio_input` (`{"event": "audio_input", "audio": "<base64>"}`), `speech_start` / `speech_end` / `flush` (manual mode only), `config.update` (change settings mid-call, see below), `end` (graceful close), `ping` (keepalive).

**Server to client:** `session.begin` (sent on connect), `vad.speech_start` / `vad.speech_end`, `transcript.partial`, `transcript.final`, `config.updated`, `pong`, `session.end` (includes `audio_duration_s`, the billed audio), `error` (`code`, `is_fatal`, `message`).

### Live config updates

Change settings mid-call without reconnecting:
    
    
    from sarvamai import RealtimeConfigUpdate
    
    await ws.send_realtime_config_update(
    
        RealtimeConfigUpdate(mode="translate", prompt="medical terminology")
    
    )

`language_code`, `prompt`, `mode`, `stream_type`, and `endpointing` apply at the next utterance boundary. `threshold`, `silence_duration_ms`, and `min_speech_duration_ms` apply immediately (`vad` mode only). `encoding`, `sample_rate`, and `return_timestamps` are connection-only.

## Error handling

Close code| Meaning  
---|---  
`1003`| Rate limit, quota exceeded, or invalid subscription key  
`1008`| Inactivity timeout, send periodic `ping`s to avoid this  
`1011`| Internal server error, retry with backoff  
`4000`| Invalid `model`/`language_code`/parameter, or account not enabled  
  
## Best practices

  * Use `stream_type="fast"` for conversational agents; reach for `simulated` only if you truly don’t need partials.
  * Drive barge-in off `vad.speech_start` or early partials, not `transcript.final`.
  * Reconfigure with `config.update` instead of reconnecting when you can.
  * Reconcile billing against `session.end.audio_duration_s`, the server-authoritative value.



Full endpoint reference: [Realtime Streaming](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/realtime/ws) API reference.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)[Best Practices for Speech-to-TextNext](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/best-practices)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)
      * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
      * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)
      * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
      * [Realtime Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming)
      * [Best Practices](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/best-practices)
      * [FAQs](https://docs.sarvam.ai/api/speech-to-text/faq)
      * How-to

      * Use Cases

      * Legacy

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


