---
url: https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate/ws/
title: WebSocket | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-22T06:32:53.169153+00:00
---

# WebSocket | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate/ws/

Skip to navigation

This page is for API Reference.

[APIs](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Legacy](https://docs.sarvam.ai/api-reference/legacy/speech-to-text/transcribe/ws)[Speech to Text Translate](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate)

# WebSocket

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate/ws.md "View this page as plain text")|More actions

WSS

wss://api.sarvam.ai/speech-to-text-translate/ws

Handshake

URL| wss://api.sarvam.ai/speech-to-text-translate/ws  
---|---  
Method| GET  
Status| 101 Switching Protocols  
  
Try it

Messages

### { "audio": { "data": "data", "sample_rate": "16000", "encoding": "audio/wav" } }Audio Translation Message

### { "type": "data", "data": { "metrics": { "audio_duration": 1.1, "processing_latency": 1.1 }, "request_id": "request_id", "transcript": "transcript" } }Translation

WebSocket channel for real-time speech to text streaming with English translation.

**Note:** This API Reference page is provided for informational purposes only. The Try It playground may not provide the best experience for streaming audio. For optimal streaming performance, please use the SDK or implement your own WebSocket client.

## HandshakeTry it

WSS

wss://api.sarvam.ai/speech-to-text-translate/ws

### Headers

Api-Subscription-KeystringRequired

API subscription key for authentication

### Query parameters

modelenumOptionalDefaults to `saaras:v2.5`

Model to be used for speech to text translation.

  * **saaras:v2.5** (default): Translation model that translates audio from any spoken Indic language to English. 
    * Example: Hindi audio → English text output



For the latest model (saaras:v3), use the `/speech-to-text` endpoint with `mode="translate"`.

Allowed values:saaras:v2.5

sample_rateenumOptionalDefaults to `16000`

Audio sample rate for the WebSocket connection. When specified as a connection parameter, only 16kHz and 8kHz are supported. 8kHz is only available via this connection parameter. If not specified, defaults to 16kHz.

Allowed values:160008000

high_vad_sensitivityenumOptional

Enable high VAD (Voice Activity Detection) sensitivity

Allowed values:truefalse

positive_speech_thresholdstringOptionalDefaults to `0.7`

VAD probability threshold (0.0–1.0) above which a frame is considered speech. Overrides the server default when provided.

negative_speech_thresholdstringOptionalDefaults to `0.45`

VAD probability threshold (0.0–1.0) below which a frame is considered silence. Overrides the server default (or the high_vad_sensitivity preset) when provided.

min_speech_framesstringOptionalDefaults to `2`

Minimum number of consecutive speech frames required to start a speech segment. Overrides the server default when provided. 

first_turn_min_speech_framesstringOptionalDefaults to `8`

Minimum speech frames required specifically for the first user turn. Overrides the server default when provided. 

negative_frames_countstringOptionalDefaults to `18`

Number of negative (silence) frames needed within the window to end a speech segment. Overrides the server default (or the high_vad_sensitivity preset) when provided.

negative_frames_windowstringOptionalDefaults to `24`

Sliding window size (in frames) over which negative frames are counted. Overrides the server default (or the high_vad_sensitivity preset) when provided.

start_speech_volume_thresholdstringOptional

Volume level (dB) below which audio is considered too quiet to be speech. When not provided, no volume-based filtering is applied.

interrupt_min_speech_framesstringOptionalDefaults to `2`

Minimum speech frames required to register a barge-in / interruption. Overrides the server default when provided.

pre_speech_pad_framesstringOptionalDefaults to `9`

Number of audio frames to prepend before the detected speech onset, ensuring the beginning of speech is not clipped. Overrides the server default when provided. 

num_initial_ignored_framesstringOptionalDefaults to `0`

Number of leading audio frames to skip entirely at connection start. Useful for discarding connection setup noise. Overrides the server default when provided. 

vad_signalsenumOptional

Enable VAD signals in response

Allowed values:truefalse

flush_signalenumOptional

Signal to flush the audio buffer and finalize transcription and translation

Allowed values:truefalse

input_audio_codecenumOptional

Audio codec/format of the input stream. Use this when sending raw PCM audio. Supported values: wav, pcm_s16le, pcm_l16, pcm_raw.

Allowed values:wavpcm_s16lepcm_l16pcm_raw

### Send

Audio Translation MessageobjectRequired

Send audio data for real-time speech to text streaming with translation

Show 1 property

OR

Translation Config MessageobjectRequired

Send configuration for speech to text streaming with translation

Show 2 properties

OR

Speech Translate Flush SignalobjectRequired

Send signal to flush audio buffer and finalize transcription and translation

Show 1 property

### Receive

TranslationobjectRequired

Receive real-time transcription and translation results from the WebSocket

Show 2 properties

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate)[Batch - Initiate JobNext](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/initiate)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * API Reference

    * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
    * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
    * [Beta APIs and Models](https://docs.sarvam.ai/api-reference/beta-apis)
    * [Meta Prompt Guide](https://docs.sarvam.ai/api-reference/metaprompt)
  * APIs

    * Speech to Text

    * Text to Speech

    * Instant Voice CloningBeta

    * Pronunciation Dictionary

    * Text Processing

    * Chat Completion

    * Responses API

    * Content Studio - Dubbing

    * Document Translation

    * Document Intelligence

    * Legacy
      * Speech to Text

      * Speech to Text Translate
        * [POSTREST](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate)
        * [WSSWebSocket](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate/ws)
        * [POSTBatch - Initiate Job](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/initiate)
        * [POSTBatch - Upload Files](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/upload)
        * [POSTBatch - Start Job](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/start)
        * [GETBatch - Get Status](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/status)
        * [POSTBatch - Download Results](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/download)

      * Document Intelligence

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


