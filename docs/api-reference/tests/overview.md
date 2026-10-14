---
url: https://docs.sarvam.ai/api-reference/tests/overview/
title: Tests API overview | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:38.870652+00:00
---

# Tests API overview | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/tests/overview/

Skip to navigation

On this page

  * What makes up a test suite
  * Base URL
  * Rate limits
  * How the pieces fit together
  * Errors
  * What this API does not do
  * Next



Scroll to top

[Voice Agents](https://docs.sarvam.ai/api-reference/conversations)[Tests](https://docs.sarvam.ai/api-reference/tests/overview)

# Tests API overview

Create test suites, run them against an agent, and read back transcripts and verdicts — the same Tests you use in the Canvas.

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/tests/overview.md "View this page as plain text")|More actions

This page is for API Reference.

A **test suite** is a set of test cases for an agent. When you run a suite, the platform plays a simulated user against a committed version of your agent, one conversation per test case, and an AI judge reads each finished transcript and grades it against the behaviors you expect. This API does everything the dashboard’s Tests tab does — build suites, run them, and read the results.

For the dashboard walkthrough of the same concepts, see [Tests](https://docs.sarvam.ai/voice-agents/build/tests) under Build.

## What makes up a test suite

Part| What it is  
---|---  
**Test case**|  One simulated conversation to grade: a user scenario plus the expected behaviors  
**User scenario**|  A brief for the simulated user — who they are, what they want, and how they behave  
**Expected behaviors**|  The checks the judge grades for that test case, each `Pass` or `Fail`  
**Category**|  A label that groups related test cases  
**Global guardrails**|  One-line rules graded on every test case in the suite, such as “never gives medical advice”  
**Variables**|  Common values that can be reused across test cases  
**Variable overrides**|  A test case’s own value for a suite variable, used for that case only  
**Variable mapping**|  Connects suite variables to the agent’s own variables for one app version  
**Max turns**|  The longest a simulated conversation can run before it is cut off  
**Run**|  One execution of the suite (or one test case) against a committed app version  
**Frequency**|  How many times each test case executes within a run  
  
## Base URL
    
    
    https://apps.sarvam.ai/api/evals/v1/{org_id}/{workspace_id}/test-suites

Suites are **workspace-scoped**. A suite created without an `app_id` is reusable across every agent in the workspace; a suite created with one is bound to that app, and each app can have at most one bound suite.

Requests are authenticated with your API key, as everywhere else in the Voice Agents API — see [Introduction](https://docs.sarvam.ai/voice-agents/api/introduction).

## Rate limits

Limit| Scope| Applies to  
---|---|---  
**60 requests / minute**|  Per API key, within an org and workspace| Every Tests endpoint  
**10 runs / 5 minutes**|  Per organization| [Run a test suite](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-suite)  
**20 runs / minute**|  Per organization| [Run a single test case](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-test-case)  
  
The per-organization run limits are shared across every key and every user in the org. Exceeding any limit returns `429` with a `Retry-After` header giving the window in seconds:
    
    
    HTTP/1.1 429 Too Many Requests
    
    Retry-After: 60

Honour `Retry-After` rather than retrying immediately. If your workload needs more headroom, higher per-key limits can be provisioned per organization — contact Sarvam support.

## How the pieces fit together

[1](https://docs.sarvam.ai/api-reference/tests/overview#create-a-suite)

### Create a suite

[Create a test suite](https://docs.sarvam.ai/voice-agents/api/tests/create) with a name, shared `variables`, `global_guardrails`, and optionally up to 200 test cases inline.

[2](https://docs.sarvam.ai/api-reference/tests/overview#add-and-refine-test-cases)

### Add and refine test cases

[Add a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/add) with a `user_scenario` and `expected_behaviors`; [update](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/update) or [duplicate](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/duplicate) cases as the suite evolves.

[3](https://docs.sarvam.ai/api-reference/tests/overview#map-suite-variables-onto-the-app)

### Map suite variables onto the app

[Create a variable mapping](https://docs.sarvam.ai/voice-agents/api/tests/mappings/create) so the suite’s variables reach the agent’s own variables. Without a mapping, runs execute with the agent’s defaults.

[4](https://docs.sarvam.ai/api-reference/tests/overview#run)

### Run

[Run a test suite](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-suite) against an `app_id` and committed `app_version`. The call returns `202` with a `run_id` immediately; execution happens in the background.

[5](https://docs.sarvam.ai/api-reference/tests/overview#poll)

### Poll

[Get a run](https://docs.sarvam.ai/voice-agents/api/tests/runs/get) until `status` is `completed` or `failed`. `completed_executions` against `total_executions` is your progress bar. The response also shows, for each test case, how many of its executions have passed so far.

[6](https://docs.sarvam.ai/api-reference/tests/overview#read-the-results)

### Read the results

[Get test case results](https://docs.sarvam.ai/voice-agents/api/tests/runs/results) returns one entry per execution, each with the full conversation transcript and a verdict for every expected behavior.

## Errors

Most errors carry a `detail` field with a message string:
    
    
    { "detail": "Test suite already exists for app_id: clinic-front-desk" }

The exception is `402` — returned by the run endpoints when the workspace has no remaining credits — which carries `details` (plural) instead:
    
    
    { "details": "Insufficient credits. Please top up your wallet to continue." }

Status| When  
---|---  
`400`| The app did not answer the pre-run ping — check the `app_id` and `app_version`  
`401`| Missing or invalid `X-API-Key`  
`402`| No remaining credits; top up to resume runs  
`403`| The key is not valid for this org or workspace  
`404`| No such suite, test case, run, or mapping in this workspace  
`409`| Creating an app-bound suite for an app that already has one  
`429`| Rate limit exceeded — honour `Retry-After`  
  
## What this API does not do

These are deliberate, not gaps to work around:

  * **No deletion.** Suites and test cases are created and edited through the API but removed only in the dashboard.
  * **No run cancellation.** A queued run executes to completion; poll it rather than trying to stop it.
  * **No AI suite generation.** Generating test cases from a description is a dashboard feature.
  * **No export.** Read results as JSON from the results endpoint.



## Next

[Best practicesWriting scenarios and behaviors that grade reliably, and getting variables to reach the agent.](https://docs.sarvam.ai/voice-agents/api/tests/best-practices)[Tests in the dashboardThe same suites, runs, and results in the Canvas.](https://docs.sarvam.ai/voice-agents/build/tests)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/boards/query/preview)[Best practicesHow to write each part of a test suite — scenarios, behaviors, guardrails, variables — and how to run it and read the results.Next](https://docs.sarvam.ai/api-reference/tests/best-practices)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


