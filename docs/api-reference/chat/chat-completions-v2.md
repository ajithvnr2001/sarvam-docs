---
url: https://docs.sarvam.ai/api-reference/chat/chat-completions-v2/
title: Chat Completion V2 | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-22T06:32:57.649964+00:00
---

# Chat Completion V2 | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/chat/chat-completions-v2/

Skip to navigation

This page is for API Reference.

[APIs](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Chat Completion](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1)

# Chat Completion V2

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/chat/chat-completions-v2.md "View this page as plain text")|More actions

POST

https://api.sarvam.ai/v2/chat/completions

POST

/v2/chat/completions

Python
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_API_KEY_HERE",
    
    )
    
    client.chat.completions_v2(
    
        messages=[
    
            {
    
                "content": "Summarise the causes of the 2008 financial crisis.",
    
                "role": "user"
    
            }
    
        ],
    
        model="glm5.3",
    
    )

Try it

200chat_completionsV2_example
    
    
    {
    
      "id": "20250101_0a1b2c3d-1234-5678-9abc-def012345678",
    
      "choices": [
    
        {
    
          "finish_reason": "stop",
    
          "index": 0,
    
          "message": {
    
            "content": "The 2008 financial crisis was driven by a housing bubble, subprime lending, and the collapse of mortgage-backed securities.",
    
            "role": "assistant",
    
            "refusal": null,
    
            "reasoning_content": null,
    
            "tool_calls": null
    
          },
    
          "logprobs": {}
    
        }
    
      ],
    
      "created": 1735689600,
    
      "model": "glm5.3",
    
      "object": "chat.completion",
    
      "system_fingerprint": null,
    
      "usage": {
    
        "completion_tokens": 24,
    
        "prompt_tokens": 18,
    
        "total_tokens": 42,
    
        "completion_tokens_details": {
    
          "reasoning_tokens": 10
    
        },
    
        "prompt_tokens_details": {
    
          "cached_tokens": 0
    
        }
    
      }
    
    }

Creates a model response for the given chat conversation, using an OpenAI-compatible request and response shape.

Requires `api-subscription-key`.

**Streaming is optional.** Default is one JSON response (`stream` omitted or `false`). Set `stream: true` for server-sent events; the stream ends with a `[DONE]` line.

**Reasoning (`glm5.3`, `deepseekv4.1-flash`):** set `reasoning_effort` to **`low`** , **`high`** , or **`max`**. Default when omitted is **`max`** — omit the field or pass **`max`** for maximum reasoning. The trace is in `choices[].message.reasoning_content` and counts toward `max_tokens`. `gemma4` does not use reasoning on this route.

Request fields documented on this operation are validated by the API. Other OpenAI-compatible fields may be forwarded to the model when sent.

Legacy `functions` / `function_call` are rejected — use `tools` and `tool_choice`.

### Authentication

api-subscription-keystring

API Key authentication via header

OR

AuthorizationBearer

Bearer authentication of the form `Bearer <token>`, where token is your auth token.

### Headers

x-session-affinitystringOptional

Optional session ID for a multi-turn conversation. Send the same value on every turn of a conversation so the turns are routed together and can reuse cached prompt context, which lowers latency on later turns. Use a new value for each conversation. The ID is scoped to your API subscription and is never shared with other customers. Use an opaque value such as a UUID, and do not put personal data in it. Requests without this header are unaffected.

### Request

This endpoint expects an object.

messageslist of objectsRequired

Non-empty conversation history. Roles: `system`, `developer`, `user`, `assistant`, `tool`. Content is a string or an array of parts (`text`, `image_url`). Images must use inline `data:image/…;base64,…` URLs — remote HTTP(S) image URLs are rejected.

Show 6 variants

modelenumRequired

Model IDs accepted by `POST /v2/chat/completions` (case-sensitive; unknown ids return `404`):

  * **`sarvam-105b`** — Sarvam flagship chat model.
  * **`glm5.3`** — 1,048,576-token context window; visible reasoning in `reasoning_content` (billed as completion tokens); tool calling; max request size 10,485,760 bytes; `n` must be `1`.
  * **`gemma4`** — image input (inline base64) and tool calling.
  * **`deepseekv4.1-flash`** — 1,048,576-token context window, tool calling, and reasoning.



Allowed values:sarvam-105bglm5.3gemma4deepseekv4.1-flash

temperaturedouble or nullOptional`0-2`Defaults to `1`

Sampling temperature from `0` to `2`. Higher values increase variation; lower values focus the output. Output is not guaranteed to be identical across requests, even at `0`. Prefer changing either `temperature` or `top_p`, not both.

top_pdouble or nullOptional`<=1`Defaults to `0.95`

Nucleus sampling: greater than `0` and at most `1`. On `glm5.3`, `top_p: 0` is rejected. Prefer changing either `top_p` or `temperature`, not both.

reasoning_effortenum or nullOptional

On reasoning models (`glm5.3`, `deepseekv4.1-flash`): **`low`** , **`high`** , or **`max`**. Default when omitted is **`max`** — omit this field or set **`max`** for maximum reasoning. Trace in `message.reasoning_content`; billed as completion tokens and counts toward `max_tokens`. Ignored on non-reasoning models such as `gemma4`.

Allowed values:lowhighmax

max_tokensinteger or nullOptional`>=1`Defaults to `2048`

Maximum tokens to generate in the completion, including reasoning tokens on reasoning models. Default `2048`. Set explicitly when you need longer answers — a low limit can yield `finish_reason: "length"` with little or no visible `content` if reasoning consumes the budget.

streamboolean or nullOptionalDefaults to `false`

Optional. Default `false` — omit or `false` for one JSON response. If `true`, the response is streamed as server-sent events and ends with a `[DONE]` line. Use `stream_options.include_usage: true` to receive a final usage chunk (including `reasoning_tokens`). That chunk has an empty `choices` array — do not assume `choices[0]` is present on every event.

stopstring or list of strings or nullOptional

Up to 4 stop sequences (string or array). Generated text excludes the matched sequence. On `glm5.3`, more than four entries may return `503 model_overloaded` rather than `400`.

Show 2 variants

ninteger or nullOptional`1-128`Defaults to `1`

Number of chat completion choices to generate per request. You are billed for tokens across all choices. Default `1`. On `glm5.3`, only `n: 1` is accepted; higher values return `400 invalid_request_error`.

seedinteger or nullOptional`-9223372036854776000-9223372036854776000`

Optional integer seed for OpenAI SDK compatibility.

frequency_penaltydouble or nullOptional`-2-2`Defaults to `0`

Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model’s likelihood to repeat the same line verbatim.

presence_penaltydouble or nullOptional`-2-2`Defaults to `0`

Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model’s likelihood to talk about new topics.

toolslist of objects or nullOptional

A list of tools the model may call. Currently, only functions are supported as a tool.

Show 2 properties

tool_choiceenum or object or nullOptional

Controls tool calling: `auto`, `none`, `required`, or a named function object. `required` with an empty `tools` array returns `400`. A named function that is not listed in `tools` returns `400`.

Show 2 variants

response_formatobject or nullOptional

An object specifying the format that the model must output. Setting `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which guarantees the model generates output matching the supplied JSON Schema. Setting `{ "type": "json_object" }` enables the older JSON mode, which guarantees valid JSON but not a specific schema.

Show 3 variants

extra_bodymap from strings to anyOptionalDefaults to `{}`

Additional model-specific options merged into the request. Must not duplicate a top-level field documented on this endpoint; duplicates return `400 invalid_request_error`.

top_kinteger or nullOptional`>=-1`

Top-k sampling. Omit or set to `-1` to disable. Values `>= 1` enable top-k; `0` is rejected. There is no documented upper bound.

min_pdouble or nullOptional`0-1`

Minimum probability mass. Must be between 0 and 1 inclusive. Outside that range is `400`.

repetition_penaltydouble or nullOptional`<=2`

Repetition penalty. Must be greater than 0 and at most 2. `0` and values above 2 are `400`.

parallel_tool_callsboolean or nullOptional

**`false`** is correctly enforced (a single tool call) on **`gemma4`** and **`deepseekv4.1-flash`**. On **`glm5.3`** and **`sarvam-105b`** , **`false`** is accepted without error but is **not** enforced — the model may still return multiple tool calls in one turn.

stream_optionsobject or nullOptional

Only valid with `stream: true` (otherwise `400`). Must be a top-level field, not inside `extra_body`. Use `{"include_usage": true}` to receive token usage in the final SSE chunk.

Show 1 property

logprobsboolean or nullOptional

If `true`, return log probabilities for output tokens (use with `top_logprobs`). Supported on **`sarvam-105b`** and **`gemma4`**. Not supported on **`glm5.3`** (`400` if enabled) or **`deepseekv4.1-flash`** (returns `503 model_overloaded` instead of a clean rejection — omit this field for that model).

top_logprobsinteger or nullOptional

How many top token log probabilities to return at each position when `logprobs` is `true` (otherwise **`400`**). Same model support as `logprobs`: works on `sarvam-105b` and `gemma4`; on `glm5.3` and `deepseekv4.1-flash`, omit entirely — do not send `0`, since many SDKs add it by default.

### Response

Successful Response

idstring

A unique identifier for the chat completion.

choiceslist of objects

A list of chat completion choices. Can be more than one if `n` is greater than 1.

Show 4 properties

createdinteger

The Unix timestamp (in seconds) of when the chat completion was created.

modelstring

The model used for the chat completion.

object"chat.completion"

The object type, which is always `chat.completion`.

service_tierstring or nullOptional

system_fingerprintstring or nullOptional

OpenAI-compatible backend fingerprint when available. Always `null` on `glm5.3`.

usageobject or nullOptional

Show 5 properties

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

[Previous](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1)[Get Model V2Next](https://docs.sarvam.ai/api-reference/chat/model-v2)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * API Reference

    * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
    * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
    * [Beta APIs and Models](https://docs.sarvam.ai/api-reference/beta-apis)
    * [Meta Prompt Guide](https://docs.sarvam.ai/api-reference/metaprompt)
  * APIs

    * Speech to Text

    * Text to Speech

    * Instant Voice CloningBeta

    * Pronunciation Dictionary

    * Text Processing

    * Chat Completion
      * [POSTChat Completion V1](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1)
      * [POSTChat Completion V2](https://docs.sarvam.ai/api-reference/chat/chat-completions-v2)
      * [GETGet Model V2](https://docs.sarvam.ai/api-reference/chat/model-v2)
      * [GETList Models V2](https://docs.sarvam.ai/api-reference/chat/models-v2)

    * Responses API

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

    * BYOK

    * v1-webhooks




  * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
  * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
  * [Beta APIs and Models](https://docs.sarvam.ai/api-reference/beta-apis)
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


