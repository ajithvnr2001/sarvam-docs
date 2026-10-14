---
url: https://docs.sarvam.ai/api/migrations/from-cartesia/text-to-speech/
title: Migrating Text-to-Speech from Cartesia to Sarvam | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:43.854718+00:00
---

# Migrating Text-to-Speech from Cartesia to Sarvam | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/migrations/from-cartesia/text-to-speech/

Skip to navigation

On this page

  * Quick start
  * Endpoint map
  * Parameter concept map
  * Streaming
  * Pronunciation dictionary
  * What’s different by design
  * Full example
  * Common mistakes
  * See also



Scroll to top

[Migrations](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)[From Cartesia](https://docs.sarvam.ai/api/migrations/from-cartesia/overview)

# Migrating Text-to-Speech from Cartesia to Sarvam

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/migrations/from-cartesia/text-to-speech.md "View this page as plain text")|More actions

This page is for Model APIs.

_Last updated: July 15, 2026_

This guide covers migrating Cartesia text-to-speech API calls to Sarvam. If you’re building a full voice agent rather than replacing individual TTS calls, start from the [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit) or [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat) voice agent build guides instead: they aren’t a 1:1 API swap and aren’t covered here.

**In short:** swap the `voice` object for a plain `speaker` name, drop the nested `output_format` object for two flat params, and change your response handling: Cartesia returns raw audio bytes, Sarvam returns JSON with base64-encoded audio in an `audios` array. Sarvam’s structured response is what makes it easy to pair audio with per-request metadata; that decode step is the change most migrations look for first.

## Quick start

Base URL and auth header change the same way for every Cartesia migration, so they’re folded in here rather than in a separate page:

| Cartesia| Sarvam  
---|---|---  
Base URL| `https://api.cartesia.ai`| `https://api.sarvam.ai`  
Auth header| `Authorization: Bearer <api_key>`| `api-subscription-key: <api_key>`  
Auth failure status| `401`| `403`  
  
With that, replace the synthesis call and add the required language code:

###### Before (Cartesia)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    from cartesia import Cartesia
    
    client = Cartesia(api_key="YOUR_CARTESIA_API_KEY")
    
    response = client.tts.generate(
    
        model_id="sonic-3.5",
    
        transcript="Welcome to our platform!",
    
        voice={
    
            "mode": "id",
    
            "id": "e07c00bc-4134-4eae-9ea4-1a55fb45746b",
    
        },
    
        output_format={
    
            "container": "wav",
    
            "encoding": "pcm_f32le",
    
            "sample_rate": 44100,
    
        },
    
    )
    
    response.write_to_file("output.wav")

Cartesia’s `generate()` returns a binary response with a `write_to_file()` (Python) or `arrayBuffer()` (JavaScript) helper. Sarvam’s `convert()` returns a JSON object; the audio lives in `response.audios` as a list of base64 strings, one per input text. Join and decode before writing to disk, or use the Python SDK’s `sarvamai.play.save()` helper, which does this for you.

The REST response is JSON with a base64 `audios` array, not a file. Decode `.audios[0]` before writing it out; see the [REST API guide](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api) for the full decode snippet.

The rest of this page covers the full endpoint and parameter mapping, streaming, pronunciation dictionaries, and common mistakes.

## Endpoint map

The tables below aren’t a checklist to apply field-by-field: Quick Start above already shows the whole call swapped over in one go. Use these tables as a reference for what changed and why, not as a sequence of edits to make yourself.

| Cartesia| Sarvam  
---|---|---  
Synchronous synthesis| `POST /tts/bytes`| `POST /text-to-speech`  
HTTP streaming| `POST /tts/sse`| `POST /text-to-speech/stream`  
WebSocket streaming| `POST /tts/websocket` (upgrade)| `GET /text-to-speech/ws`  
Voice discovery| `GET /voices` (paginated, searchable)| No API call needed; speaker names are a fixed list on the [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices) page  
  
## Parameter concept map

Cartesia| Sarvam| Note  
---|---|---  
`model_id` (`sonic-3.5`, `sonic-3`, or dated pins like `sonic-3-2026-01-12`)| `model` (`bulbul:v2` or `bulbul:v3`)| One current model to pick, not a family of dated version pins  
`voice` (object, e.g. `{"mode": "id", "id": "<uuid>"}`)| `speaker` (plain lowercase name, e.g. `shubh`, `priya`)| No object to construct or lookup call to make; pick a name directly from the [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices) page  
`output_format` (object, e.g. `{"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100}`)| `speech_sample_rate` \+ `output_audio_codec` (flat params)| Same two settings, passed directly instead of nested in an object  
`generation_config.emotion` (`sonic-3`+; dozens of named emotions)| Speaker choice| Pick the speaker whose baseline delivery already carries the tone you want; see [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)  
`generation_config.speed` (float `0.6`-`1.5`, `sonic-3`+); the top-level `speed` (`slow`/`normal`/`fast`) is deprecated in favor of it| `pace` (float, `0.5`-`2.0` on v3, `0.3`-`3.0` on v2)| One continuous dial across every model, with no deprecated alternative to avoid  
`pronunciation_dict_id` (`sonic-3`\+ only)| `dict_id` (`bulbul:v3` only)| Same concept, and both platforms restrict it to their latest model generation  
`language` (two-letter code, e.g. `hi`; optional)| `language_code` (BCP-47, e.g. `hi-IN`; **required** on every request)| Guarantees the right pronunciation and prosody on every call, which matters most for code-mixed Indian-language text  
Response: raw binary audio (`BinaryAPIResponse`, via `.write_to_file()`)| Response: JSON, audio as base64 strings in `audios`| Structured response makes it straightforward to pair audio with per-request metadata; decode `.audios[0]` before writing to disk  
  
## Streaming

| Cartesia| Sarvam  
---|---|---  
HTTP streaming| `POST /tts/sse` (server-sent events): `chunk` events (base64 audio in `data`), a final `done` event, or an `error` event on failure| [HTTP Stream API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream) (`POST /text-to-speech/stream`): audio returned progressively over one request the same way, with no persistent connection  
WebSocket| `POST /tts/websocket` upgrade, every message tied to a `context_id`: `"continue": true` on all but the last chunk of text, then `{"context_id": ..., "flush": true}` to force out buffered audio or `{"context_id": ..., "cancel": true}` to stop a generation| [WebSocket API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket): `ws.configure(...)` once, then repeated `ws.convert(text)` (equivalent to a `continue` chunk) and `ws.flush()` (equivalent to `flush`) on the same connection, with no separate context ID to track since one connection is already one context  
Tone/speed/volume controls| `generation_config` (emotion, speed, volume), `sonic-3` and newer only| `pace` (and `pitch`/`loudness` on `bulbul:v2`), the same way whether you’re on REST, HTTP streaming, or WebSocket  
  
## Pronunciation dictionary

Both platforms use plain text-to-alias substitution rather than phonetic transcription, so the underlying concept carries over directly:

| Cartesia| Sarvam  
---|---|---  
Rule format| `{"text": "original", "alias": "replacement"}` pairs| Word-alias (plain text substitution), the same idea  
Scope| Referenced via a single `pronunciation_dict_id` per request| Referenced via a single `dict_id` per request  
Language handling| One dictionary applies across the request’s language| Rules are nested per `language_code`; only entries matching the request’s language apply  
Model support| `sonic-3` and newer only| `bulbul:v3` only  
  
Since both dictionaries are simple text replacements, porting entries over is mostly a data migration, not a rewrite: copy each `text`/`alias` pair into Sarvam’s format and nest it under the right `language_code`. See the [Pronunciation Dictionary guide](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary) for the full format and upload flow.

## What’s different by design

  * **Ready-to-use voices, no cloning step.** Sarvam ships a curated, named set of 30+ Bulbul v3 voices, professionally tuned and ready to call immediately, with no per-request cloning or training step to manage.
  * **Plain speaker names, no voice object.** Sarvam’s `speaker` is a lowercase name you pick straight from the [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices) page, rather than a `{"mode": "id", "id": "<uuid>"}` object you construct or fetch from `/voices` first.
  * **Flat output settings.** `speech_sample_rate` and `output_audio_codec` are top-level params rather than a nested `output_format` object, so there’s less request-building code either way.
  * **One continuous pace control.** `pace` works the same way across `bulbul:v2` and `bulbul:v3`, rather than switching between a `slow`/`normal`/`fast` enum on older models and a continuous `0.6`-`1.5` float on newer ones.
  * **Explicit language targeting.** Every Sarvam request carries `language_code`, so pronunciation and prosody are correct by design on every call, especially valuable for Hindi, Hinglish, and other code-mixed Indian-language text.
  * **Indian language depth is Sarvam’s specific strength.** Sarvam covers Hindi plus 9 other Indian languages (Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia), natively tuned for code-mixed input like Hinglish, alongside dedicated `verbatim`, `translit`, and `codemix` modes on the speech-to-text side.



## Full example

A small wrapper function, before and after, showing the complete set of changes together:

###### Before (Cartesia)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    from cartesia import Cartesia
    
    client = Cartesia(api_key="YOUR_CARTESIA_API_KEY")
    
    def synthesize(text: str, out_path: str) -> None:
    
        response = client.tts.generate(
    
            model_id="sonic-3.5",
    
            transcript=text,
    
            voice={"mode": "id", "id": "e07c00bc-4134-4eae-9ea4-1a55fb45746b"},
    
            output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
    
        )
    
        response.write_to_file(out_path)

## Common mistakes

###### Writing the response body directly as an audio file

The single most common migration bug. Cartesia’s REST response is the audio file itself; Sarvam’s is JSON. Code that does `f.write(response.content)` unmodified will produce a file full of JSON text, not audio. Decode `response.audios[0]` from base64 first.

###### Forgetting language_code

It’s required on every request, by design: this is what guarantees Sarvam applies the correct pronunciation and prosody instead of relying on the optional, best-effort `language` Cartesia infers from the voice. Include it from the start rather than treating it as optional.

###### Looking for a named-emotion equivalent

There isn’t a direct swap for `generation_config.emotion`, and that’s fine: pick a speaker whose baseline delivery already matches what you need instead of trying to force `pace` to compensate; see [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices) for per-speaker tone descriptions.

###### Assuming pronunciation dictionaries work on bulbul:v2

Like Cartesia’s own `sonic-3` restriction, Sarvam’s `dict_id` only applies on `bulbul:v3`. If you migrate a dictionary-dependent request onto `bulbul:v2`, the dictionary is silently ignored.

###### Porting a dated model_id pin as-is

Cartesia’s dated pins (e.g. `sonic-3-2026-01-12`) don’t have a Sarvam equivalent to match one-to-one. Map them to the corresponding model family instead: any `sonic-3*` pin to `bulbul:v3`, any older pin to `bulbul:v2`.

## See also

  * [Migration overview](https://docs.sarvam.ai/api/migrations/from-cartesia/overview): base URL, auth, and SDK client changes
  * [Migrating Speech-to-Text](https://docs.sarvam.ai/api/migrations/from-cartesia/speech-to-text)
  * [Which Text-to-Speech API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/which-api-to-use)
  * [TTS Best Practices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices)
  * [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)
  * [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/migrations/from-cartesia/overview)[Migrating Speech-to-Text from Cartesia to SarvamNext](https://docs.sarvam.ai/api/migrations/from-cartesia/speech-to-text)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
        * [Overview](https://docs.sarvam.ai/api/migrations/from-cartesia/overview)
        * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-cartesia/text-to-speech)
        * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-cartesia/speech-to-text)

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


