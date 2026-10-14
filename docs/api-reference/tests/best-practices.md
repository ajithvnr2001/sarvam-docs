---
url: https://docs.sarvam.ai/api-reference/tests/best-practices/
title: Best practices | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:41.060339+00:00
---

# Best practices | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/tests/best-practices/

Skip to navigation

On this page

  * Writing a user scenario
  * Writing expected behaviors
  * Behavior or guardrail?
  * When to use variables and overrides
  * Why map suite variables to agent variables
  * Suite run or single test-case run?
  * Polling a run
  * Reading the results
  * Next



Scroll to top

[Voice Agents](https://docs.sarvam.ai/api-reference/conversations)[Tests](https://docs.sarvam.ai/api-reference/tests/overview)

# Best practices

How to write each part of a test suite — scenarios, behaviors, guardrails, variables — and how to run it and read the results.

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/tests/best-practices.md "View this page as plain text")|More actions

This page is for API Reference.

## Writing a user scenario

The `user_scenario` is a brief for the simulated user on how to behave. The simulator improvises within it, so describe the person and their goal rather than the exact words:

> The caller has an appointment tomorrow but wants a weekend slot. They are in a hurry, switch to Hindi midway, and ask twice whether a cancellation fee applies.

Keep **one intent per scenario**. A scenario that asks the user to reschedule, then cancel, then complain produces one long conversation where a `Fail` tells you little — split it into three test cases.

## Writing expected behaviors

An expected behavior is a check the judge grades against the finished transcript. The judge can only check what it can see, so write each behavior as one **observable, yes-or-no question** :

|   
---|---  
✅| “Repeats the final date and time back to the caller before ending the call”  
✅| “Proposes at least two specific slots instead of asking the caller to choose blindly”  
❌| “Handles the call well” — nothing concrete to check  
❌| “Is polite and confirms the booking and offers alternatives” — three checks in one; you won’t know which failed  
  
Use the `name` as a short label you’ll recognise in results, and the `description` to tell the judge exactly what counts as a pass.

## Behavior or guardrail?

An **expected behavior** is specific to one test case — it asks “did the agent do its job in this scenario?”. A **global guardrail** is graded against every test case in the suite — it asks “did the agent stay inside policy, whatever the scenario?”.

For example, _“Offers at least two alternative slots”_ belongs in the rescheduling test case’s expected behaviors, while _“Never gives medical advice”_ belongs in the suite’s guardrails, because it must hold in every conversation.

| Expected behaviors| Global guardrails  
---|---|---  
Graded against| The one test case they belong to| Every test case in the suite  
Shape| `name` \+ `description`| One sentence, up to 500 characters, at most 20 per suite  
Verdict| One per behavior| One collective `Guardrails` verdict per execution  
  
A simple test: if you find yourself copying the same behavior into every test case, it is a guardrail.

## When to use variables and overrides

Use suite **variables** for values that appear across many test cases — a customer name, an amount due, a preferred language. They let you change a value once instead of editing every scenario. Reference a variable inside a user scenario with double braces, and the value is filled in when the test runs:

> The caller owes `{{due_amount}}` and asks for two more weeks to pay.

Use a test case’s **variable overrides** when one case needs a different value to trigger the flow it tests. For example, keep `due_amount: 4500` at the suite level, and override it to `120000` in the one case that checks whether large amounts are escalated.

## Why map suite variables to agent variables

A suite’s variables do **not** automatically reach the agent. The agent has its own variable names (set under [Variables & personalization](https://docs.sarvam.ai/voice-agents/build/variables-personalization)), and the two are connected by a [variable mapping](https://docs.sarvam.ai/voice-agents/api/tests/mappings/create) created per `app_id` and `app_version`:
    
    
    { "app_id": "clinic-front-desk", "app_version": 4,
    
      "variable_mapping": { "customer_name": "patient_name" } }

Keys are the **agent’s** variable names; values are the **suite’s**. Create a mapping whenever the agent’s instruction uses variables and you want your test values to flow into them. Without one, the run still executes, but the agent falls back to its default variable values — your carefully parameterised cases all end up testing the same thing. Recreate the mapping when you commit a new app version.

## Suite run or single test-case run?

[Run a single test case](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-test-case) while you are writing or fixing that case. [Run a test suite](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-suite) as your regression check — after committing a new agent version, or before a release. Note that a suite run consumes more credits: every test case executes, multiplied by `frequency`, so a 50-case suite at `frequency: 2` is 100 simulated conversations.

## Polling a run

Starting a run returns `202` with a `run_id` — execution happens in the background, and [Get a run](https://docs.sarvam.ai/voice-agents/api/tests/runs/get) is how you follow it:

  * Poll every **30–60 seconds** until `status` is `completed` or `failed`. A run simulates whole conversations, so it takes minutes; polling faster just spends requests on identical answers.
  * `completed_executions` against `total_executions` is your progress bar.
  * A `402` when starting the run means the workspace is out of credits.



## Reading the results

Start from the run summary and drill down only where something failed:

  1. **Per-case pass counts first.** In [Get a run](https://docs.sarvam.ai/voice-agents/api/tests/runs/get), each test case reports `passed` out of `total_executions`. An execution counts as passed only when _every_ expected behavior passed. `0/3` is broken; `2/3` is flaky.
  2. **Then open the failing case.** [Get test case results](https://docs.sarvam.ai/voice-agents/api/tests/runs/results) returns one entry per execution, each with the full transcript and the judge’s verdict for every behavior.
  3. **Read the judge’s reasoning.** Every `Pass` or `Fail` comes with a short explanation of what the agent said. There is also one extra entry, `Guardrails`, which grades the suite’s guardrails for that conversation.



## Next

[Tests API overviewBase URL, rate limits, the run lifecycle, and the error envelope.](https://docs.sarvam.ai/voice-agents/api/tests/overview)[Tests in the dashboardBuild and run the same suites from the Canvas.](https://docs.sarvam.ai/voice-agents/build/tests)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/tests/overview)[List test suitesNext](https://docs.sarvam.ai/api-reference/tests/list)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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

    * Tests
      * [Overview](https://docs.sarvam.ai/api-reference/tests/overview)
      * [Best practices](https://docs.sarvam.ai/api-reference/tests/best-practices)
      * [GETList test suites](https://docs.sarvam.ai/api-reference/tests/list)
      * [POSTCreate a test suite](https://docs.sarvam.ai/api-reference/tests/create)
      * [GETGet a test suite](https://docs.sarvam.ai/api-reference/tests/get)
      * [PATCHUpdate a test suite](https://docs.sarvam.ai/api-reference/tests/update)
      * Test cases

      * Variable mappings

      * Runs

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


