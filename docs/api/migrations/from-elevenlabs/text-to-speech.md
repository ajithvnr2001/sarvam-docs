---
url: https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech/
title: Migrating Text-to-Speech from ElevenLabs to Sarvam | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:45.694424+00:00
---

# Migrating Text-to-Speech from ElevenLabs to Sarvam | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech/

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

[Migrations](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)[From ElevenLabs](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)

# Migrating Text-to-Speech from ElevenLabs to Sarvam

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech.md "View this page as plain text")|More actions

This page is for Model APIs.

_Last updated: July 15, 2026_

This guide covers migrating ElevenLabs text-to-speech API calls to Sarvam. If you’re building a full voice agent rather than replacing individual TTS calls, start from the [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit) or [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat) voice agent build guides instead: they aren’t a 1:1 API swap and aren’t covered here.

**In short:** swap `voice_id` for `speaker`, add a required `language_code`, and change your response handling: ElevenLabs returns raw audio bytes, Sarvam returns JSON with base64-encoded audio in an `audios` array. Sarvam’s structured response is what makes it easy to pair audio with per-request metadata; that decode step is the change most migrations look for first.

## Quick start

Base URL and auth header change the same way for every ElevenLabs migration, so they’re folded in here rather than in a separate page:

| ElevenLabs| Sarvam  
---|---|---  
Base URL| `https://api.elevenlabs.io`| `https://api.sarvam.ai`  
Auth header| `xi-api-key`| `api-subscription-key`  
Auth failure status| `401`| `403`  
  
With that, replace the synthesis call and add the required language code:

###### Before (ElevenLabs)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    from elevenlabs import ElevenLabs
    
    client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")
    
    audio = client.text_to_speech.convert(
    
        voice_id="21m00Tcm4TlvDq8ikWAM",
    
        model_id="eleven_multilingual_v2",
    
        text="Welcome to our platform!",
    
        voice_settings={
    
            "stability": 0.5,
    
            "similarity_boost": 0.75,
    
            "style": 0.0,
    
            "use_speaker_boost": True,
    
            "speed": 1.0,
    
        },
    
    )
    
    with open("output.mp3", "wb") as f:
    
        for chunk in audio:
    
            f.write(chunk)

ElevenLabs’ Python and JavaScript SDKs hand back an iterable/stream of audio chunks you can write directly. Sarvam’s `convert()` returns a JSON object; the audio lives in `response.audios` as a list of base64 strings, one per input text. Join and decode before writing to disk, or use the Python SDK’s `sarvamai.play.save()` helper, which does this for you.

The REST response is JSON with a base64 `audios` array, not a file. Decode `.audios[0]` before writing it out; see the [REST API guide](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api) for the full decode snippet.

The rest of this page covers the full endpoint and parameter mapping, streaming, pronunciation dictionaries, and common mistakes.

## Endpoint map

The tables below aren’t a checklist to apply field-by-field: Quick Start above already shows the whole call swapped over in one go. Use these tables as a reference for what changed and why, not as a sequence of edits to make yourself.

| ElevenLabs| Sarvam  
---|---|---  
Synchronous synthesis| `POST /v1/text-to-speech/{voice_id}`| `POST /text-to-speech`  
HTTP streaming| `POST /v1/text-to-speech/{voice_id}/stream`| `POST /text-to-speech/stream`  
WebSocket streaming| `GET wss://.../v1/text-to-speech/{voice_id}/stream-input`| `GET /text-to-speech/ws`  
Voice discovery| `GET /v2/voices` (paginated, searchable)| No API call needed; speaker names are a fixed list on the [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices) page  
  
## Parameter concept map

ElevenLabs| Sarvam| Note  
---|---|---  
`voice_id` (opaque ID, e.g. `21m00Tcm4TlvDq8ikWAM`)| `speaker` (plain lowercase name, e.g. `shubh`, `priya`)| No lookup call required, pick a name directly from the [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices) page  
`model_id` (`eleven_multilingual_v2`, `eleven_flash_v2_5`, `eleven_v3`, etc.)| `model` (`bulbul:v2` or `bulbul:v3`)| Two model versions total, not a family of speed/quality tiers  
`voice_settings.stability`| Built into the voice| Every Bulbul speaker is pre-tuned for consistent delivery, so there’s no separate dial to calibrate  
`voice_settings.similarity_boost`| Not needed| Sarvam speakers are production-ready studio voices rather than per-request clones, so there’s nothing to tune  
`voice_settings.style`| Speaker choice| Pick the speaker whose baseline delivery already matches the expressiveness you want; see [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)  
`voice_settings.use_speaker_boost`| Not needed| Clarity is tuned in by default on every speaker  
`voice_settings.speed` (default `1.0`)| `pace` (default `1.0`, range `0.5` to `2.0` on v3, `0.3` to `3.0` on v2)| Same idea, wider range on Sarvam’s side  
`language_code` (optional, most models infer language from voice/model)| `language_code` (**required** on every request)| Guarantees the right pronunciation and prosody on every call, which matters most for code-mixed Indian-language text  
`output_format` (single string, e.g. `mp3_44100_128`)| `speech_sample_rate` \+ `output_audio_codec` (separate params, available on REST and streaming)| Defaults to WAV at 24000 Hz; set `output_audio_codec` (`mp3`, `opus`, `flac`, `aac`, `wav`, etc.) and `speech_sample_rate` independently to change either  
`pronunciation_dictionary_locators`| `dict_id`| Both are scoped and reusable across requests, format differs, see [Pronunciation dictionary](https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech#pronunciation-dictionary) below  
Response: raw binary audio (`application/octet-stream` or per `output_format`)| Response: JSON, audio as base64 strings in `audios`| Structured response makes it straightforward to pair audio with per-request metadata; decode `.audios[0]` before writing to disk  
  
`pitch` and `loudness` give you fine-grained tone and volume control on **`bulbul:v2`**. On **`bulbul:v3`** , which adds a larger voice set and stronger code-mixed handling, tone comes from speaker choice instead, so pick a speaker whose baseline delivery already fits rather than reaching for these two params.

## Streaming

| ElevenLabs| Sarvam  
---|---|---  
HTTP streaming| `POST /v1/text-to-speech/{voice_id}/stream`| [HTTP Stream API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream) (`POST /text-to-speech/stream`): both return audio progressively over one request, no persistent connection  
WebSocket| `.../stream-input`: initial message carrying `voice_settings`, then `SendText` messages (optional `flush` flag), closed with an empty-text message| [WebSocket API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket): `ws.configure(...)` once, then repeated `ws.convert(text)` and `ws.flush()` on the same connection  
Character limits| A single large call, e.g. up to 10,000 characters on `eleven_multilingual_v2`| WebSocket up to 2500 chars/message (under 500 recommended for lowest latency), REST up to 2500 on `bulbul:v3` (1500 on `bulbul:v2`), HTTP streaming up to 3500 regardless of model, may need chunking logic that didn’t previously exist  
  
## Pronunciation dictionary

Both platforms let you fix mispronounced brand names and acronyms without retraining a model, but the mechanism differs:

| ElevenLabs| Sarvam  
---|---|---  
Rule types| Phoneme rules (IPA) and word-alias rules| Word-alias (plain text substitution), simple to author and audit  
Scope| Referenced via `pronunciation_dictionary_locators` in the request| Referenced via a single `dict_id` per request  
Language handling| Rules can be tied to specific words regardless of language| Rules are nested per `language_code`; only entries matching the request’s language apply  
Limits| Varies by plan| 10 dictionaries per user, 100 words per dictionary, 1 MB per upload, 1 dictionary per request  
Model support| Available across ElevenLabs’ model tiers| **`bulbul:v3` only**: a request can’t combine a pronunciation dictionary with the v2-only `pitch`/`loudness` params  
  
If your ElevenLabs dictionary relies on IPA phoneme rules for precise pronunciation control, plan to rewrite it: Sarvam dictionaries use plain word-to-word text replacements (e.g. `"NAIC": "N A I C"`), which are simpler to author and audit than phonetic transcriptions. See the [Pronunciation Dictionary guide](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary) for the full format and upload flow.

## What’s different by design

  * **Ready-to-use voices out of the box.** Sarvam ships a curated, named set of 30+ Bulbul v3 voices, professionally tuned and ready to call immediately, with no per-request cloning or training step to manage. If your ElevenLabs setup relies on cloned or custom voices, the [Instant Voice Cloning migration guide](https://docs.sarvam.ai/api/migrations/from-elevenlabs/voice-cloning) covers creating a saved voice and generating speech with its `voice_id`.
  * **Explicit language targeting.** Every Sarvam request carries `language_code`, so pronunciation and prosody are correct by design on every call, especially valuable for Hindi, Hinglish, and other code-mixed Indian-language text where auto-detection is prone to guessing wrong.
  * **A simpler tuning surface.** Tone and delivery come from picking the right speaker plus `pace` (and `pitch`/`loudness` on v2), instead of calibrating `stability`, `similarity_boost`, `style`, and `use_speaker_boost` separately. Fewer knobs, less trial and error to land on a voice that sounds right.
  * **Indian language depth is Sarvam’s specific strength.** Sarvam covers Hindi plus 9 other Indian languages (Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia), natively tuned for code-mixed input like Hinglish. If your product needs those languages, this is the reason to migrate, not just a side effect of it.
  * **Instant voice discovery.** Every speaker is listed with audio previews on the [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices) page: no API call, no pagination, nothing to query.



## Full example

A small wrapper function, before and after, showing the complete set of changes together:

###### Before (ElevenLabs)

###### After (Sarvam)

PythonJavaScriptcURL
    
    
    from elevenlabs import ElevenLabs
    
    client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")
    
    def synthesize(text: str, out_path: str):
    
        audio = client.text_to_speech.convert(
    
            voice_id="21m00Tcm4TlvDq8ikWAM",
    
            model_id="eleven_multilingual_v2",
    
            text=text,
    
            voice_settings={"stability": 0.5, "similarity_boost": 0.75},
    
        )
    
        with open(out_path, "wb") as f:
    
            for chunk in audio:
    
                f.write(chunk)

## Common mistakes

###### Writing the response body directly as an audio file

The single most common migration bug. ElevenLabs’ REST response is the audio file itself; Sarvam’s is JSON. Code that does `f.write(response.content)` unmodified will produce a file full of JSON text, not audio. Decode `response.audios[0]` from base64 first.

###### Forgetting language_code

It’s required on every request, by design: this is what guarantees Sarvam applies the correct pronunciation and prosody instead of guessing from the `speaker` name. Include it from the start rather than treating it as optional.

###### Trying to tune pace/pitch instead of picking the right speaker

`pace` and `pitch` aren’t drop-in replacements for `stability` or `style`. Rather than compensating with those params, pick a speaker whose baseline delivery already matches what you need; see the [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices) page for per-speaker tone descriptions.

###### Reusing pitch/loudness on bulbul:v3

Both params are accepted syntactically but only take effect on `bulbul:v2`. If output sounds unchanged after setting them, confirm which model version the request is actually using.

###### Porting an IPA-based pronunciation dictionary as-is

Sarvam’s dictionary format is plain word-to-word substitution, not phoneme rules. An ElevenLabs dictionary built on IPA transcriptions needs to be rewritten as text replacements, not just re-uploaded.

## See also

  * [Migration overview](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview): base URL, auth, and SDK client changes
  * [Migrating Speech-to-Text](https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text)
  * [Which Text-to-Speech API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/which-api-to-use)
  * [TTS Best Practices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices)
  * [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)
  * [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)[Migrating Speech-to-Text from ElevenLabs to SarvamNext](https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


