---
url: https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/realtime/ws/
title: Realtime Streaming | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-17T14:23:24.318142+00:00
---

# Realtime Streaming | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/realtime/ws/

Skip to navigation

This page is for API Reference.

[APIs](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Speech to Text](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)

# Realtime Streaming

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/realtime/ws.md "View this page as plain text")|More actions

WSS

wss://api.sarvam.ai/speech-to-text-realtime/ws

Handshake

URL| wss://api.sarvam.ai/speech-to-text-realtime/ws  
---|---  
Method| GET  
Status| 101 Switching Protocols  
  
Try it

Messages

### { "event": "audio_input", "audio": "audio" }Realtime Audio Input

### { "event": "session.begin", "request_id": "request_id" }Realtime Session Begin

WebSocket channel for real-time speech to text streaming powered by the `saaras:v3-realtime` (default) or `saaras:v4` model.

**Authentication:** Pass your API subscription key via the `API-SUBSCRIPTION-KEY` header, or (in browsers) via the WebSocket subprotocol `api-subscription-key.<key>` — the server echoes the subprotocol back.

**Note:** This API Reference page is provided for informational purposes only. The Try It playground may not provide the best experience for streaming audio. For optimal streaming performance, please use the SDK or implement your own WebSocket client.

## HandshakeTry it

WSS

wss://api.sarvam.ai/speech-to-text-realtime/ws

### Headers

Api-Subscription-KeystringRequired

API subscription key for authentication

### Query parameters

language_codeenumRequired

BCP-47 language code of the input audio. **Required.**

**Supported languages (saaras:v3-realtime and saaras:v4):**

  * `auto`: Adaptive automatic language detection
  * `en-IN`: English
  * `hi-IN`: Hindi
  * `bn-IN`: Bengali
  * `kn-IN`: Kannada
  * `ml-IN`: Malayalam
  * `mr-IN`: Marathi
  * `or-IN`: Odia
  * `pa-IN`: Punjabi
  * `ta-IN`: Tamil
  * `te-IN`: Telugu
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

modelenumOptionalDefaults to `saaras:v3-realtime`

Speech-to-text model for this endpoint. `saaras:v3-realtime` (default) or `saaras:v4`.

Allowed values:saaras:v3-realtimesaaras:v4

stream_typeenumOptionalDefaults to `balanced`

Controls audio chunking and latency behaviour.

  * **fast** : Partials at low latency.
  * **balanced** (default): Partials with better accuracy.
  * **simulated** : No partials.



Allowed values:fastbalancedsimulated

modeenumOptionalDefaults to `transcribe`

Task applied on the final transcript, not on partial transcripts. Streaming partials are always straight transcription regardless of this value.

  * **transcribe** (default): Standard transcription in the source language script.
  * **translate** : Translation to English.
  * **verbatim** : Exact transcription in the original script (includes disfluencies).
  * **translit** : Transliteration to Latin script.
  * **codemix** : Code-mixed output (native + English).



Allowed values:transcribetranslateverbatimtranslitcodemix

promptstringOptional

Optional context/terminology hint to bias decoding. Applied on the final transcript.

keytermsstringOptional

JSON-encoded array of up to 50 domain-specific terms (names, places, brands, technical terms) to bias recognition toward, e.g. `keyterms=["Sarvam","New Delhi","Vistaar"]`. Each keyterm can contain up to 64 characters. Applied to the transcripts for the whole session; **only supported with`model="saaras:v4"`**. Do not use the older `keyterm` or `hotwords` fields.

endpointingenumOptionalDefaults to `vad`

Turn detection strategy.

  * **vad** (default): Voice Activity Detection automatically detects turn boundaries.
  * **manual** : The client delimits turns with `speech_start` / `speech_end` events.



Allowed values:vadmanual

encodingenumOptionalDefaults to `linear16`

Audio encoding of the input stream. **Mono only.**

Allowed values:linear16linear32mulawalaw

sample_rateenumOptionalDefaults to `16000`

Audio sample rate in Hz. Must match the actual audio.

**Accepted values:**

  * `8000`
  * `16000` (default)



Any other value closes the connection with code `4000`.

Allowed values:160008000

return_timestampsenumOptionalDefaults to `false`

When `true`, adds segment-level `start_s` / `end_s` audio-time offsets to `transcript.final`.

Allowed values:truefalse

thresholdstringOptionalDefaults to `0.3`

Speech-detection sensitivity (0.0–1.0; higher = needs louder/clearer speech). Only applies when `endpointing=vad`.

prefix_padding_msstringOptionalDefaults to `300`

Audio (ms, ≥0) included before the detected speech onset. Only applies when `endpointing=vad`.

silence_duration_msstringOptionalDefaults to `500`

Silence (ms, ≥0) after speech that marks end-of-turn. Only applies when `endpointing=vad`.

min_speech_duration_msstringOptionalDefaults to `250`

Minimum speech duration (ms, ≥0) for a valid utterance. Only applies when `endpointing=vad`.

### Send

Realtime Audio InputobjectRequired

Send an audio chunk for real-time transcription (saaras:v3-realtime, saaras:v4)

Show 2 properties

OR

Realtime Speech StartobjectRequired

Signal the start of an utterance (endpointing=manual only)

Show 1 property

OR

Realtime Speech EndobjectRequired

Signal the end of an utterance (endpointing=manual only)

Show 1 property

OR

Realtime FlushobjectRequired

Show 1 property

OR

Realtime Config UpdateobjectRequired

Update session config mid-stream

Show 9 properties

OR

Realtime End SessionobjectRequired

Gracefully end the realtime session

Show 1 property

OR

Realtime PingobjectRequired

Send a keepalive ping to the realtime WebSocket

Show 1 property

### Receive

Realtime Session BeginobjectRequired

Receive the session.begin event with the resolved session config

Show 3 properties

OR

Realtime VAD EventsobjectRequired

Receive VAD speech start/end events (endpointing=vad only)

Show 3 properties

OR

Realtime VAD EventsobjectRequired

Receive VAD speech start/end events (endpointing=vad only)

Show 3 properties

OR

Realtime Partial TranscriptobjectRequired

Receive streaming partial transcripts during an utterance

Show 4 properties

OR

Realtime Final TranscriptobjectRequired

Receive the final transcript for a completed utterance

Show 7 properties

OR

Realtime Config UpdatedobjectRequired

Receive the config.updated acknowledgement after a config.update

Show 2 properties

OR

Realtime PongobjectRequired

Receive the pong response to a client ping

Show 1 property

OR

Realtime Session EndobjectRequired

Receive the session.end summary when the session closes

Show 5 properties

OR

Realtime ErrorobjectRequired

Receive non-fatal or fatal error notifications

Show 5 properties

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/download)[RESTNext](https://docs.sarvam.ai/api-reference/text-to-speech/convert)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


