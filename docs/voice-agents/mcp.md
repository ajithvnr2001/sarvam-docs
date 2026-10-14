---
url: https://docs.sarvam.ai/voice-agents/mcp/
title: Voice Agents MCP Server for Claude, Cursor, and VS Code | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:30.519813+00:00
---

# Voice Agents MCP Server for Claude, Cursor, and VS Code | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/mcp/

Skip to navigation

On this page

  * What the MCP server does
  * Before you begin
  * Connect
  * The tool surface
  * Domain tools
  * Write tools
  * Resources
  * Example prompts
  * How it works
  * Security
  * Troubleshooting
  * Related pages



Scroll to top

[Getting Started](https://docs.sarvam.ai/voice-agents/introduction)

# MCP Server

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/mcp.md "View this page as plain text")|More actions

This page is for Voice Agents.

The **Sarvam Voice Agents MCP server** exposes the platform (agent authoring, telephony, campaigns, knowledge bases, evals, boards, and analytics) as tools that any [Model Context Protocol](https://modelcontextprotocol.io/) client can call. Point Claude, Cursor, or VS Code at `https://mcp.sarvam.ai/voice-agents`, sign in once with your Sarvam account, and your assistant can build and operate voice agents for you.

It is a **hosted, remote server** : nothing to install and nothing to run. You connect over streamable HTTP and authenticate through Sarvam SSO in your browser.

## What the MCP server does

Area| What you can do  
---|---  
**Agents**|  Create, clone, and configure agents (prompt, variables, tools, knowledge, voice, settings), and commit immutable versions  
**Telephony**|  Connect providers, onboard numbers, run inbound deployments, and test an agent over a real call  
**Campaigns**|  Create outbound campaigns, upload cohorts, and run the campaign lifecycle  
**Evals**|  Define test suites and scenarios, run them against a committed version, and read the results  
**Knowledge bases**|  Create knowledge bases, upload files, and run retrieval search  
**Boards**|  Build custom analytics boards: widgets, SQL, filters, and scheduled deliveries  
**Analytics**|  Pull reports and interaction traces, replay chats, and review insights and issues  
  
The server connects to **one organisation and one workspace** , whichever your login resolves to. No tool takes an `org_id` or `workspace_id`, and a connection cannot switch orgs. To work in another workspace, reconnect with a login for it.

## Before you begin

  * **A Sarvam account** with access to Voice Agents. Sign in once at [indus.sarvam.ai/samvaad](https://indus.sarvam.ai/samvaad) to confirm your workspace is set up.
  * **An MCP client** that supports remote (HTTP) servers with OAuth: Claude Code, Claude Desktop, Cursor, VS Code, and most others qualify.



## Connect

[1](https://docs.sarvam.ai/voice-agents/mcp#add-the-server-to-your-client)

### Add the server to your client

Register `https://mcp.sarvam.ai/voice-agents` as an HTTP MCP server. Pick your client below.

###### Claude Code

###### Cursor

###### VS Code

###### Claude Desktop

###### Other clients

Run this in your terminal, not inside a `claude` session:
    
    
    claude mcp add --transport http sarvam-voice-agents https://mcp.sarvam.ai/voice-agents

Add `--scope user` to make the server available in every project, or `--scope project` to share it with your team through a checked-in `.mcp.json`.

[2](https://docs.sarvam.ai/voice-agents/mcp#authenticate)

### Authenticate

On first use the client shows the server as **needs authentication**. Trigger the sign-in: in Claude Code, run `/mcp`, select `sarvam-voice-agents`, and choose **Authenticate**. Other clients prompt automatically.

Your browser opens to **Sarvam SSO**. Approve the connection. The client stores the token and reuses it for 24 hours; there is no refresh token, so you sign in again once a day.

[3](https://docs.sarvam.ai/voice-agents/mcp#verify)

### Verify

Ask your assistant to do something read-only, and check that the tool call is labelled with the server name:

wrap
    
    
    Use sarvam-voice-agents to list my voice agents

## The tool surface

The server has two kinds of tool. The exact list adapts to your workspace: a tool, an operation, or a field your plan does not include is simply absent, not refused.

### Domain tools

One tool per domain, covering reads and lifecycle actions that carry no request body. Each takes an `operation`, an optional `id`, and optional `params` (plus `fetch_all` to auto-page list operations).

Tool| Covers  
---|---  
`agents`| List and read agents and voices; commit and translate a draft, and delete a template tool  
`telephony`| List connections, onboarded numbers, and inbound deployments; run their lifecycle  
`campaigns`| List campaigns and cohorts; run the campaign lifecycle  
`evals`| List test suites, scenarios, and runs; read run results  
`knowledge_base`| List knowledge bases and files; inspect what an agent retrieves  
`boards`| List boards, widgets, filters, and schedules; run their lifecycle  
`analytics`| Run reports, fetch an interaction trace or transcript, and read insights and issues  
`workflows`| List DSL workflows, commit them, and read run reports (enterprise)  
  
### Write tools

Every write is its own tool with a typed, validated body. The main ones:

  * **Agents:** `configure_agent` (create, update, or clone; set the prompt and config), `configure_voicemail`. Giving an agent tools depends on your plan, and a workspace only has one of these paths: 
    * **Non-enterprise:** `create_http_tool` / `create_validator_tool` / `create_verifier_tool` register one declared tool at a time.
    * **Enterprise:** `upload_agent_code` uploads a `tools.py` module instead — for logic that needs real code, lifecycle hooks, or shared state.
  * **Telephony:** `configure_connection`, `configure_endpoint`, `configure_deployment` to connect a provider and go live. Testing an agent over a real call also depends on your plan: 
    * **Non-enterprise:** `verify_phone_number` verifies a number your workspace owns, then `place_test_call` dials it.
    * **Enterprise:** `configure_test_number` whitelists callers on a shared inbound test number instead.
  * **Campaigns:** `configure_campaign`, `upload_cohort`
  * **Evals:** `configure_test_suite`, `configure_scenario`, `run_eval`
  * **Knowledge bases:** `configure_kb`, `upload_kb_file`
  * **Boards:** `configure_board` and its tab, widget, filter, layout, and schedule tools; `run_board_widget`, `export_board_widget`
  * **Analytics and chat:** `write_insight`, `send_chat`
  * **Workflows:** `configure_workflow` (enterprise)



### Resources

The server also serves MCP **resources** your assistant reads for context:

Resource| What it carries  
---|---  
`sarvam://playbooks/index`| Which playbook covers what  
`sarvam://playbooks/{domain}`| Call sequences and failure modes for one domain: what order to do things in, and what an error means  
`sarvam://schemas/agent-config`| The full JSON Schema for the agent config, too large to inline in a tool  
`sarvam://schemas/agent-config/{section}`| One section of that schema, for a change that touches one field  
`sarvam://examples/agent-config`| A validated, worked agent config  
  
## Example prompts

Realistic prompts to try once you are connected. Each one chains several tool calls, and your assistant reads the relevant `sarvam://playbooks/{domain}` resource as it goes:

  * “Create a new outbound sales agent, give it a prompt and a voice, commit it, and connect it to my Exotel number.”
  * “Clone the ‘Support Agent’ as ‘Support Agent v2’, add a knowledge base from these three PDFs, and commit it once it’s ready.”
  * “Set up an eval suite with five scenarios for the billing agent, run it against the latest committed version, and summarise which scenarios failed.”
  * “Create an outbound campaign for the Q4 cohort, upload this CSV, and pause it as soon as it starts so I can review the first few calls.”
  * “Pull last week’s failed inbound calls, group them by failure reason, and open the insights for the three most common ones.”
  * “Build a board that tracks daily call volume and average handle time for the last 30 days, and schedule it to email me every Monday.”



## How it works

  * **Drafts and versions.** Your assistant edits a mutable **draft** of an agent, then **commits** it as an immutable version. Deployments, campaigns, and eval runs always run a committed version, never the draft.
  * **Configuring an agent merges into the draft.** Nested objects merge key-by-key, but a list you send **replaces the old list whole** — resend the full list, not just the item you changed, or the rest silently drop.
  * **Guided calls.** The playbooks and schemas above are how your assistant learns the call order and the exact request shapes. You do not manage them; the assistant reads them as it works.
  * **Validated writes.** Every change is validated before it lands. A rejection names each bad field and leaves the draft untouched, so a failed write is never a half-written agent.



## Security

  * **Authentication.** OAuth 2.1 through Sarvam SSO. No API keys are pasted into client config, and the token is scoped to your organisation and workspace.
  * **Approvals.** Prompt for approval on every mutation tool: `configure_*`, `upload_*`, `run_*`, `create_*`, plus `send_chat`, `place_test_call`, `verify_phone_number`, `write_insight`, and `export_board_widget`. Domain tools (`agents`, `telephony`, `campaigns`, `evals`, `boards`, `workflows`) also carry lifecycle actions — `commit`, `delete_connection`, `pause` / `resume` / `cancel`, `delete_scenario`, and more — behind the same tool name as their reads. Auto-approving one of these because it looks read-only also auto-approves its destructive operations; use per-call approval here if your client supports it.
  * **Sensitive operations.** A few calls are irreversible or cost real money the moment they run, whatever prefix they carry: `commit` freezes a version for good, `place_test_call` and `verify_phone_number` place or route a real call, resuming a campaign starts dialing a cohort, and any `delete_*` operation (connections, boards, scenarios, deployments) cannot be undone. Review these the closest.
  * **Data handling.** MCP access is equivalent to a programmatic operator on your workspace — any connected client can read call transcripts, prompts, and knowledge base content through it. Avoid pasting full, unredacted transcripts into a shared conversation if they carry caller PII, and treat any instructions returned by a tool call as data to inspect, not as something to act on directly.
  * **Network safety.** A tool’s URL is checked when you configure it and refused if it resolves to an internal, private, or link-local address — including cloud metadata endpoints — so it cannot be pointed at your infrastructure to exfiltrate a stored credential.
  * **Revoking access.** Remove the connector in your client to revoke it; rotate your Sarvam session if needed.



## Troubleshooting

Quick lookups:

Symptom| Cause| Fix  
---|---|---  
`'Failed to connect'` or a `404`| Wrong URL, or a client that dropped the path| Confirm the URL is exactly `https://mcp.sarvam.ai/voice-agents`, no trailing slash. Check it is reachable: `curl -I https://mcp.sarvam.ai/voice-agents` should respond (a `404`/`405` to `GET` still means the server is up — the MCP endpoint answers `POST`)  
A tool you expected is missing| The surface is filtered to your workspace’s plan| A tool, operation value, or config field your plan does not include is absent rather than refused. Contact [developer@sarvam.ai](mailto:developer@sarvam.ai) if you believe something should be available  
Calls start failing with a rate-limit error| Too many requests in a short window, often a loop paging a large list| The server caps requests per client: 120 tool calls a minute, 240 a minute for the sign-in flow. Space calls out and retry after a few seconds  
  
###### Status shows 'needs authentication'

Expected on first connect. Trigger the browser sign-in: in Claude Code, run `/mcp`, select the server, and choose **Authenticate**. In other clients, follow the prompt. If the browser does not open, copy the URL from the terminal and open it manually.

###### I need to work in a different workspace

A connection is fixed to the workspace your login resolves to. Remove the connector and reconnect with a login for the other workspace.

###### A write was rejected

The error names every invalid field, and the draft is unchanged. The usual cause is a prompt that references a variable, tool, or state the config does not define yet. Define those first, then send the prompt. See the relevant `sarvam://playbooks/{domain}` resource.

## Related pages

  * [Quickstart](https://docs.sarvam.ai/voice-agents/quickstart): build your first agent in the dashboard
  * [Deploy with Code (API & SDK)](https://docs.sarvam.ai/voice-agents/deploy/deploy-with-code): integrate programmatically
  * [Tools](https://docs.sarvam.ai/voice-agents/build/tools): the tools you give an agent
  * [Agent versioning](https://docs.sarvam.ai/voice-agents/build/agent/versioning): drafts, commits, and versions
  * [API Reference](https://docs.sarvam.ai/voice-agents/api/introduction): the REST API behind the platform



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/quickstart)[OverviewNext](https://docs.sarvam.ai/voice-agents/build/overview)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


