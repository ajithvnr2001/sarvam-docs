---
url: https://docs.sarvam.ai/api-reference/text/translate-text/
title: Text Translation | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-17T14:23:23.043321+00:00
---

# Text Translation | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/text/translate-text/

Skip to navigation

This page is for API Reference.

[APIs](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Text Processing](https://docs.sarvam.ai/api-reference/text/translate-text)

# Text Translation

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/text/translate-text.md "View this page as plain text")|More actions

POST

https://api.sarvam.ai/translate

POST

/translate

Python
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_API_KEY_HERE",
    
    )
    
    client.text.translate(
    
        input="Hello, how are you?",
    
        source_language_code="en-IN",
    
        target_language_code="hi-IN",
    
    )

Try it

200Successful
    
    
    {
    
      "request_id": "20250101_0a1b2c3d-1234-5678-9abc-def012345678",
    
      "translated_text": "नमस्ते, आप कैसे हैं?",
    
      "source_language_code": "en-IN"
    
    }

**Short text** — strings, chat messages, and snippets. You are on the right endpoint (`POST /translate`).

**Whole files** — PDF, Word, Excel, PowerPoint, or HTML with layout preserved. Use the [Document Translation API](https://docs.sarvam.ai/api-reference/translate-document/create-doc-translation) (`POST /translate/document/jobs`) instead of pasting file contents into this endpoint.

[Document TranslationUpload once, translate into multiple languages per job, and export in the same format as the source (PDF→PDF, DOCX→DOCX).](https://docs.sarvam.ai/api-reference/translate-document/create-doc-translation)[Document Translation guideOverview, pricing, and step-by-step flows for doc-to-doc translation.](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)

**Translation** converts text from one language to another while preserving its meaning. For Example: **‘मैं ऑफिस जा रहा हूँ’** translates to **‘I am going to the office’** in English, where the script and language change, but the original meaning remains the same.

Available languages:

  * **`bn-IN`** : Bengali
  * **`en-IN`** : English
  * **`gu-IN`** : Gujarati
  * **`hi-IN`** : Hindi
  * **`kn-IN`** : Kannada
  * **`ml-IN`** : Malayalam
  * **`mr-IN`** : Marathi
  * **`od-IN`** : Odia
  * **`pa-IN`** : Punjabi
  * **`ta-IN`** : Tamil
  * **`te-IN`** : Telugu



### Newly added languages:

  * **`as-IN`** : Assamese
  * **`brx-IN`** : Bodo
  * **`doi-IN`** : Dogri
  * **`kok-IN`** : Konkani
  * **`ks-IN`** : Kashmiri
  * **`mai-IN`** : Maithili
  * **`mni-IN`** : Manipuri (Meiteilon)
  * **`ne-IN`** : Nepali
  * **`sa-IN`** : Sanskrit
  * **`sat-IN`** : Santali
  * **`sd-IN`** : Sindhi
  * **`ur-IN`** : Urdu



For hands-on practice, you can explore the notebook tutorial on [Translate API Tutorial](https://github.com/sarvamai/sarvam-ai-cookbook/blob/main/notebooks/translate/Translate_API_Tutorial.ipynb).

### Authentication

api-subscription-keystring

API Key authentication via header

### Request

This endpoint expects an object.

inputstringRequired`<=2000 characters`

The text you want to translate is the input text that will be processed by the translation model. The maximum is 1000 characters for Mayura:v1 and 2000 characters for Sarvam-Translate:v1.

source_language_codeenumRequired

Source language code for translation input.

**mayura:v1 Languages:** Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu

**sarvam-translate:v1 Languages:** All mayura:v1 languages and Assamese, Bodo, Dogri, Konkani, Kashmiri, Maithili, Manipuri, Nepali, Sanskrit, Santali, Sindhi, Urdu

**Note:** mayura:v1 supports automatic language detection using ‘auto’ as the source language code.

Show 24 enum values

target_language_codeenumRequired

The language code of the translated text. This specifies the target language for translation.

**mayura:v1 Languages:** Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu

**sarvam-translate:v1 Languages:** All mayura:v1 and Assamese, Bodo, Dogri, Konkani, Kashmiri, Maithili, Manipuri, Nepali, Sanskrit, Santali, Sindhi, Urdu

Show 23 enum values

speaker_genderenumOptional

Please specify the gender of the speaker for better translations.

Allowed values:MaleFemale

modeenumOptional

Specifies the tone or style of the translation.

**Model Support:**

  * **mayura:v1** : Supports formal, classic-colloquial, modern-colloquial, and code-mixed modes
  * **sarvam-translate:v1** : Only formal mode is supported



**Default:** formal

Allowed values:formalmodern-colloquialclassic-colloquialcode-mixed

modelenumOptional

Specifies the translation model to use.

  * mayura:v1: Supports 12 languages with all modes, output scripts, and automatic language detection.
  * sarvam-translate:v1: Supports all 22 scheduled languages of India, formal mode only.



Allowed values:mayura:v1sarvam-translate:v1

output_scriptenum or nullOptional

**output_script** : This is an optional parameter which controls the transliteration style applied to the output text.

**Transliteration** : Converting text from one script to another while preserving pronunciation.

For mayura:v1 - We support transliteration with four options:

  * **`null`**(default): No transliteration applied.
  * **`roman`** : Transliteration in Romanized script.
  * **`fully-native`** : Transliteration in the native script with formal style.
  * **`spoken-form-in-native`** : Transliteration in the native script with spoken style.



For sarvam-translate:v1 - Transliteration is not supported.

### Example:

English: Your EMI of Rs. 3000 is pending. Default modern translation: आपका Rs. 3000 का EMI pending है (when `null` is passed).

With postprocessing enabled:

  * **roman output** : aapka Rs. 3000 ka EMI pending hai.



Allowed values:romanfully-nativespoken-form-in-native

numerals_formatenumOptional

`numerals_format` is an optional parameter with two options (supported for both mayura:v1 and sarvam-translate:v1):

  * **`international`** (default): Uses regular numerals (0-9).
  * **`native`** : Uses language-specific native numerals.



### Example:

  * If `international` format is selected, we use regular numerals (0-9). For example: `मेरा phone number है: 9840950950`.
  * If `native` format is selected, we use language-specific native numerals, like: `मेरा phone number है: ९८४०९५०९५०`.



Allowed values:internationalnative

### Response

Successful Response

request_idstring or null

translated_textstring

Translated text result in the requested target language.

source_language_codestring

Detected or provided source language of the input text.

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

[Previous](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/delete)[TransliterationNext](https://docs.sarvam.ai/api-reference/text/transliterate-text)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * API Reference

    * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
    * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
    * [Access to Beta APIs](https://docs.sarvam.ai/api-reference/beta-apis)
    * [Meta Prompt Guide](https://docs.sarvam.ai/api-reference/metaprompt)
  * APIs

    * Speech to Text

    * Text to Speech

    * Instant Voice CloningBeta

    * Pronunciation Dictionary

    * Text Processing
      * [POSTText Translation](https://docs.sarvam.ai/api-reference/text/translate-text)
      * [POSTTransliteration](https://docs.sarvam.ai/api-reference/text/transliterate-text)
      * [POSTLanguage Detection](https://docs.sarvam.ai/api-reference/text/identify-language)

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


