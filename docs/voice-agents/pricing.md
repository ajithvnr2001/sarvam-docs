---
url: https://docs.sarvam.ai/voice-agents/pricing/
title: Voice Agents Pricing in India: Per-Minute Rates in INR | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-23T06:39:02.235639+00:00
---

# Voice Agents Pricing in India: Per-Minute Rates in INR | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/pricing/

Skip to navigation

On this page

  * Plans
  * What counts as a minute
  * Estimate your monthly cost
  * Telephony and phone numbers
  * Testing
  * Rate limits
  * FAQ



Scroll to top

[Settings](https://docs.sarvam.ai/voice-agents/settings/api-key)

# Pricing

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/pricing.md "View this page as plain text")|More actions

This page is for Voice Agents.

Sarvam Voice Agents is billed per minute of conversation. The rate is end to end: it covers the platform that runs your agent and the speech recognition, language, and voice models behind it. There is no separate model or token charge.

Prices are in Indian rupees (₹) and exclude GST.

## Plans

Plan| Voice agent rate| Minimum subscription| Best for  
---|---|---|---  
Pay as you go| ₹3.50 per minute| None| Under 3,000 minutes a month  
Pro| ₹3.25 per minute| ₹9,999| 3,000 to 16,000 minutes a month  
Growth| ₹3.15 per minute| ₹49,999| 16,000 to 65,000 minutes a month  
Business| ₹3.00 per minute| ₹1,99,999| 65,000 minutes to 2 lakh minutes a month  
Enterprise| Custom| Committed volume| 2 lakh minutes a month and above  
  
  * **Self-serve plans are prepaid.** A paid plan is a minimum monthly subscription that comes back in full as credits, one credit per rupee. Minutes beyond those credits are billed at the same plan rate from your credit balance.
  * **Enterprise is postpaid.** Pricing is set on your committed monthly volume, and you are invoiced monthly for the minutes you use, with your commitment as the minimum. Enterprise also adds workflows, WhatsApp campaigns, custom tool authoring, custom rate limits, and forward deployed engineering support. [Talk to sales](https://www.sarvam.ai/contact-us).



Choose or change a plan in the [Sarvam platform](https://indus.sarvam.ai/samvaad/pricing).

## What counts as a minute

A minute is one 60-second pulse, and each call is rounded up to whole pulses. A 45-second call counts as 1 minute, and a 61-second call counts as 2 minutes. On pay as you go, that is ₹3.50 and ₹7.00.

## Estimate your monthly cost

On a paid plan, you pay the plan’s minimum monthly subscription or your minutes multiplied by the plan rate, whichever is higher:
    
    
    monthly cost = max(plan minimum subscription, minutes × plan rate)

On pay as you go there is no minimum, so the cost is `minutes × ₹3.50`.

Minutes a month| Plan| Monthly cost| On pay as you go  
---|---|---|---  
1,000| Pay as you go| ₹3,500| ₹3,500  
10,000| Pro| ₹32,500| ₹35,000  
50,000| Growth| ₹1,57,500| ₹1,75,000  
1,00,000 (1 lakh)| Business| ₹3,00,000| ₹3,50,000  
2,00,000 (2 lakh) and above| Enterprise| [Talk to sales](https://www.sarvam.ai/contact-us)| ₹7,00,000  
  
Telephony, phone numbers, and test runs are billed on top, at the rates below.

## Telephony and phone numbers

Telephony is metered separately from agent minutes, in 30-second pulses, each rounded up. Rates are the same on every plan.

Item| Price| Billed per  
---|---|---  
Bring your own telephony| Free| Your provider bills you directly  
Sarvam telephony (Vobiz)| ₹0.20| 30-second pulse  
Call forwarding to a phone number (PSTN)| ₹0.40| 30-second pulse  
Call forwarding to a SIP destination| ₹0.35| 30-second pulse  
Phone number rental (11, 79, or 80 series)| ₹59| Number, per 30 days  
  
  * **Bring your own telephony.** Exotel, Smartflo, Plivo, Twilio, Vobiz, InTalk, and Pulse connect self-serve. Custom SIP is available on Business and Enterprise and is set up by the Sarvam team. See [Bring your own telephony](https://docs.sarvam.ai/voice-agents/deploy/telephony/bring-your-own).
  * **Rent a number from Sarvam.** Rented numbers renew every 30 days until you cancel. See [Rent a number from Sarvam](https://docs.sarvam.ai/voice-agents/deploy/telephony/rent-from-sarvam).
  * **Forwarded calls.** Once the agent forwards a call, it is off the call, so the forwarded part is charged only as telephony, not as agent minutes. For example, if the agent hands over after 50 seconds and the forwarded call lasts 2 minutes, you pay 1 agent minute plus 4 forwarding pulses (₹1.60 to a phone number).



A 45-second call on Sarvam telephony is 1 agent minute and 2 telephony pulses. On pay as you go, that is ₹3.50 for the agent and ₹0.40 for telephony.

## Testing

Item| Price| Billed per  
---|---|---  
Simulated test run| ₹2| Run  
  
Simulated runs [test an agent](https://docs.sarvam.ai/voice-agents/build/tests) against scripted scenarios before it takes real calls.

## Rate limits

Plan| Concurrent calls| Calls started per minute  
---|---|---  
Pay as you go| 4| 20  
Pro| 10| 50  
Growth| 30| 150  
Business| 200| 800  
Enterprise| Custom| Custom  
  
Limits apply across your organisation. Every campaign, instant outbound call, and inbound call counts toward them, and a call that would go past a limit is rejected.

As a guide, the concurrent calls you need are roughly the calls you start per second, times your connect rate, times your average talk time in seconds. If your plan’s limits are not enough, upgrade to the next plan or talk to sales about Enterprise limits.

The [concurrent agent campaign limit](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-lifecycle) is separate from your plan. If you hit it, too many campaigns are active or scheduled at the same time. Pause or stop some campaigns to continue. Upgrading your plan does not raise it.

## FAQ

###### How much does a voice AI agent cost per minute in India?

On Sarvam Voice Agents, ₹3.50 per minute on pay as you go, ₹3.25 on Pro, ₹3.15 on Growth, and ₹3 on Business. From 2 lakh minutes a month, Enterprise pricing is set on your committed volume. Prices are in rupees and exclude GST.

###### Is there additional pricing for the models?

No. The per-minute rate covers the platform that runs your agent and the speech recognition, language, and voice models behind it. The only items billed on top are telephony, phone numbers, and simulated test runs.

###### Which plan should I choose?

Pay as you go below 3,000 minutes a month, Pro from 3,000, Growth from 16,000, and Business from 65,000 minutes. From 2 lakh minutes a month, talk to sales about Enterprise.

###### Is telephony included in the per-minute rate?

No. Telephony and phone number rental are billed separately at the rates in [Telephony and phone numbers](https://docs.sarvam.ai/voice-agents/pricing#telephony-and-phone-numbers). Bringing your own telephony provider is free on Sarvam, and your provider bills you directly.

###### What happens if I use more minutes than my plan's credits?

Your agents keep taking calls. Extra minutes are billed at your plan’s per-minute rate from your credit balance.

###### Am I charged for unanswered, busy, or voicemail calls?

Only calls that connect are charged. A call that is not answered, is busy, or fails to connect costs nothing, with no agent minutes and no telephony charge. A call answered by voicemail has connected, so it is billed like any other call, for as long as the agent stays on the line.

###### What happens if my credits run short when a number renews?

A rented number renews every 30 days, and the rental is taken from your credit balance at the rate in [Telephony and phone numbers](https://docs.sarvam.ai/voice-agents/pricing#telephony-and-phone-numbers). If your credits can’t cover it on the renewal date, the number is released, and the campaigns and deployments using it are cancelled. There is no grace period, so keep enough credits for every number before it renews. The **Renews At** column on the phone numbers page shows each date.

###### Which languages do the agents speak?

11 Indian languages and English: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, and Assamese. Agents also handle code-mixed speech.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/settings/extensions)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
    * [Call recordings](https://docs.sarvam.ai/voice-agents/monitor/call-recordings)
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
  * [Call recordings](https://docs.sarvam.ai/voice-agents/monitor/call-recordings)
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
  * [Get forwarded recording](https://docs.sarvam.ai/voice-agents/api/analytics/forwarded-recordings)
  * [Get transcript](https://docs.sarvam.ai/voice-agents/api/analytics/transcripts)
  * [Get trace](https://docs.sarvam.ai/voice-agents/api/analytics/traces)
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


