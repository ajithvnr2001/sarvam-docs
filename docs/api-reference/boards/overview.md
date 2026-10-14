---
url: https://docs.sarvam.ai/api-reference/boards/overview/
title: Boards API overview | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:37.870884+00:00
---

# Boards API overview | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/boards/overview/

Skip to navigation

On this page

  * Base URL
  * Rate limits
  * How the pieces fit together
  * Errors
  * What this API does not do
  * Next



Scroll to top

[Voice Agents](https://docs.sarvam.ai/api-reference/conversations)[Boards](https://docs.sarvam.ai/api-reference/boards/overview)

# Boards API overview

Create, edit, and run analytics boards over REST — the same boards you build under Monitor.

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/boards/overview.md "View this page as plain text")|More actions

This page is for API Reference.

A **board** is a custom analytics dashboard: a set of SQL-backed widgets, grouped into tabs, parameterised by filters your team can change without editing the query. This API does everything the dashboard does — discover the schema, develop a query, save it as a widget, run it, and schedule recurring delivery of the result.

For the dashboard walkthrough of the same concepts, see [Boards](https://docs.sarvam.ai/voice-agents/monitor/boards) under Monitor.

## Base URL
    
    
    https://apps.sarvam.ai/api/analytics/v1/{org_id}/{workspace_id}

Boards are **workspace-scoped** : board paths carry no `app_id`, and a board can query across every agent in the workspace.

Requests are authenticated with your API key, as everywhere else in the Voice Agents API — see [Introduction](https://docs.sarvam.ai/voice-agents/api/introduction).

## Rate limits

Four limits apply, and a request must satisfy every one that covers it: a per-key limit on every boards endpoint, plus a per-organization limit on each of the three endpoints that run queries.

Limit| Scope| Applies to  
---|---|---  
**Configured per organization**|  Per API key| Every boards endpoint  
**20 requests / minute**|  Per organization| `POST /query-preview`  
**20 requests / minute**|  Per organization| `POST /widgets/{widget_id}/run`  
**50 requests / minute**|  Per organization| `POST /tabs/{tab_id}/run`  
  
The per-organization limits are shared across every key and every user in the org — a colleague running queries in the dashboard consumes the same budget as your integration.

Exceeding any of them returns `429` with a `Retry-After` header giving the wait in seconds:
    
    
    HTTP/1.1 429 Too Many Requests
    
    Retry-After: 60
    
    { "detail": "Rate limit exceeded. Please wait before making more requests." }

Honour `Retry-After` rather than retrying immediately, and back off exponentially if you see repeated `429`s. If your workload needs more headroom, higher limits can be provisioned per organization — contact Sarvam support.

## How the pieces fit together

[1](https://docs.sarvam.ai/api-reference/boards/overview#discover-the-schema)

### Discover the schema

[Get query schema](https://docs.sarvam.ai/voice-agents/api/boards/query/schema) returns the tables and columns available to board SQL, with their types. Start here — it is the authoritative list, and querying anything outside it fails.

[2](https://docs.sarvam.ai/api-reference/boards/overview#develop-the-query)

### Develop the query

[Preview query](https://docs.sarvam.ai/voice-agents/api/boards/query/preview) runs ad-hoc SQL and returns rows without saving anything.

[3](https://docs.sarvam.ai/api-reference/boards/overview#save-it-as-a-widget)

### Save it as a widget

[Create board](https://docs.sarvam.ai/voice-agents/api/boards/create), then [Create widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/create) with your SQL, a visualization type, and the filters its `{{tokens}}` declare.

[4](https://docs.sarvam.ai/api-reference/boards/overview#run-it)

### Run it

[Run widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/run) for one result, or [Run tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/run) for every widget on a tab in a single call.

[5](https://docs.sarvam.ai/api-reference/boards/overview#have-it-delivered)

### Have it delivered

[Create notification rule](https://docs.sarvam.ai/voice-agents/api/boards/notifications/create) emails or Slacks a widget’s result on a cron schedule.

Filters are never created directly — that is why [List filters](https://docs.sarvam.ai/voice-agents/api/boards/filters/list) and [Update filter](https://docs.sarvam.ai/voice-agents/api/boards/filters/update) exist but “create filter” does not. A filter comes into being when a `{{token}}` appears in a widget’s SQL, and the board’s filter set is the union of the tokens across its widgets. See [Writing board SQL](https://docs.sarvam.ai/voice-agents/api/boards/sql#filter-tokens).

## Errors

Every error carries a `detail` field. For most failures it is a message string:
    
    
    { "detail": "Dashboard 0b7f2c9a-5e41-4d2a-9f3b-8c1d6e7a0b52 not found" }

Not-found messages call boards _dashboards_ , and name the missing tab, widget, filter, or rule the same way.

For SQL and query-execution failures it is an object with a machine-readable `code`, so you can branch on the cause rather than parsing prose:
    
    
    { "detail": { "code": "FORBIDDEN_TABLE", "message": "Table `users` is not available." } }

Request validation failures — a malformed UUID in the path, or a field outside its limits — return `422` with `detail` as a **list** of errors. The run endpoints also use `422` for `CLICKHOUSE_ERROR`, where `detail` is an object, so check whether `detail` is a list before reading `code`.

The full code table is on [Writing board SQL](https://docs.sarvam.ai/voice-agents/api/boards/sql).

## What this API does not do

These are deliberate, not gaps to work around:

  * **No deletion.** There are no `DELETE` routes. Boards, tabs, widgets, and notification rules are created and edited through the API but removed only in the dashboard.
  * **No CSV export.** Widget downloads are a dashboard feature. Read results as JSON from the run endpoints.
  * **No whole-board run.** The tab is the unit — call [Run tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/run) once per tab.
  * **No AI query generation.** Generating SQL from a plain-language prompt is dashboard-only.



## Next

[Writing board SQLWhich tables you can query, filter tokens, and every error code.](https://docs.sarvam.ai/voice-agents/api/boards/sql)[Best practicesChoosing between preview, widget run, and tab run — plus caching and polling.](https://docs.sarvam.ai/voice-agents/api/boards/best-practices)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/analytics/transcripts)[Writing board SQLThe dialect, the tables you can reach, filter tokens, and what each rejection means.Next](https://docs.sarvam.ai/api-reference/boards/sql)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


