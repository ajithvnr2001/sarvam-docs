---
url: https://docs.sarvam.ai/voice-agents/build/genie/
title: Genie | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-17T14:23:31.942677+00:00
---

# Genie | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/build/genie/

Skip to navigation

On this page

  * Opening Genie
  * Chats and context
  * Build and refine agents
  * Connect an agent to a phone number
  * Create and run campaigns
  * Analyze calls
  * Confirmations and safeguards
  * Good to know



Scroll to top

[Build](https://docs.sarvam.ai/voice-agents/build/overview)

# Genie

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/build/genie.md "View this page as plain text")|More actions

This page is for Voice Agents.

Genie is the AI assistant built into Voice Agents. Describe what you want in plain language and Genie does the work on the platform for you - from drafting a new agent, to putting it live on a phone number, to launching an outbound campaign and explaining why calls didn’t connect.

Describe an agent and Genie builds it, connects it to a phone number, launches an outbound campaign, and explains why calls dropped - all from one chat.

Area| What you can ask Genie to do  
---|---  
[**Build**](https://docs.sarvam.ai/voice-agents/build/genie#build-and-refine-agents)|  Create and edit agents - instructions, variables, tools, voice, languages, knowledge bases, and test suites.  
[**Deploy**](https://docs.sarvam.ai/voice-agents/build/genie#connect-an-agent-to-a-phone-number)|  Find your phone numbers, put an agent live on a number for inbound calls, and place a test call to your phone.  
[**Campaigns**](https://docs.sarvam.ai/voice-agents/build/genie#create-and-run-campaigns)|  Create outbound campaigns, upload contact lists, and pause, resume, edit, or cancel them.  
[**Analyze**](https://docs.sarvam.ai/voice-agents/build/genie#analyze-calls)|  Summarize call performance, diagnose failed calls, read transcripts, check tool errors, and build Boards.  
  
Genie can only use the platform features available to your plan and workspace. If a feature (for example, workflows) isn’t enabled for your workspace, Genie will tell you it can’t do that yet.

## Opening Genie

Genie lives in a panel docked to the right of every Voice Agents page. Because the panel stays open as you move between pages, one conversation can span building an agent, deploying it, and checking its calls.

There are several ways to open it:

  * **Ask Genie** \- the button at the top right of the page header on Agents, Campaigns, Inbound calls, Boards, and other pages. It’s hidden while the Genie panel is already open.
  * **Agents home** \- type into **What should your voice agent do?** on **Build → Agents**. Genie creates a new agent, opens it in the editor, and starts building from your description. Use **Create from scratch** if you’d rather start with a blank agent.
  * **Improve with Genie** \- the button in the agent editor header. Genie and **Test agent** share the same side panel, so opening one closes the other.
  * **Customise with AI** \- on a template, clones it and asks Genie to adapt it to your use case.



![The Agents page with the Ask Genie button in the header, the prompt "What should your voice agent do?", and Create from scratch.](https://docs.sarvam.ai/_fern-img/f0cc6783f476163244bcfa873bf40138d543f9b8aa85f028af36cc0b67ad09ba.webp)

The Agents homepage: describe an agent for Genie to build, or click Ask Genie at the top right to open the panel.

![The Genie panel docked on the right with the heading "What's on your mind?" and suggested prompts.](https://docs.sarvam.ai/_fern-img/aa1392d3c18ee8fdb049dee2e6affe0e24eef88d36b5863cbb57930aae77ff14.webp)

The Genie panel, with starter suggestions and a message box.

### Chats and context

  * **Genie knows where you are.** Each message includes the page you’re on - the agent, campaign, knowledge base, or board you’re viewing - so “pause this campaign” or “why are calls failing here?” just works.
  * **Chats belong to your workspace, not to a single agent.** Use **New chat** to start fresh and **Chat history** to search and reopen past chats. Genie reopens your most recent chat when you come back.
  * **Pages refresh automatically.** When Genie changes something - an agent, a deployment, a campaign, a board - the page you have open updates without a reload.
  * **Queue follow-ups.** You can type up to five more requests while Genie is working, or press **Stop** to cancel the current one.
  * Rate any reply with **Good response** or **Bad response** to help us improve Genie.



## Build and refine agents

Describe the agent you want and Genie runs a guided build: it asks a few questions one at a time, shows a **Build plan** , and then works through it - inputs and outputs, tools, instructions, guardrails, greeting, languages, voice, call handling (voicemail and silence), and the call goal - before a final quality pass and a saved version. When the plan is done, a **Plan has been executed** strip appears with a **Test agent** button.

On an existing agent, Genie makes simple changes directly and proposes a plan for larger ones. It can:

  * Rewrite or tighten the [instructions](https://docs.sarvam.ai/voice-agents/build/system-prompt) and greeting, or restore the previous version of the prompt after a rewrite.
  * Add or change [variables](https://docs.sarvam.ai/voice-agents/build/variables-personalization), including post-call extraction (for example, “did the customer promise to pay, and when?”).
  * Set up [API tools](https://docs.sarvam.ai/voice-agents/build/tools/https-tool) through a setup card. Credentials go in a masked field and are never shown in chat.
  * Configure [call transfer](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer) to a human.
  * Change [languages, voice, pitch, and pace](https://docs.sarvam.ai/voice-agents/build/voice-language), and add pronunciation rules.
  * Create a [knowledge base](https://docs.sarvam.ai/voice-agents/build/knowledge-base) from files you upload in chat and attach it to the agent.
  * Create [test suites and scenarios](https://docs.sarvam.ai/voice-agents/build/tests), run them, and summarize the results.
  * Review the agent and resolve open suggestions on the canvas.



![The Genie panel showing a completed five-step build plan for Priya, an EMI reminder agent, followed by its input and output variables.](https://docs.sarvam.ai/_fern-img/2a8d80d1b334abb00a460a031418cc3e0f31815e4029423a827574e8f52b8a0d.webp)

Genie builds an agent from a one-line description: a build plan, then a saved version and a summary of its variables.

###### Example prompts

  * “Create a voice agent that calls customers 3 days before their EMI is due and reminds them to pay.”
  * “Make the agent speak Hindi and Tamil too, and start in Hindi.”
  * “Switch to a calmer female voice and slow the pace down a little.”
  * “Capture whether the customer promised to pay and the promised date after each call.”
  * “Transfer the call to a human when the caller asks for one.”
  * “Create a few test scenarios for angry customers and run them.”



In the editor, you can also select text in the instructions and type in **Describe a change…** for a targeted edit. See [Navigating the build interface](https://docs.sarvam.ai/voice-agents/build/navigating-workspace).

## Connect an agent to a phone number

Genie can take an agent from the editor to a live phone line. It can:

  * List your [telephony connections and phone numbers](https://docs.sarvam.ai/voice-agents/deploy/telephony), and manage [number groups](https://docs.sarvam.ai/voice-agents/deploy/telephony/groups).
  * Create an [inbound deployment](https://docs.sarvam.ai/voice-agents/deploy/inbounds) that puts an agent on one or more numbers, with optional answering hours (24/7 by default) and a call-end webhook.
  * Pause, resume, or delete a deployment, or switch it to a newer version of the agent.
  * Upload a known-callers list so the agent can greet returning callers by name.
  * **Place a test call to your phone.** Genie first sends a one-time code by SMS to verify your number, then calls up to 10 verified numbers so you can hear the agent.



Genie asks which connection to use and then which number. It only uses numbers that are already connected to your workspace - to add new numbers, see [Bring your own telephony](https://docs.sarvam.ai/voice-agents/deploy/telephony/bring-your-own) or [Rent from Sarvam](https://docs.sarvam.ai/voice-agents/deploy/telephony/rent-from-sarvam).

![The Genie panel asking which phone number to use, then confirming the agent is live for inbound calls.](https://docs.sarvam.ai/_fern-img/96ad76994d3e638bcf76b940cf951b5843476b237188661bb7966939ca5eda8d.webp)

Asking Genie to put an agent live on a phone number.

###### Example prompts

  * “Which phone numbers do we have connected?”
  * “Put my Support Agent live on our Exotel number for inbound calls.”
  * “Only answer calls Monday to Saturday, 9 am to 7 pm.”
  * “Move the inbound deployment to the version I just saved.”
  * “Call me so I can hear the agent.”
  * “Pause the inbound line for the Collections agent.”



Deployments and campaigns always run a **saved version** of your agent, never the unsaved draft. A test call can use the draft. Test calls are real calls and use credits.

## Create and run campaigns

Genie can set up and manage [outbound campaigns](https://docs.sarvam.ai/voice-agents/deploy/campaigns) end to end:

  * **Create a campaign** with the agent and version, caller numbers, [dialing rate](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dialing-rate), retry rules (for example, retry busy and no-answer twice after 30 minutes), calling window (days and hours, in IST by default), and start and end dates.
  * **Upload contacts.** Share a CSV in chat and Genie maps its columns to the agent’s variables - phone number, customer name, due date, and so on. It reports how many rows were accepted and why any were rejected. See [Cohorts](https://docs.sarvam.ai/voice-agents/deploy/campaigns/cohorts).
  * **Manage the campaign** \- pause, resume, extend the end date, change the calling window, or cancel it.
  * **Webhooks** \- check call-end webhook deliveries and retry the ones that failed.
  * **Do Not Disturb** \- add, remove, or look up numbers on your workspace’s [DND list](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dnd), or import one from a CSV (where DND is enabled).



A campaign starts dialing on its schedule as soon as it’s created, so Genie always asks you to confirm before creating one.

![The Genie panel beside Outbound Campaigns, with answered questions for caller number and retries, and a summary of the new scheduled EMI reminder campaign.](https://docs.sarvam.ai/_fern-img/130e8a2cdfd9eae2a3468a1c832e5d51e4ec6bfb467cdd8603d197f17488f2cf.webp)

Genie asks for the caller number and retry rules, then creates the campaign and summarizes its settings.

###### Example prompts

  * “Set up an outbound campaign for the EMI reminder agent, calling weekdays 10 am to 6 pm.”
  * “Dial at 1 call per second and retry busy and no-answer twice after 30 minutes.”
  * “Here’s the contact list. The phone column is ‘mobile’ and ‘name’ is the customer name.”
  * “How many rows were rejected from the upload, and why?”
  * “Pause the March reminders campaign.”
  * “Add this number to the do-not-call list.”



## Analyze calls

Ask Genie questions about how your agents and campaigns are performing, and it pulls the data from [Agent Analytics](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics) and answers in chat:

  * **Performance summaries** \- call volume, engagement, and connect rates for an agent, several agents, your whole workspace, or a single campaign, over any date range.
  * **Why calls didn’t connect** \- a breakdown of non-connection reasons such as busy, no answer, or provider failures.
  * **Find calls** \- list calls or dial attempts that match a filter, and open a call’s [transcript](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/call-logs) to explain what went wrong.
  * **Tool health** \- error rates and latency for each of the agent’s tools, and the failed calls behind them.
  * **Boards** \- for charts, Genie builds a [Board](https://docs.sarvam.ai/voice-agents/monitor/boards) with number, table, bar, or line widgets and filters, schedules regular deliveries, and exports widget data to CSV.



Genie links to the relevant pages - such as call logs or analytics - so you can dig deeper.

![The Genie panel answering "Why did so many calls fail yesterday?" with the connect rate, a table of non-connection reasons, key findings, and a call logs link.](https://docs.sarvam.ai/_fern-img/280024a4963f80ac4bafd36831bbf0cc60086a2b72f120040f8034c2cb10897c.webp)

Genie explains why calls failed, with a breakdown of non-connection reasons and a link to the call logs.

###### Example prompts

  * “How did my collections agent do this week?”
  * “What’s the connect rate for the March campaign, and why are calls not connecting?”
  * “Show me calls from yesterday where the customer asked for a human.”
  * “Pull the transcript of the last failed call and tell me what went wrong.”
  * “Which of my agent’s tools are erroring most, and how slow is the payment lookup?”
  * “Build a board with daily calls, connect rate, and average duration for the Sales agent, and email it to me every Monday.”



## Confirmations and safeguards

Genie can make real changes, so it checks with you before anything that places calls, affects live traffic, or can’t be undone. It shows a question card and waits for **Yes** or **No** :

  * **Calls and live traffic** \- placing a test call, creating a campaign, switching a live deployment to a new version, or pausing a deployment.
  * **Permanent changes** \- cancelling a campaign, deleting a deployment, connection, knowledge base, file, tool, variable, test scenario, secret, or board item, and replacing most of the agent’s instructions.
  * **Editing a different agent** \- Genie can read any agent in your workspace, but it only edits the agent you’re working on or one you confirm (**Yes, edit it**).



If you answer **No** , Genie stops and won’t retry unless you ask again.

## Good to know

  * Genie stays on platform tasks. It won’t answer general questions, and it won’t make up business details such as prices, policies, or API endpoints - it asks you instead.
  * Never paste API keys or passwords into chat. Genie asks for credentials in a masked field or uses your [workspace secrets](https://docs.sarvam.ai/voice-agents/build/tools/https-tool).
  * Genie writes agent configuration in English, and the platform handles translation to the agent’s other languages.
  * Genie can’t delete agents.
  * In the agent editor, you need the edit lock to message Genie. With view-only access, you can read the chat history but can’t send messages.
  * For long tasks, Genie may pause with **Turn limit exceeded**. Click **Continue** to let it keep going.



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/build/process)[TestsNext](https://docs.sarvam.ai/voice-agents/build/tests)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


