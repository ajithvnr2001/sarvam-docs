---
url: https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api/
title: Streaming Speech-to-Text API | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:20.527020+00:00
---

# Streaming Speech-to-Text API | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api/

Skip to navigation

On this page

  * Overview
  * Supported Modes (Saaras v3 and v4)
  * Key Benefits
  * Common Use Cases
  * Getting Started
  * Choosing a Mode
  * Full Example
  * Enhanced Processing with Voice Detection
  * Instant Processing with Flush Signals
  * Custom Audio Configuration
  * Handling Disconnects
  * Voice-Agent Barge-In
  * API Reference
  * Connection Parameters
  * Fine VAD Tuning Parameters
  * Audio Data Parameters
  * Response Types
  * Key Differences: STT vs STTT
  * Best Practices



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Speech to Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)[Legacy](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)

# Streaming Speech-to-Text API

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api.md "View this page as plain text")|More actions

This page is for Model APIs.

## Overview

Transform audio into text in real-time with our WebSocket-based streaming API. Built for applications requiring immediate speech processing with minimal delay.

For complete API reference documentation, see the [Speech-to-Text WebSocket API Reference](https://docs.sarvam.ai/api-reference/legacy/speech-to-text/transcribe/ws) section.

**Looking for lower latency and true partial transcripts?** [Realtime Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming) (`saaras:v3-realtime`, beta) supersedes this endpoint for new voice-agent and live-transcription work, interim transcripts as the user speaks, millisecond-based VAD tuning, and live mid-call reconfiguration. This page documents the generally-available legacy WebSocket (`saaras:v3`).

**Model Availability:** The Speech-to-Text streaming endpoint (`/speech-to-text/ws`) now defaults to **Saaras v4** , with `saaras:v3` also accepted. The Speech-to-Text-Translate streaming endpoint (`/speech-to-text-translate/ws`) defaults to **Saaras v3** , with `saaras:v2.5` kept on the translate endpoint for backward compatibility, and `saaras:v4` also accepted. Saaras v3 and v4 support multiple output modes via the `mode` parameter (`translate`, `transcribe`, `verbatim`, `translit`, `codemix`) on both endpoints.

### Supported Modes (Saaras v3 and v4)

Mode| Description| Output  
---|---|---  
`transcribe`| Standard transcription in the original language| Text in source language  
`translate`| Transcribe and translate to English| English text  
`verbatim`| Word-for-word transcription including filler words and repetitions| Verbatim text in source language  
`translit`| Transcribe and transliterate to Roman script| Romanized text  
`codemix`| Transcribe code-mixed speech (e.g., Hindi-English) naturally| Code-mixed text  
  
### Key Benefits

Ultra-Low Latency

Get transcription results in milliseconds, not seconds. Process speech as it happens with near-instantaneous responses.

Multi-Language Support

Support for 10+ Indian languages plus English with high accuracy transcription and translation capabilities.

Advanced Voice Detection

Smart Voice Activity Detection (VAD) with customizable sensitivity for optimal speech boundary detection.

### Common Use Cases

  * **Live Transcription** : Real-time captions for meetings, webinars, and broadcasts
  * **Voice Assistants** : Interactive voice applications with immediate responses
  * **Call Centers** : Live call transcription and analysis
  * **Accessibility** : Real-time captioning for hearing-impaired users



**Audio Format Support** : Streaming APIs only support **two audio formats** :

  * **WAV** (`wav`)
  * **Raw PCM** (`pcm_s16le`, `pcm_l16`, `pcm_raw`)



Other formats like MP3, AAC, OGG, etc. are not supported for WebSocket streaming. Find sample audio files in our [GitHub cookbook](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/sample_data/stt).

**Python SDK limitation:** `ws.transcribe()`’s `encoding` argument is currently fixed to `"audio/wav"` (the SDK’s `AudioData` type only accepts that literal), passing a PCM value there raises a client-side `ValidationError` before any network call. Raw PCM (`pcm_s16le`, `pcm_l16`, `pcm_raw`) can only be sent today via a hand-rolled WebSocket client, not the Python SDK’s per-message helper.

## Getting Started

Get up and running with streaming in minutes. Simply change the `mode` parameter to switch between transcription, translation, and other output formats.

### Choosing a Mode

**JS/Node SDK limitation:** The JS SDK’s `connect()` does not currently support the `mode` parameter, it has no `mode` field in `ConnectArgs`, so any `mode` you pass is silently dropped and the connection always runs in the default `transcribe` mode. The Python SDK examples on this page work as shown. To use `translate`, `verbatim`, `translit`, or `codemix` from Node today, connect via a raw WebSocket client and append `?mode=...` to the URL yourself.

###### Saaras v3

###### Saaras v4

Still available on this endpoint.

###### Transcribe

###### Translate

###### Verbatim

###### Translit

###### Codemix

Transcribe audio in the original language.

PythonJavaScript
    
    
    async with client.speech_to_text_streaming.connect(
    
        model="saaras:v3",
    
        mode="transcribe",              # Standard transcription
    
        language_code="en-IN",
    
        high_vad_sensitivity=True
    
    ) as ws:
    
        await ws.transcribe(audio=audio_data)
    
        response = await ws.recv()
    
        print(f"Transcription: {response}")

### Full Example

Here’s a complete working example. Change the `mode` parameter to switch between any of the supported modes:

PythonJavaScript
    
    
    import asyncio
    
    import base64
    
    from sarvamai import AsyncSarvamAI
    
    # Load your audio file
    
    with open("path/to/your/audio.wav", "rb") as f:
    
        audio_data = base64.b64encode(f.read()).decode("utf-8")
    
    async def basic_transcription():
    
        # Initialize client with your API key
    
        client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
        # Connect and transcribe: change mode as needed
    
        async with client.speech_to_text_streaming.connect(
    
            model="saaras:v4",
    
            mode="transcribe",
    
            language_code="en-IN",
    
            high_vad_sensitivity=True
    
        ) as ws:
    
            await ws.transcribe(audio=audio_data)
    
            response = await ws.recv()
    
            print(f"Result: {response}")
    
    asyncio.run(basic_transcription())

### Enhanced Processing with Voice Detection

Add smart voice activity detection for better accuracy and control:

PythonJavaScript
    
    
    import asyncio
    
    import base64
    
    from sarvamai import AsyncSarvamAI
    
    with open("path/to/your/audio.wav", "rb") as f:
    
        audio_data = base64.b64encode(f.read()).decode("utf-8")
    
    async def enhanced_transcription():
    
        client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
        async with client.speech_to_text_streaming.connect(
    
            model="saaras:v4",
    
            mode="transcribe",              # Change mode as needed
    
            language_code="hi-IN",
    
            high_vad_sensitivity=True,       # Better voice detection
    
            vad_signals=True                # Get speech start/end signals
    
        ) as ws:
    
            await ws.transcribe(
    
                audio=audio_data,
    
                encoding="audio/wav",
    
                sample_rate=16000
    
            )
    
            
    
            async for message in ws:
    
                if message.type == "events":
    
                    # VAD signals arrive as events (signal_type is START_SPEECH / END_SPEECH)
    
                    print(f"Voice activity: {message.data.signal_type}")
    
                elif message.type == "data":
    
                    print(f"Result: {message.data.transcript}")
    
                    break
    
    asyncio.run(enhanced_transcription())

### Instant Processing with Flush Signals

Force immediate processing without waiting for silence detection:

PythonJavaScript
    
    
    import asyncio
    
    import base64
    
    from sarvamai import AsyncSarvamAI
    
    with open("path/to/your/audio.wav", "rb") as f:
    
        audio_data = base64.b64encode(f.read()).decode("utf-8")
    
    async def instant_processing():
    
        client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
        async with client.speech_to_text_streaming.connect(
    
            model="saaras:v4",
    
            mode="transcribe",              # Change mode as needed
    
            language_code="en-IN",
    
            flush_signal=True               # Enable manual control
    
        ) as ws:
    
            await ws.transcribe(
    
                audio=audio_data,
    
                encoding="audio/wav",
    
                sample_rate=16000
    
            )
    
            
    
            # Force immediate processing
    
            await ws.flush()
    
            async for message in ws:
    
                print(f"Result: {message}")
    
                break
    
    asyncio.run(instant_processing())

### Custom Audio Configuration

Optimize for your specific audio setup (e.g., 8kHz telephony audio):

PythonJavaScript
    
    
    import asyncio
    
    import base64
    
    from sarvamai import AsyncSarvamAI
    
    with open("path/to/your/audio.wav", "rb") as f:
    
        audio_data = base64.b64encode(f.read()).decode("utf-8")
    
    async def custom_audio_config():
    
        client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
        async with client.speech_to_text_streaming.connect(
    
            model="saaras:v4",
    
            mode="transcribe",              # Change mode as needed
    
            language_code="kn-IN",
    
            sample_rate=8000,               # Match your audio
    
            high_vad_sensitivity=True
    
        ) as ws:
    
            await ws.transcribe(
    
                audio=audio_data,
    
                encoding="audio/wav",       # Python SDK currently only supports "audio/wav"
    
                sample_rate=8000             # Must match connection setting
    
            )
    
            
    
            response = await ws.recv()
    
            print(f"Result: {response}")
    
    asyncio.run(custom_audio_config())

**Important: Sample Rate Configuration for 8kHz Audio**

When working with 8kHz audio, you **must** set the `sample_rate` parameter in **both** places:

  1. **When connecting to the WebSocket** (connection parameter)
  2. **When sending audio data** (transcribe parameter)



Both values must match your audio’s actual sample rate. Mismatched sample rates will result in poor transcription quality or errors.
    
    
    async with client.speech_to_text_streaming.connect(
    
        model="saaras:v4",
    
        mode="transcribe",
    
        language_code="en-IN",
    
        sample_rate=8000        # Must match your audio
    
    ) as ws:
    
        await ws.transcribe(
    
            audio=audio_data,
    
            sample_rate=8000    # Must match connection setting
    
        )

For detailed endpoint documentation, see: [Speech-to-Text WebSocket](https://docs.sarvam.ai/api-reference/legacy/speech-to-text/transcribe/ws) | [Speech-to-Text Translate WebSocket](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate/ws)

## Handling Disconnects

Long-lived sockets will occasionally drop (network blips, idle timeouts, server restarts). Inspect the WebSocket close code and reconnect with backoff.

Close code| Meaning| What to do  
---|---|---  
`1000`| Normal closure| You called `close()`, nothing to do  
`1001`| Going away| Server or client shutting down, reconnect  
`1006`| Abnormal closure (no close frame)| Network drop, reconnect with backoff  
`1011`| Server error| Retry with backoff; if persistent, check [status](https://status.sarvam.ai/)  
`4xxx`| Application-specific| Read the close reason for details (e.g. auth or quota); fix before reconnecting  
  
Codes `1000`–`1015` are standard WebSocket codes. Any `4000`–`4999` code is application-specific, always read the accompanying close reason string rather than assuming a fixed meaning.

**Reconnect with exponential backoff** (pseudocode, applies to both SDKs):
    
    
    attempt = 0
    
    while not connected and attempt < MAX_ATTEMPTS:
    
        try:
    
            open WebSocket and resume streaming
    
            attempt = 0                      # reset on success
    
        except (close 1006 / 1011 / network error):
    
            delay = min(BASE * 2 ** attempt, MAX_DELAY)   # e.g. 0.5s, 1s, 2s, 4s ... capped
    
            sleep(delay + small random jitter)
    
            attempt += 1
    
        on close 4xxx (auth/quota): stop and surface the error  # do not blind-retry

Do not auto-retry on `4xxx` auth/quota closes, fix the underlying issue first (see [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)).

## Voice-Agent Barge-In

In a voice agent, the user may start speaking while your TTS reply is still playing (“barge-in”). Use `vad_signals=true` and treat the `START_SPEECH` event as the cue to **stop playback immediately** and let the user take the turn.
    
    
    async with client.speech_to_text_streaming.connect(
    
        model="saaras:v4",
    
        mode="transcribe",
    
        language_code="hi-IN",
    
        high_vad_sensitivity=True,   # ~64ms silence boundary at 16kHz, snappier for conversation
    
        vad_signals=True,            # emit START_SPEECH / END_SPEECH events
    
    ) as ws:
    
        await ws.transcribe(audio=mic_chunk, encoding="audio/wav", sample_rate=16000)
    
        async for message in ws:
    
            if message.type == "events" and message.data.signal_type == "START_SPEECH":
    
                tts_player.stop()          # barge-in: cut off the agent's current reply
    
            elif message.type == "data":
    
                handle_user_turn(message.data.transcript)

For conversational use, prefer `high_vad_sensitivity=True` (~64ms silence boundary at 16kHz. See the Fine VAD Tuning table below) so the agent reacts quickly. See the LiveKit and Pipecat voice-agent integration guides for full agent setups, and [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits) for concurrency limits on streaming connections.

## API Reference

### Connection Parameters

Configure your WebSocket connection with these parameters:

Parameter| Type| Description| Example  
---|---|---|---  
`language_code`| string| Language for speech recognition (STT only)| `"en-IN"`, `"hi-IN"`, `"kn-IN"`  
`model`| string| Model version to use. `"saaras:v4"` (default) or `"saaras:v3"` on the STT endpoint| `"saaras:v4"` (STT), `"saaras:v2.5"` (STT-Translate)  
`mode`| string| Output mode (**STT endpoint / saaras:v3 and saaras:v4 only**): transcribe, translate, verbatim, translit, codemix| `"transcribe"`  
`keyterms`| string| JSON-encoded list of keyterms to bias recognition (**STT endpoint,`saaras:v4` only**). Up to 50 terms, 64 characters each| `["Sarvam","New Delhi","Vistaar"]`  
`sample_rate`| integer| Audio sample rate in Hz| `8000`, `16000`  
`input_audio_codec`| string| Audio codec format. Only `wav` and raw PCM formats (`pcm_s16le`, `pcm_l16`, `pcm_raw`) are supported| `"wav"`, `"pcm_s16le"`  
`high_vad_sensitivity`| boolean| Enhanced voice activity detection| `true`, `false`  
`vad_signals`| boolean| Receive speech start/end events| `true`, `false`  
`flush_signal`| boolean| Enable manual buffer flushing| `true`, `false`  
  
### Fine VAD Tuning Parameters

For finer control than the `high_vad_sensitivity` preset, both the STT and STT-Translate WebSockets accept these optional parameters. Any value you pass overrides the server default (and the `high_vad_sensitivity` preset, where they overlap):

Parameter| Type| Description| Default| `high_vad_sensitivity=true`  
---|---|---|---|---  
`positive_speech_threshold`| float| VAD probability (0.0–1.0) above which a frame counts as speech| `0.7`| `0.7`  
`negative_speech_threshold`| float| VAD probability (0.0–1.0) below which a frame counts as silence| `0.45`| `0.5`  
`min_speech_frames`| integer| Consecutive speech frames required to start a speech segment| `2`| `2`  
`first_turn_min_speech_frames`| integer| Speech frames required specifically for the first user turn| `8`| `8`  
`negative_frames_count`| integer| Silence frames within the window needed to end a speech segment| `18`| `2`  
`negative_frames_window`| integer| Sliding window size (in frames) over which silence frames are counted| `24`| `2`  
`start_speech_volume_threshold`| float| Volume (dB) below which audio is treated as too quiet to be speech| None (no volume filtering)| None  
`interrupt_min_speech_frames`| integer| Speech frames required to register a barge-in / interruption| `2`| `2`  
`pre_speech_pad_frames`| integer| Audio frames prepended before the detected speech onset so the start isn’t clipped| `9`| `9`  
`num_initial_ignored_frames`| integer| Leading audio frames skipped at connection start (e.g. setup noise)| `0`| `0`  
  
One frame is **512 audio samples** : 32 ms at 16 kHz, 64 ms at 8 kHz. All fine VAD parameters are optional; if you only need quicker end-of-speech detection, start with `high_vad_sensitivity=true` before reaching for these.

### Audio Data Parameters

When sending audio data to the streaming endpoint:

Parameter| Type| Description| Required  
---|---|---|---  
`audio`| string| Base64-encoded audio data|   
`encoding`| string| Audio format. The Python SDK’s `transcribe()` helper currently only accepts `"audio/wav"`|   
`sample_rate`| integer| Audio sample rate (16000 Hz recommended). Must match the connection parameter|   
  
### Response Types

When `vad_signals=true`, you’ll receive different message types:

**For STT:**

  * **`speech_start`** : Voice activity detected
  * **`speech_end`** : Voice activity stopped
  * **`transcript`** : Final transcription result



**For STTT:**

  * **`speech_start`** : Voice activity detected
  * **`speech_end`** : Voice activity stopped
  * **`translation`** : Final translation result



### Key Differences: STT vs STTT

Aspect| STT| STTT  
---|---|---  
Model| `saaras:v4` (default), `saaras:v3`| `saaras:v3` (default), `saaras:v4`, `saaras:v2.5` (legacy)  
Method| `transcribe()`| `translate()`  
Mode| `transcribe`, `verbatim`, `translit`, `codemix` (saaras:v3/v4 only)| `translate` (default), `transcribe`, `verbatim`, `translit`, `codemix` (saaras:v3/v4 only)  
Language Code| Required| Not required (auto-detected)  
Output Language| Same as input| English only  
  
### Best Practices

  * **Audio Quality & Sample Rate**: 
    * Use 16kHz sample rate for best results
    * For 8kHz audio, **always set`sample_rate=8000` in both connection and transcribe/translate calls**
    * Ensure both sample rate parameters match your actual audio sample rate
  * **Silence Handling** : 
    * Use 1 second silence when `high_vad_sensitivity=false`
    * Use ~64ms silence at 16kHz when `high_vad_sensitivity=true` (see the Fine VAD Tuning table for exact frame counts)
  * **Continuous Streaming** : Send audio data continuously for real-time results
  * **Error Handling** : Always implement proper WebSocket error handling
  * **Model Selection** : 
    * Use Saaras (`saaras:v3` or `saaras:v4`) with the `mode` parameter for the best transcription quality and flexible output modes (use `mode="transcribe"` for same-language transcription and `mode="translate"` for direct translation to English)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/agri-rural)[Text-to-Speech OverviewNext](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
        * [Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)

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


