---
url: https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/
title: REST | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-17T14:23:24.093289+00:00
---

# REST | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/

Skip to navigation

This page is for API Reference.

[APIs](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Speech to Text](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)

# REST

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe.md "View this page as plain text")|More actions

POST

https://api.sarvam.ai/speech-to-text

POST

/speech-to-text

Python
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_API_KEY_HERE",
    
    )
    
    client.speech_to_text.transcribe(
    
        file="example_file",
    
    )

Try it

200Successful
    
    
    {
    
      "request_id": "20250101_0a1b2c3d-1234-5678-9abc-def012345678",
    
      "transcript": "नमस्ते, आप कैसे हैं?",
    
      "language_code": "hi-IN"
    
    }

## Speech to Text API

This API transcribes speech to text in multiple Indian languages and English. Supports transcription for interactive applications.

### Available Options:

  * **REST API** (Current Endpoint): For quick responses under 30 seconds with immediate results
  * **Batch API** : For longer audio files, [Follow This Documentation](https://docs.sarvam.ai/api-reference-docs/api-guides-tutorials/speech-to-text/batch-api)
    * Supports diarization (speaker identification)



### Note:

  * Pricing differs for REST and Batch APIs
  * Diarization is only available in Batch API with separate pricing
  * Please refer to [here](https://docs.sarvam.ai/api-reference-docs/pricing) for detailed pricing information



### Authentication

api-subscription-keystring

API Key authentication via header

### Request

This endpoint expects a multipart form containing a file.

filefileRequired

The audio file to transcribe. Supported formats include WAV, MP3, AAC, AIFF, OGG, OPUS, FLAC, MP4/M4A, AMR, WMA, WebM, and PCM formats. The API automatically detects most codec formats, but for PCM files (pcm_s16le, pcm_l16, pcm_raw), you must specify the input_audio_codec parameter. PCM files are supported only at 16kHz sample rate. The API works best with audio files sampled at 16kHz. If the audio contains multiple channels, they will be merged into a single channel.

modelenumOptional

Specifies the model to use for speech-to-text conversion.

  * **saaras:v4** (default, recommended, latest): Flexible output formats across all modes (transcribe, translate, verbatim, translit, codemix), supporting Global + Indian English and 22 Indic languages.

  * **saaras:v3** : State-of-the-art model with flexible output formats. Supports multiple modes via the `mode` parameter: transcribe, translate, verbatim, translit, codemix.




Allowed values:saaras:v3saaras:v4

modeenum or nullOptionalDefaults to `transcribe`

Mode of operation. **Only applicable when using saaras:v3 model.**

Example audio: ‘मेरा फोन नंबर है 9840950950’

  * **transcribe** (default): Standard transcription in the original language with proper formatting and number normalization.

    * Output: `मेरा फोन नंबर है 9840950950`
  * **translate** : Translates speech from any supported Indic language to English.

    * Output: `My phone number is 9840950950`
  * **verbatim** : Exact word-for-word transcription without normalization, preserving filler words and spoken numbers as-is.

    * Output: `मेरा फोन नंबर है नौ आठ चार zero नौ पांच zero नौ पांच zero`
  * **translit** : Romanization - Transliterates speech to Latin/Roman script only.

    * Output: `mera phone number hai 9840950950`
  * **codemix** : Code-mixed text with English words in English and Indic words in native script.

    * Output: `मेरा phone number है 9840950950`



Allowed values:transcribetranslateverbatimtranslitcodemix

language_codeenumOptional

Specifies the language of the input audio in BCP-47 format.

**Available Options:**

  * `unknown`: Use when the language is not known; the API will auto-detect.
  * `hi-IN`: Hindi
  * `bn-IN`: Bengali
  * `kn-IN`: Kannada
  * `ml-IN`: Malayalam
  * `mr-IN`: Marathi
  * `od-IN`: Odia
  * `pa-IN`: Punjabi
  * `ta-IN`: Tamil
  * `te-IN`: Telugu
  * `en-IN`: English
  * `gu-IN`: Gujarati
  * `as-IN`: Assamese
  * `ur-IN`: Urdu
  * `ne-IN`: Nepali
  * `kok-IN`: Konkani
  * `ks-IN`: Kashmiri
  * `sd-IN`: Sindhi
  * `sa-IN`: Sanskrit
  * `sat-IN`: Santali
  * `mni-IN`: Manipuri
  * `brx-IN`: Bodo
  * `mai-IN`: Maithili
  * `doi-IN`: Dogri



Show 24 enum values

with_timestampsbooleanOptionalDefaults to `false`

Enables chunk-level timestamps in the response. If set to `true`, the response includes a `timestamps` object with `words`, `start_time_seconds`, and `end_time_seconds` (each entry covers a sentence or phrase, not an individual word).

**Note:** Word-level timestamps are not supported. Speaker diarization is not supported on the REST API; use the Batch API for diarized, chunk-level timestamps.

input_audio_codecenumOptional

Input Audio codec/format of the input file. PCM files are supported only at 16kHz sample rate.

Show 24 enum values

keytermslist of strings or nullOptional

List of up to 50 domain-specific terms (names, places, brands, technical terms) to bias recognition toward. Each keyterm can contain up to 64 characters. Put phrases such as `New Delhi` in one list item; do not send comma-separated terms in one string. Keyterms bias recognition — they do not guarantee that a term will appear in the transcript. **Only supported with`model=saaras:v4`.** Sent as a JSON-encoded array in one multipart form field, e.g. `keyterms=["Sarvam","New Delhi","Vistaar"]`. Do not use the older `keyterm` or `hotwords` fields.

### Response

Successful Response

request_idstring or null

transcriptstring

The transcribed text from the provided audio file.

language_codestring or null

This will return the BCP-47 code of language spoken in the input. If multiple languages are detected, this will return language code of most predominant spoken language. If no language is detected, this will be null

timestampsobject or nullOptional

Chunk-level timestamps for the transcribed text (sentence/phrase segments, not individual words). Present only when `with_timestamps` is `true`; omitted otherwise.

Show 3 properties

language_probabilitydouble or nullOptional

Float value (0.0 to 1.0) indicating confidence in the detected language. Present when `language_code` is omitted or set to `unknown`; omitted (or null) when a specific language code is provided.

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

503

Service Unavailable Error

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/metaprompt)[Batch - Initiate JobNext](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/initiate)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * API Reference

    * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
    * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
    * [Access to Beta APIs](https://docs.sarvam.ai/api-reference/beta-apis)
    * [Meta Prompt Guide](https://docs.sarvam.ai/api-reference/metaprompt)
  * APIs

    * Speech to Text
      * [POSTREST](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)
      * [POSTBatch - Initiate Job](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/initiate)
      * [POSTBatch - Upload Files](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/upload)
      * [POSTBatch - Start Job](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/start)
      * [GETBatch - Get Status](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/status)
      * [POSTBatch - Download Results](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/download)
      * [WSSRealtime Streaming](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/realtime/ws)

    * Text to Speech

    * Instant Voice CloningBeta

    * Pronunciation Dictionary

    * Text Processing

    * Chat Completion

    * Responses APIBeta

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
  * [Access to Beta APIs](https://docs.sarvam.ai/api-reference/beta-apis)
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


