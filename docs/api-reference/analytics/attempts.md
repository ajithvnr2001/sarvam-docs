---
url: https://docs.sarvam.ai/api-reference/analytics/attempts/
title: Get attempts | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:13:43.246758+00:00
---

# Get attempts | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/analytics/attempts/

Skip to navigation

This page is for API Reference.

[Voice Agents](https://docs.sarvam.ai/api-reference/conversations)[Analytics](https://docs.sarvam.ai/api-reference/analytics/attempts)

# Get attempts

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/analytics/attempts.md "View this page as plain text")|More actions

GET

https://apps.sarvam.ai/api/analytics/v1/:org_id/:workspace_id/:app_id/attempts

GET

/api/analytics/v1/:org_id/:workspace_id/:app_id/attempts

Python
    
    
    import requests
    
    url = "https://apps.sarvam.ai/api/analytics/v1/acme-corp-7c2e9f/support-ws-4b1d8a/support-bot-3f9a1c2e-7b4d/attempts"
    
    querystring = {"end_datetime":"2026-10-07T23:59:59+05:30","filter_conditions":"[{\"field\":\"channel_direction\",\"operator\":\"equals\",\"value\":\"outbound\"},{\"field\":\"duration_in_seconds\",\"operator\":\"greater_than\",\"value\":\"30\"},{\"field\":\"agent_variables.loan_status\",\"operator\":\"equals\",\"value\":\"overdue\"},{\"field\":\"agent_variables.loan_status\",\"operator\":\"equals\",\"value\":\"due_today\"}]","start_datetime":"2026-10-01T00:00:00+05:30"}
    
    headers = {"X-API-Key": "<your-api-key>"}
    
    response = requests.get(url, headers=headers, params=querystring)
    
    print(response.json())

Try it

200First page
    
    
    {
    
      "items": [
    
        {
    
          "attempt_id": "6d3a9e2f-1b7c-4c58-9f04-8e2b5d7a1c93",
    
          "interaction_id": "20261007/9f1c2a7e-4b3d-4e8a-a1f0-6c2d9b7e5a14",
    
          "user_identifier": "LN-2026-004817",
    
          "user_contact": "+919876543210",
    
          "user_contact_masked": "+91******3210",
    
          "user_contact_hashed": "4f9a2c7e1b8d3f60a5c4e2b19d7f8a3c6e1b5d9f2a7c4e8b0d3f6a1c9e5b2d7f",
    
          "connectivity_status": "connected",
    
          "failure_reason": "NO_FAILURE_REASON",
    
          "ended_by": "USER_ENDS",
    
          "next_action_status": "UNKNOWN",
    
          "duration_in_seconds": 142.6,
    
          "start_datetime": "2026-10-07T05:12:08",
    
          "end_datetime": "2026-10-07T05:14:31",
    
          "attempted_at": "2026-10-07T05:11:57",
    
          "language_name": "Hindi",
    
          "num_messages": 14,
    
          "average_agent_response_time_in_seconds": 1.18,
    
          "average_user_response_time_in_seconds": 2.46,
    
          "channel_type": "v2v",
    
          "channel_direction": "outbound",
    
          "channel_protocol": "websocket",
    
          "retry_attempt": 1,
    
          "server_retry_attempt": 0,
    
          "campaign_id": "emi-reminder-oct-2026",
    
          "cohort_id": "cohort-0921-overdue",
    
          "is_debug_call": 0,
    
          "has_log_issues": 0,
    
          "audio_url": "https://agents.sarvam.ai/media?org_id=acme-corp-7c2e9f&workspace_id=support-ws-4b1d8a&app_id=support-bot-3f9a1c2e-7b4d&interaction_id=20261007/9f1c2a7e-4b3d-4e8a-a1f0-6c2d9b7e5a14&audio_hash=merged_audio",
    
          "agent_variables": {
    
            "customer_name": "Priya Sharma",
    
            "emi_amount": "4500",
    
            "loan_status": "overdue",
    
            "promised_payment_date": "2026-10-10"
    
          },
    
          "channel_provider": null
    
        }
    
      ],
    
      "total": 37,
    
      "limit": 1,
    
      "offset": 0,
    
      "next_page_uri": "?start_datetime=2026-10-01T00%3A00%3A00%2B05%3A30&end_datetime=2026-10-07T23%3A59%3A59%2B05%3A30&limit=1&offset=1",
    
      "prev_page_uri": ""
    
    }

Returns a page of attempts for one agent in a date range. An attempt is one try at reaching a user, connected or not — use it for connection rates, failures and retries. A connected attempt links to its conversation through `interaction_id`.

Responses are cached for 60 seconds. Each item includes `user_contact`, the user’s **full, unmasked** phone number or email. Treat responses as personal data.

### Path parameters

org_idstringRequired

Organization ID.

workspace_idstringRequired

Workspace ID.

app_idstringRequired

Agent ID. Copy it from the agent’s **···** menu in the dashboard (**Copy agent ID**).

### Headers

X-API-KeystringRequired

Your workspace API key.

### Query parameters

sort_byenumOptionalDefaults to `attempt_id`

Field to sort by. Default `attempt_id`. Unknown values return `422`.

Show 7 enum values

sort_orderenumOptionalDefaults to `asc`

`asc` (default) or `desc`. Case-insensitive.

Allowed values:ascdesc

start_datetimedatetimeRequired

Start of the range, inclusive. ISO 8601 with an offset, e.g. `2026-10-01T00:00:00+05:30` (encode `+` as `%2B`). Without an offset, UTC is assumed.

end_datetimedatetimeRequired

End of the range, inclusive. Same format as `start_datetime`, and must be later than it.

limitintegerOptional`1-1000`Defaults to `20`

Items per page, 1–1000. Default `20`.

offsetintegerOptional`>=0`Defaults to `0`

Items to skip. Default `0`. To page, you can follow `next_page_uri` instead.

filter_conditionsstringOptional

URL-encoded JSON array of `{field, operator, value}` conditions. `value` is always a string, even for numbers. Conditions on the same field are ORed; on different fields, ANDed.
    
    
    [{"field": "duration_in_seconds", "operator": "greater_than", "value": "30"}]
    

Operators and filterable fields are listed under [Filtering](https://docs.sarvam.ai/voice-agents/api/analytics/overview#filtering).

### Response

A page of attempts.

itemslist of objects

The attempts on this page.

Show 30 properties

totalinteger

Total number of attempts matching the request, across all pages.

limitinteger

The `limit` applied to this page.

offsetinteger

The `offset` applied to this page.

next_page_uristring

Query string for the next page, e.g. `?start_datetime=...&limit=20&offset=20`. Append it to the endpoint path. `""` when there is no next page.

prev_page_uristring

Query string for the previous page. `""` when there is none.

### Errors

400

Bad Request Error

401

Unauthorized Error

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

[Previous](https://docs.sarvam.ai/api-reference/instant-outbound/webhook-payload)[Get interactionsNext](https://docs.sarvam.ai/api-reference/analytics/interactions)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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

    * Instant Outbound

    * Analytics
      * [GETGet attempts](https://docs.sarvam.ai/api-reference/analytics/attempts)
      * [GETGet interactions](https://docs.sarvam.ai/api-reference/analytics/interactions)
      * [GETGet recordings](https://docs.sarvam.ai/api-reference/analytics/recordings)
      * [GETGet transcripts](https://docs.sarvam.ai/api-reference/analytics/transcripts)

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


