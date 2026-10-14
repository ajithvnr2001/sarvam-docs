---
url: https://docs.sarvam.ai/voice-agents/build/tools/https-tool/
title: API tool | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:24.227284+00:00
---

# API tool | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/build/tools/https-tool/

Skip to navigation

On this page

  * Lifecycle: when the tool runs
  * Two ways to create one
  * Mock tool
  * Real integration
  * Authoring an API tool
  * Authentication
  * Call-context variables
  * How to use them
  * Network access
  * Typical build order
  * Practical notes



Scroll to top

[Build](https://docs.sarvam.ai/voice-agents/build/overview)[Agent](https://docs.sarvam.ai/voice-agents/build/agent/overview)[Tools](https://docs.sarvam.ai/voice-agents/build/tools)

# API tool

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/build/tools/https-tool.md "View this page as plain text")|More actions

This page is for Voice Agents.

An API tool is a webhook the agent can call mid-conversation to talk to an external system, look up an order, book a slot, or post a lead to your CRM. At runtime the agent invokes it by name (`call tool:your_tool_name` in the instructions), the platform makes the HTTP request, and the response comes back for the agent to use in its reply.

## Lifecycle: when the tool runs

Set **When should this tool run?** to one of:

  * **run** (default, shown as _During conversation_): the LLM-callable webhook, invoked by the agent mid-conversation.
  * **on_start** : fires automatically at call start, typically to pull data into [agent variables](https://docs.sarvam.ai/voice-agents/build/variables-personalization) before the conversation begins.
  * **on_end** : fires automatically at call end, typically to push captured variables out to your endpoint.



`on_start` and `on_end` are **lifecycle hooks** : there is no LLM in the loop, so they are never referenced from the instructions and cannot use a response template. See [On-start & on-end hooks](https://docs.sarvam.ai/voice-agents/build/on-start-on-end-hooks).

## Two ways to create one

### Mock tool

For prototyping, or when you don’t have a real backend yet (or just have example response JSON). Supply a **name** and a **canned response** ; the platform fills in sensible defaults (a test URL, JSON body, playground mock config) and returns your canned response every time. Great for designing and testing the conversation flow before the real API exists. See [Mocking a tool](https://docs.sarvam.ai/voice-agents/build/tools/mocking-a-tool).

### Real integration

Provide the actual **endpoint URL** , **HTTP method** (GET / POST / PUT / PATCH / DELETE), any static **headers** , **body** , **query** or **path** parameters, and the **auth** setup. The fastest way is to paste a **cURL** command, the builder fills in the method, URL, headers, and body, and everything stays editable. You can also map fields from the response into agent variables so the agent can speak them back.

## Authoring an API tool

  1. **Name and describe the tool.** Use a snake_case **name** (for example, `get_order_status`) and a clear **description** , the agent uses both to decide when to call it.
  2. **Set your API call.** Choose the **method** and **URL** , configure **Path** , **Params** , **Headers** , **Body** , and **Auth** , then press **Test** to try it live. Pasting a **cURL** command still fills these in for you.
  3. **Say what the agent gets back.** Write a response template for how the agent should use the result (for example, `The account balance is {{balance}}`); type `@` to insert a field from the reply.
  4. **Advanced.** Set **Max wait** (timeout), **If it fails** (what the agent says on a timeout or error), and **Save reply into variables** (store response fields into [agent variables](https://docs.sarvam.ai/voice-agents/build/variables-personalization)).



![Animated walkthrough of the Create tool panel - naming the tool, generating with AI, and setting method, URL, headers, and other API options.](https://docs.sarvam.ai/_fern-files/sarvam-api-docs.docs.buildwithfern.com/bc26d3038cd39e3c2c42810cfc799219ed25406da5ca1839c04c45e96e6835b4/voice-agents/images/https-tool.gif)

Create tool: name and describe the tool, then configure the HTTP API call.

## Authentication

Supported auth types: **none** , **bearer token** , **api_key** , and **basic**.

For any authenticated tool, the credential value is **never typed into the tool config**. You enter it through a secure masked input, the secret is stored safely in your workspace (see [Secrets](https://docs.sarvam.ai/voice-agents/settings/secrets)), and the tool references it, so tokens and keys never sit in plain text in the agent definition.

## Call-context variables

An API tool can receive live call context alongside the [agent variables](https://docs.sarvam.ai/voice-agents/build/variables-personalization) you define. Four are available:

Variable| What it carries| Typical use  
---|---|---  
**User Identifier**|  The caller’s phone number| Identify the caller in your CRM, personalize the response, or log the interaction against their account  
**Call Transcript**|  The full conversation transcript so far| Let your backend see what was said — compliance logging, sentiment analysis, or context for the lookup  
**Interaction ID**|  The unique ID of the current call| Idempotency keys, deduplication, and correlating tool calls with call records in [Call Logs](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/call-logs)  
**Call Length**|  How long the call has been running| Time-based logic — escalate long calls, or skip a lookup when the call is about to hit the [max call length](https://docs.sarvam.ai/voice-agents/build/conversation-settings#max-call-length)  
  
### How to use them

  1. Open the tool editor for your API tool (or create one — see [Authoring an API tool](https://docs.sarvam.ai/voice-agents/build/tools/https-tool#authoring-an-api-tool)).
  2. In the **Body** , **Params** , or **Headers** section, type `@` to open the variable picker. The call-context variables appear alongside your agent variables.
  3. Select **User Identifier** , **Call Transcript** , **Interaction ID** , or **Call Length** — the platform substitutes the live value at request time, the same way it substitutes agent variables.
  4. Press **Test** to verify your endpoint receives the values you expect.



**User Identifier** is populated on inbound calls. On outbound calls, use the number from the [campaign](https://docs.sarvam.ai/voice-agents/deploy/campaigns) contact instead.

Because these are resolved at request time, a mid-call tool always sees the current state: the transcript includes everything said up to that point, and **Call Length** reflects the elapsed duration when the tool fires.

## Network access

If your endpoint sits behind a firewall or VPC (for example, an internal CRM), allowlist Sarvam’s IP so the platform can reach it:

`4.213.167.70`

Add this IP to your firewall or security group rules before testing the tool.

## Typical build order

  1. Create the tool (mock or real).
  2. Enable it on the agent.
  3. Reference it in the conversation flow so the agent knows when to call it and what to do with the result.
  4. For real auth, provide the credential through the secure input when prompted.



## Practical notes

  * **Keep timeouts tight** (configurable up to 30s) so the caller isn’t left waiting in silence.
  * **Map the response into variables** so the agent can use what it fetched (“I see your order shipped Tuesday”).
  * **Design around latency** : a mid-call API hit means a pause on the line, so have the agent say something like “let me pull that up” first.



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer)[Data validation & verificationNext](https://docs.sarvam.ai/voice-agents/build/tools/data-validation)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * Settings

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


