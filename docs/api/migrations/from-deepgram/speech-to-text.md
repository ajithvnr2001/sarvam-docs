---
url: https://docs.sarvam.ai/api/migrations/from-deepgram/speech-to-text/
title: Migrating Speech-to-Text from Deepgram to Sarvam | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:44.274023+00:00
---

# Migrating Speech-to-Text from Deepgram to Sarvam | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/migrations/from-deepgram/speech-to-text/

Skip to navigation

On this page

  * Quick start
  * Endpoint map
  * Parameter concept map
  * Diarization and long-form audio
  * Streaming
  * What’s different by design
  * Full example
  * Common mistakes
  * See also



Scroll to top

[Migrations](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)[From Deepgram](https://docs.sarvam.ai/api/migrations/from-deepgram/overview)

# Migrating Speech-to-Text from Deepgram to Sarvam

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/migrations/from-deepgram/speech-to-text.md "View this page as plain text")|More actions

This page is for Model APIs.

_Last updated: July 15, 2026_

This guide covers migrating Deepgram speech-to-text (transcription) API calls to Sarvam. If you’re building a full voice agent rather than transcribing audio directly, start from the [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit) or [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat) voice agent build guides instead: they aren’t a 1:1 API swap and aren’t covered here.

**In short:** swap `model` for `model`, read the transcript from a flatter response shape, and pick the right Sarvam API for the job: REST for short synchronous requests, Batch for diarized or very long audio, and WebSocket for real-time streaming.

## Quick start

Base URL and auth header change the same way for every Deepgram migration, so they’re folded in here rather than in a separate page:

| Deepgram| Sarvam  
---|---|---  
Base URL| `https://api.deepgram.com`| `https://api.sarvam.ai`  
Auth header| `Authorization: Token <api_key>`| `api-subscription-key: <api_key>`  
Auth failure status| `401`| `403`  
  
With that, replace the transcription call:

###### Before (Deepgram)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    from deepgram import DeepgramClient
    
    client = DeepgramClient(api_key="YOUR_DEEPGRAM_API_KEY")
    
    with open("audio.wav", "rb") as f:
    
        response = client.listen.v1.media.transcribe_file(
    
            request=f.read(),
    
            model="nova-3",
    
            language="en",
    
        )
    
    print(response.results.channels[0].alternatives[0].transcript)

The rest of this page covers the full endpoint and parameter mapping, diarization via the Batch API, streaming, and common mistakes.

## Endpoint map

The tables below aren’t a checklist to apply field-by-field: Quick Start above already shows the whole call swapped over in one go. Use these tables as a reference for what changed and why, not as a sequence of edits to make yourself.

| Deepgram| Sarvam  
---|---|---  
Synchronous transcription| `POST /v1/listen`| `POST /speech-to-text` (up to 30 seconds per request; use Batch for longer audio)  
Diarized or very long audio| Same `POST /v1/listen` call, with `diarize_model` set| Batch API: `POST /speech-to-text/job/v1` (create), upload, start, then poll or receive a webhook callback, up to 2 hours per file  
Real-time streaming transcription| `POST /v1/listen` (WebSocket upgrade)| `GET /speech-to-text/ws`  
  
## Parameter concept map

Deepgram| Sarvam| Note  
---|---|---  
`model` (`nova-3`, `nova-2`, and other version/domain variants)| `model` (`saaras:v3`)| One current model to pass, not a family of version and domain-specific variants  
`request` (raw audio bytes, e.g. `open(...).read()`)| `file` (an open file object)| Same idea; Sarvam takes the file handle directly rather than pre-reading it into bytes  
`language` (BCP-47, e.g. `en`; optional)| `language_code` (BCP-47, e.g. `en-IN`; optional; pass `unknown` to auto-detect)| Same concept, region-qualified codes on Sarvam’s side  
`diarize_model` (enables diarization on the same synchronous call)| `with_diarization` \+ `num_speakers` (Batch API only)| Same concept; on Sarvam, diarization is a Batch job parameter rather than a flag on the fast synchronous endpoint  
`smart_format` / `punctuate` / `numerals` (formatting toggles)| Handled automatically| Sarvam applies sensible formatting by default, so there’s no separate set of toggles to configure  
Response: `results.channels[0].alternatives[0].transcript` \+ `.words[]`| Response: `transcript` \+ `diarized_transcript.entries[]` (Batch, with `speaker_id` and segment timing)| Flatter response shape; no channel/alternative nesting to walk through  
  
Deepgram’s response also supports optional sentiment, topic, intent, and summary detection, and content redaction, layered on top of the transcript. Sarvam’s Speech-to-Text focuses on transcription accuracy, output modes (`transcribe`, `translate`, `verbatim`, `translit`, `codemix`), and Indian-language coverage; if you need that kind of downstream text analysis, run Sarvam’s transcript through [Chat Completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview) as a second step.

## Diarization and long-form audio

Deepgram enables diarization on the same synchronous call via `diarize_model`; Sarvam’s Batch API handles both diarization and long-form audio instead:

Before (Deepgram)After (Sarvam)
    
    
    from deepgram import DeepgramClient
    
    client = DeepgramClient(api_key="YOUR_DEEPGRAM_API_KEY")
    
    with open("meeting.wav", "rb") as f:
    
        response = client.listen.v1.media.transcribe_file(
    
            request=f.read(),
    
            model="nova-3",
    
            language="en",
    
            diarize_model="latest",
    
        )

See the [Batch API guide](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) for webhook setup and its [Speaker Diarization section](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#speaker-diarization) for the current per-job speaker limit.

## Streaming

| Deepgram| Sarvam  
---|---|---  
Connection config| WebSocket upgrade of `/v1/listen`: `model`, `language`, `encoding`, `sample_rate`, `interim_results`, `endpointing`| [WebSocket API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api) (`GET /speech-to-text/ws`): `model`, `mode`, `language_code`, `sample_rate`  
Server messages| `Results`, `Metadata`, `UtteranceEnd`, `SpeechStarted`| Transcript for your chosen `mode` directly, plus `START_SPEECH`/`END_SPEECH` events when `vad_signals=true`  
Turn-end detection| `endpointing` (silence duration before finalizing) + `vad_events`| `high_vad_sensitivity` \+ `vad_signals`: one automatic “this turn just ended” signal  
Partial transcripts| `interim_results` flag| No separate flag; returns the transcript for your chosen `mode` directly as each segment finalizes  
Finalize / close| `{"type": "Finalize"}` / `{"type": "CloseStream"}`| `flush_signal` plus an explicit `ws.flush()` call / simply closing the connection  
  
Deepgram also offers **Flux** (`flux-general-en`/`flux-general-multi`), a separate `GET /v2/listen` endpoint purpose-built for conversational turn detection, with its own tuning params (`eager_eot_threshold`, `eot_threshold`). Sarvam’s turn-detection features (`high_vad_sensitivity`, `vad_signals`) live in the same WebSocket API used for regular transcription, so there’s no separate model or endpoint to choose between for conversational use.

## What’s different by design

  * **One current model, not a version-and-domain matrix.** Deepgram’s `nova-3`, `nova-2-medical`, `nova-2-finance`, and similar domain-specific variants become a single `saaras:v3`, used the same way across REST, Batch, and Streaming.
  * **A flatter response shape.** `response.transcript` reads directly, rather than walking `results.channels[0].alternatives[0].transcript`.
  * **Diarization and long-form audio share one workflow.** The Batch API handles speaker diarization, files up to 2 hours, and multiple files per job in a single job-based flow, with the same `with_diarization`/`num_speakers` parameters either way.
  * **Flexible output modes on one model.** `saaras:v3` supports `transcribe`, `translate`, `verbatim`, `translit`, and `codemix` modes on the same endpoint.
  * **Indian language depth is Sarvam’s specific strength.** Saaras v3 covers 22 Indian languages, including Assamese, Konkani, Kashmiri, Sindhi, Sanskrit, Santali, Manipuri, Bodo, Maithili, and Dogri, with native handling for code-mixed speech like Hinglish.



## Full example

A small wrapper function, before and after, showing the complete set of changes together:

###### Before (Deepgram)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    from deepgram import DeepgramClient
    
    client = DeepgramClient(api_key="YOUR_DEEPGRAM_API_KEY")
    
    def transcribe(path: str) -> str:
    
        with open(path, "rb") as f:
    
            response = client.listen.v1.media.transcribe_file(
    
                request=f.read(),
    
                model="nova-3",
    
                language="en",
    
            )
    
        return response.results.channels[0].alternatives[0].transcript

## Common mistakes

###### Passing an open file handle instead of bytes

Sarvam’s `file` parameter takes the open file object directly (`file=open(path, "rb")`), unlike Deepgram’s `request`, which expects the bytes already read out (`request=f.read()`). Passing a file handle where Deepgram’s SDK expects bytes, or vice versa, is the most common porting slip.

###### Expecting diarization on the fast REST endpoint

Deepgram enables diarization on the same synchronous call via `diarize_model`. Sarvam’s `with_diarization` is a Batch API parameter instead, so diarized requests need to go through the Batch workflow even for a short file.

###### Walking the nested channels/alternatives path out of habit

Sarvam’s response is flat: `response.transcript`, not `response.results.channels[0].alternatives[0].transcript`. Update any code that destructures the Deepgram response shape.

###### Sending Batch parameters as top-level fields

Calling the Batch endpoints directly over HTTP (rather than through the SDK) requires nesting parameters under `job_parameters`, e.g. `{"job_parameters": {"model": "saaras:v3", ...}}`. A flat body modeled on Deepgram’s request shape won’t be picked up.

## See also

  * [Migration overview](https://docs.sarvam.ai/api/migrations/from-deepgram/overview): base URL, auth, and SDK client changes
  * [Which Speech-to-Text API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
  * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
  * [Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)
  * [Speaker Diarization](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#speaker-diarization)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/migrations/from-deepgram/text-to-speech)[Migrating from Gemini: OverviewNext](https://docs.sarvam.ai/api/migrations/from-gemini/overview)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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

    * Example Voice Agents

  * Self-Hosted Deployments

    * Overview

    * AWS SageMaker

  *     * Migrations
      * From ElevenLabs

      * From Cartesia

      * From Deepgram
        * [Overview](https://docs.sarvam.ai/api/migrations/from-deepgram/overview)
        * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-deepgram/text-to-speech)
        * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-deepgram/speech-to-text)

      * From Gemini




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


