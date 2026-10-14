---
url: https://docs.sarvam.ai/api-reference/responses/create-stream/
title: Create Response | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:01.857467+00:00
---

# Create Response | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/responses/create-stream/

Skip to navigation

This page is for API Reference.

[APIs](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Responses](https://docs.sarvam.ai/api-reference/responses/create-stream)

# Create Response

Beta

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/responses/create-stream.md "View this page as plain text")|More actions

POST

https://api.sarvam.ai/v2/responses

POST

/v2/responses

Python
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_API_KEY_HERE",
    
    )
    
    client.responses.create_stream(
    
        model="glm5.3",
    
        input="Summarise the causes of the 2008 financial crisis.",
    
        store=False,
    
    )

Try it

200responses_create_example

Generate a model reply in the OpenAI Responses format.

**Models:** `sarvam-105b`, `glm5.3`, `gemma4`, and `deepseekv4.1-flash` (ids are case-sensitive).

**Each call is independent.** Send the full conversation in `input` every time — nothing is stored for you. Leave out `store` or set it to `false` (`true` returns **`400`**). You cannot load a past response by id (`GET /v2/responses/{id}` is always **`404`**).

**Streaming is optional.** Default is a single JSON body (`stream` omitted or `false`). Set `stream: true` only if you want server-sent events.

**Reasoning (`glm5.3`, `deepseekv4.1-flash`):** both support `low`, `high`, and `max`. On `glm5.3`, `reasoning.effort` only accepts **`low`** or **`high`** — omit `reasoning` / `effort` for **`max`** -level reasoning, since sending the literal string **`"max"`** returns **`400`**. On `deepseekv4.1-flash`, all three values including `max` work directly. On `glm5.3`, read the trace from the reasoning item’s `summary[0].text`. Reasoning tokens count toward `max_output_tokens`, which has no default cap — omitting it means unbounded generation.

Other fields are documented below. See the [Responses API guide](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/responses-api).

### Authentication

api-subscription-keystring

API Key authentication via header

OR

AuthorizationBearer

Bearer authentication of the form `Bearer <token>`, where token is your auth token.

### Request

This endpoint expects an object.

modelenumRequired

Model IDs accepted by `POST /v2/responses` (case-sensitive; unknown ids return `404`):

  * **`sarvam-105b`** — Sarvam flagship model.
  * **`glm5.3`** — 1,048,576-token context; reasoning in `output` as a `reasoning` item; flat function tools; max request size 10,485,760 bytes.
  * **`gemma4`** — vision (inline base64 images) and tools.
  * **`deepseekv4.1-flash`** — long context, tools, and reasoning.



Allowed values:sarvam-105bglm5.3gemma4deepseekv4.1-flash

inputstring or list of objectsRequired

A prompt string, or the conversation so far as a list of items. Replay the full list on every request because this endpoint does not store prior turns.

Show 2 variants

streamtrueRequired

Optional. Default `false` — same as chat completions. Omit or `false` for one JSON response body. Set `true` to stream named server-sent events. There is no `[DONE]` sentinel — the stream ends on `response.completed`, `response.incomplete`, or `response.failed`.

max_output_tokensinteger or nullOptional

Maximum output tokens to generate, including reasoning tokens on reasoning models. If omitted, there is no default cap — generation is unbounded and continues until the model stops on its own or the context window fills. Always set this explicitly in production. Values above the model context window return `400`.

temperaturedouble or nullOptional`0-2`Defaults to `1`

Sampling temperature between 0 and 2. Default **`1`** on `glm5.3` when omitted. Output is not bit-reproducible, even at `0`.

storeboolean or nullOptional

Must be `false` or omitted (omitting is `200` and echoed as `false`). `true` is `400 invalid_request_error` — nothing created here is retrievable. OpenAI SDKs default this to `true`, so a default `client.responses.create(...)` fails.

toolslist of objects or nullOptional

Function tools use the **flat** Responses shape (`type`, `name`, `parameters`, `strict`) — the nested chat-completions tool shape is **`400`**. `tool_choice: required` with no tools returns **`400`**. Function `arguments` in output are a JSON **string** (parse before use). Multiple tool calls per turn are supported; use **`parallel_tool_calls: true`** or omit (see that field).

Show 5 properties

tool_choiceenum or object or map from strings to any or nullOptional

Forwarded exactly as written: `none`, `auto`, `required`, `{ "type": "function", "name": "..." }`, or another object.

Show 2 variants

reasoningobject or nullOptional

Optional reasoning config for `glm5.3` and `deepseekv4.1-flash`. On `glm5.3`, a reasoning item is always in `output` — read `summary[0].text`. **`effort`:** on `glm5.3`, `low` or `high` only — omit for `max`-level reasoning (the literal string `max` returns `400`); on `deepseekv4.1-flash`, `low`, `high`, or `max` all work directly. Optional **`summary`:** `auto` or `detailed`.

Show 2 properties

extra_bodymap from strings to anyOptionalDefaults to `{}`

Merged into the outbound body. Must not overwrite any modelled field (`400`). `max_tool_calls` and `prompt` are `400` here and in `extra_body` — not supported by any serving deployment.

instructionsstring or nullOptional

System-style instructions. Echoed back on the response object when set.

top_pdouble or nullOptional`<=1`Defaults to `0.95`

Nucleus sampling. Default **`0.95`** on `glm5.3` when omitted. Must be greater than **`0`** and at most **`1`** (`0` is rejected on `glm5.3`).

top_kinteger or nullOptional

Top-k sampling on `glm5.3`. Omit or use **`-1`** to disable; values **`≥ 1`** enable top-k. **`0`** is rejected.

frequency_penaltydouble or nullOptional`-2-2`

Optional. Range `-2` to `2`. May be accepted and echoed on Responses without changing model output.

presence_penaltydouble or nullOptional`-2-2`

Optional. Range `-2` to `2`. May be accepted and echoed on Responses without changing model output.

textobject or nullOptional

Output format. If you send `text`, `format` is required (`400` when missing). `json_object` and strict `json_schema` are honoured on `glm5.3` and skip the reasoning item.

Show 1 property

parallel_tool_callsboolean or nullOptional

Not currently enforced on this route for any model that supports tool calling here (`glm5.3`, `gemma4`, `deepseekv4.1-flash`). Setting **`false`** is accepted without error, but the model may still return multiple tool calls in one turn.

ninteger or nullOptional

**Ignored** on this route — Responses always returns one output. Accepted for OpenAI SDK compatibility only; omit or leave at `1`.

seedinteger or nullOptional

**Ignored** on Responses. Accepted for SDK compatibility only.

previous_response_idstring or nullOptional

`400 invalid_request_error`. This endpoint holds no state — replay the conversation in `input`. OpenAI and Fireworks use this to continue a chat; we do not.

conversationstring or map from strings to anyOptional

Conversation state is not supported. Omit this field and replay the complete conversation in `input`.

Show 2 variants

backgroundboolean or nullOptional

`true` is `400 invalid_request_error`. This endpoint is synchronous only.

max_tool_callsinteger or nullOptional

`400 invalid_request_error` — not supported by any serving deployment, top-level or via `extra_body`.

### Response

typestring

The event type.

### Errors

400

Bad Request Error

401

Unauthorized Error

403

Forbidden Error

404

Not Found Error

413

Content Too Large Error

429

Too Many Requests Error

502

Bad Gateway Error

503

Service Unavailable Error

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/get-download-links)[IntroductionManage deployments, campaigns, outbound calls, and analytics for your voice agents over REST.Next](https://docs.sarvam.ai/api-reference/conversations)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [STREAMCreate ResponseBeta](https://docs.sarvam.ai/api-reference/responses/create-stream)

  * Voice Agents

    * [Introduction](https://docs.sarvam.ai/api-reference/conversations)
    * Deployments

    * Campaigns

    * Instant Outbound

    * Analytics

    * Boards

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


