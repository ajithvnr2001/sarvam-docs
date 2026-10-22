---
url: https://docs.sarvam.ai/api-reference/text-to-speech/stream/
title: WebSocket | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-22T06:32:49.287124+00:00
---

# WebSocket | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/text-to-speech/stream/

Skip to navigation

This page is for API Reference.

[APIs](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Text to Speech](https://docs.sarvam.ai/api-reference/text-to-speech/convert)

# WebSocket

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/text-to-speech/stream.md "View this page as plain text")|More actions

WSS

wss://api.sarvam.ai/text-to-speech/ws

Handshake

URL| wss://api.sarvam.ai/text-to-speech/ws  
---|---  
Method| GET  
Status| 101 Switching Protocols  
  
Try it

Messages

### { "type": "config", "data": { "language_code": "bn-IN", "speaker": "anushka" } }Configure Connection

### { "type": "audio", "data": { "content_type": "content_type", "audio": "audio" } }Audio Output

WebSocket channel for real-time TTS synthesis.

**Note:** This API Reference page is provided for informational purposes only. The Try It playground may not provide the best experience for streaming audio. For optimal streaming performance, please use the SDK or implement your own WebSocket client.

**Model-Specific Notes:**

  * **bulbul:v2:** Supports pitch, loudness, pace (0.3-3.0). Default sample rate: 22050 Hz.
  * **bulbul:v3:** Does NOT support pitch/loudness. Pace range: 0.5-2.0. Supports temperature parameter (0.01–1.0). Default sample rate: 22050 Hz when `speech_sample_rate` is omitted. Preprocessing is always enabled.
  * **bulbul:v4-flash:** Same request/response contract as bulbul:v3, with 200+ persona voices. Default sample rate: 22050 Hz when omitted.



## HandshakeTry it

WSS

wss://api.sarvam.ai/text-to-speech/ws

### Headers

Api-Subscription-KeystringRequired

API subscription key for authentication

### Query parameters

modelenumOptionalDefaults to `bulbul:v2`

Text to speech model to use.

  * **bulbul:v2** (default): Standard TTS model with pitch/loudness support
  * **bulbul:v4-flash** : Latest model, recommended for new integrations — same contract as bulbul:v3, with a 200+ voice persona catalog
  * **bulbul:v3** : Stable model (API default when omitted) with temperature control (no pitch/loudness)



Allowed values:bulbul:v2bulbul:v3bulbul:v4-flash

send_completion_eventenumOptionalDefaults to `true`

Enable completion event notifications when TTS generation finishes. When set to true, an event message will be sent when the final audio chunk has been generated.

Allowed values:truefalse

### Send

Configure ConnectionobjectRequired

Send initial configuration for text-to-speech streaming

Show 2 properties

OR

Send TextobjectRequired

Send text chunk for speech synthesis

Show 2 properties

OR

Flush SignalobjectRequired

Send signal to end text streaming.

Show 1 property

OR

Ping SignalobjectRequired

Send ping signal to keep the TTS WebSocket connection alive.

Show 1 property

### Receive

Audio OutputobjectRequired

Receive audio chunks from the TTS WebSocket.

Show 2 properties

OR

Event NotificationobjectRequired

Receive completion event notifications from the TTS WebSocket (if send_completion_event is enabled)

Show 2 properties

OR

Error ResponseobjectRequired

Receive error messages from the TTS WebSocket

Show 2 properties

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/text-to-speech/convert-stream)[Create VoiceNext](https://docs.sarvam.ai/api-reference/voice-cloning/create-voice)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


