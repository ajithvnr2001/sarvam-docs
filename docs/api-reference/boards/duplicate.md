---
url: https://docs.sarvam.ai/api-reference/boards/duplicate/
title: Duplicate board | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:13:44.355442+00:00
---

# Duplicate board | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/boards/duplicate/

Skip to navigation

This page is for API Reference.

[Voice Agents](https://docs.sarvam.ai/api-reference/conversations)[Boards](https://docs.sarvam.ai/api-reference/boards/overview)

# Duplicate board

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/boards/duplicate.md "View this page as plain text")|More actions

POST

https://apps.sarvam.ai/api/analytics/v1/:org_id/:workspace_id/boards/:board_id/duplicate

Copy with a new name and tagCopy with the default name, inheriting the tag

POST

/api/analytics/v1/:org_id/:workspace_id/boards/:board_id/duplicate

Python
    
    
    import requests
    
    url = "https://apps.sarvam.ai/api/analytics/v1/org_id/workspace_id/boards/0b7f2c9a-5e41-4d2a-9f3b-8c1d6e7a0b52/duplicate"
    
    payload = {
    
        "name": "Campaign Overview (Q4)",
    
        "tag": "Quarterly reporting"
    
    }
    
    headers = {
    
        "X-API-Key": "<your-api-key>",
    
        "Content-Type": "application/json"
    
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(response.json())

Try it

201Copy with a new name and tag
    
    
    {
    
      "id": "5c2e9f14-8a3b-4d70-b6e1-0f9d4a7c2e83",
    
      "name": "Campaign Overview (Q4)",
    
      "created_by": {
    
        "type": "api_key",
    
        "id": "sk_live_a1b2c3"
    
      },
    
      "created_at": "2026-09-15T06:02:47Z",
    
      "updated_by": {
    
        "type": "api_key",
    
        "id": "sk_live_a1b2c3"
    
      },
    
      "updated_at": "2026-09-15T06:02:47Z",
    
      "tabs": [
    
        {
    
          "id": "b2d8f0a6-4e17-4c93-a5b1-7d2e6f9c0a34",
    
          "name": "Connectivity",
    
          "position": 0,
    
          "widgets": [
    
            {
    
              "id": "d6a1c3e8-9f42-4b05-8e7d-2a4c6b1f3e90",
    
              "board_id": "5c2e9f14-8a3b-4d70-b6e1-0f9d4a7c2e83",
    
              "name": "Daily connected calls",
    
              "sql": "SELECT\n  toDate(effective_datetime) AS day,\n  countIf(v2v_connectivity_status = 'connected') AS connected,\n  count() AS total\nFROM EngagementFactsBoardsView\nWHERE effective_datetime >= {{start_date}}\n  [[AND app_id = {{agent_id}}]]\nGROUP BY day\nORDER BY day",
    
              "viz_type": "line",
    
              "viz_config": {
    
                "x_axis": "day",
    
                "y_axis": [
    
                  "connected",
    
                  "total"
    
                ]
    
              },
    
              "created_by": {
    
                "type": "api_key",
    
                "id": "sk_live_a1b2c3"
    
              },
    
              "created_at": "2026-09-15T06:02:47Z",
    
              "updated_by": {
    
                "type": "api_key",
    
                "id": "sk_live_a1b2c3"
    
              },
    
              "updated_at": "2026-09-15T06:02:47Z"
    
            },
    
            {
    
              "id": "08e5b7d2-6c19-4fa3-b8d0-5e1a9c7f2b64",
    
              "board_id": "5c2e9f14-8a3b-4d70-b6e1-0f9d4a7c2e83",
    
              "name": "Calls by language",
    
              "sql": "SELECT language_name, count() AS calls\nFROM EngagementFactsBoardsView\nWHERE effective_datetime >= {{start_date}}\nGROUP BY language_name\nORDER BY calls DESC",
    
              "viz_type": "bar",
    
              "viz_config": {
    
                "x_axis": "language_name",
    
                "y_axis": [
    
                  "calls"
    
                ]
    
              },
    
              "created_by": {
    
                "type": "api_key",
    
                "id": "sk_live_a1b2c3"
    
              },
    
              "created_at": "2026-09-15T06:02:47Z",
    
              "updated_by": {
    
                "type": "api_key",
    
                "id": "sk_live_a1b2c3"
    
              },
    
              "updated_at": "2026-09-15T06:02:47Z"
    
            }
    
          ]
    
        }
    
      ],
    
      "filters": [
    
        {
    
          "id": "c4f7a2e9-3b58-4d16-9a0c-8e2b5d7f1a43",
    
          "internal_name": "start_date",
    
          "display_label": "Start date",
    
          "filter_type": "date",
    
          "is_required": true,
    
          "default_value": "2026-09-01T00:00:00+05:30",
    
          "dropdown_options": null
    
        },
    
        {
    
          "id": "61b9d4f3-7a2e-4c85-b0d6-3f8e1a5c9d27",
    
          "internal_name": "agent_id",
    
          "display_label": "Agent",
    
          "filter_type": "string",
    
          "is_required": false,
    
          "default_value": null,
    
          "dropdown_options": null
    
        }
    
      ],
    
      "tag": "Quarterly reporting"
    
    }

Deep-copies the board, with new IDs for the board and everything on it, and returns the copy in full, in the same shape as a board read. The copy is named `<source name> (copy)` and inherits the source’s tag unless you send `name` or `tag`.

### Path parameters

org_idstringRequired

Organization ID

workspace_idstringRequired

Workspace ID

board_idstringRequired`format: "uuid"`

Board ID, as returned in `id` by Create board or List boards. Must be a UUID; anything else is rejected with 422.

### Headers

X-API-KeystringRequired

Your workspace API key.

### Request

This endpoint expects a nullable object.

namestring or nullOptional`4-80 characters`

Name for the copy, 4 to 80 characters. Defaults to `<source name> (copy)`.

tagstring or nullOptional`4-80 characters`

Tag for the copy, 4 to 80 characters. Omit to inherit the source board’s tag; send null to leave the copy untagged.

### Response

Successful Response

idstring`format: "uuid"`

Board identifier, used as `{board_id}` in every nested route

namestring

Board display name

created_byobject

Actor that created the board

Show 2 properties

created_atdatetime

Creation time, UTC, RFC 3339

updated_byobject

Actor that last changed the board or anything on it

Show 2 properties

updated_atdatetime

Last change time, UTC, RFC 3339

tabslist of objects

The board's tabs in position order, each with its widgets nested

Show 4 properties

filterslist of objects

Every filter token declared by this board's widgets, in display order

Show 7 properties

tagstring or nullOptional

The board's grouping tag, or null when untagged

### Errors

400

Bad Request Error

401

Unauthorized Error

403

Forbidden Error

404

Not Found Error

422

Unprocessable Entity Error

429

Too Many Requests Error

500

Internal Server Error

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/boards/update)[Create tabNext](https://docs.sarvam.ai/api-reference/boards/tabs/create)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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

    * Boards
      * [Overview](https://docs.sarvam.ai/api-reference/boards/overview)
      * [Writing board SQL](https://docs.sarvam.ai/api-reference/boards/sql)
      * [Best practices](https://docs.sarvam.ai/api-reference/boards/best-practices)
      * [GETList boards](https://docs.sarvam.ai/api-reference/boards/list)
      * [POSTCreate board](https://docs.sarvam.ai/api-reference/boards/create)
      * [GETGet board](https://docs.sarvam.ai/api-reference/boards/get)
      * [PATCHUpdate board](https://docs.sarvam.ai/api-reference/boards/update)
      * [POSTDuplicate board](https://docs.sarvam.ai/api-reference/boards/duplicate)
      * Tabs

      * Widgets

      * Filters

      * Notifications

      * Query

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


