---
url: https://docs.sarvam.ai/voice-agents/api/boards/best-practices/
title: Best practices | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:04.037545+00:00
---

# Best practices | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/api/boards/best-practices/

Skip to navigation

On this page

  * Which endpoint should I call?
  * Prefer a tab run over N widget runs
  * Caching
  * Staying inside the query budget
  * Handling rate limits
  * Notification rules
  * End-to-end
  * Next



Scroll to top

[API Reference](https://docs.sarvam.ai/voice-agents/api/introduction)[Boards](https://docs.sarvam.ai/voice-agents/api/boards/overview)

# Best practices

Choosing the right endpoint, keeping queries fast, and building an integration that stays inside its budget.

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/api/boards/best-practices.md "View this page as plain text")|More actions

This page is for Voice Agents.

## Which endpoint should I call?

The four ways to get numbers out of boards are not interchangeable. Picking the wrong one is the most common cause of avoidable `429`s.

You want to…| Call| Why  
---|---|---  
Iterate on a query you are still writing| [Preview query](https://docs.sarvam.ai/voice-agents/api/boards/query/preview)| Nothing is saved. Capped at **20/min** — a development tool, not a production data source  
Read one metric repeatedly| [Run widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/run)| Results are cached, and the query lives in one place your team can see and edit  
Render a page of metrics at once| [Run tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/run)| One call instead of N, widgets run concurrently, and **50/min** is the most generous budget  
Receive numbers without polling| [Create notification rule](https://docs.sarvam.ai/voice-agents/api/boards/notifications/create)| Push instead of pull; costs no request budget at all  
  
### Prefer a tab run over N widget runs

Rendering six widgets one at a time costs six requests against a 20/min budget. [Run tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/run) costs one against a 50/min budget, and runs the widgets concurrently, so it is faster as well as cheaper.

A tab run also degrades gracefully. Each result is tagged `ok` or `error`, and a widget that fails does not fail the request — you still get every other widget.

Always branch on `status` before reading `rows`. Treating the array as uniformly successful will break the first time one query times out.

`filter_values_used` echoes back what was actually applied after merging your `filter_values` over each filter’s default — useful for labelling a rendered page, and for confirming a default was what you assumed. Each value is a string, or `null` for a filter that had neither a value nor a default. Values you send for tokens the board has no filter for are ignored, so a typo in a token name fails silently rather than with an error.

## Caching

Widget runs and tab runs are cached for **60 seconds** , keyed by widget, filter values, and row limit. Editing a widget invalidates its cache immediately.

  * Polling the same widget with the same filters more often than once a minute returns identical rows and still consumes request budget. Match your poll interval to the cache, not to your refresh animation.
  * Changing any filter value is a different cache key, so a dashboard where users move filters around will miss the cache often. Budget for that.
  * Preview is **not** cached — every call executes, so it is the wrong endpoint to poll on a timer.



## Staying inside the query budget

Every run gets 15 seconds and a row cap. Exceeding the time budget returns `408` with code `TIMEOUT`; reaching the row cap returns `200` with `truncated: true`.

The dialect-level advice for keeping a query fast — filter on `effective_datetime` early, aggregate in the database rather than returning raw rows, name your columns instead of `SELECT *` — is the same whether you write the query here or in the dashboard editor, and lives on [SQL best practices](https://docs.sarvam.ai/voice-agents/monitor/clickhouse-sql-best-practices).

Two things are specific to calling this over the API:

There is no cursor for stepping through a large result — `row_limit` is a cap, not a page size.

**`truncated: true` means your answer may be wrong, not just short.** It is set whenever the number of rows returned equals the effective limit, so rows beyond the cap may have been dropped, and any total, average, or max you compute from those rows may be derived from a partial set. Raising `row_limit` is rarely the right fix — it just moves the cliff. Aggregate further or narrow the range so the full answer fits.

The flag cannot tell a cut-off result from one that hit your own `LIMIT` exactly: a top-20 query that returns 20 rows also reports `truncated: true`. Treat it as a warning only for queries that are not meant to stop at a fixed count.
    
    
    if result["truncated"] and not query_has_own_limit:
    
        raise RuntimeError("possibly partial result — aggregate in SQL instead of raising row_limit")

**`row_limit` and a `LIMIT` in your SQL are not the same control.** `row_limit` is the ceiling; a `LIMIT` inside the query can narrow the result below it but never widen it past it, and an in-SQL `LIMIT` is itself clamped to 1000 — so a `row_limit` above 1000 only helps when the SQL has no `LIMIT`. If you want the top 20, write `ORDER BY ... LIMIT 20` — don’t set `row_limit: 20` and hope the ordering holds.

## Handling rate limits

Every limit — the per-key limit and the three per-organization run limits — returns `429` with `Retry-After` in seconds; sleep for that long and back off exponentially on repeated `429`s, with jitter if several workers share a key.

The per-organization limits are shared with people using the dashboard, so an integration that consumes the entire preview budget will make boards feel broken for your colleagues.

## Notification rules

For anything on a fixed schedule, a notification rule beats polling: it costs no request budget and survives your service being down.

  * The cron is a five-field expression evaluated in **IST (Asia/Kolkata)** , and it may not fire more than once an hour — `* * * * *` is rejected. `next_run_at` in the response is UTC.
  * At least one of `email_recipients` or `slack_webhook_url` is required. Both may be set. A webhook URL must start with `https://hooks.slack.com/`.
  * `slack_webhook_url` is write-only — no endpoint ever returns it. Use `slack_configured` to tell whether one is set, and `slack_channel_name` to label it.
  * Pause a rule with `{"enabled": false}` rather than recreating it later; disabling clears `next_run_at`.



## End-to-end

Discover the schema, develop a query, save it, and run it.

curlPython
    
    
    BASE="https://apps.sarvam.ai/api/analytics/v1/$ORG_ID/$WORKSPACE_ID"
    
    # 1. What can I query?
    
    curl -s "$BASE/query-schema" -H "X-API-Key: $SARVAM_API_KEY"
    
    # 2. Try the SQL without saving anything.
    
    curl -s -X POST "$BASE/query-preview" \
    
      -H "X-API-Key: $SARVAM_API_KEY" -H "Content-Type: application/json" \
    
      -d '{
    
            "sql": "SELECT language_name, count() AS calls FROM EngagementFactsBoardsView WHERE effective_datetime >= {{start_date}} GROUP BY language_name ORDER BY calls DESC",
    
            "filter_values": { "start_date": { "filter_type": "date", "value": "2026-09-01T00:00:00+05:30" } },
    
            "row_limit": 100
    
          }'
    
    # 3. Create a board (returns board_id).
    
    curl -s -X POST "$BASE/boards" \
    
      -H "X-API-Key: $SARVAM_API_KEY" -H "Content-Type: application/json" \
    
      -d '{ "name": "Campaign Overview", "tag": "Weekly reporting" }'
    
    # 4. Save the query as a widget (returns widget_id).
    
    curl -s -X POST "$BASE/boards/$BOARD_ID/widgets" \
    
      -H "X-API-Key: $SARVAM_API_KEY" -H "Content-Type: application/json" \
    
      -d '{
    
            "name": "Calls by language",
    
            "sql": "SELECT language_name, count() AS calls FROM EngagementFactsBoardsView WHERE effective_datetime >= {{start_date}} GROUP BY language_name ORDER BY calls DESC",
    
            "viz_type": "bar",
    
            "viz_config": { "x_axis": "language_name", "y_axis": ["calls"] },
    
            "filters": [
    
              { "internal_name": "start_date", "display_label": "Start date", "filter_type": "date", "default_value": "2026-09-01T00:00:00+05:30" }
    
            ]
    
          }'
    
    # 5. Run it.
    
    curl -s -X POST "$BASE/boards/$BOARD_ID/widgets/$WIDGET_ID/run" \
    
      -H "X-API-Key: $SARVAM_API_KEY" -H "Content-Type: application/json" \
    
      -d '{ "filter_values": { "start_date": { "filter_type": "date", "value": "2026-09-01T00:00:00+05:30" } } }'

## Next

[Writing board SQLAllowed tables, filter tokens, and every error code.](https://docs.sarvam.ai/voice-agents/api/boards/sql)[Boards API overviewBase URL, rate limits, and the error envelope.](https://docs.sarvam.ai/voice-agents/api/boards/overview)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/api/boards/sql)[List boardsNext](https://docs.sarvam.ai/voice-agents/api/boards/list)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Introduction](https://docs.sarvam.ai/voice-agents/introduction)
    * [Why Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents)
    * [Overview](https://docs.sarvam.ai/voice-agents/overview)
    * [Quickstart](https://docs.sarvam.ai/voice-agents/quickstart)
    * [MCP Server](https://docs.sarvam.ai/voice-agents/mcp)
  * Build

    * [Overview](https://docs.sarvam.ai/voice-agents/build/overview)
    * Architecture

    * [Navigating the build interface](https://docs.sarvam.ai/voice-agents/build/navigating-workspace)
    * [Agent](https://docs.sarvam.ai/voice-agents/build/agent/overview)

    * [Prompt Practices](https://docs.sarvam.ai/voice-agents/build/single-state-agents)
    * [Building & improving agents](https://docs.sarvam.ai/voice-agents/build/process)
    * [Genie](https://docs.sarvam.ai/voice-agents/build/genie)
    * [Tests](https://docs.sarvam.ai/voice-agents/build/tests)

    * Advanced concepts

  * Deploy

    * [Overview](https://docs.sarvam.ai/voice-agents/deploy/overview)
    * [Phone Numbers](https://docs.sarvam.ai/voice-agents/deploy/telephony)

    * [Inbounds](https://docs.sarvam.ai/voice-agents/deploy/inbounds)
    * [Campaigns](https://docs.sarvam.ai/voice-agents/deploy/campaigns)

    * [Deploy with Code (API & SDK)](https://docs.sarvam.ai/voice-agents/deploy/deploy-with-code)
  * Monitor

    * [Overview](https://docs.sarvam.ai/voice-agents/monitor/overview)
    * [Agent Analytics](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics)

    * [Boards](https://docs.sarvam.ai/voice-agents/monitor/boards)

    * [SQL best practices](https://docs.sarvam.ai/voice-agents/monitor/clickhouse-sql-best-practices)
  * SDKs

    * [Python](https://docs.sarvam.ai/voice-agents/deploy/sdks/python)
    * [Web (TypeScript)](https://docs.sarvam.ai/voice-agents/deploy/sdks/web)
    * [React Native](https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native)
    * [Flutter](https://docs.sarvam.ai/voice-agents/deploy/sdks/flutter)
  * API Reference

    * [Introduction](https://docs.sarvam.ai/voice-agents/api/introduction)
    * Deployments

    * Campaigns

    * Instant Outbound

    * Analytics

    * Boards
      * [Overview](https://docs.sarvam.ai/voice-agents/api/boards/overview)
      * [Writing board SQL](https://docs.sarvam.ai/voice-agents/api/boards/sql)
      * [Best practices](https://docs.sarvam.ai/voice-agents/api/boards/best-practices)
      * [GETList boards](https://docs.sarvam.ai/voice-agents/api/boards/list)
      * [POSTCreate board](https://docs.sarvam.ai/voice-agents/api/boards/create)
      * [GETGet board](https://docs.sarvam.ai/voice-agents/api/boards/get)
      * [PATCHUpdate board](https://docs.sarvam.ai/voice-agents/api/boards/update)
      * [POSTDuplicate board](https://docs.sarvam.ai/voice-agents/api/boards/duplicate)
      * Tabs

      * Widgets

      * Filters

      * Notifications

      * Query

    * Tests

    * BYOK

  * Settings

    * [API Key](https://docs.sarvam.ai/voice-agents/settings/api-key)
    * [Secrets](https://docs.sarvam.ai/voice-agents/settings/secrets)
    * [Policy](https://docs.sarvam.ai/voice-agents/settings/policy)
    * [Data retention](https://docs.sarvam.ai/api/platform/data-retention "Data retention")
    * [Extensions](https://docs.sarvam.ai/voice-agents/settings/extensions)
    * [Pricing](https://docs.sarvam.ai/voice-agents/pricing)



  * [Introduction](https://docs.sarvam.ai/voice-agents/introduction)
  * [Why Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents)
  * [Overview](https://docs.sarvam.ai/voice-agents/overview)
  * [Quickstart](https://docs.sarvam.ai/voice-agents/quickstart)
  * [MCP Server](https://docs.sarvam.ai/voice-agents/mcp)
  * [Overview](https://docs.sarvam.ai/voice-agents/build/overview)
  * [Introduction](https://docs.sarvam.ai/voice-agents/build/concepts/introduction)
  * [Run-time](https://docs.sarvam.ai/voice-agents/build/run-time)
  * [Models](https://docs.sarvam.ai/voice-agents/build/models)
  * [Harness](https://docs.sarvam.ai/voice-agents/build/concepts/harness)
  * [Navigating the build interface](https://docs.sarvam.ai/voice-agents/build/navigating-workspace)
  * [Agent](https://docs.sarvam.ai/voice-agents/build/agent/overview)
  * [Instruction](https://docs.sarvam.ai/voice-agents/build/system-prompt)
  * [Variables & personalization](https://docs.sarvam.ai/voice-agents/build/variables-personalization)
  * [Tools](https://docs.sarvam.ai/voice-agents/build/tools)
  * [Core tools](https://docs.sarvam.ai/voice-agents/build/tools/core-tools)
  * [Call transfer](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer)
  * [API tool](https://docs.sarvam.ai/voice-agents/build/tools/https-tool)
  * [Data validation & verification](https://docs.sarvam.ai/voice-agents/build/tools/data-validation)
  * [Mocking a tool](https://docs.sarvam.ai/voice-agents/build/tools/mocking-a-tool)
  * [Code Tools](https://docs.sarvam.ai/voice-agents/build/tools/code-tools)
  * [On-start & on-end hooks](https://docs.sarvam.ai/voice-agents/build/on-start-on-end-hooks)
  * [Knowledge base](https://docs.sarvam.ai/voice-agents/build/knowledge-base)
  * [Agent versioning](https://docs.sarvam.ai/voice-agents/build/agent/versioning)
  * [Speakers & voice](https://docs.sarvam.ai/voice-agents/build/voice-language)
  * [Conversation settings](https://docs.sarvam.ai/voice-agents/build/conversation-settings)
  * [Prompt Practices](https://docs.sarvam.ai/voice-agents/build/single-state-agents)
  * [Building & improving agents](https://docs.sarvam.ai/voice-agents/build/process)
  * [Genie](https://docs.sarvam.ai/voice-agents/build/genie)
  * [Tests](https://docs.sarvam.ai/voice-agents/build/tests)
  * [Write test cases](https://docs.sarvam.ai/voice-agents/build/tests/write-test-cases)
  * [Run tests & review results](https://docs.sarvam.ai/voice-agents/build/tests/run-tests)
  * [Multi-state agents](https://docs.sarvam.ai/voice-agents/build/states-conversation-flow)
  * [Overview](https://docs.sarvam.ai/voice-agents/deploy/overview)
  * [Phone Numbers](https://docs.sarvam.ai/voice-agents/deploy/telephony)
  * [Bring Your Own Telephony](https://docs.sarvam.ai/voice-agents/deploy/telephony/bring-your-own)
  * [Exotel](https://docs.sarvam.ai/voice-agents/deploy/telephony/exotel)
  * [Twilio](https://docs.sarvam.ai/voice-agents/deploy/telephony/twilio)
  * [Smartflo](https://docs.sarvam.ai/voice-agents/deploy/telephony/smartflo)
  * [Pulse](https://docs.sarvam.ai/voice-agents/deploy/telephony/pulse)
  * [Intalk](https://docs.sarvam.ai/voice-agents/deploy/telephony/intalk)
  * [Vobiz](https://docs.sarvam.ai/voice-agents/deploy/telephony/vobiz)
  * [Plivo](https://docs.sarvam.ai/voice-agents/deploy/telephony/plivo)
  * [Rent from Sarvam](https://docs.sarvam.ai/voice-agents/deploy/telephony/rent-from-sarvam)
  * [Manage Phone Numbers](https://docs.sarvam.ai/voice-agents/deploy/telephony/manage-numbers)
  * [Groups](https://docs.sarvam.ai/voice-agents/deploy/telephony/groups)
  * [Inbounds](https://docs.sarvam.ai/voice-agents/deploy/inbounds)
  * [Campaigns](https://docs.sarvam.ai/voice-agents/deploy/campaigns)
  * [Create a campaign](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign)
  * [Campaign details](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-details)
  * [Cohorts](https://docs.sarvam.ai/voice-agents/deploy/campaigns/cohorts)
  * [Dialing rate & concurrency](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dialing-rate)
  * [Campaign lifecycle](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-lifecycle)
  * [Do Not Disturb (DND)](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dnd)
  * [Best practices](https://docs.sarvam.ai/voice-agents/deploy/campaigns/best-practices)
  * [Deploy with Code (API & SDK)](https://docs.sarvam.ai/voice-agents/deploy/deploy-with-code)
  * [Overview](https://docs.sarvam.ai/voice-agents/monitor/overview)
  * [Agent Analytics](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics)
  * [Overview tab](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/overview)
  * [Connectivity](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/connectivity)
  * [Engagement](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/engagement)
  * [Tools](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/tools)
  * [Goals](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/goals)
  * [Group by](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/group-by)
  * [Call Logs](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/call-logs)
  * [Log Analyser](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/log-analyser)
  * [Boards](https://docs.sarvam.ai/voice-agents/monitor/boards)
  * [Create a board](https://docs.sarvam.ai/voice-agents/monitor/boards/create-board)
  * [Create a widget](https://docs.sarvam.ai/voice-agents/monitor/boards/create-widget)
  * [Filters](https://docs.sarvam.ai/voice-agents/monitor/boards/filters)
  * [SQL best practices](https://docs.sarvam.ai/voice-agents/monitor/clickhouse-sql-best-practices)
  * [Python](https://docs.sarvam.ai/voice-agents/deploy/sdks/python)
  * [Web (TypeScript)](https://docs.sarvam.ai/voice-agents/deploy/sdks/web)
  * [React Native](https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native)
  * [Flutter](https://docs.sarvam.ai/voice-agents/deploy/sdks/flutter)
  * [Introduction](https://docs.sarvam.ai/voice-agents/api/introduction)
  * [Create deployment](https://docs.sarvam.ai/voice-agents/api/deployments/create)
  * [List deployments](https://docs.sarvam.ai/voice-agents/api/deployments/list)
  * [Get deployment](https://docs.sarvam.ai/voice-agents/api/deployments/get)
  * [Update deployment](https://docs.sarvam.ai/voice-agents/api/deployments/update)
  * [Update status](https://docs.sarvam.ai/voice-agents/api/deployments/update-status)
  * [Delete deployment](https://docs.sarvam.ai/voice-agents/api/deployments/delete)
  * [Webhook payload](https://docs.sarvam.ai/voice-agents/api/deployments/webhooks/webhook-payload)
  * [List webhook deliveries](https://docs.sarvam.ai/voice-agents/api/deployments/webhooks/list)
  * [Retry webhook deliveries](https://docs.sarvam.ai/voice-agents/api/deployments/webhooks/retry)
  * [Upload cohort](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/upload)
  * [Stream cohort](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/stream)
  * [List cohorts](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/list)
  * [Get cohort](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/get)
  * [Download cohort file](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/download)
  * [Create campaign](https://docs.sarvam.ai/voice-agents/api/campaigns/create)
  * [List campaigns](https://docs.sarvam.ai/voice-agents/api/campaigns/list)
  * [Get campaign](https://docs.sarvam.ai/voice-agents/api/campaigns/get)
  * [Update campaign](https://docs.sarvam.ai/voice-agents/api/campaigns/update)
  * [Update status](https://docs.sarvam.ai/voice-agents/api/campaigns/update-status)
  * [Webhook payload](https://docs.sarvam.ai/voice-agents/api/campaigns/webhooks/webhook-payload)
  * [List webhook deliveries](https://docs.sarvam.ai/voice-agents/api/campaigns/webhooks/list)
  * [Retry webhook deliveries](https://docs.sarvam.ai/voice-agents/api/campaigns/webhooks/retry)
  * [Upload cohort](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/upload)
  * [Stream cohort](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/stream)
  * [List cohorts](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/list)
  * [Get cohort](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/get)
  * [Download cohort file](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/download)
  * [Create outbound call](https://docs.sarvam.ai/voice-agents/api/instant-outbound/create)
  * [Webhook payload](https://docs.sarvam.ai/voice-agents/api/instant-outbound/webhook-payload)
  * [Overview](https://docs.sarvam.ai/voice-agents/api/analytics/overview)
  * [List attempts](https://docs.sarvam.ai/voice-agents/api/analytics/attempts)
  * [List interactions](https://docs.sarvam.ai/voice-agents/api/analytics/interactions)
  * [Get recording](https://docs.sarvam.ai/voice-agents/api/analytics/recordings)
  * [Get transcript](https://docs.sarvam.ai/voice-agents/api/analytics/transcripts)
  * [Overview](https://docs.sarvam.ai/voice-agents/api/boards/overview)
  * [Writing board SQL](https://docs.sarvam.ai/voice-agents/api/boards/sql)
  * [Best practices](https://docs.sarvam.ai/voice-agents/api/boards/best-practices)
  * [List boards](https://docs.sarvam.ai/voice-agents/api/boards/list)
  * [Create board](https://docs.sarvam.ai/voice-agents/api/boards/create)
  * [Get board](https://docs.sarvam.ai/voice-agents/api/boards/get)
  * [Update board](https://docs.sarvam.ai/voice-agents/api/boards/update)
  * [Duplicate board](https://docs.sarvam.ai/voice-agents/api/boards/duplicate)
  * [Create tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/create)
  * [Update tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/update)
  * [Run tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/run)
  * [Create widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/create)
  * [Update widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/update)
  * [Duplicate widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/duplicate)
  * [Run widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/run)
  * [List filters](https://docs.sarvam.ai/voice-agents/api/boards/filters/list)
  * [Update filter](https://docs.sarvam.ai/voice-agents/api/boards/filters/update)
  * [Create notification rule](https://docs.sarvam.ai/voice-agents/api/boards/notifications/create)
  * [List notification rules](https://docs.sarvam.ai/voice-agents/api/boards/notifications/list)
  * [Get notification rule](https://docs.sarvam.ai/voice-agents/api/boards/notifications/get)
  * [Update notification rule](https://docs.sarvam.ai/voice-agents/api/boards/notifications/update)
  * [Get query schema](https://docs.sarvam.ai/voice-agents/api/boards/query/schema)
  * [Preview query](https://docs.sarvam.ai/voice-agents/api/boards/query/preview)
  * [Overview](https://docs.sarvam.ai/voice-agents/api/tests/overview)
  * [Best practices](https://docs.sarvam.ai/voice-agents/api/tests/best-practices)
  * [List test suites](https://docs.sarvam.ai/voice-agents/api/tests/list)
  * [Create a test suite](https://docs.sarvam.ai/voice-agents/api/tests/create)
  * [Get a test suite](https://docs.sarvam.ai/voice-agents/api/tests/get)
  * [Update a test suite](https://docs.sarvam.ai/voice-agents/api/tests/update)
  * [Add a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/add)
  * [Get a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/get)
  * [Update a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/update)
  * [Duplicate a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/duplicate)
  * [Map suite variables onto an app](https://docs.sarvam.ai/voice-agents/api/tests/mappings/create)
  * [Get the variable mapping](https://docs.sarvam.ai/voice-agents/api/tests/mappings/get)
  * [Run a test suite](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-suite)
  * [Run a single test case](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-test-case)
  * [List runs](https://docs.sarvam.ai/voice-agents/api/tests/runs/list)
  * [Get a run](https://docs.sarvam.ai/voice-agents/api/tests/runs/get)
  * [Get test case results](https://docs.sarvam.ai/voice-agents/api/tests/runs/results)
  * [Overview](https://docs.sarvam.ai/voice-agents/api/byok/overview)
  * [Obtain access token](https://docs.sarvam.ai/voice-agents/api/byok/auth)
  * [Decrypt key](https://docs.sarvam.ai/voice-agents/api/byok/decrypt-key)
  * [Rotate key](https://docs.sarvam.ai/voice-agents/api/byok/rotate-key)
  * [API Key](https://docs.sarvam.ai/voice-agents/settings/api-key)
  * [Secrets](https://docs.sarvam.ai/voice-agents/settings/secrets)
  * [Policy](https://docs.sarvam.ai/voice-agents/settings/policy)
  * [Extensions](https://docs.sarvam.ai/voice-agents/settings/extensions)
  * [Pricing](https://docs.sarvam.ai/voice-agents/pricing)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


