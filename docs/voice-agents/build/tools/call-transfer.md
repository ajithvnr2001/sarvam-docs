---
url: https://docs.sarvam.ai/voice-agents/build/tools/call-transfer/
title: Call transfer | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:23.719975+00:00
---

# Call transfer | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/build/tools/call-transfer/

Skip to navigation

On this page

  * When the agent should transfer
  * Supported telephony
  * Destination types
  * How to configure
  * Example
  * After a transfer
  * Best practices
  * Troubleshooting
  * Next



Scroll to top

[Build](https://docs.sarvam.ai/voice-agents/build/overview)[Agent](https://docs.sarvam.ai/voice-agents/build/agent/overview)[Tools](https://docs.sarvam.ai/voice-agents/build/tools)

# Call transfer

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer.md "View this page as plain text")|More actions

This page is for Voice Agents.

Call transfer lets a voice agent hand a live phone call to a human, another number, or your own SIP trunk when the conversation needs it - an escalation, a specialist, or an explicit request to speak to someone.

It is a [core tool](https://docs.sarvam.ai/voice-agents/build/tools/core-tools). You configure the destination under **Settings → In Call Actions** ; the model decides _when_ to transfer from the conversation.

Call transfer is available on **phone calls**. It is not available in chat or the browser voice tester.

## When the agent should transfer

Write a clear instruction so the model transfers at the right moment. Typical triggers:

  * The caller asks to speak to a human, an agent, or a named team (sales, billing, collections)
  * The request needs human judgment the agent cannot complete
  * An escalation rule fires (for example, a dispute, a cancellation, or a complaint)



Be specific in the [instruction](https://docs.sarvam.ai/voice-agents/build/system-prompt). Type `@` and insert the **`call_transfer`** tool so the agent knows exactly what to call. “When the caller asks for a refund, confirm they want a human, then transfer using `call_transfer`” works better than “transfer the call”.

![The Instructions editor with a refund-handoff prompt that ends in the call_transfer tool chip.](https://docs.sarvam.ai/_fern-img/1dd2186771cf94a3924b16aa06c3516ee02416b0f849dcd14b7f76eebdfec749.webp)

Instruction that transfers a refund request with the call_transfer tool.

## Supported telephony

Provider| Call transfer  
---|---  
**[Vobiz](https://docs.sarvam.ai/voice-agents/deploy/telephony/vobiz)** (your own account or [Rent from Sarvam](https://docs.sarvam.ai/voice-agents/deploy/telephony/rent-from-sarvam))| Supported end to end. No extra setup on the Vobiz platform.  
**[Plivo](https://docs.sarvam.ai/voice-agents/deploy/telephony/plivo)**|  Supported end to end. No extra setup on the Plivo platform.  
  
Call transfer is not self-serve on other telephony providers.

Prefer Vobiz or Plivo if you want to configure and test transfers yourself. Numbers rented through **Rent from Sarvam** use Vobiz underneath, so they support call transfer the same way.

## Destination types

Choose one destination type per agent. The value can be fixed, or read from an [agent variable](https://docs.sarvam.ai/voice-agents/build/variables-personalization) at runtime.

Type| Format| Example  
---|---|---  
**Phone number (PSTN)**|  E.164| `+919876543210`  
**SIP URI**|  SIP address| `sip:support@example.com`  
  
Use a **variable** when the destination depends on the caller - for example a campaign column, an on-start CRM lookup, or a language-specific queue. The variable’s value is resolved when the transfer runs.

The destination must answer. A number that rings out, goes to voicemail, or rejects the call looks like a failed transfer even when the agent invoked the tool correctly. Test with a phone you control.

## How to configure

Call transfer is configured as **Call forwarding** under **Settings → In Call Actions**.

![Call forwarding settings with the toggle on, Destination type set to Phone number, Value type set to Static value, and Forward to set to +919876543210.](https://docs.sarvam.ai/_fern-img/a77d63216ef1ba4bbf222c8f589c2f5e3acba59f51434aabf76b1934706775bf.webp)

Call forwarding in Settings → In Call Actions: destination type, value type, and the number to forward to.

[1](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer#open-the-agent)

### Open the agent

In Voice Agents, open the agent you want to transfer from.

[2](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer#go-to-settings--in-call-actions)

### Go to Settings → In Call Actions

On the Canvas, open **Settings** , then **In Call Actions**.

[3](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer#turn-on-call-forwarding)

### Turn on Call forwarding

Enable **Call forwarding** , then set **Destination type** to **Phone number** or **SIP URI**.

[4](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer#set-the-destination)

### Set the destination

Set **Value type** to **Static value** and enter the number or SIP URI in **Forward to**. Or bind an [agent variable](https://docs.sarvam.ai/voice-agents/build/variables-personalization) so the value is filled at runtime.

[5](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer#tell-the-agent-when-to-transfer)

### Tell the agent when to transfer

In the [instruction](https://docs.sarvam.ai/voice-agents/build/system-prompt), state the conditions and insert **`call_transfer`** with `@`. For example: “When the user requests a refund, acknowledge the request, confirm they want a human support agent, and, upon confirmation, transfer the call using `call_transfer`.”

[6](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer#commit-and-test-on-a-phone)

### Commit and test on a phone

[Commit](https://docs.sarvam.ai/voice-agents/build/agent/versioning) the agent, then place a real [phone](https://docs.sarvam.ai/voice-agents/build/navigating-workspace#testing-the-agent) call. Browser voice and chat cannot exercise a transfer.

## Example

**Caller:** “Can I talk to someone on your sales team?”

**Agent:** “Sure, I’ll connect you now.”

The agent calls `call_transfer`. The live call is bridged to the configured sales number or SIP URI.

## After a transfer

Transferred calls are visible in [Call Logs](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/call-logs) like any other conversation.

  * **End Reason** is `CALL_TRANSFER` when the agent handed the call off.
  * Transfer **status** and the **recording of the transferred leg** are captured, so you can see whether the destination answered and what happened after the handoff.



Filter Call Logs by agent, campaign, or date, then look for `CALL_TRANSFER` in **End Reason**.

## Best practices

  * **Be specific in the prompt.** Name the situations that should transfer (human request, billing dispute, cancellation) instead of a generic “escalate if needed”.
  * **Confirm the destination is reachable** before you go live - a wrong number or an unmanned queue fails the caller, not just the metric.
  * **Use a variable for routing.** When sales and support should land on different numbers, set the destination from a campaign column or an [on-start hook](https://docs.sarvam.ai/voice-agents/build/on-start-on-end-hooks), rather than hard-coding one number for every caller.
  * **Plan for a failed transfer.** Tell the agent what to say and do if the destination does not answer - offer a callback, take a message, or continue the conversation.
  * **Test on the same telephony you will use in production.** A transfer that works on Vobiz is not a test of an Exotel number.



## Troubleshooting

Symptom| What to check  
---|---  
The agent says it cannot transfer| Call transfer is not enabled on the agent, or the call is not on a [supported provider](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer#supported-telephony).  
The agent says it will transfer, but nothing happens| The model announced the intent and did not call the tool. Tighten the instruction so the transfer step is unambiguous.  
The transfer fires, but nobody picks up| The destination did not answer. Confirm the number or SIP URI, and that a person or queue is staffed.  
You are on Exotel and transfers do not complete| Call transfer on Exotel is not self-serve. [Contact the Sarvam team](mailto:support@sarvam.ai).  
Browser or chat tests never transfer| Expected. Use **test agent → Phone** , or a live inbound / campaign call.  
  
## Next

[Core toolsOther built-in tools the harness provides.](https://docs.sarvam.ai/voice-agents/build/tools/core-tools)[VariablesPass a dynamic transfer destination at runtime.](https://docs.sarvam.ai/voice-agents/build/variables-personalization)[VobizConnect Vobiz - the provider with end-to-end transfer support.](https://docs.sarvam.ai/voice-agents/deploy/telephony/vobiz)[Call LogsFind transferred calls by End Reason.](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/call-logs)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/build/tools/core-tools)[API toolNext](https://docs.sarvam.ai/voice-agents/build/tools/https-tool)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


