---
url: https://docs.sarvam.ai/api-reference/text-to-speech/convert/
title: REST | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-22T06:32:49.532654+00:00
---

# REST | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/text-to-speech/convert/

Skip to navigation

This page is for API Reference.

[APIs](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Text to Speech](https://docs.sarvam.ai/api-reference/text-to-speech/convert)

# REST

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/text-to-speech/convert.md "View this page as plain text")|More actions

POST

https://api.sarvam.ai/text-to-speech

POST

/text-to-speech

Python
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_API_KEY_HERE",
    
    )
    
    client.text_to_speech.convert(
    
        text="Welcome to Sarvam AI!",
    
        language_code="hi-IN",
    
    )

Try it

200Successful
    
    
    {
    
      "request_id": "20250101_0a1b2c3d-1234-5678-9abc-def012345678",
    
      "audios": [
    
        "UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA="
    
      ]
    
    }

Convert text into spoken audio. The output is a base64-encoded audio string that must be decoded before use.

**Available Models:**

  * **bulbul:v4-flash** : Latest model, recommended for new integrations — same request/response contract as bulbul:v3, with a 200+ voice persona catalog
  * **bulbul:v3** : Stable model (API default when `model` is omitted) with 30+ voices and temperature control
  * **bulbul:v2** : Legacy model with pitch and loudness controls



**Important Notes for bulbul:v3 and bulbul:v4-flash:**

  * Pitch and loudness parameters are NOT supported
  * Pace range: 0.5 to 2.0
  * Preprocessing is automatically enabled
  * Default sample rate is 22050 Hz when `speech_sample_rate` is omitted
  * Supports sample rates: 8000, 16000, 22050, 24000 Hz (REST API also supports 32000, 44100, 48000 Hz)



### Authentication

api-subscription-keystring

API Key authentication via header

### Request

This endpoint expects an object.

textstringRequired

The text(s) to be converted into speech.

**Features:**

  * Supports code-mixed text (English and Indic languages)



**Model-specific limits:**

  * **bulbul:v3:** Max 2500 characters
  * **bulbul:v4-flash:** Max 2500 characters
  * **bulbul:v2:** Max 1500 characters



**Important Note:**

  * For numbers larger than 4 digits, use commas (e.g., ‘10,000’ instead of ‘10000’)
  * This ensures proper pronunciation as a whole number



Show 1 variants

language_codeenumRequired

The language code in BCP-47 format.

Show 11 enum values

speakerenum or nullOptionalDefaults to `shubh`

The speaker voice to be used for the output audio.

**Default:** shubh (for bulbul:v3), anushka (for bulbul:v2), shubh_enhi_ads (for bulbul:v4-flash). For v4, you can omit `speaker` to use `shubh_enhi_ads`, or set any persona ID from the Voices guide (v3/v2 short names are not valid).

**Model Compatibility (Speakers compatible with respective model):**

  * **bulbul:v3:**
    * shubh (default), aditya, ritu, priya, neha, rahul, pooja, rohan, simran, kavya, amit, dev, ishita, shreya, ratan, varun, manan, sumit, roopa, kabir, aayan, ashutosh, advait, anand, tanya, tarun, sunny, mani, gokul, vijay, shruti, suhani, mohit, kavitha, rehan, soham, rupali
  * **bulbul:v4-flash:**
    * 200+ persona voices named `<name>_<language>_<style>` (e.g. `shubh_hi_devotional`, `simran_en_customer`). See the [Voices guide](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices#bulbul-v4-flash-voices) for the full catalog.
  * **bulbul:v2:**
    * Female: anushka, manisha, vidya, arya
    * Male: abhilash, karun, hitesh



**Note:** Speaker selection must match the chosen model version.

**Important:** Speaker names are case-sensitive and must be lowercase (e.g., `ritu` not `Ritu`).

Show 266 enum values

pitchdouble or nullOptional

Controls the pitch of the audio. Lower values result in a deeper voice, while higher values make it sharper. The suitable range is between -0.75 and 0.75. Default is 0.0.

**Note:** This parameter is only supported for bulbul:v2. It is NOT supported for bulbul:v3 or bulbul:v4-flash.

pacedouble or nullOptional`0.3-3`Defaults to `1`

Controls the speed of the audio. Lower values result in slower speech, while higher values make it faster. Default is 1.0.

**Model-specific ranges:**

  * **bulbul:v3:** 0.5 to 2.0
  * **bulbul:v4-flash:** 0.5 to 2.0
  * **bulbul:v2:** 0.3 to 3.0



loudnessdouble or nullOptional`0.1-3`

Controls the loudness of the audio. Lower values result in quieter audio, while higher values make it louder. The suitable range is between 0.3 and 3.0. Default is 1.0.

**Note:** This parameter is only supported for bulbul:v2. It is NOT supported for bulbul:v3 or bulbul:v4-flash.

speech_sample_rateenum or nullOptionalDefaults to `22050`

Specifies the sample rate of the output audio. Supported values are 8000, 16000, 22050, 24000, 32000, 44100, 48000 Hz.

**Note:** Higher sample rates (32000, 44100, 48000 Hz) are only available with bulbul:v3 and bulbul:v4-flash via the REST API, not in streaming mode.

**Default:** 22050 Hz

Show 7 enum values

enable_preprocessingbooleanOptionalDefaults to `false`

Controls whether normalization of English words and numeric entities (e.g., numbers, dates) is performed. Set to true for better handling of mixed-language text.

**Model-specific behavior:**

  * **bulbul:v3:** Not Supported
  * **bulbul:v4-flash:** Not Supported
  * **bulbul:v2:** Default is false



modelenumOptional

Specifies the model to use for text-to-speech conversion.

**Available models:**

  * **bulbul:v4-flash:** Latest model, recommended for new integrations — same contract as bulbul:v3, with a 200+ voice persona catalog
  * **bulbul:v3:** Stable model (API default when `model` is omitted) with 30+ voices, pace, and temperature control
  * **bulbul:v2:** Legacy model with pitch, loudness, and pace controls



Allowed values:bulbul:v2bulbul:v3bulbul:v4-flash

output_audio_codecenum or nullOptionalDefaults to `wav`

Specifies the audio codec for the output audio file. Different codecs offer various compression and quality characteristics.

**Note:** On `/text-to-speech` with **bulbul:v3** and **bulbul:v4-flash** , `opus` is listed for schema compatibility but currently returns a validation error; use `wav`, `mp3`, `aac`, `flac`, or `linear16`.

Show 8 enum values

temperaturedouble or nullOptional`0.01-1`Defaults to `0.6`

Temperature controls how much randomness and expressiveness the TTS model uses while generating speech.

Lower values produce more stable and consistent output, while higher values sound more expressive but may introduce artifacts or errors. The suitable range is between 0.01 and 1.0. Default is 0.6.

**Note:** This parameter is only supported for bulbul:v3 and bulbul:v4-flash. It has no effect on bulbul:v2.

dict_idstring or nullOptional

The ID of a pronunciation dictionary to apply during synthesis. When provided, matching words in the input text will be replaced with their custom pronunciations before generating speech.

Create and manage dictionaries via the [Pronunciation Dictionary API](https://docs.sarvam.ai/api-reference-docs/pronunciation-dictionary/create). Only supported by **bulbul:v3** and **bulbul:v4-flash**.

enable_cached_responsesbooleanOptionalDefaults to `false`

Enable caching for the request. When enabled, identical requests will return cached audio instead of regenerating. Default is false.

**Note:** Currently in beta and only available for bulbul:v1 and bulbul:v2 models.

### Response

Successful Response

request_idstring or null

audioslist of strings

The output audio files in WAV format, encoded as base64 strings. Each string corresponds to one of the input texts.

### Errors

400

Bad Request Error

403

Forbidden Error

422

Unprocessable Entity Error

429

Too Many Requests Error

500

Internal Server Error

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/realtime/ws)[REST StreamNext](https://docs.sarvam.ai/api-reference/text-to-speech/convert-stream)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * API Reference

    * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
    * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
    * [Beta APIs and Models](https://docs.sarvam.ai/api-reference/beta-apis)
    * [Meta Prompt Guide](https://docs.sarvam.ai/api-reference/metaprompt)
  * APIs

    * Speech to Text

    * Text to Speech
      * [POSTREST](https://docs.sarvam.ai/api-reference/text-to-speech/convert)
      * [POSTREST Stream](https://docs.sarvam.ai/api-reference/text-to-speech/convert-stream)
      * [WSSWebSocket](https://docs.sarvam.ai/api-reference/text-to-speech/stream)

    * Instant Voice CloningBeta

    * Pronunciation Dictionary

    * Text Processing

    * Chat Completion

    * Responses API

    * Content Studio - Dubbing

    * Document Translation

    * Document Intelligence

    * Legacy

    * Responses

  * Voice Agents

    * [Introduction](https://docs.sarvam.ai/api-reference/conversations)
    * Deployments

    * Campaigns

    * Instant Outbound

    * Analytics

    * Boards

    * Tests

    * BYOK

    * v1-webhooks




  * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
  * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
  * [Beta APIs and Models](https://docs.sarvam.ai/api-reference/beta-apis)
  * [Meta Prompt Guide](https://docs.sarvam.ai/api-reference/metaprompt)
  * [REST](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)
  * [Batch - Initiate Job](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/initiate)
  * [Batch - Upload Files](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/upload)
  * [Batch - Start Job](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/start)
  * [Batch - Get Status](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/status)
  * [Batch - Download Results](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/download)
  * [Realtime Streaming](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/realtime/ws)
  * [REST](https://docs.sarvam.ai/api-reference/text-to-speech/convert)
  * [REST Stream](https://docs.sarvam.ai/api-reference/text-to-speech/convert-stream)
  * [WebSocket](https://docs.sarvam.ai/api-reference/text-to-speech/stream)
  * [Create Voice](https://docs.sarvam.ai/api-reference/voice-cloning/create-voice)
  * [Generate Speech](https://docs.sarvam.ai/api-reference/voice-cloning/clone)
  * [REST Stream](https://docs.sarvam.ai/api-reference/voice-cloning/clone-stream)
  * [WebSocket](https://docs.sarvam.ai/api-reference/voice-cloning/clone-ws)
  * [List Voices](https://docs.sarvam.ai/api-reference/voice-cloning/list-voices)
  * [Get Voice](https://docs.sarvam.ai/api-reference/voice-cloning/get-voice)
  * [Delete Voice](https://docs.sarvam.ai/api-reference/voice-cloning/delete-voice)
  * [Create](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/create)
  * [List](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/list)
  * [Get](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/get)
  * [Update](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/update)
  * [Delete](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/delete)
  * [Text Translation](https://docs.sarvam.ai/api-reference/text/translate-text)
  * [Transliteration](https://docs.sarvam.ai/api-reference/text/transliterate-text)
  * [Language Detection](https://docs.sarvam.ai/api-reference/text/identify-language)
  * [Chat Completion V1](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1)
  * [Chat Completion V2](https://docs.sarvam.ai/api-reference/chat/chat-completions-v2)
  * [Get Model V2](https://docs.sarvam.ai/api-reference/chat/model-v2)
  * [List Models V2](https://docs.sarvam.ai/api-reference/chat/models-v2)
  * [Create Response](https://docs.sarvam.ai/api-reference/responses/create)
  * [Create Dubbing Job](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/create-dub)
  * [Start Job](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/start-dub)
  * [Live Status](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/live-status)
  * [Export Status](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/export-status)
  * [Create Document Translation Job](https://docs.sarvam.ai/api-reference/translate-document/create-doc-translation)
  * [Start Job](https://docs.sarvam.ai/api-reference/translate-document/start-doc-translation)
  * [Live Status](https://docs.sarvam.ai/api-reference/translate-document/doc-translation-live-status)
  * [Trigger Export](https://docs.sarvam.ai/api-reference/translate-document/doc-translation-trigger-export)
  * [Export Status](https://docs.sarvam.ai/api-reference/translate-document/doc-translation-export-status)
  * [Create Upload URL](https://docs.sarvam.ai/api-reference/doc-ai/job/upload)
  * [Digitise Document](https://docs.sarvam.ai/api-reference/doc-ai/job/digitise)
  * [Extract Fields](https://docs.sarvam.ai/api-reference/doc-ai/job/extract)
  * [Get Job Status](https://docs.sarvam.ai/api-reference/doc-ai/job/status)
  * [Get Job Results](https://docs.sarvam.ai/api-reference/doc-ai/job/results)
  * [Get Download URL](https://docs.sarvam.ai/api-reference/doc-ai/job/download-url)
  * [WebSocket](https://docs.sarvam.ai/api-reference/legacy/speech-to-text/transcribe/ws)
  * [REST](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate)
  * [WebSocket](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate/ws)
  * [Batch - Initiate Job](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/initiate)
  * [Batch - Upload Files](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/upload)
  * [Batch - Start Job](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/start)
  * [Batch - Get Status](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/status)
  * [Batch - Download Results](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/download)
  * [Initialise Job](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/initialise)
  * [Get Upload Links](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/get-upload-links)
  * [Start Job](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/start)
  * [Get Status](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/get-status)
  * [Get Download Links](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/get-download-links)
  * [Create Response](https://docs.sarvam.ai/api-reference/responses/create-stream)
  * [Introduction](https://docs.sarvam.ai/api-reference/conversations)
  * [Create deployment](https://docs.sarvam.ai/api-reference/deployments/create)
  * [List deployments](https://docs.sarvam.ai/api-reference/deployments/list)
  * [Get deployment](https://docs.sarvam.ai/api-reference/deployments/get)
  * [Update deployment](https://docs.sarvam.ai/api-reference/deployments/update)
  * [Update status](https://docs.sarvam.ai/api-reference/deployments/update-status)
  * [Delete deployment](https://docs.sarvam.ai/api-reference/deployments/delete)
  * [Upload cohort](https://docs.sarvam.ai/api-reference/deployments/cohorts/upload)
  * [Stream cohort](https://docs.sarvam.ai/api-reference/deployments/cohorts/stream)
  * [List cohorts](https://docs.sarvam.ai/api-reference/deployments/cohorts/list)
  * [Get cohort](https://docs.sarvam.ai/api-reference/deployments/cohorts/get)
  * [Download cohort file](https://docs.sarvam.ai/api-reference/deployments/cohorts/download)
  * [Create campaign](https://docs.sarvam.ai/api-reference/campaigns/create)
  * [List campaigns](https://docs.sarvam.ai/api-reference/campaigns/list)
  * [Get campaign](https://docs.sarvam.ai/api-reference/campaigns/get)
  * [Update campaign](https://docs.sarvam.ai/api-reference/campaigns/update)
  * [Update status](https://docs.sarvam.ai/api-reference/campaigns/update-status)
  * [Webhook payload](https://docs.sarvam.ai/api-reference/campaigns/webhook-payload)
  * [Upload cohort](https://docs.sarvam.ai/api-reference/campaigns/cohorts/upload)
  * [Stream cohort](https://docs.sarvam.ai/api-reference/campaigns/cohorts/stream)
  * [List cohorts](https://docs.sarvam.ai/api-reference/campaigns/cohorts/list)
  * [Get cohort](https://docs.sarvam.ai/api-reference/campaigns/cohorts/get)
  * [Download cohort file](https://docs.sarvam.ai/api-reference/campaigns/cohorts/download)
  * [Create outbound call](https://docs.sarvam.ai/api-reference/instant-outbound/create)
  * [Webhook payload](https://docs.sarvam.ai/api-reference/instant-outbound/webhook-payload)
  * [Get attempts](https://docs.sarvam.ai/api-reference/analytics/attempts)
  * [Get interactions](https://docs.sarvam.ai/api-reference/analytics/interactions)
  * [Get recordings](https://docs.sarvam.ai/api-reference/analytics/recordings)
  * [Get transcripts](https://docs.sarvam.ai/api-reference/analytics/transcripts)
  * [Overview](https://docs.sarvam.ai/api-reference/boards/overview)
  * [Writing board SQL](https://docs.sarvam.ai/api-reference/boards/sql)
  * [Best practices](https://docs.sarvam.ai/api-reference/boards/best-practices)
  * [List boards](https://docs.sarvam.ai/api-reference/boards/list)
  * [Create board](https://docs.sarvam.ai/api-reference/boards/create)
  * [Get board](https://docs.sarvam.ai/api-reference/boards/get)
  * [Update board](https://docs.sarvam.ai/api-reference/boards/update)
  * [Duplicate board](https://docs.sarvam.ai/api-reference/boards/duplicate)
  * [Create tab](https://docs.sarvam.ai/api-reference/boards/tabs/create)
  * [Update tab](https://docs.sarvam.ai/api-reference/boards/tabs/update)
  * [Run tab](https://docs.sarvam.ai/api-reference/boards/tabs/run)
  * [Create widget](https://docs.sarvam.ai/api-reference/boards/widgets/create)
  * [Update widget](https://docs.sarvam.ai/api-reference/boards/widgets/update)
  * [Duplicate widget](https://docs.sarvam.ai/api-reference/boards/widgets/duplicate)
  * [Run widget](https://docs.sarvam.ai/api-reference/boards/widgets/run)
  * [List filters](https://docs.sarvam.ai/api-reference/boards/filters/list)
  * [Update filter](https://docs.sarvam.ai/api-reference/boards/filters/update)
  * [Create notification rule](https://docs.sarvam.ai/api-reference/boards/notifications/create)
  * [List notification rules](https://docs.sarvam.ai/api-reference/boards/notifications/list)
  * [Get notification rule](https://docs.sarvam.ai/api-reference/boards/notifications/get)
  * [Update notification rule](https://docs.sarvam.ai/api-reference/boards/notifications/update)
  * [Get query schema](https://docs.sarvam.ai/api-reference/boards/query/schema)
  * [Preview query](https://docs.sarvam.ai/api-reference/boards/query/preview)
  * [Overview](https://docs.sarvam.ai/api-reference/tests/overview)
  * [Best practices](https://docs.sarvam.ai/api-reference/tests/best-practices)
  * [List test suites](https://docs.sarvam.ai/api-reference/tests/list)
  * [Create a test suite](https://docs.sarvam.ai/api-reference/tests/create)
  * [Get a test suite](https://docs.sarvam.ai/api-reference/tests/get)
  * [Update a test suite](https://docs.sarvam.ai/api-reference/tests/update)
  * [Add a test case](https://docs.sarvam.ai/api-reference/tests/test-cases/add)
  * [Get a test case](https://docs.sarvam.ai/api-reference/tests/test-cases/get)
  * [Update a test case](https://docs.sarvam.ai/api-reference/tests/test-cases/update)
  * [Duplicate a test case](https://docs.sarvam.ai/api-reference/tests/test-cases/duplicate)
  * [Map suite variables onto an app](https://docs.sarvam.ai/api-reference/tests/mappings/create)
  * [Get the variable mapping](https://docs.sarvam.ai/api-reference/tests/mappings/get)
  * [Run a test suite](https://docs.sarvam.ai/api-reference/tests/runs/run-suite)
  * [Run a single test case](https://docs.sarvam.ai/api-reference/tests/runs/run-test-case)
  * [List runs](https://docs.sarvam.ai/api-reference/tests/runs/list)
  * [Get a run](https://docs.sarvam.ai/api-reference/tests/runs/get)
  * [Get test case results](https://docs.sarvam.ai/api-reference/tests/runs/results)
  * [Overview](https://docs.sarvam.ai/api-reference/byok/overview)
  * [Obtain access token](https://docs.sarvam.ai/api-reference/byok/auth)
  * [Decrypt key](https://docs.sarvam.ai/api-reference/byok/decrypt-key)
  * [Rotate key](https://docs.sarvam.ai/api-reference/byok/rotate-key)
  * [List Webhook Deliveries](https://docs.sarvam.ai/api-reference/v-1-webhooks/list-webhook-deliveries)
  * [Retry Webhook Deliveries](https://docs.sarvam.ai/api-reference/v-1-webhooks/retry-webhook-deliveries)
  * [List Deployment Webhook Deliveries](https://docs.sarvam.ai/api-reference/v-1-webhooks/list-deployment-webhook-deliveries)
  * [Retry Deployment Webhook Deliveries](https://docs.sarvam.ai/api-reference/v-1-webhooks/retry-deployment-webhook-deliveries)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


