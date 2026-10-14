---
url: https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/
title: Streaming Text-to-Speech API | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:46.222502+00:00
---

# Streaming Text-to-Speech API | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/

Skip to navigation

On this page

  * Why WebSocket Streaming
  * Code Examples
  * Best Practices
  * End of Speech Signal
  * Using send_completion_event
  * Streaming TTS WebSocket – Integration Guide
  * Input Message Types
  * Handling Disconnects
  * Voice-Agent Barge-In



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Text to Speech](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)[Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream)

# Streaming Text-to-Speech API

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket.md "View this page as plain text")|More actions

This page is for Model APIs.

WebSocket-based streaming endpoint that sends audio chunks progressively as text is processed. Connect once, stream text in, receive audio out, no polling, no repeated HTTP calls.

For complete API reference documentation, see the [Text-to-Speech API Reference](https://docs.sarvam.ai/api-reference/text-to-speech/convert) section.

**Common use cases:**

  * **Conversational AI agents** : Stream TTS responses in real time for voice-based assistants
  * **Interactive podcasts** : Generate and play back dialogue on the fly with minimal delay
  * **Low-latency applications** : Any scenario where time-to-first-byte (TTFB) matters (IVR, live narration, kiosks)



## Why WebSocket Streaming

Low Latency Playback

Audio playback begins as soon as the first chunk is synthesized, no need to wait for the full response.

11 Languages (10 Indian + English)

Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia, and English (Indian accent).

Persistent Connection

Single WebSocket connection handles multiple text to speech conversions. Send config once, then stream text continuously.

SDK Support

Python (`AsyncSarvamAI`) and JavaScript (`SarvamAIClient`) SDKs with built-in async/await and event-driven patterns for seamless integration.

## Code Examples

### Best Practices

  * Always send the config message first
  * Use flush messages strategically to ensure complete text processing
  * Send ping messages to maintain long-running connections



PythonJavaScript
    
    
    import asyncio
    
    import base64
    
    from sarvamai import AsyncSarvamAI, AudioOutput
    
    async def tts_stream():
    
        client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
        async with client.text_to_speech_streaming.connect(model="bulbul:v4-flash") as ws:
    
            await ws.configure(language_code="hi-IN", speaker="simran_en_customer")
    
            print("Sent configuration")
    
            long_text = (
    
                "भारत की संस्कृति विश्व की सबसे प्राचीन और समृद्ध संस्कृतियों में से एक है।"
    
                "यह विविधता, सहिष्णुता और परंपराओं का अद्भुत संगम है, "
    
                "जिसमें विभिन्न धर्म, भाषाएं, त्योहार, संगीत, नृत्य, वास्तुकला और जीवनशैली शामिल हैं।"
    
            )
    
            await ws.convert(long_text)
    
            print("Sent text message")
    
            await ws.flush()
    
            print("Flushed buffer")
    
            # Audio streams back as chunks. The server keeps the socket open for
    
            # any further text, so we stop once no new audio arrives within a short
    
            # window (the `async with` block closes the connection on exit).
    
            chunk_count = 0
    
            with open("output.mp3", "wb") as f:
    
                while True:
    
                    try:
    
                        message = await asyncio.wait_for(ws.recv(), timeout=3.0)
    
                    except asyncio.TimeoutError:
    
                        break
    
                    if isinstance(message, AudioOutput):
    
                        chunk_count += 1
    
                        f.write(base64.b64decode(message.data.audio))
    
                        f.flush()
    
            print(f"All {chunk_count} chunks saved to output.mp3")
    
            print("Audio generation complete")
    
    if __name__ == "__main__":
    
        asyncio.run(tts_stream())
    
    # --- Notebook/Colab usage ---
    
    # await tts_stream()

## End of Speech Signal

The TTS streaming API now supports an end of speech signal that allows for clean stream termination when speech generation is complete.

### Using `send_completion_event`

When you set `send_completion_event=True` in the connection, the API will send a completion event when speech generation ends, allowing your application to handle stream termination gracefully.

Python
    
    
    import asyncio
    
    import base64
    
    from sarvamai import AsyncSarvamAI, AudioOutput, EventResponse
    
    async def tts_stream():
    
        client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
        async with client.text_to_speech_streaming.connect(
    
            model="bulbul:v4-flash", send_completion_event=True
    
        ) as ws:
    
            await ws.configure(
    
                language_code="hi-IN",
    
                speaker="simran_en_customer",
    
            )
    
            print("Sent configuration")
    
            long_text = (
    
                "भारत की संस्कृति विश्व की सबसे प्राचीन और समृद्ध "
    
                "संस्कृतियों में से एक है।"
    
                "यह विविधता, सहिष्णुता और परंपराओं का अद्भुत संगम है, "
    
                "जिसमें विभिन्न धर्म, भाषाएं, त्योहार, संगीत, नृत्य, "
    
                "वास्तुकला और जीवनशैली शामिल हैं।"
    
            )
    
            await ws.convert(long_text)
    
            print("Sent text message")
    
            await ws.flush()
    
            print("Flushed buffer")
    
            chunk_count = 0
    
            with open("output.mp3", "wb") as f:
    
                async for message in ws:
    
                    if isinstance(message, AudioOutput):
    
                        chunk_count += 1
    
                        audio_chunk = base64.b64decode(message.data.audio)
    
                        f.write(audio_chunk)
    
                        f.flush()
    
                    elif isinstance(message, EventResponse):
    
                        print(f"Received completion event: {message.data.event_type}")
    
                        # Break when we receive the final event
    
                        if message.data.event_type == "final":
    
                            break
    
            print(f"All {chunk_count} chunks saved to output.mp3")
    
            print("Audio generation complete")
    
    if __name__ == "__main__":
    
        asyncio.run(tts_stream())
    
    # --- Notebook/Colab usage ---
    
    # await tts_stream()

## Streaming TTS WebSocket – Integration Guide

Easily convert text to speech in real time using Sarvam’s low-latency WebSocket-based TTS API.

### Input Message Types

###### Config Message

###### Text Message

###### Flush Message

###### Ping Message

Sets up voice parameters and must be the first message sent after connection. **Parameters:**

  * `min_buffer_size`: Minimum character length that triggers buffer flushing for TTS model processing
  * `max_chunk_length`: Maximum length for sentence splitting (adjust based on content length)
  * `output_audio_codec`: Supports multiple formats: `mp3`, `wav`, `aac`, `opus`, `flac`, `linear16` (LINEAR16), `mulaw` (μ-law), and `alaw` (A-law)
  * `output_audio_bitrate`: Choose from 5 supported bitrate options


    
    
    {
    
      "type": "config",
    
      "data": {
    
        "speaker": "simran_en_customer",
    
        "language_code": "en-IN",
    
        "pace": 1.2,
    
        "min_buffer_size": 50,
    
        "max_chunk_length": 200,
    
        "output_audio_codec": "mp3",
    
        "output_audio_bitrate": "128k"
    
      }
    
    }

## Handling Disconnects

Close code| Meaning| What to do  
---|---|---  
`1000`| Normal closure| You called `close()`, nothing to do  
`1001`| Going away| Server/client shutting down, reconnect  
`1006`| Abnormal closure (no close frame)| Network drop, reconnect with backoff  
`1011`| Server error| Retry with backoff; if persistent, check [status](https://status.sarvam.ai/)  
`4xxx`| Application-specific| Read the close reason (e.g. auth/quota); fix before reconnecting  
  
Codes `1000`–`1015` are standard WebSocket codes; `4000`–`4999` are application-specific, always read the accompanying close reason rather than assuming a fixed meaning. An idle connection closes automatically after ~1 minute, so send `ping()` to keep long-lived sessions open.

**Reconnect with exponential backoff** (pseudocode):
    
    
    attempt = 0
    
    while not connected and attempt < MAX_ATTEMPTS:
    
        try:
    
            open WebSocket, send config, resume sending text
    
            attempt = 0                      # reset on success
    
        except (close 1006 / 1011 / network error):
    
            delay = min(BASE * 2 ** attempt, MAX_DELAY)   # e.g. 0.5s, 1s, 2s, 4s ... capped
    
            sleep(delay + small random jitter)
    
            attempt += 1
    
        on close 4xxx (auth/quota): stop and surface the error  # do not blind-retry

Don’t auto-retry on `4xxx` auth/quota closes, fix the cause first (see [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)).

## Voice-Agent Barge-In

When a user interrupts the agent mid-reply, you want playback to stop instantly. The TTS WebSocket has **no server-side cancel/clear message** : `convert`, `flush`, `ping`, and `close` are the only client messages. Handle barge-in entirely on the client:

  1. **Stop playback locally** the moment your STT detects `speech_start`, flush/clear your local audio buffer and stop the player.
  2. **Close the TTS socket** for the interrupted utterance so the server stops generating (any in-flight chunks are simply discarded on your side).
  3. **Open a fresh connection** for the agent’s next reply.


    
    
    # In your STT speech_start handler (see the STT WebSocket barge-in recipe):
    
    tts_player.stop()        # 1. stop and clear local audio playback immediately
    
    await tts_ws.close()     # 2. close the TTS socket to stop further generation
    
    # 3. open a new client.text_to_speech_streaming.connect(...) for the next turn

Because there’s no in-band cancel, keep TTS replies chunked into shorter `convert()` calls so a barge-in discards less already-generated audio. See the [STT WebSocket barge-in recipe](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api), the LiveKit and Pipecat voice-agent guides, and [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits) for streaming concurrency limits.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream)[Pronunciation DictionaryNext](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)
      * [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)
      * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/which-api-to-use)
      * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)
      * Streaming API
        * [HTTP Stream](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream)
        * [WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket)

      * [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
      * [Best Practice Guide for Bulbul v4 Flash](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices)
      * [Best Practices (Bulbul v3)](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices)
      * How-to

      * Use Cases

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


