---
url: https://docs.sarvam.ai/api-reference/boards/sql/
title: Writing board SQL | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:38.569122+00:00
---

# Writing board SQL | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/boards/sql/

Skip to navigation

On this page

  * Start from the schema
  * Read-only, single statement
  * Filter tokens
  * Declaring filters is optional
  * Query budget
  * Error codes
  * Next



Scroll to top

[Voice Agents](https://docs.sarvam.ai/api-reference/conversations)[Boards](https://docs.sarvam.ai/api-reference/boards/overview)

# Writing board SQL

The dialect, the tables you can reach, filter tokens, and what each rejection means.

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/boards/sql.md "View this page as plain text")|More actions

This page is for API Reference.

Every widget is one SQL query. Sarvam’s analytics store is ClickHouse — column-oriented and tuned for aggregation over large call datasets, so some functions and conventions differ from PostgreSQL or MySQL.

This page covers what the API enforces. For dialect patterns and worked query shapes, see [SQL best practices](https://docs.sarvam.ai/voice-agents/monitor/clickhouse-sql-best-practices).

## Start from the schema

Call [Get query schema](https://docs.sarvam.ai/voice-agents/api/boards/query/schema) before writing anything. It returns the tables available to **this** workspace with their columns and ClickHouse types:
    
    
    {
    
      "tables": [
    
        {
    
          "name": "EngagementFactsBoardsView",
    
          "columns": [
    
            { "name": "interaction_id", "type": "String" },
    
            { "name": "effective_datetime", "type": "DateTime" },
    
            { "name": "v2v_connectivity_status", "type": "LowCardinality(String)" },
    
            { "name": "language_name", "type": "LowCardinality(String)" },
    
            { "name": "audio_duration", "type": "Nullable(Float32)" }
    
          ]
    
        }
    
      ]
    
    }

Table names are **unqualified** — use them exactly as returned, with no database prefix. Referencing anything outside this catalog fails with `FORBIDDEN_TABLE`.

Do not write `org_id` or `workspace_id` predicates. Tenant scoping is applied server-side on every query and cannot be bypassed or opted out of. Adding your own scoping clause is at best redundant; results are additionally verified before they are returned, and a response that would cross tenants is refused with `TENANT_ISOLATION_BREACH`.

## Read-only, single statement

Widget SQL must be exactly one `SELECT`. CTEs, subqueries, joins, and unions are all fine as long as they only read.

These are rejected at save time, not at run time:

Rejected| Why  
---|---  
Anything other than `SELECT`| The surface is read-only  
Two statements separated by `;`| One statement per widget  
`SETTINGS`| Would override the tenancy, read-only, and timeout settings applied per query  
`FORMAT`, `INTO OUTFILE`| Would control the wire format or write to disk  
`LIMIT BY`| Not supported in widget SQL  
`LIMIT` with `OFFSET`| Use `row_limit` instead  
`LIMIT` that is not a positive integer literal| Must be a constant  
  
`SETTINGS`, `FORMAT`, and `INTO OUTFILE` are rejected anywhere in the statement, including inside a CTE, a subquery, or one branch of a union.

A plain `LIMIT n` is allowed and can narrow a result, but never widens it: on preview and widget runs it is clamped to 1000.

## Filter tokens

Tokens let one query serve many views without being rewritten.

Syntax| Meaning  
---|---  
`{{name}}`| **Required.** The run fails with `UNRESOLVED_TOKEN` if no value is supplied and the filter has no default.  
`[[ ... {{name}} ... ]]`| **Optional.** The whole bracketed clause is dropped when no value is supplied.  
      
    
    SELECT
    
      toDate(effective_datetime) AS day,
    
      countIf(v2v_connectivity_status = 'connected') AS connected,
    
      count() AS total
    
    FROM EngagementFactsBoardsView
    
    WHERE effective_datetime >= {{start_date}}
    
      [[AND app_id = {{agent_id}}]]
    
    GROUP BY day
    
    ORDER BY day

With no `agent_id` supplied, that query runs across every agent. With one, it narrows to that agent. `start_date` is required either way.

Two things worth knowing:

  * **Your SQL is validated twice** — once with every optional block kept and once with all of them removed. A query that only parses when a filter happens to be present is rejected when you save it, not at run time when the filter is absent. A dangling `WHERE` left by a removed block is the usual cause.
  * **`[[ ]]` is only special when it contains a token.** ClickHouse nested-array literals like `[[1,2],[3,4]]` pass through untouched.



### Declaring filters is optional

Writing the token into your SQL is enough. When you create or update a widget, every `{{token}}` in its SQL that the board does not already have a filter for gets one created automatically, labelled with the token name, typed `string`, with no default.

The `filters` array on [Create widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/create) exists only to give those filters better metadata up front:
    
    
    {
    
      "filters": [
    
        { "internal_name": "start_date", "display_label": "Start date", "filter_type": "date", "default_value": "2026-09-01T00:00:00+05:30" },
    
        { "internal_name": "agent_id", "display_label": "Agent", "filter_type": "string", "default_value": null }
    
      ]
    
    }

Send it when you want a readable label, a non-`string` type, a default value, or dropdown options — `filter_type` is one of `number`, `string`, `date`, or `dropdown`, and a `dropdown` must also carry `dropdown_options`. Omit it and you can set the same things later with [Update filter](https://docs.sarvam.ai/voice-agents/api/boards/filters/update). A token name (`internal_name`) must match `^[a-zA-Z_][a-zA-Z0-9_]*$` and be at most 64 characters.

Every value — a default or a run-time value — is sent as a string and parsed according to `filter_type`:

`filter_type`| Value format  
---|---  
`date`| A full ISO 8601 timestamp **with a timezone offset** , e.g. `2026-09-01T00:00:00+05:30`. A date-only value such as `2026-09-01` is rejected with `INVALID_FILTER_VALUE` (`date value must include a timezone offset`). The value is converted to UTC before it is bound.  
`number`| A decimal string, e.g. `"10"` or `"2.5"`  
`string`, `dropdown`| Bound as a string, unchanged  
  
A default is not checked when you save it — a `date` default without an offset only fails when a run falls back to it.

Auto-creation never overwrites a filter that already exists, so a token shared by several widgets keeps whatever metadata it was given the first time, and re-saving a widget will not undo your edits.

A filter is **required** when at least one widget uses its token outside an optional block — that is what `is_required` on [List filters](https://docs.sarvam.ai/voice-agents/api/boards/filters/list) reports. It does not take the default into account: a required filter with a `default_value` falls back to that default when a run sends no value, and only a required filter with **no** default makes the run fail with `UNRESOLVED_TOKEN`. So the filters a run must supply are the ones with `is_required: true` and `default_value: null` — which is every required filter on a widget saved with no `filters` array, since auto-created filters are typed `string` with no default.

Supply values at run time keyed by token name, with the declared type alongside the raw value. Values for tokens the board has no filter for are ignored. [Preview query](https://docs.sarvam.ai/voice-agents/api/boards/query/preview) has no board and therefore no defaults, so every token outside an optional block must be supplied there.
    
    
    {
    
      "filter_values": {
    
        "start_date": { "filter_type": "date", "value": "2026-09-01T00:00:00+05:30" },
    
        "agent_id":   { "filter_type": "string", "value": "support-agent-v3" }
    
      }
    
    }

## Query budget

Each run executes under fixed server-side limits:

Limit| Value| On breach  
---|---|---  
Execution time| 15 seconds| `408` `TIMEOUT`  
Rows returned, preview and widget run| `row_limit` — default 1000, max 10 000| `truncated: true`  
Rows returned, tab run| 1000 per widget, fixed| `truncated: true`  
`LIMIT` written into your SQL| Clamped to 1000| Silently clamped  
  
The effective row limit is the smaller of `row_limit` and your SQL’s `LIMIT`. Because an in-SQL `LIMIT` is itself clamped to 1000, a `row_limit` above 1000 only helps when the SQL has no `LIMIT`.

`truncated` is `true` whenever the number of rows returned equals the effective limit, so it means the result _may_ have been cut. A query ending in `LIMIT 10` that returns exactly 10 rows reports `truncated: true` even though nothing was lost.

[Run tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/run) takes no `row_limit` — the per-widget cap there is fixed and not caller-settable.

## Error codes

SQL and execution failures return `detail` as an object with a `code`:
    
    
    { "detail": { "code": "FORBIDDEN_TABLE", "message": "Table `users` is not available." } }

Code| Status| Cause| Fix  
---|---|---|---  
`PARSE_ERROR`| `400`| Unparseable SQL, multiple statements, or a forbidden clause| Check the message — it names the clause  
`NON_SELECT`| `400`| The statement is not a `SELECT`| Rewrite as a read  
`FORBIDDEN_TABLE`| `400`| A table outside this workspace’s catalog| Re-read [Get query schema](https://docs.sarvam.ai/voice-agents/api/boards/query/schema)  
`UNRESOLVED_TOKEN`| `400`| A required `{{token}}` had no value and no default| Supply it in `filter_values`, give it a default, or wrap it in `[[ ]]`  
`INVALID_FILTER_VALUE`| `400`| A value does not fit its declared `filter_type` — most often a `date` without a timezone offset| Send the format the type expects; for dates, a full timestamp with offset  
`TENANT_ISOLATION_BREACH`| `403`| The result would have crossed tenants| Remove hand-written tenancy predicates; report it if it persists  
`TIMEOUT`| `408`| Exceeded the 15-second budget| Narrow the time range, aggregate earlier, filter on `effective_datetime`  
`CLICKHOUSE_ERROR`| `422`| The database rejected the query — type mismatch, unknown column, bad function| The `clickhouse_error` field carries the underlying message  
  
A `CLICKHOUSE_ERROR` means your SQL passed validation but failed on execution, so it is almost always a column name or a type problem. `PARSE_ERROR` means it never reached the database.

`422` is also the status for request validation failures, such as a malformed UUID or a `row_limit` above 10 000. Those carry `detail` as a **list** rather than an object, so check whether `detail` is a list before reading `code`.

On [Run tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/run), a widget that fails with any of these codes other than `TENANT_ISOLATION_BREACH` does not fail the request: it comes back inside the `200` response with `status: "error"` and an `error` object carrying the same `code` and `message`. A tenant-isolation breach fails the whole tab run with `403`.

## Next

[Best practicesWhich endpoint to reach for, caching, and polling.](https://docs.sarvam.ai/voice-agents/api/boards/best-practices)[Preview queryRun SQL without saving a widget.](https://docs.sarvam.ai/voice-agents/api/boards/query/preview)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/boards/overview)[Best practicesChoosing the right endpoint, keeping queries fast, and building an integration that stays inside its budget.Next](https://docs.sarvam.ai/api-reference/boards/best-practices)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


