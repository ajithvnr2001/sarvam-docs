---
url: https://docs.sarvam.ai/api/migrations/from-gemini/speech-to-text/
title: Migrating Speech-to-Text from Gemini to Sarvam | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:46.441282+00:00
---

# Migrating Speech-to-Text from Gemini to Sarvam | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/migrations/from-gemini/speech-to-text/

Skip to navigation

On this page

  * Quick start
  * Endpoint map
  * Parameter concept map
  * Long audio and diarization
  * What’s different by design
  * Full example
  * Common mistakes
  * See also



Scroll to top

[Migrations](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)[From Gemini](https://docs.sarvam.ai/api/migrations/from-gemini/overview)

# Migrating Speech-to-Text from Gemini to Sarvam

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/migrations/from-gemini/speech-to-text.md "View this page as plain text")|More actions

This page is for Model APIs.

_Last updated: July 15, 2026_

This guide covers migrating Gemini audio transcription calls to Sarvam. If you’re building a full voice agent with live, bidirectional audio rather than transcribing recorded audio one call at a time, start from the [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit) or [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat) voice agent build guides instead: they aren’t a 1:1 API swap and aren’t covered here.

**In short:** Gemini transcribes audio by passing it, along with a natural-language instruction, to a general model. Sarvam has a dedicated transcription endpoint. Swap the text-plus-audio input list for a `transcribe()` call with a `mode` parameter, and read the result from a guaranteed-clean `transcript` field instead of `interaction.output_text`.

## Quick start

Base URL and auth header change the same way for every Gemini migration, so they’re folded in here rather than in a separate page:

| Gemini API| Sarvam  
---|---|---  
Base URL| `https://generativelanguage.googleapis.com`| `https://api.sarvam.ai`  
Auth header| `x-goog-api-key: <api_key>`| `api-subscription-key: <api_key>`  
Auth failure status| `401`| `403`  
  
With that, replace the transcription call:

###### Before (Gemini)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    import base64
    
    from google import genai
    
    client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
    
    with open("audio.mp3", "rb") as f:
    
        audio_bytes = f.read()
    
    interaction = client.interactions.create(
    
        model="gemini-3.5-flash",
    
        input=[
    
            {"type": "text", "text": "Generate a transcript of the speech."},
    
            {
    
                "type": "audio",
    
                "data": base64.b64encode(audio_bytes).decode("utf-8"),
    
                "mime_type": "audio/mp3",
    
            },
    
        ],
    
    )
    
    print(interaction.output_text)

Gemini’s reply is a model’s response to your prompt, so its exact wording and formatting can vary between calls unless your prompt constrains it carefully. Sarvam’s `response.transcript` is a dedicated field that always contains just the transcript.

The rest of this page covers the full endpoint and parameter mapping, long audio, and common mistakes.

## Endpoint map

The tables below aren’t a checklist to apply field-by-field: Quick Start above already shows the whole call swapped over in one go. Use these tables as a reference for what changed and why, not as a sequence of edits to make yourself.

| Gemini API| Sarvam  
---|---|---  
Transcription| `POST /v1beta/interactions`, with the audio passed as an input content block alongside a text prompt asking for a transcript| `POST /speech-to-text` (up to 30 seconds per request; use Batch for longer audio)  
Long audio (up to 9.5 hours per prompt)| Upload via `client.files.upload(...)` first, then reference the file’s `uri` in the input| Batch API: `POST /speech-to-text/job/v1` (create), upload, start, then poll or receive a webhook callback, up to 2 hours per file  
Real-time streaming transcription| Not applicable to this endpoint; live audio goes through the Live API instead| `GET /speech-to-text/ws`  
  
## Parameter concept map

Gemini API| Sarvam| Note  
---|---|---  
`model` (a general model, e.g. `gemini-3.5-flash`, shared with text generation)| `model` (`saaras:v3`, a dedicated speech-to-text model)| A transcription-specific endpoint and model, rather than a general model prompted to behave like one  
A natural-language prompt (e.g. `{"type": "text", "text": "Generate a transcript of the speech."}`)| `mode="transcribe"` (a dedicated parameter)| An explicit parameter rather than an instruction the model has to interpret correctly every time  
`{"type": "audio", "data": ..., "mime_type": ...}` input block (or `"uri"` for an uploaded file)| `file` (upload the audio file directly)| Same concept: the audio goes in as the file content either way  
No dedicated language parameter; Gemini infers language from the audio and the prompt| `language_code` (optional, BCP-47, e.g. `hi-IN`; pass `unknown` to auto-detect)| Same auto-detect behavior available explicitly, plus the option to hint the language for better accuracy  
Response: `interaction.output_text` (a model reply satisfying the prompt)| Response: `response.transcript` (a dedicated, transcript-only field)| Guaranteed to be just the transcript, not a model’s phrasing of one  
  
## Long audio and diarization

**For files over 20 MB, upload first instead of inlining the audio.**

Before (Gemini)After (Sarvam)
    
    
    from google import genai
    
    client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
    
    uploaded_file = client.files.upload(file="long-meeting.mp3")
    
    interaction = client.interactions.create(
    
        model="gemini-3.5-flash",
    
        input=[
    
            {"type": "text", "text": "Generate a transcript of the speech."},
    
            {
    
                "type": "audio",
    
                "uri": uploaded_file.uri,
    
                "mime_type": uploaded_file.mime_type,
    
            },
    
        ],
    
    )
    
    print(interaction.output_text)

Sarvam’s REST endpoint caps at 30 seconds of audio regardless of file size. For a file like this one, use the [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) instead, shown next, rather than the direct `transcribe()` call above.

**Move diarized or long-form audio to the Batch API.**

Before (Gemini)After (Sarvam)
    
    
    from google import genai
    
    client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
    
    # Not available as a dedicated mode: Gemini has no speaker-labeling parameter.
    
    # You'd need to prompt the model to attempt speaker labeling in its reply,
    
    # with no guarantee of a consistent, structured format back.
    
    uploaded_file = client.files.upload(file="meeting.mp3")
    
    interaction = client.interactions.create(
    
        model="gemini-3.5-flash",
    
        input=[
    
            {"type": "text", "text": "Transcribe this and label each speaker."},
    
            {
    
                "type": "audio",
    
                "uri": uploaded_file.uri,
    
                "mime_type": uploaded_file.mime_type,
    
            },
    
        ],
    
    )

See the [Batch API guide](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) for webhook setup and its [Speaker Diarization section](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#speaker-diarization) for the current per-job speaker limit.

## What’s different by design

  * **A dedicated transcription endpoint.** `POST /speech-to-text` and `mode="transcribe"` are purpose-built for turning audio into text, rather than a general model interpreting a natural-language request.
  * **A guaranteed-clean transcript field.** `response.transcript` always holds just the transcript, with no prompt-engineering needed to keep a general-purpose model from adding commentary or reformatting the text.
  * **Flexible output modes on one model.** `saaras:v3` also supports `translate`, `verbatim`, `translit`, and `codemix` modes as explicit parameters, rather than needing a differently worded prompt for each.
  * **Diarization comes standard, not prompted for.** Sarvam’s Batch API identifies and labels speakers with `with_diarization` and `num_speakers`, returning a structured `diarized_transcript`, rather than relying on a model’s best-effort attempt inside free-text output.
  * **Indian language depth is Sarvam’s specific strength.** Saaras v3 covers 22 Indian languages, including Assamese, Konkani, Kashmiri, Sindhi, Sanskrit, Santali, Manipuri, Bodo, Maithili, and Dogri, with native handling for code-mixed speech like Hinglish.



## Full example

A small wrapper function, before and after, showing the complete set of changes together:

###### Before (Gemini)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    import base64
    
    from google import genai
    
    client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
    
    def transcribe(path: str) -> str:
    
        with open(path, "rb") as f:
    
            audio_bytes = f.read()
    
        interaction = client.interactions.create(
    
            model="gemini-3.5-flash",
    
            input=[
    
                {"type": "text", "text": "Generate a transcript of the speech."},
    
                {
    
                    "type": "audio",
    
                    "data": base64.b64encode(audio_bytes).decode("utf-8"),
    
                    "mime_type": "audio/mp3",
    
                },
    
            ],
    
        )
    
        return interaction.output_text

## Common mistakes

###### Trusting interaction.output_text as a clean transcript

It’s a model’s reply to your prompt, so it can include extra phrasing, partial answers, or formatting depending on how the prompt was worded. Read `response.transcript` on Sarvam’s side instead, which is always transcript-only.

###### Wording a prompt instead of setting a parameter

Sarvam’s `mode` parameter (`transcribe`, `translate`, `verbatim`, `translit`, `codemix`) replaces the need to phrase a natural-language instruction carefully and hope the model interprets it the same way every time.

###### Expecting structured diarization from a prompted request

Asking Gemini to “label each speaker” in the prompt returns free text, not a structured, per-segment breakdown. Sarvam’s `with_diarization` and `num_speakers` are Batch API parameters that return a dedicated `diarized_transcript` field, so route diarized requests through the Batch workflow instead of relying on prompt wording.

###### Sending Batch parameters as top-level fields

Calling the Batch endpoints directly over HTTP (rather than through the SDK) requires nesting parameters under `job_parameters`, e.g. `{"job_parameters": {"model": "saaras:v3", ...}}`. A flat body won’t be picked up.

## See also

  * [Migration overview](https://docs.sarvam.ai/api/migrations/from-gemini/overview): base URL, auth, and SDK client changes
  * [Migrating Chat Completion](https://docs.sarvam.ai/api/migrations/from-gemini/chat-completion)
  * [Migrating Text-to-Speech](https://docs.sarvam.ai/api/migrations/from-gemini/text-to-speech)
  * [Which Speech-to-Text API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
  * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
  * [Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/migrations/from-gemini/text-to-speech)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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

      * From Gemini
        * [Overview](https://docs.sarvam.ai/api/migrations/from-gemini/overview)
        * [Chat Completion](https://docs.sarvam.ai/api/migrations/from-gemini/chat-completion)
        * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-gemini/text-to-speech)
        * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-gemini/speech-to-text)




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


