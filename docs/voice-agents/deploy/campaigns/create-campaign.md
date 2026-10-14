---
url: https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign/
title: Create a campaign | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:26.312896+00:00
---

# Create a campaign | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign/

Skip to navigation

On this page

  * Test dial
  * Phone number rotation
  * Enable phone number rotation
  * Where to go next



Scroll to top

[Deploy](https://docs.sarvam.ai/voice-agents/deploy/overview)[Campaigns](https://docs.sarvam.ai/voice-agents/deploy/campaigns)

# Create a campaign

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign.md "View this page as plain text")|More actions

This page is for Voice Agents.

From **Deploy → Campaigns** , click **Create Campaign** to open the **Schedule campaign** wizard. It has four steps — **Agent** , **Recipients** , **Schedule** , and **Review & Launch** — shown as tabs across the top, with a **Step X of 4** counter at the bottom. Move forward with **Next** and back with **Back** ; your progress is kept as you move between steps.

Closing the wizard before you launch prompts **Discard campaign?** — all progress is lost and the action can’t be undone. Choose **Keep editing** to return, or **Discard** to abandon it.

By default you can have **10 concurrent agent campaigns**. Concurrent means campaigns that are **Active** or **Scheduled**. The limit is checked when you **create** an agent campaign and when you **pause** an agent campaign. [Contact the Sarvam team](https://www.sarvam.ai/contact-us) if you need a higher limit.

[1](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign#agent)

### Agent

Choose what runs the campaign and where it dials from:

  * **Campaign name** — a clear name for the campaign.
  * **Select agent** — the agent, plus the committed **Version** to run.
  * **Connections** — pick a telephony **Connection** , then the **Phone numbers** to dial from. Toggle **By number** to choose individual numbers, or **By group** to use a whole [group](https://docs.sarvam.ai/voice-agents/deploy/telephony/groups).



Click **Next** to continue.

[2](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign#recipients)

### Recipients

Upload your contact list (cohort) and map its columns to the agent’s variables.

  * **Upload cohort** — drop in a CSV. Each row must include a phone number plus any details your agent uses during the call. Use **Download Sample** if you need the expected format.
  * **Cohort name** — a name for this batch of contacts. (A [cohort](https://docs.sarvam.ai/voice-agents/deploy/campaigns/cohorts) is the batch you upload; every campaign starts with one and you can add more later.)
  * **Map phone number and agent variables to columns** — match each agent field to a CSV column. **Preview sample row** shows the mapped values for one row; use **Random** / **Pick random row** to spot-check different rows.



The mapping table has a row per field:

Column| What it does  
---|---  
**Field**|  The agent variable to fill (for example `Phone Number`, `developer_name`, `gender`).  
**CSV column**|  The column from your file to pull the value from — search the list, or set **None** to leave it unmapped.  
**Required**|  Marks the field as mandatory. **Phone Number** is always required.  
**Formatting functions**|  An optional transform applied to the raw CSV value before the call (see below).  
**Preview**|  The resulting value for the previewed row.  
  
###### Formatting functions

Add a transform under **Formatting functions → Add** to clean or reshape a column before it reaches the agent:

  * **Indian Currency** — format a number as Indian currency.
  * **Date** — normalize a date value.
  * **String Replace** — find and replace within the text.
  * **String Strip** — trim surrounding whitespace.
  * **String Capitalize** — capitalize the value.
  * **Indian State Language Map** — map an Indian state to its language.
  * **Format Language Name** — normalize a language name.



###### Override default values

Expand **Override default values** to map CSV columns onto per-contact conversation defaults — **Initial message** , **Initial state** , and **Initial language**. Left as **None** , each call uses the agent’s configured default; map a column to personalize it per contact.

Click **Validate** to check the file and mapping before continuing. Validation reports how many rows are **valid** versus **removed**.

[3](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign#schedule)

### Schedule

Set when the campaign runs and how it retries:

  * **Campaign period** — **Start date time** (**Now** , or a **Custom** date and time) and **End date time** (**Today** , or **Custom**). Starting **Now** kicks off roughly two minutes after scheduling.
  * **Attempts per second** — the dialing rate (calls placed each second). Defaults to `2`. Dialing too aggressively can flag your numbers as spam — start low and watch [Connectivity](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/connectivity). See [Dialing rate & concurrency](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dialing-rate) for how this interacts with concurrency and your plan limits.
  * **Allowed days** — the days of the week the campaign may dial.
  * **Calls allowed between** — the daily time window (for example `09:00 am`–`06:00 pm`).
  * **Retry configuration** — a toggle. Leave it **off** to dial each contact once; turn it **on** to retry unanswered contacts (see below).
  * **Advanced → Webhook URL** — an optional endpoint that receives an event as each call finishes.
  * **Advanced → Phone number rotation** — retry the same contact from a different agent number each time. See [Phone number rotation](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign#phone-number-rotation) below.



###### Retry configuration

With retries **on** :

  * **Max retries** — `0`–`20` (default `3`).
  * **Retry interval** — minutes between attempts (default `30`). Tick **Customize interval per attempt** to set a different gap for each attempt.
  * **Retry on** — which outcomes trigger a retry:



Outcome| Notes  
---|---  
**Busy**|  Line was busy.  
**No Answer**|  Rang but wasn’t picked up.  
**Failed**|  The call failed to connect.  
**Short Duration**|  Connected but ended too quickly — set the **threshold (seconds)** below which it counts as short.  
**Provider Error**|  A telephony-provider error — set its own **Max retries** and **Interval (min)**.  
**Internal Error**|  A system-side error — set its own **Max retries** and **Interval (min)**.  
  
[4](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign#review--launch)

### Review & Launch

A read-only summary of every step — **Agent** (agent and version, campaign name, connection, phone numbers), **Recipients** (file, valid/removed row counts, mappings), and **Schedule** (period, allowed time, days, CPS, retries). Expand a section to double-check the details.

Optionally run a **Test dial** (below), then tick **I have reviewed this campaign and I am ready to launch** and click **Launch**.

## Test dial

On the **Review & Launch** step, **Test dial** (_optional but recommended_) places an instant outbound call to a few internal numbers so you can verify the agent works end-to-end before going live.

  * Test calls dial **from this campaign’s numbers** , but **don’t count toward campaign metrics**.
  * The agent uses the variables from **one cohort row** — the previewed row is shown, and **Pick random row** swaps it. Complete the cohort mapping first, otherwise no preview variables are available.
  * Under **Test numbers** , select up to **5** numbers (or **Add a number**), then click **Place test calls**.



## Phone number rotation

When phone number rotation is enabled, every subsequent call to the same user uses a different agent number until each number in your pool has been used once for that user.

If User X gets a no-answer on +91-111, the retry to User X will not call from +91-111 again. It picks from the other numbers in the pool (for example +91-222 or +91-333). Only after all numbers have been used for User X does the pool reset and reuse begin.

Use it when a campaign has multiple outbound numbers and you want retries to the same contact to come from a fresh caller ID each time — for example, to avoid a contact learning to ignore one number.

Rotation only applies on agent campaigns, and you need **two or more agent numbers** on the campaign (the **Agent** step) for it to have an effect.

### Enable phone number rotation

**UI** — in the campaign wizard:

  1. **Agent** — select a connection and two or more phone numbers (or a group with multiple numbers).
  2. **Schedule** — set campaign period, dialing rate, and retries. Expand **Advanced**.
  3. Turn **Phone number rotation** on.
  4. Continue to **Review & Launch**, then launch.



The **Advanced** panel also includes an optional **Webhook URL** ; rotation is controlled only by the **Phone number rotation** toggle.

**API** — set `phone_rotation.agent` to `true` on `app_config` when creating or updating a campaign:
    
    
    {
    
      "phone_rotation": {
    
        "agent": true
    
      }
    
    }

Full `app_config` example:
    
    
    {
    
      "app_config": {
    
        "app_id": "your-agent-id",
    
        "app_version": 1,
    
        "app_type": "agent",
    
        "attempts_per_second": 1.0,
    
        "connection_configs": [
    
          {
    
            "connection_id": "Exotel-Sarv-0f9a37e1-adf6",
    
            "phone_numbers": [
    
              "+918048637405",
    
              "+912048566401",
    
              "+917948229334"
    
            ],
    
            "weight": 1
    
          }
    
        ],
    
        "retry_config": {
    
          "max_retries": 3,
    
          "retry_interval_minutes": [5, 5, 5],
    
          "retry_on": {
    
            "busy": { "enabled": true },
    
            "failed": { "enabled": true },
    
            "no_answer": { "enabled": true }
    
          }
    
        },
    
        "phone_rotation": {
    
          "agent": true
    
        }
    
      }
    
    }

Field| UI equivalent| Description  
---|---|---  
`phone_rotation.agent`| **Phone number rotation** toggle| `true` = on; `false` (default) = off  
`connection_configs[].phone_numbers`| **Agent** step phone selection| Numbers in the rotation pool — need at least two  
  
Create: `POST /api/scheduling/v1/orgs/{org_id}/workspaces/{workspace_id}/campaigns`

Update: `PATCH /api/scheduling/v1/orgs/{org_id}/workspaces/{workspace_id}/campaigns/{campaign_id}` — pass the full updated `app_config` while the campaign is **Scheduled** or **Paused**.

Start with a low **Attempts per second** and a small cohort, place a **Test dial** to confirm the agent behaves, then watch [Connectivity](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/connectivity) for the first hour before scaling up. See [Best practices](https://docs.sarvam.ai/voice-agents/deploy/campaigns/best-practices) for the full launch checklist.

## Where to go next

[CohortsAdd more contact batches to a running campaign.](https://docs.sarvam.ai/voice-agents/deploy/campaigns/cohorts)[Campaign detailsTrack metrics, cohorts, and schedules once it’s live.](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-details)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/deploy/campaigns)[Campaign detailsNext](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-details)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Create a campaign](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign)
      * [Campaign details](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-details)
      * [Cohorts](https://docs.sarvam.ai/voice-agents/deploy/campaigns/cohorts)
      * [Dialing rate & concurrency](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dialing-rate)
      * [Campaign lifecycle](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-lifecycle)
      * [Do Not Disturb (DND)](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dnd)
      * [Best practices](https://docs.sarvam.ai/voice-agents/deploy/campaigns/best-practices)

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


