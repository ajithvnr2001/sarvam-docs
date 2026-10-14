---
url: https://docs.sarvam.ai/api-reference/campaigns/webhook-payload/
title: Campaigns webhook payload | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:38.208066+00:00
---

# Campaigns webhook payload | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/campaigns/webhook-payload/

Skip to navigation

On this page

  * Payload schema
  * Examples
  * Connected attempt
  * Not connected attempt



Scroll to top

[Voice Agents](https://docs.sarvam.ai/api-reference/conversations)[Campaigns](https://docs.sarvam.ai/api-reference/campaigns/create)

# Campaigns webhook payload

The payload Sarvam POSTs to your webhook after every campaign call attempt.

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/campaigns/webhook-payload.md "View this page as plain text")|More actions

This page is for API Reference.

After each call attempt completes — whether or not it connected — Sarvam sends a `POST` request to your webhook URL with the attempt result. Configure the webhook URL in the campaign’s `app_config.webhook_config`.

## Payload schema

Field| Type| Description  
---|---|---  
`app_id`| string (required)| ID of the agent.  
`app_version`| integer (required)| Version of the agent.  
`attempt_id`| string (required)| Unique identifier for this call attempt.  
`campaign_id`| string (required)| Campaign this attempt belongs to.  
`cohort_id`| string (required)| Cohort this attempt belongs to.  
`completion_status`| string (required)| Outcome of the call. One of `completed`, `partial`, `failed`.  
`connectivity_status`| string | null| Whether the call connected. One of `connected`, `busy`, `no_answer`, `failed`, or `null`.  
`next_action_status`| string | null| Next action for the retry engine (`retry`, `reschedule`, `business_retry`, `short_duration_retry`, `provider_error_retry`, `internal_error_retry`), or `null` if terminal.  
`failure_reason`| string | null| Reason for failure, if applicable.  
`user_identifier`| string (required)| Unique identifier for the user (from cohort transformation config).  
`user_phone_number`| string (required)| Phone number of the user in E.164 format.  
`agent_phone_number`| string | null| Phone number used by the agent for the call.  
`duration`| number | null| Call duration in seconds. `null` if the call did not connect.  
`interaction_id`| string | null| Unique interaction ID for retrieving transcripts and recordings. `null` if the call did not connect.  
`retry_attempt`| integer (required)| Which attempt this is (`0` = first attempt, `1` = first retry, and so on).  
`executed_at`| string | null| Timestamp when the call was executed (ISO 8601).  
`start_datetime`| string | null| Call start timestamp (ISO 8601 UTC). `null` if the call did not connect.  
`end_datetime`| string | null| Call end timestamp (ISO 8601 UTC). `null` if the call did not connect.  
`initial_agent_variables`| object | null| Agent variables passed to the call from the cohort.  
`final_agent_variables`| object | null| Agent variables at the end of the conversation. `null` if the call did not connect.  
`output_agent_variables`| object | null| Variables collected by the agent during the call. `null` if the call did not connect.  
`interaction_transcript`| array | null| Transcript of the conversation as a list of turns. Each turn has `role` (`"agent"` or `"user"`) and `en_text`. `null` if the call did not connect.  
`metadata`| object | null| Custom metadata from the webhook configuration.  
  
## Examples

### Connected attempt
    
    
    {
    
      "app_id": "my-agent-app",
    
      "app_version": 1,
    
      "attempt_id": "019d392a-4f5a-7db3-904a-6ecebb9aac96",
    
      "campaign_id": "welcome-campaign-2026",
    
      "cohort_id": "cohort-batch-01",
    
      "completion_status": "completed",
    
      "connectivity_status": "connected",
    
      "next_action_status": null,
    
      "failure_reason": null,
    
      "user_identifier": "user-1001",
    
      "user_phone_number": "+919876543210",
    
      "agent_phone_number": "+91804XXXXXXX",
    
      "duration": 42.5,
    
      "interaction_id": "20260329/a1b2c3d4-10:30:00-e5f6a7b8",
    
      "retry_attempt": 0,
    
      "executed_at": "2026-03-29T10:30:45+05:30",
    
      "start_datetime": "2026-03-29T05:00:32Z",
    
      "end_datetime": "2026-03-29T05:01:15Z",
    
      "initial_agent_variables": {
    
        "customer_name": "Rahul Kumar",
    
        "outstanding_amount": "1500"
    
      },
    
      "final_agent_variables": {
    
        "payment_confirmed": "yes",
    
        "sentiment": "positive"
    
      },
    
      "output_agent_variables": {
    
        "payment_confirmed": "yes"
    
      },
    
      "interaction_transcript": [
    
        { "role": "agent", "en_text": "Hello Rahul, I'm calling about your pending payment of 1500 rupees." },
    
        { "role": "user", "en_text": "Yes, I'll pay today." }
    
      ],
    
      "metadata": { "team": "collections" }
    
    }

### Not connected attempt
    
    
    {
    
      "app_id": "my-agent-app",
    
      "app_version": 1,
    
      "attempt_id": "019d392a-11c6-72bd-8eb7-c37e84bbd1f3",
    
      "campaign_id": "welcome-campaign-2026",
    
      "cohort_id": "cohort-batch-01",
    
      "completion_status": "failed",
    
      "connectivity_status": "failed",
    
      "next_action_status": "retry",
    
      "failure_reason": "TelephonyProvider: Rate Limit Exceeded",
    
      "user_identifier": "user-1002",
    
      "user_phone_number": "+919876543211",
    
      "agent_phone_number": "+91804XXXXXXX",
    
      "duration": null,
    
      "interaction_id": null,
    
      "retry_attempt": 1,
    
      "executed_at": "2026-03-29T10:40:26+05:30",
    
      "start_datetime": null,
    
      "end_datetime": null,
    
      "initial_agent_variables": {
    
        "customer_name": "Priya Sharma",
    
        "outstanding_amount": "2500"
    
      },
    
      "final_agent_variables": null,
    
      "output_agent_variables": null,
    
      "interaction_transcript": null,
    
      "metadata": { "team": "collections" }
    
    }

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/campaigns/update-status)[Upload cohortNext](https://docs.sarvam.ai/api-reference/campaigns/cohorts/upload)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [POSTCreate campaign](https://docs.sarvam.ai/api-reference/campaigns/create)
      * [GETList campaigns](https://docs.sarvam.ai/api-reference/campaigns/list)
      * [GETGet campaign](https://docs.sarvam.ai/api-reference/campaigns/get)
      * [PATCHUpdate campaign](https://docs.sarvam.ai/api-reference/campaigns/update)
      * [PUTUpdate status](https://docs.sarvam.ai/api-reference/campaigns/update-status)
      * [Webhook payload](https://docs.sarvam.ai/api-reference/campaigns/webhook-payload)
      * Cohorts

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


