---
url: https://docs.sarvam.ai/api/getting-started/models/saaras/
title: Saaras | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:35.455192+00:00
---

# Saaras | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/getting-started/models/saaras/

Skip to navigation

On this page

  * At a Glance
  * Saaras v3 vs v4
  * Output Modes
  * Key Features
  * Language Support
  * API Response Format
  * Key Capabilities
  * Limits
  * Known Limitations
  * Next Steps
  * About Saaras v2.5
  * Key Features (v2.5)
  * Translation Quality (v2.5 Benchmarks)
  * Migration Guide



Scroll to top

[Getting Started](https://docs.sarvam.ai/api/getting-started/welcome)[Models](https://docs.sarvam.ai/api/getting-started/models)

# Saaras

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/getting-started/models/saaras.md "View this page as plain text")|More actions

This page is for Model APIs.

Saaras is our state-of-the-art speech recognition family with flexible output formats. It supports multiple output modes including transcription, translation, verbatim, transliteration, and code-mixed outputs. Saaras is built to make Indic languages LLM-comprehensible, offering accurate transcriptions and translations across 23 languages (22 Indian languages + English).

**Saaras v4** is the latest model and is now the default, recommended model, adding Global English support (in addition to Indian English) across all output modes while keeping the same 22 Indic language coverage. **Saaras v3** remains available. Both are available on the **Speech-to-Text endpoint** (`/speech-to-text`) and support multiple output modes via the `mode` parameter.

## At a Glance

|   
---|---  
**Model ID**| `saaras:v4` (default, recommended, latest), `saaras:v3`  
**What it does**|  Speech-to-text with five output modes: transcribe, translate, verbatim, translit, codemix  
**Languages**|  23 (22 Indian + English), automatic language detection ([full list](https://docs.sarvam.ai/api/getting-started/models/saaras#language-support)). `saaras:v4` additionally supports Global English alongside Indian English  
**APIs**| [REST](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api) (≤30 s), [Batch](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) (≤2 hr/file), [WebSocket streaming](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)  
**Input limits**|  30 s per REST request; WAV, MP3, AAC, FLAC, OGG and more, [all limits](https://docs.sarvam.ai/api/getting-started/models/saaras#limits)  
**Pricing**| [Pricing page](https://docs.sarvam.ai/api/getting-started/pricing)  
**Best for**|  Voice agents, call analytics, 8 kHz telephony audio, code-mixed speech  
**Known limitations**| [See below](https://docs.sarvam.ai/api/getting-started/models/saaras#known-limitations)  
  
## Saaras v3 vs v4

| Saaras v3| Saaras v4  
---|---|---  
**Status**| |  Default, recommended, latest  
**Output modes**|  transcribe, translate, verbatim, translit, codemix| transcribe, translate, verbatim, translit, codemix  
**English support**|  Indian English (`en-IN`)| Indian English **and** Global English  
**Endpoint**| `/speech-to-text`| `/speech-to-text`  
  
`saaras:v4` is now the default model — you’ll get it even if you omit the `model` parameter. To use the previous model instead, set `model="saaras:v3"` in any of the requests below. The request/response shape is identical across both.

`saaras:v4` also supports **Keyterm Prompting** : a list of up to 50 domain-specific names, places, brands, or technical terms to bias recognition toward. The examples below pass `keyterms` — it is accepted only on `saaras:v4`, on the REST and Batch APIs, so drop that argument when using `saaras:v3` or the streaming endpoint. See [Keyterm Prompting](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/keyterms).

## Output Modes

Saaras supports multiple output modes via the `mode` parameter, available on both `saaras:v3` and `saaras:v4`. Each mode produces different output formats for the same input audio.

**Example audio:** _“मेरा फोन नंबर है 9840950950”_

Mode| Description| Example Output  
---|---|---  
`transcribe` (default)| Standard transcription in the original language with proper formatting and number normalization| `मेरा फोन नंबर है 9840950950`  
`translate`| Translates speech from any supported Indic language to English| `My phone number is 9840950950`  
`verbatim`| Exact word-for-word transcription without normalization, preserving filler words and spoken numbers as-is| `मेरा फोन नंबर है नौ आठ चार zero नौ पांच zero नौ पांच zero`  
`translit`| Romanization - Transliterates speech to Latin/Roman script| `mera phone number hai 9840950950`  
`codemix`| Code-mixed text with English words in English and Indic words in native script| `मेरा phone number है 9840950950`  
  
## Key Features

Domain-Aware Translation

Advanced prompting system for domain-specific translation and hotword retention, ensuring accurate context preservation.

Superior Telephony Performance

Optimized for 8KHz telephony audio with enhanced multi-speaker recognition capabilities.

Intelligent Entity Preservation

Preserves proper nouns and entities accurately across languages, maintaining context and meaning.

Multi-Language Support

Supports 23 languages (22 Indian + English) with optional language identification.

Speaker Diarization

Provides diarized outputs with precise timestamps for multi-speaker conversations through batch API.

Direct Translation

Converts speech directly to English text, eliminating the need for separate transcription and translation steps.

Global English (v4)

`saaras:v4` extends English recognition beyond Indian English (`en-IN`) to Global English accents, on top of the same 22 Indic languages.

## Language Support

Saaras v3 supports 23 languages (22 Indian languages + English) with comprehensive dialect and accent coverage, including code-mixed audio support and intelligent proper noun preservation for speech-to-English translation.

Language| Language Code| | Language| Language Code  
---|---|---|---|---  
Hindi| `hi-IN`| | Assamese| `as-IN`  
Bengali| `bn-IN`| | Urdu| `ur-IN`  
Kannada| `kn-IN`| | Nepali| `ne-IN`  
Malayalam| `ml-IN`| | Konkani| `kok-IN`  
Marathi| `mr-IN`| | Kashmiri| `ks-IN`  
Odia| `od-IN`| | Sindhi| `sd-IN`  
Punjabi| `pa-IN`| | Sanskrit| `sa-IN`  
Tamil| `ta-IN`| | Santali| `sat-IN`  
Telugu| `te-IN`| | Manipuri| `mni-IN`  
English| `en-IN`| | Bodo| `brx-IN`  
Gujarati| `gu-IN`| | Maithili| `mai-IN`  
| | | Dogri| `doi-IN`  
  
Language codes are optional. When not specified or set to `unknown`, the model will automatically detect the input language and return a `language_probability` score indicating detection confidence.

**Additional Capabilities:**

  * Includes dialects and accents of the above languages
  * Code-mixed audio support
  * Intelligent Proper Noun and Entity Preservation to ensure proper nouns, regional names, and entities are recognized and retained accurately during transcription



## API Response Format

The Speech-to-Text API returns a JSON response with the following fields:

Field| Type| Description  
---|---|---  
`request_id`| `string`| Unique identifier for the API request.  
`transcript`| `string`| The transcribed text from the provided audio file.  
`timestamps`| `object or null`| Contains chunk-level timestamps (`start_time_seconds`, `end_time_seconds`, `words`, each entry is a sentence/phrase, not an individual word). Only included when `with_timestamps` is set to `true`. Word-level timestamps are not supported.  
`diarized_transcript`| `object or null`| Diarized transcript with speaker labels. Available through batch API.  
`language_code`| `string or null`| BCP-47 code of the detected language (e.g., `hi-IN`). Returns the most predominant language if multiple are detected. Returns `null` if no language is detected.  
`language_probability`| `number or null`| Float value (0.0 to 1.0) indicating the probability of the detected language being correct. Higher values indicate higher confidence. Returns a value when `language_code` is not provided or set to `unknown`. Returns `null` when a specific `language_code` is provided (language detection is skipped). Always present in the response.  
  
**Example Response:**
    
    
    {
    
      "request_id": "20260209_abc123-def4-5678-ghij-klmnopqrstuv",
    
      "transcript": "नमस्ते, आप कैसे हैं?",
    
      "timestamps": null,
    
      "diarized_transcript": null,
    
      "language_code": "hi-IN",
    
      "language_probability": 0.95
    
    }

## Key Capabilities

###### Transcribe Mode

###### Translate Mode

###### Verbatim Mode

###### Translit Mode

###### Codemix Mode

Standard transcription in the original language with proper formatting and number normalization. This is the default mode.

PythonJavaScriptcURL
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_SARVAM_API_KEY"
    
    )
    
    try:
    
        response = client.speech_to_text.transcribe(
    
            file=open("audio.wav", "rb"),
    
            model="saaras:v4",
    
            mode="transcribe",  # default mode
    
            keyterms=["Sarvam", "New Delhi", "Vistaar"]
    
        )
    
        print(response.transcript)
    
        # Output: मेरा फोन नंबर है 9840950950
    
    except Exception as e:
    
        print(f"Error: {e}")

## Limits

Limit| Value  
---|---  
Max audio duration (real-time REST)| 30 seconds  
Supported formats| WAV, MP3, AAC, AIFF, OGG, OPUS, FLAC, MP4, AMR, WMA, WebM (auto-detected)  
Raw PCM input (`pcm_s16le`, `pcm_l16`, `pcm_raw`)| Requires `input_audio_codec`; must be 16 kHz  
Longer audio| Use the [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) (up to 2 hours per file)  
Rate limits| See [Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)  
  
## Known Limitations

Limitation| Detail| Workaround  
---|---|---  
**30-second cap on real-time REST**|  The real-time `/speech-to-text` endpoint only accepts audio up to 30 seconds long| Use the [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) for longer recordings (up to 2 hours per file)  
**`mode` parameter is v3/v4-only**| The `mode` parameter (transcribe / translate / verbatim / codemix) works only with `saaras:v3` and `saaras:v4`| Use `saaras:v3` or `saaras:v4`; older versions ignore `mode`  
**Translate mode outputs English only**| `mode="translate"` always produces English text, regardless of input language| Use transcribe mode if you need output in the original language  
  
## Next Steps

[Developer quickstartLearn how to integrate Saaras v4 into your application.](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)[API ReferenceComplete API documentation for Speech-to-Text endpoint.](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[CookbookStep-by-step tutorial for speech-to-text transcription.](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)

* * *

###### Saaras v2.5 (Deprecated Soon)

**Deprecation Notice:** Saaras v2.5 will be deprecated soon. We recommend migrating to **Saaras v3** for improved accuracy and performance. The v2.5 model will continue to work during the transition period, but new features and improvements will only be available in v3.

### About Saaras v2.5

Saaras v2.5 is the previous speech translation model available in the **Speech-to-Text Translate endpoint** (`/speech-to-text-translate`). It converts speech directly to English text with enhanced telephony support and intelligent entity preservation.

**Key Difference:** Saaras v2.5 uses the `/speech-to-text-translate` endpoint, while Saaras v3 uses the `/speech-to-text` endpoint with mode parameter support.

### Key Features (v2.5)

Domain-Aware Translation

Advanced prompting system for domain-specific translation and hotword retention, ensuring accurate context preservation.

Superior Telephony Performance

Optimized for 8KHz telephony audio with enhanced multi-speaker recognition capabilities.

Intelligent Entity Preservation

Preserves proper nouns and entities accurately across languages, maintaining context and meaning.

Multi-Language Support

Supports 11 Indian languages with optional language identification.

Speaker Diarization

Provides diarized outputs with precise timestamps for multi-speaker conversations through batch API.

Direct Translation

Converts speech directly to English text, eliminating the need for separate transcription and translation steps.

### Translation Quality (v2.5 Benchmarks)

COMET score, a robust metric for evaluating machine speech-translations, assesses semantic accuracy, fluency, and contextual relevance. Saaras v2.5 achieves exceptional performance on the Vistaar+Indicvoices Benchmark, a dataset curated from diverse Indian language audio sources, including code-mixed content, noisy environments, and regional accents.

**COMET Score Performance:**

  * **Across 11 Languages:** 89.3%
  * **English:** 94.62%
  * **Hindi:** 91.83%
  * **9 Other languages:** 88.41%



_Higher is better; Compared on VISTAAR + IndicVoices Benchmark_

Why COMET? It evaluates not only lexical accuracy but also how well the translation captures meaning and context, critical for Indic languages with complex structures.

**Dataset Description:** Contains real-world, multi-accented speech samples that covers 10 major Indic languages, ensuring representation of India’s linguistic diversity. Includes code-mixed phrases, domain-specific vocabulary, and colloquial expressions.

### Migration Guide

To migrate from Saaras v2.5 to v3:

  1. **Change the endpoint:** Switch from `/speech-to-text-translate` to `/speech-to-text`
  2. **Update the model parameter:** Change from `saaras:v2.5` to `saaras:v3`
  3. **Add the mode parameter:** Use `mode="translate"` to get English output (similar to v2.5 behavior)


    
    
    # Endpoint change
    
    - POST /speech-to-text-translate
    
    + POST /speech-to-text
    
    # Parameter changes
    
    - model="saaras:v2.5"
    
    + model="saaras:v4"
    
    + mode="translate"

**SDK Migration:**
    
    
     # Python
    
    - response = client.speech_to_text.translate(
    
    -     file=open("audio.wav", "rb"), model="saaras:v2.5"
    
    - )
    
    + response = client.speech_to_text.transcribe(
    
    +     file=open("audio.wav", "rb"), model="saaras:v4", mode="translate"
    
    + )
    
    # JavaScript
    
    - const response = await client.speechToText.translate({ file: fs.createReadStream("audio.wav"), model: "saaras:v2.5" });
    
    + const response = await client.speechToText.transcribe({ file: fs.createReadStream("audio.wav"), model: "saaras:v4", mode: "translate" });

The response format remains compatible.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/getting-started/models)[BulbulNext](https://docs.sarvam.ai/api/getting-started/models/bulbul)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
    * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
    * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
    * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
    * [Models](https://docs.sarvam.ai/api/getting-started/models)
      * [Saaras](https://docs.sarvam.ai/api/getting-started/models/saaras)
      * [Bulbul](https://docs.sarvam.ai/api/getting-started/models/bulbul)
      * [Sarvam 105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)
      * [Open-Weight ModelsBeta](https://docs.sarvam.ai/api/getting-started/models/openweight)

      * [Mayura](https://docs.sarvam.ai/api/getting-started/models/mayura)
      * [Sarvam Translate](https://docs.sarvam.ai/api/getting-started/models/sarvam-translate)
      * [Sarvam Vision](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)
      * Deprecated Models

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


