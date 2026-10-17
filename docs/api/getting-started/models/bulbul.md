---
url: https://docs.sarvam.ai/api/getting-started/models/bulbul/
title: Bulbul | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-17T14:23:19.729198+00:00
---

# Bulbul | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/getting-started/models/bulbul/

Skip to navigation

On this page

  * At a Glance
  * Bulbul v4 Flash vs v3
  * Key Features
  * Language Support
  * Bulbul v3
  * Bulbul v4 Flash
  * Available Speakers
  * Bulbul v3
  * Bulbul v4 Flash
  * Key Capabilities
  * Limits
  * Known Limitations
  * Next Steps



Scroll to top

[Getting Started](https://docs.sarvam.ai/api/getting-started/welcome)[Models](https://docs.sarvam.ai/api/getting-started/models)

# Bulbul

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/getting-started/models/bulbul.md "View this page as plain text")|More actions

This page is for Model APIs.

Bulbul v4 Flash is our latest text-to-speech model — 200+ persona voices and the same API contract as Bulbul v3. Bulbul v3 remains the API default when `model` is omitted and offers 30+ classic speaker names, improved audio quality, and up to 2500 characters per request.

**Bulbul v4 Flash** is the latest model, offering the same request and response contract as `bulbul:v3` but with a much larger, persona-based voice catalog (200+ speaker voices across style and use case). **Bulbul v3** remains the API default when `model` is omitted. Both are available on the **Text-to-Speech endpoint** (`/text-to-speech`).

## At a Glance

|   
---|---  
**Model ID**| `bulbul:v4-flash` (latest, recommended for new integrations), `bulbul:v3` (stable; API default when `model` is omitted), `bulbul:v2` (legacy)  
**What it does**|  Text-to-speech with natural speaker voices and pace control  
**Languages**|  11 (10 Indian + English), [full list](https://docs.sarvam.ai/api/getting-started/models/bulbul#language-support)  
**APIs**| [REST](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api), [HTTP streaming](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream), [WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket)  
**Input limits**|  2,500 characters per REST request; sample rates up to 48 kHz (REST API only), [all limits](https://docs.sarvam.ai/api/getting-started/models/bulbul#limits)  
**Pricing**| [Pricing page](https://docs.sarvam.ai/api/getting-started/pricing)  
**Best for**|  Voice agents, IVR prompts, narration and audio content  
**Known limitations**| [See below](https://docs.sarvam.ai/api/getting-started/models/bulbul#known-limitations)  
  
## Bulbul v4 Flash vs v3

| Bulbul v4 Flash| Bulbul v3  
---|---|---  
**Status**|  Latest, recommended for new integrations| Stable (API default when `model` omitted)  
**Speaker voices**|  200+ persona voices (222 IDs), organized by language and style, see [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices#bulbul-v4-flash-voices)| 30+ named speakers  
**Languages (voices)**|  Hindi, English, `enhi`, Bengali, Gujarati, Kannada, Marathi, Punjabi, Tamil, Telugu — see [v4 catalog note](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices#bulbul-v4-flash-voices)| 11 BCP-47 codes (incl. Malayalam, Odia)  
**Request/response shape**|  Same| Same  
**Endpoint**| `/text-to-speech`| `/text-to-speech`  
  
For new integrations, set `model="bulbul:v4-flash"` in any of the requests below along with a `speaker` value from the [Bulbul v4 Flash voice catalog](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices#bulbul-v4-flash-voices). The request/response shape is identical to `bulbul:v3`.

## Key Features

200+ Persona Voices (v4 Flash)

222 persona voices on `bulbul:v4-flash`, organized by language and style (for example `simran_en_customer`, `ishita_hi_devotional`).

30+ Speaker Voices (v3)

On `bulbul:v3`: natural-sounding voices including Shubh, Aditya, Ritu, Simran, Anand, Roopa, Priya, and more.

Extended Character Limit

Support for up to 2500 characters per request for longer content generation.

Sample Rate Options

REST accepts 8000–48000 Hz (see [Limits](https://docs.sarvam.ai/api/getting-started/models/bulbul#limits)). Streaming accepts 8000–24000 Hz. Omitted → 22050 Hz output.

Language Support (v3)

On `bulbul:v3`: support for 11 languages (10 Indian + English) with BCP-47 codes. The target language code is primarily used by the pre-TTS text normalization model.

Natural Prosody

Human-like speech patterns with natural intonation and emotional expression.

Pace Control

Adjustable speech speed from 0.5x to 2.0x for customized delivery.

## Language Support

### Bulbul v3

Bulbul v3 supports the following Indian languages:

Hindi (`hi-IN`), Bengali (`bn-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), Gujarati (`gu-IN`), Kannada (`kn-IN`), Malayalam (`ml-IN`), Marathi (`mr-IN`), Punjabi (`pa-IN`), Odia (`od-IN`), English (`en-IN`)

### Bulbul v4 Flash

Bulbul v4 Flash voices cover Hindi, English, English–Hindi (`enhi`), Bengali, Gujarati, Kannada, Marathi, Punjabi, Tamil, and Telugu. Malayalam and Odia are not yet offered on v4 Flash.

## Available Speakers

### Bulbul v3

Bulbul v3 offers 30+ speaker voices:

**Speakers:** Shubh (default), Aditya, Ritu, Priya, Neha, Rahul, Pooja, Rohan, Simran, Kavya, Amit, Dev, Ishita, Shreya, Ratan, Varun, Manan, Sumit, Roopa, Kabir, Aayan, Ashutosh, Advait, Anand, Tanya, Tarun, Sunny, Mani, Gokul, Vijay, Shruti, Suhani, Mohit, Kavitha, Rehan, Soham, Rupali

### Bulbul v4 Flash

Bulbul v4 Flash offers 200+ persona voices (222 catalog IDs). Most IDs follow `<name>_<language>_<style>` (for example `ishita_hi_devotional`, `simran_en_customer`); some use the `enhi` tag for English–Hindi code-mixed styles. Browse the full catalog on the [Voices page](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices#bulbul-v4-flash-voices).

Use the `speaker` parameter to select specific voices for your use case. For **bulbul:v4-flash** , omit `speaker` to use the default persona **`shubh_enhi_ads`** , or pick any ID from the v4 catalog. The v3 default `shubh` is not valid on this model.

**REST output codec:** `wav`, `mp3`, `aac`, `flac`, and `linear16` work with **bulbul:v3** and **bulbul:v4-flash**. The `opus` value may appear in the schema but currently returns an error on `/text-to-speech`; prefer `mp3` for compressed audio.

## Key Capabilities

###### Basic Usage

###### Speaker Selection

###### Sample Rate Control

Convert text to speech with Bulbul v4 Flash — recommended for new integrations.

PythonJavaScriptcURL
    
    
    from sarvamai import SarvamAI
    
    from sarvamai.play import play, save
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_SARVAM_API_KEY"
    
    )
    
    response = client.text_to_speech.convert(
    
        text="Hello, how are you today?",
    
        language_code="en-IN",
    
        model="bulbul:v4-flash",
    
        speaker="simran_en_customer",
    
    )
    
    # Play the audio
    
    play(response)
    
    # Save the response to a file
    
    save(response, "output.wav")

## Limits

Limit| Value  
---|---  
Max characters per request (REST)| 2,500  
`pace`| 0.5–2.0 (`bulbul:v3`, `bulbul:v4-flash`) / 0.3–3.0 (`bulbul:v2`)  
`pitch`| -1.0 to 1.0; suitable range -0.75 to 0.75 (`bulbul:v2` only)  
`loudness`| 0.1–3.0 (`bulbul:v2` only)  
`speech_sample_rate`| REST: 8000 / 16000 / 22050 / 24000 / 32000 / 44100 / 48000. Streaming: 8000 / 16000 / 22050 / 24000. Omitted → 22050 Hz output  
Rate limits| See [Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)  
  
## Known Limitations

Limitation| Detail| Workaround  
---|---|---  
**No SSML support**|  Bulbul does not support SSML tags for fine-grained prosody control| Use `pace` for coarse control; split text at natural pause points  
**Romanised Indic input degrades quality**|  Transliterated input (e.g., `"Aapka order confirm ho gaya hai"`) significantly reduces output quality| Always use native script for Indic words (e.g., `"आपका order confirm हो गया है"`)  
**High sample rates are REST-only**| `32000`, `44100`, and `48000` are accepted on REST only; streaming accepts up to `24000`| Use ≤ 24000 Hz for HTTP stream or WebSocket  
  
## Next Steps

[Developer quickstartLearn how to integrate the Bulbul v3 API within your application.](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)[API ReferenceComplete API documentation for text to speech endpoints.](https://docs.sarvam.ai/api-reference/text-to-speech/convert)[CookbookStep-by-step tutorial for text-to-speech implementation.](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/getting-started/models/saaras)[Sarvam-105BNext](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


