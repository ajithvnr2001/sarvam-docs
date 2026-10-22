---
url: https://docs.sarvam.ai/api/getting-started/models/
title: Models | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-22T06:32:45.512908+00:00
---

# Models | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/getting-started/models/

Skip to navigation

On this page

  * Model Selection Guide
  * Open-Weight Models
  * Language Support Overview
  * 23-language set (Saaras v4, Sarvam Translate, Sarvam Vision)
  * 11-language set (Bulbul v3, Mayura, Sarvam-105B)
  * Use Cases
  * Build a multilingual voice assistant
  * Localize content across Indian languages
  * Analyze multilingual customer interactions
  * Create inclusive learning experiences
  * Extract and digitize document content



Scroll to top

[Getting Started](https://docs.sarvam.ai/api/getting-started/welcome)

# Models

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/getting-started/models.md "View this page as plain text")|More actions

This page is for Model APIs.

Sarvam AI provides a purpose-built AI stack for building applications in Indian languages. Our models span speech-to-text, speech translation, text translation, and high-quality text-to-speech, designed specifically for India’s linguistic diversity, accents, and real-world usage patterns.

Each model is trained and evaluated on Indian languages and culturally grounded data, enabling higher accuracy in production scenarios. With simple, well-documented APIs and predictable performance, developers can build, deploy, and scale India-first AI experiences without managing model complexity.

New to building for Indian languages? Start with [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india), a practical guide to language coverage, code-mixing, scripts, native numerals, 8kHz telephony audio, and pronunciation control.

## Model Selection Guide

**Sarvam Models** : trained for Indian languages:

Model| API| Description  
---|---|---  
[Saaras v4](https://docs.sarvam.ai/api/getting-started/models/saaras)| Speech to Text| Latest, default ASR model — 23 language support (22 Indian + Global/Indian English) and multiple output modes: transcribe, translate, verbatim, translit, codemix.  
[Saaras v3](https://docs.sarvam.ai/api/getting-started/models/saaras)| Speech to Text| Previous ASR model, still available — 23 languages (22 Indian + Indian English) with the same output modes as v4, without Global English.  
[Bulbul v4 Flash](https://docs.sarvam.ai/api/getting-started/models/bulbul)| Text to Speech| Latest text-to-speech model — 200+ persona voices with natural prosody, and the same request/response contract as v3.  
[Bulbul v3](https://docs.sarvam.ai/api/getting-started/models/bulbul)| Text to Speech| Stable text-to-speech model with 30+ named speakers across 11 languages (10 Indian + English). The API default when `model` is omitted.  
[Sarvam Instant Voice Cloning](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview)| Instant Voice Cloning (Beta)| Create a voice from a short reference clip and synthesize speech with it across 12 Indian languages - clone inline per request, or save the voice once and reuse its ID.  
[Sarvam-105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)| Chat Completion| 105B parameter flagship model (`sarvam-105b`) for complex reasoning, coding, and agentic tasks.  
[Sarvam-105B Conversations](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)| Chat Completion| Conversational variant (`sarvam-105b-conversations`), post-trained for real-time dialogue and voice agents.  
[Mayura](https://docs.sarvam.ai/api/getting-started/models/mayura)| Text Translation| High-quality translation between 11 languages (10 Indian + English) with context preservation.  
[Sarvam-Translate](https://docs.sarvam.ai/api/getting-started/models/sarvam-translate)| Text Translation| Extended translation support for all 23 languages (22 Indian + English) with superior accuracy.  
[Sarvam Vision](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)| Document Intelligence| Extract and digitize content from documents in 23 languages with accurate OCR and structured output.  
  
## Open-Weight Models

Open-weight models are available on **`/v2`** using the same Sarvam API key and credits.

Model| Context window| Modality| Reasoning  
---|---|---|---  
[GLM-5.3](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)| 1,048,576 tokens| Text → text| Yes  
[Gemma 4 31B](https://docs.sarvam.ai/api/getting-started/models/openweight/gemma-4-31b)| 131,072 tokens| Text + image → text| No  
[DeepSeek V4.1 Flash](https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash)| 1,048,576 tokens| Text → text| Yes  
  
[Read more about the open-weight models →](https://docs.sarvam.ai/api/getting-started/models/openweight)

## Language Support Overview

Language coverage varies by model. Check the table below before picking one. Full per-model tables are linked from each model’s own page.

Model| Languages| Status  
---|---|---  
**Saaras v4** (Speech to Text)| 23 (22 Indian + Global/Indian English), [full list](https://docs.sarvam.ai/api/getting-started/models/saaras#language-support)| Recommended  
**Saaras v3** (Speech to Text)| 23 (22 Indian + Indian English), [full list](https://docs.sarvam.ai/api/getting-started/models/saaras#language-support)| Active  
**Sarvam Translate** (Text Translation)| 23 (22 Indian + English), [full list](https://docs.sarvam.ai/api/getting-started/models/sarvam-translate#language-support)| Active  
**Sarvam Vision** (Document Intelligence)| 23 (22 Indian + English), [full list](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision#supported-languages)| Active  
**Bulbul v4 Flash** (Text to Speech)| 10 (Hindi, English, English–Hindi, Bengali, Gujarati, Kannada, Marathi, Punjabi, Tamil, Telugu), [full list](https://docs.sarvam.ai/api/getting-started/models/bulbul#language-support)| Latest  
**Bulbul v3** (Text to Speech)| 11 (10 Indian + English), [full list](https://docs.sarvam.ai/api/getting-started/models/bulbul#language-support)| Active (API default)  
**Sarvam Instant Voice Cloning**|  12 Indian languages, [full list](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/supported-languages)| Active (Beta)  
**Mayura** (Text Translation)| 11 (10 Indian + English), [full list](https://docs.sarvam.ai/api/getting-started/models/mayura#language-support)| Active  
**Sarvam-105B** (Chat LLM)| 11 (10 Indian + English), `sarvam-105b`| Active  
**Sarvam-105B Conversations** (Chat LLM)| 11 (10 Indian + English), `sarvam-105b-conversations`| Active  
**GLM-5.3** (Chat LLM, [open-weight](https://docs.sarvam.ai/api/getting-started/models/openweight))| See the model page for language coverage| Active  
**Gemma 4 31B** (Chat LLM, [open-weight](https://docs.sarvam.ai/api/getting-started/models/openweight))| See the model page for language coverage| Active  
**DeepSeek V4.1 Flash** (Chat LLM, [open-weight](https://docs.sarvam.ai/api/getting-started/models/openweight))| See the model page for language coverage| Active  
  
### 23-language set (Saaras v4, Sarvam Translate, Sarvam Vision)

Language| Code| | Language| Code  
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
  
### 11-language set (Bulbul v3, Mayura, Sarvam-105B)

Language| Code| | Language| Code  
---|---|---|---|---  
Hindi| `hi-IN`| | Kannada| `kn-IN`  
Bengali| `bn-IN`| | Malayalam| `ml-IN`  
Tamil| `ta-IN`| | Marathi| `mr-IN`  
Telugu| `te-IN`| | Punjabi| `pa-IN`  
Gujarati| `gu-IN`| | Odia| `od-IN`  
English| `en-IN`| | |   
  
* * *

## Use Cases

###### Voice Assistant

###### Content Localization

###### Call Center Analytics

###### Educational Platform

###### Document Processing

### Build a multilingual voice assistant

  1. **Speech Input** : Use Saaras v4 with `mode="transcribe"` to convert user speech to text
  2. **Understanding** : Process with Sarvam-105B for intelligent responses
  3. **Speech Output** : Convert responses to speech with Bulbul



Perfect for customer service, smart home devices, and accessibility applications.

[Learn how to build a voice agent with LiveKit →](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

###### Legacy Models

The following models are still available but are being phased out. We recommend migrating to the newer models listed above.

[Sarvam-M: Chat & Reasoning (Deprecated)24B parameter multilingual chat model with hybrid reasoning. Deprecated and no longer available through the API. Migrate to Sarvam-105B.](https://docs.sarvam.ai/api/getting-started/models/sarvam-m)[Sarvam-30B: Chat LLM (Deprecated)30B parameter multilingual chat model with strong reasoning and conversational capabilities. Deprecated. Migrate to Sarvam-105B.](https://docs.sarvam.ai/api/getting-started/models/sarvam-30b)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/getting-started/building-for-india)[SaarasNext](https://docs.sarvam.ai/api/getting-started/models/saaras)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
    * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
    * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
    * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
    * [Models](https://docs.sarvam.ai/api/getting-started/models)
      * [Saaras](https://docs.sarvam.ai/api/getting-started/models/saaras)
      * [Bulbul](https://docs.sarvam.ai/api/getting-started/models/bulbul)
      * [Sarvam 105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)
      * [Open-Weight Models](https://docs.sarvam.ai/api/getting-started/models/openweight)

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


