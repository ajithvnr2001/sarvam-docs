---
url: https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text/
title: Migrating Speech-to-Text from ElevenLabs to Sarvam | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:45.381847+00:00
---

# Migrating Speech-to-Text from ElevenLabs to Sarvam | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text/

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

[Migrations](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)[From ElevenLabs](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)

# Migrating Speech-to-Text from ElevenLabs to Sarvam

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text.md "View this page as plain text")|More actions

This page is for Model APIs.

_Last updated: July 15, 2026_

This guide covers migrating ElevenLabs speech-to-text (transcription) API calls to Sarvam. If you’re building a full voice agent rather than transcribing audio directly, start from the [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit) or [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat) voice agent build guides instead: they aren’t a 1:1 API swap and aren’t covered here.

**In short:** swap `model_id` for `model`, upload the audio file directly instead of passing a `source_url`, and pick the right Sarvam API for the job: REST for short synchronous requests, Batch for long-form or multi-speaker audio, and WebSocket for real-time streaming.

## Quick start

Base URL and auth header change the same way for every ElevenLabs migration, so they’re folded in here rather than in a separate page:

| ElevenLabs| Sarvam  
---|---|---  
Base URL| `https://api.elevenlabs.io`| `https://api.sarvam.ai`  
Auth header| `xi-api-key`| `api-subscription-key`  
Auth failure status| `401`| `403`  
  
With that, replace the synchronous transcription call:

###### Before (ElevenLabs)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    from elevenlabs import ElevenLabs
    
    client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")
    
    with open("audio.mp3", "rb") as f:
    
        transcription = client.speech_to_text.convert(
    
            file=f,
    
            model_id="scribe_v2",
    
            language_code="eng",
    
            tag_audio_events=True,
    
        )
    
    print(transcription.text)

`with_diarization` and `num_speakers` are Batch API parameters. For a request like this one under 30 seconds, use the REST call above; for diarized or longer audio, use the Batch workflow below.

The rest of this page covers the full endpoint and parameter mapping, diarization via the Batch API, streaming, and common mistakes.

## Endpoint map

The tables below aren’t a checklist to apply field-by-field: Quick Start above already shows the whole call swapped over in one go. Use these tables as a reference for what changed and why, not as a sequence of edits to make yourself.

| ElevenLabs| Sarvam  
---|---|---  
Synchronous transcription| `POST /v1/speech-to-text`| `POST /speech-to-text` (up to 30 seconds of audio per request)  
Long-form or multi-speaker transcription| `POST /v1/speech-to-text` with `webhook: true`| Batch API: `POST /speech-to-text/job/v1` (create), upload, start, then poll or receive a webhook callback, up to 2 hours per file and 20 files per job  
Real-time streaming transcription| `wss://.../v1/speech-to-text/realtime`| `GET /speech-to-text/ws`  
  
## Parameter concept map

ElevenLabs| Sarvam| Note  
---|---|---  
`model_id` (`scribe_v1` or `scribe_v2` for REST and webhook requests; `scribe_v2_realtime` is a separate value used only on the WebSocket)| `model` (`saaras:v3`)| One current model across REST, Batch, and Streaming, rather than a different model_id per endpoint  
`file` or `source_url` (fetch directly from a hosted URL)| `file` (upload the audio/video file directly)| Download the source once, then upload it: a single, predictable step for every request  
`language_code` (optional, ISO-639-1/3, e.g. `eng`)| `language_code` (optional, BCP-47, e.g. `ta-IN`; pass `unknown` to auto-detect)| Same idea; `unknown` gives you the same auto-detect behavior as leaving ElevenLabs’ `language_code` unset  
`diarize` (boolean)| `with_diarization` (boolean, Batch API)| Same concept; on Sarvam this is a Batch job parameter alongside `num_speakers`  
`tag_audio_events` (boolean, tags laughter/applause, default `true`)| Not applicable| Sarvam transcripts contain spoken words only, so there’s nothing to toggle for non-speech event tags  
`webhook` (boolean flag on the same endpoint)| `callback` (`url` \+ `auth_token`, set when creating a Batch job)| Async processing lives in the Batch API rather than a flag on the sync endpoint; same idea, one dedicated workflow for longer audio  
Response: `text` \+ `words[]` (word-level timing, speaker IDs)| Response: `transcript` \+ `diarized_transcript.entries[]` (Batch, with `speaker_id` and segment timing)| Field names differ; see the timestamps note below for granularity  
  
Sarvam’s Batch API returns timestamps per chunk (sentence or phrase segment), which is precise enough for subtitle alignment and audio navigation. If your ElevenLabs integration reads individual `words[].start`/`end` for word-by-word highlighting, adjust it to work at the chunk level instead.

## Diarization and long-form audio

ElevenLabs’ `/v1/speech-to-text` has no separate mode for this; Sarvam’s Batch API handles both:

Before (ElevenLabs)After (Sarvam)
    
    
    from elevenlabs import ElevenLabs
    
    client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")
    
    transcription = client.speech_to_text.convert(
    
        file=open("meeting.mp3", "rb"),
    
        model_id="scribe_v2",
    
        diarize=True,
    
        num_speakers=3,
    
        webhook=True,
    
    )

See the [Batch API guide](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) for webhook setup and its [Speaker Diarization section](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#speaker-diarization) for the current per-job speaker limit.

## Streaming

| ElevenLabs| Sarvam  
---|---|---  
Connection config| Realtime WebSocket (`wss://.../v1/speech-to-text/realtime`): `model_id: scribe_v2_realtime`, `language_code`, `audio_format`| [WebSocket API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api) (`GET /speech-to-text/ws`): `model="saaras:v3"`, `mode`, `language_code`  
Streamed events| `partial_transcript` events, then `committed_transcript` (or `committed_transcript_with_timestamps`) once a segment finalizes| Transcript for your chosen `mode` directly, plus `START_SPEECH`/`END_SPEECH` events when `vad_signals=true`  
Finalizing a segment| `commit` flag on the audio chunk, or VAD `commit_strategy`| `flush_signal` plus an explicit `ws.flush()` call, or automatic end-of-speech detection via `high_vad_sensitivity`  
  
## What’s different by design

  * **One current model, not a version matrix.** ElevenLabs’ `scribe_v1`, `scribe_v2`, and `scribe_v2_realtime` become a single `saaras:v3`, used the same way across REST, Batch, and Streaming.
  * **Direct file upload, no third-party fetch.** Sarvam transcribes the file you send it. Download the source once (from a URL, cloud storage, or elsewhere) and upload it directly, so every request starts from the same predictable input.
  * **Diarization and long-form audio share one workflow.** The Batch API handles speaker diarization, files up to 2 hours, and multiple files per job in a single job-based flow, using the same `with_diarization`/`num_speakers` parameters whether the request is a short call or a large batch.
  * **A consistent response shape.** Whether diarization is on or off, Sarvam always returns the same `transcript` (plus `diarized_transcript` when enabled), rather than switching structure based on a multichannel or output-style flag.
  * **Indian language depth is Sarvam’s specific strength.** Saaras v3 covers 22 Indian languages, including Assamese, Konkani, Kashmiri, Sindhi, Sanskrit, Santali, Manipuri, Bodo, Maithili, and Dogri, with dedicated `verbatim`, `translit`, and `codemix` output modes for code-mixed speech like Hinglish.



## Full example

A small wrapper function, before and after, showing the complete set of changes together:

###### Before (ElevenLabs)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    from elevenlabs import ElevenLabs
    
    client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")
    
    def transcribe(path: str) -> str:
    
        with open(path, "rb") as f:
    
            transcription = client.speech_to_text.convert(
    
                file=f,
    
                model_id="scribe_v2",
    
                language_code="eng",
    
                tag_audio_events=True,
    
            )
    
        return transcription.text

## Common mistakes

###### Passing a URL instead of a file

Sarvam’s `file` parameter expects an open file object or byte stream, not a URL string. If your ElevenLabs code used `source_url` to pull audio from a hosted link, download it once and upload the local file instead.

###### Expecting diarization on the REST endpoint

`with_diarization` is a Batch API parameter, not something the synchronous REST endpoint accepts. If you need diarized output, send the request through the Batch workflow, even for a short file.

###### Reading Batch timestamps as word-level

Batch API timestamps cover sentence or phrase chunks, not individual words. If your ElevenLabs integration builds word-by-word highlighting from `words[].start`/`end`, adjust it to highlight at the chunk level instead.

###### Sending Batch parameters as top-level fields

Calling the Batch endpoints directly over HTTP (rather than through the SDK) requires nesting parameters under `job_parameters`, e.g. `{"job_parameters": {"model": "saaras:v3", ...}}`. A flat body modeled on ElevenLabs’ request shape won’t be picked up.

###### Looking for a scribe_v1-vs-v2 equivalent

There’s only one current-generation model, `saaras:v3`, across every endpoint. Older `saarika`/`saaras:v2.5` model names you’ll see elsewhere in Sarvam’s docs are legacy and being phased out, not a version choice to replicate.

## See also

  * [Migration overview](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview): base URL, auth, and SDK client changes
  * [Which Speech-to-Text API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
  * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
  * [Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)
  * [Speaker Diarization](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#speaker-diarization)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech)[Migrating Instant Voice Cloning from ElevenLabs to SarvamNext](https://docs.sarvam.ai/api/migrations/from-elevenlabs/voice-cloning)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
        * [Overview](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)
        * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech)
        * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text)
        * [Instant Voice Cloning](https://docs.sarvam.ai/api/migrations/from-elevenlabs/voice-cloning)

      * From Cartesia

      * From Deepgram

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


