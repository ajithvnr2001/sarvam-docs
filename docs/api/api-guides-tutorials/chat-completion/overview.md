---
url: https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview/
title: Chat Completion API | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-22T06:32:46.039752+00:00
---

# Chat Completion API | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview/

Skip to navigation

On this page

  * V1 Chat Completion
  * V2 Chat Completion
  * V2 models
  * Session affinity for multi-turn conversations
  * V2 feature support
  * Features
  * V1 features and examples
  * Streaming
  * Tool Calling (Function Calling)
  * Controlling tool use with tool_choice
  * Structured Outputs (JSON)
  * Structured Outputs with json_schema
  * JSON mode with json_object
  * Alternative: Tool calling as a JSON schema
  * Alternative: Prompt-based JSON
  * API Response Format
  * Success Response Structure
  * Response Fields
  * Error Responses
  * Limits



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Large Language Models](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)

# Chat Completion API

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview.md "View this page as plain text")|More actions

This page is for Model APIs.

Use the Chat Completion API to build conversational AI experiences with native support for Indian languages and deep contextual reasoning. Sarvam provides two versions: V1 for Sarvam models and V2 for Sarvam and open-weight models.

Use the [Sarvam chat skill](https://github.com/sarvamai/skills/tree/main/chat) to generate correct chat completion code from your AI coding assistant:
    
    
    npx skills add sarvamai/skills --skill chat

See [Agent Skills](https://docs.sarvam.ai/api/developer-tools/agent-skills) for the full list.

Our Chat Completion APIs support the following chat models:

[Sarvam-105BModel ID `sarvam-105b`. Flagship model for complex reasoning, coding, and agentic workflows. 128K token context length.](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)[Sarvam-105B ConversationsModel ID `sarvam-105b-conversations`. Conversational variant post-trained for real-time dialogue and voice-agent workloads.](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b#conversational-variant)

Simply pass the model name as the `model` parameter (e.g., `model="sarvam-105b"` or `model="sarvam-105b-conversations"`).

**Endpoints:** `POST /v1/chat/completions` serves `sarvam-105b` and `sarvam-105b-conversations`. `POST /v2/chat/completions` serves `sarvam-105b`, `glm5.3`, `gemma4`, and `deepseekv4.1-flash`. See [Open-Weight Models](https://docs.sarvam.ai/api/getting-started/models/openweight).

**Token budgeting:** the context length covers _everything_ , your messages, any `reasoning_content` the model produces in think mode, and the generated reply (capped by `max_tokens`, default 2048). Reasoning tokens are billed as completion tokens, so high `reasoning_effort` increases both latency and cost. For long conversations, trim or summarize older turns instead of resending the full history.

**Authentication:** like every Sarvam API, this endpoint uses the `api-subscription-key` header. It additionally accepts `Authorization: Bearer <key>` for OpenAI-compatible tooling. See [Authentication](https://docs.sarvam.ai/api-reference/authentication) for details.

**Sarvam-M (24B)** has been deprecated and is no longer available through the Chat Completions API. Please migrate to **Sarvam-105B** for improved performance.

## V1 Chat Completion

`POST /v1/chat/completions` supports `sarvam-105b` and `sarvam-105b-conversations`. Use V1 for Sarvam’s flagship and conversational models. See the [Chat Completion V1 API Reference](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1) for the complete request and response schema.

PythonJavaScriptcURL
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    response = client.chat.completions(
    
        model="sarvam-105b",
    
        messages=[{"role": "user", "content": "What is the capital of India?"}],
    
    )
    
    print(response.choices[0].message.content)

## V2 Chat Completion

`POST /v2/chat/completions` supports `sarvam-105b`, `glm5.3`, `gemma4`, and `deepseekv4.1-flash`. Use V2 for the OpenAI-compatible API and open-weight models. See the [Chat Completion V2 API Reference](https://docs.sarvam.ai/api-reference/chat/chat-completions-v2) for the complete request and response schema.

PythonJavaScriptcURL
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    response = client.chat.completions_v2(
    
        model="glm5.3",
    
        messages=[{"role": "user", "content": "Explain photosynthesis briefly."}],
    
    )
    
    print(response.choices[0].message.content)

### V2 models

Model ID| Type| Context| Reasoning| Guide  
---|---|---|---|---  
`sarvam-105b`| Sarvam| 128K| Hybrid| [Sarvam-105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)  
`glm5.3`| Open-weight| 1M| `low` · `high` · `max`| [GLM-5.3](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)  
`gemma4`| Open-weight| 131K, text + image| None| [Gemma 4 31B](https://docs.sarvam.ai/api/getting-started/models/openweight/gemma-4-31b)  
`deepseekv4.1-flash`| Open-weight| 1M| `low` · `high` · `max`| [DeepSeek V4.1 Flash](https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash)  
  
Confirm what your key can use with [`GET /v2/models`](https://docs.sarvam.ai/api-reference/chat/models-v2).

### Session affinity for multi-turn conversations

Session affinity is currently supported on the **`gemma4`** model. Send the optional **`x-session-affinity`** header with the same value on every turn of a conversation. Turns that share a session ID are routed together and can reuse cached prompt context, which lowers latency on later turns of long conversations.

  * Use one stable ID per conversation, and a new ID for each new conversation.
  * Session IDs are scoped to your API subscription. Another customer who sends the same value does not share your session.
  * Use an opaque value such as a UUID. Do not put personal data in it.
  * The header is optional. Requests without it behave exactly as before, and responses are the same whether or not you send it.
  * Other models (`sarvam-105b`, `glm5.3`, `deepseekv4.1-flash`) accept the header but ignore it.
  * When you contact support about a conversation, include its session ID.



PythoncURL
    
    
    import uuid
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    session_id = str(uuid.uuid4())  # one per conversation
    
    messages = [{"role": "user", "content": "Plan a 3-day trip to Jaipur."}]
    
    response = client.chat.completions_v2(
    
        model="gemma4",
    
        messages=messages,
    
        request_options={"additional_headers": {"x-session-affinity": session_id}},
    
    )
    
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    
    messages.append({"role": "user", "content": "Add a day trip to Ajmer."})
    
    # Next turn: reuse the same session ID
    
    response = client.chat.completions_v2(
    
        model="gemma4",
    
        messages=messages,
    
        request_options={"additional_headers": {"x-session-affinity": session_id}},
    
    )

### V2 feature support

Feature| `sarvam-105b`| `glm5.3`| `gemma4`| `deepseekv4.1-flash`  
---|---|---|---|---  
Streaming| | | |   
Tool calling| | | |   
Structured output (`response_format`)| | | |   
Log probabilities| | `400`| |  not returned  
Multiple choices (`n` > 1)| | `400`| |   
`parallel_tool_calls: false` enforced| | | |   
Session affinity (`x-session-affinity`)| | | |   
  
###### V2 behaviour notes

  * **Model IDs are case-sensitive.** An unknown ID returns `404 not_found_error`.
  * **Auth failures return`403`**, not `401`, with `invalid_api_key_error`.
  * **Streaming is optional.** Omit `stream` (or set `false`) for one JSON response, `true` for server-sent events.
  * **Parallel tool calls:** on the Responses API, `parallel_tool_calls: false` isn’t enforced for any model.
  * **Reasoning on Responses:** `deepseekv4.1-flash` accepts `low`, `high`, `max`. `glm5.3` accepts only `low` or `high`; omit `reasoning` to get `max` (the string `"max"` returns `400`).
  * **Reasoning budget:** reasoning tokens count against `max_tokens` (default `2048` on Chat). Responses’ `max_output_tokens` has no default, so omitting it means unbounded generation.
  * **`stop`:** up to 4 sequences. On `glm5.3`, more than four may return `503` instead of `400`.
  * **Errors:** invalid JSON or types return `400` with `error.message`; overload returns `503` (retry with backoff).
  * Model-specific limits are listed under each [open-weight model guide](https://docs.sarvam.ai/api/getting-started/models/openweight).



The **Limits** table at the bottom of this page applies to **V1** (`sarvam-105b` / `sarvam-105b-conversations`), not V2 open-weight models.

## Features

Hybrid Thinking Mode

  * Supports both “think” and “non-think” modes
  * Think mode for complex logical reasoning
  * Non-think mode for efficient conversations
  * Ideal for mathematical and coding tasks



Advanced Indic Skills

  * Post-trained on Indian languages
  * Native English proficiency
  * Authentic Indian cultural values
  * Rich understanding of local context



Superior Reasoning Capabilities

  * Outperforms similar-sized models
  * Strong performance on coding tasks
  * Excellent mathematical reasoning
  * Advanced problem-solving abilities



Seamless Chatting Experience

  * Full Indic script support
  * Romanized language support
  * Multilingual conversation handling
  * Natural language understanding



## V1 features and examples

###### Basic Chat Completion

###### Multi-turn Conversation

###### Hindi (Indic Script)

PythonJavaScriptcURL
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_SARVAM_API_KEY",
    
    )
    
    response = client.chat.completions(
    
        model="sarvam-105b",
    
        messages=[
    
            {"role": "user", "content": "Hey, what is the capital of India?"}
    
        ],
    
    )
    
    print(response)

Key Considerations

  * Reasoning effort options: low, medium, high

    * Thinking mode is **on by default** (`low`); pass `reasoning_effort=None` (Python) / `reasoning_effort: null` (JS, cURL) to disable it
    * Higher values increase reasoning depth
    * Reasoning tokens (returned as `reasoning_content`) count toward your completion tokens and bill. Use lower effort or disable reasoning for latency- and cost-sensitive paths
  * Output length is capped by `max_tokens` (default 2048), raise it for long-form generation




Because thinking mode is on by default, a low `max_tokens` (e.g. under a few hundred) can be consumed entirely by reasoning, you’ll get `finish_reason: "length"` with an empty `content` and only `reasoning_content` populated. Either keep `max_tokens` generous or disable reasoning with `reasoning_effort=None` for short replies.

## Streaming

Set `stream: true` to receive the response incrementally over [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) instead of waiting for the full completion. This is essential for responsive chat UIs and voice-agent pipelines, where you want to start rendering (or speaking) the reply as soon as the first tokens arrive.

Both SDKs return an iterator of `chat.completion.chunk` objects. Each chunk carries a `delta` with the new portion of the message, `delta.content` for the reply text and, when reasoning is enabled, `delta.reasoning_content` for thinking tokens.

PythonJavaScriptcURL
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_SARVAM_API_KEY",
    
    )
    
    stream = client.chat.completions(
    
        model="sarvam-105b",
    
        messages=[
    
            {"role": "user", "content": "Write a short poem about the monsoon."}
    
        ],
    
        stream=True,
    
    )
    
    for chunk in stream:
    
        # The final chunk reports usage and has no choices: guard before indexing
    
        if chunk.choices and chunk.choices[0].delta.content:
    
            print(chunk.choices[0].delta.content, end="", flush=True)

Over raw HTTP, each event is a `data:` line containing a `chat.completion.chunk` JSON object. The final data chunk carries `usage` (with an empty `choices` array), and the stream ends with `data: [DONE]`:
    
    
    data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1699000000,"model":"sarvam-105b","choices":[{"index":0,"delta":{"role":"assistant","content":"The"},"finish_reason":null}]}
    
    data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1699000000,"model":"sarvam-105b","choices":[{"index":0,"delta":{"content":" rains"},"finish_reason":null}]}
    
    data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1699000000,"model":"sarvam-105b","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}
    
    data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1699000000,"model":"sarvam-105b","choices":[],"usage":{"prompt_tokens":19,"completion_tokens":3,"total_tokens":22}}
    
    data: [DONE]

When `reasoning_effort` is set, thinking tokens stream first via `delta.reasoning_content`, followed by the reply via `delta.content`. Check both fields if you display reasoning to users.

## Tool Calling (Function Calling)

Describe functions your application exposes with the `tools` parameter, and the model will decide when to call them, returning the function name and JSON arguments instead of (or alongside) a text reply. You execute the function yourself, append the result as a `tool` message, and call the API again so the model can produce its final answer.

The flow is:

  1. Send the conversation plus `tools` definitions.
  2. If the model wants a tool, the response has `finish_reason: "tool_calls"` and `message.tool_calls` with the function name and stringified JSON `arguments`.
  3. Run the function, append the assistant message and a `{"role": "tool", "tool_call_id": ..., "content": ...}` message with the result.
  4. Call the API again, the model answers using the tool output.



PythonJavaScriptcURL
    
    
    import json
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    tools = [
    
        {
    
            "type": "function",
    
            "function": {
    
                "name": "get_weather",
    
                "description": "Get the current weather for an Indian city",
    
                "parameters": {
    
                    "type": "object",
    
                    "properties": {
    
                        "city": {"type": "string", "description": "City name, e.g. Mumbai"},
    
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
    
                    },
    
                    "required": ["city"],
    
                },
    
            },
    
        }
    
    ]
    
    messages = [{"role": "user", "content": "What's the weather in Mumbai right now?"}]
    
    response = client.chat.completions(
    
        model="sarvam-105b",
    
        messages=messages,
    
        tools=tools,
    
        tool_choice="auto",
    
    )
    
    message = response.choices[0].message
    
    if message.tool_calls:
    
        tool_call = message.tool_calls[0]
    
        args = json.loads(tool_call.function.arguments)
    
        # Run your actual function here
    
        weather = {"city": args["city"], "temperature": 31, "condition": "Humid"}
    
        messages.append(
    
            {
    
                "role": "assistant",
    
                "tool_calls": [
    
                    {
    
                        "id": tool_call.id,
    
                        "type": "function",
    
                        "function": {
    
                            "name": tool_call.function.name,
    
                            "arguments": tool_call.function.arguments,
    
                        },
    
                    }
    
                ],
    
            }
    
        )
    
        messages.append(
    
            {
    
                "role": "tool",
    
                "tool_call_id": tool_call.id,
    
                "content": json.dumps(weather),
    
            }
    
        )
    
        final = client.chat.completions(
    
            model="sarvam-105b",
    
            messages=messages,
    
            tools=tools,
    
        )
    
        print(final.choices[0].message.content)

A tool-call response looks like:
    
    
    {
    
      "choices": [
    
        {
    
          "index": 0,
    
          "finish_reason": "tool_calls",
    
          "message": {
    
            "role": "assistant",
    
            "content": null,
    
            "tool_calls": [
    
              {
    
                "id": "call_abc123",
    
                "type": "function",
    
                "function": {
    
                  "name": "get_weather",
    
                  "arguments": "{\"city\": \"Mumbai\", \"unit\": \"celsius\"}"
    
                }
    
              }
    
            ]
    
          }
    
        }
    
      ]
    
    }

### Controlling tool use with `tool_choice`

Value| Behavior  
---|---  
`"auto"` (default when tools are provided)| The model decides whether to call a tool or reply directly  
`"none"`| The model never calls a tool, tools are ignored  
`"required"`| The model must call at least one tool  
`{"type": "function", "function": {"name": "get_weather"}}`| Forces the model to call the named function  
  
`function.arguments` is a **JSON string** , not an object, always parse it (and validate against your schema) before executing the function.

## Structured Outputs (JSON)

The Chat Completions API supports the OpenAI-compatible `response_format` parameter for getting reliably structured JSON:

`response_format`| Behavior  
---|---  
`{"type": "json_schema", "json_schema": {...}}`| **Structured Outputs** : output is constrained to match the JSON Schema you supply (recommended)  
`{"type": "json_object"}`| **JSON mode** : output is guaranteed to be valid JSON, but not a specific schema  
`{"type": "text"}` (default)| Plain text output  
  
### Structured Outputs with `json_schema`

Pass a JSON Schema under `json_schema.schema`, and set `"strict": true` to enforce adherence. The structured reply arrives as a JSON **string** in `message.content`, parse it before use.

PythonJavaScriptcURL
    
    
    import json
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    response = client.chat.completions(
    
        model="sarvam-105b",
    
        messages=[
    
            {
    
                "role": "user",
    
                "content": "Order: 2 masala dosas and 1 filter coffee to Koramangala, Bengaluru.",
    
            }
    
        ],
    
        response_format={
    
            "type": "json_schema",
    
            "json_schema": {
    
                "name": "food_order",
    
                "strict": True,
    
                "schema": {
    
                    "type": "object",
    
                    "properties": {
    
                        "items": {
    
                            "type": "array",
    
                            "items": {
    
                                "type": "object",
    
                                "properties": {
    
                                    "name": {"type": "string"},
    
                                    "quantity": {"type": "integer"},
    
                                },
    
                                "required": ["name", "quantity"],
    
                                "additionalProperties": False,
    
                            },
    
                        },
    
                        "city": {"type": "string"},
    
                    },
    
                    "required": ["items", "city"],
    
                    "additionalProperties": False,
    
                },
    
            },
    
        },
    
    )
    
    order = json.loads(response.choices[0].message.content)
    
    print(order)
    
    # {'items': [{'name': 'masala dosa', 'quantity': 2}, {'name': 'filter coffee', 'quantity': 1}], 'city': 'Bengaluru'}

Both `/v1/chat/completions` and `/v2/chat/completions` expose `response_format` as a typed SDK parameter. On V2, call `client.chat.completions_v2`; see the [Chat Completion V2 API Reference](https://docs.sarvam.ai/api-reference/chat/chat-completions-v2).

The `json_schema` object accepts:

Field| Type| Description  
---|---|---  
`name`| string (required)| Name of the response format. Alphanumeric characters, underscores and dashes only  
`schema`| object| The output structure, described as a [JSON Schema](https://json-schema.org/) object  
`strict`| boolean| Enable strict schema adherence when generating the output (default `false`)  
`description`| string| What the format is for, helps the model decide how to respond  
  
### JSON mode with `json_object`

When you only need valid JSON without enforcing a specific structure, use `{"type": "json_object"}` and describe the desired shape in your prompt:
    
    
    curl -X POST https://api.sarvam.ai/v1/chat/completions \
    
      -H "api-subscription-key: $SARVAM_API_KEY" \
    
      -H "Content-Type: application/json" \
    
      -d '{
    
        "model": "sarvam-105b",
    
        "messages": [
    
          {"role": "system", "content": "Reply with a JSON object: {\"sentiment\": \"positive\" | \"negative\" | \"neutral\", \"confidence\": number}"},
    
          {"role": "user", "content": "यह फिल्म शानदार थी!"}
    
        ],
    
        "response_format": {"type": "json_object"}
    
      }'

Even with Structured Outputs, validate the parsed JSON against your expected schema (e.g. with `pydantic` or `zod`) before acting on it, the schema constrains the model’s output shape, but your application logic may have stricter requirements (value ranges, business rules, etc.).

### Alternative: Tool calling as a JSON schema

If your workflow is already built around [tool calling](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview#tool-calling-function-calling), you can also get structured output by defining a single tool whose `parameters` schema describes the structure you want, and forcing it with `tool_choice`. The model’s `arguments` are then constrained to the schema.

PythonJavaScript
    
    
    import json
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    response = client.chat.completions(
    
        model="sarvam-105b",
    
        messages=[
    
            {
    
                "role": "user",
    
                "content": "Order: 2 masala dosas and 1 filter coffee to Koramangala, Bengaluru.",
    
            }
    
        ],
    
        tools=[
    
            {
    
                "type": "function",
    
                "function": {
    
                    "name": "extract_order",
    
                    "description": "Extract a structured food order",
    
                    "parameters": {
    
                        "type": "object",
    
                        "properties": {
    
                            "items": {
    
                                "type": "array",
    
                                "items": {
    
                                    "type": "object",
    
                                    "properties": {
    
                                        "name": {"type": "string"},
    
                                        "quantity": {"type": "integer"},
    
                                    },
    
                                    "required": ["name", "quantity"],
    
                                },
    
                            },
    
                            "delivery_area": {"type": "string"},
    
                            "city": {"type": "string"},
    
                        },
    
                        "required": ["items", "city"],
    
                    },
    
                },
    
            }
    
        ],
    
        tool_choice={"type": "function", "function": {"name": "extract_order"}},
    
    )
    
    arguments = response.choices[0].message.tool_calls[0].function.arguments
    
    order = json.loads(arguments)
    
    print(order)
    
    # {'items': [{'name': 'masala dosa', 'quantity': 2}, {'name': 'filter coffee', 'quantity': 1}], 'delivery_area': 'Koramangala', 'city': 'Bengaluru'}

### Alternative: Prompt-based JSON

For simple cases, you can also instruct the model to reply with JSON only, set a low `temperature`, and validate the output before using it (consider [JSON mode](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview#json-mode-with-json_object) instead, which guarantees valid JSON):
    
    
    import json
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    response = client.chat.completions(
    
        model="sarvam-105b",
    
        messages=[
    
            {
    
                "role": "system",
    
                "content": (
    
                    "Reply with a single JSON object only, no prose, no markdown fences. "
    
                    'Schema: {"sentiment": "positive" | "negative" | "neutral", "confidence": number}'
    
                ),
    
            },
    
            {"role": "user", "content": "यह फिल्म शानदार थी!"},
    
        ],
    
        temperature=0.1,
    
    )
    
    raw = response.choices[0].message.content
    
    try:
    
        result = json.loads(raw)
    
    except json.JSONDecodeError:
    
        # Retry, or strip markdown fences / extra text before parsing
    
        raise
    
    print(result)

Always validate model-produced JSON against your expected schema (e.g. with `pydantic` or `zod`) and add a retry path, prompt-based JSON is good, but not guaranteed.

## API Response Format

### Success Response Structure
    
    
    {
    
      "id": "chatcmpl-abc123",
    
      "object": "chat.completion",
    
      "created": 1699000000,
    
      "model": "sarvam-105b",
    
      "choices": [
    
        {
    
          "index": 0,
    
          "message": {
    
            "role": "assistant",
    
            "content": "The capital of India is New Delhi. It has been the capital since 1931."
    
          },
    
          "finish_reason": "stop"
    
        }
    
      ],
    
      "usage": {
    
        "prompt_tokens": 15,
    
        "completion_tokens": 25,
    
        "total_tokens": 40
    
      }
    
    }

### Response Fields

Field| Type| Description  
---|---|---  
`id`| string| Unique identifier for the completion request  
`object`| string| Always `"chat.completion"`  
`created`| integer| Unix timestamp when the completion was created  
`model`| string| The model used for completion  
`choices[].index`| integer| Index of the choice in the list  
`choices[].message.role`| string| Always `"assistant"`  
`choices[].message.content`| string| The generated text response (`null` when the model calls a tool)  
`choices[].message.reasoning_content`| string| Thinking steps (only when `reasoning_effort` is set)  
`choices[].message.tool_calls`| array| Tool invocations requested by the model (only when using [tool calling](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview#tool-calling-function-calling))  
`choices[].finish_reason`| string| Why generation stopped: `"stop"`, `"length"`, `"tool_calls"`, `"content_filter"`, or `"function_call"` (legacy, only reachable via the deprecated `functions` parameter, which currently returns `503`; use `tools`/`tool_choice` instead)  
`usage.prompt_tokens`| integer| Tokens in the input prompt  
`usage.completion_tokens`| integer| Tokens in the generated response  
`usage.total_tokens`| integer| Total tokens used (prompt + completion)  
  
## Error Responses

All errors return a JSON object with an `error` field (`message`, `code`, `request_id`). The full error-code table, retry guidance, and SDK exception reference live on the central [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting) page.

Errors specific to this endpoint:

HTTP Status| Error Code| When This Happens| What To Do  
---|---|---|---  
`400`| `invalid_request_error`| Missing `messages` array or missing `model` field, invalid parameters, or context overflow| Include both `model` and a valid `messages` array; check temperature (0–2) and model name  
  
###### Error Handling Code Example
    
    
    from sarvamai import SarvamAI
    
    from sarvamai.core.api_error import ApiError
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    try:
    
        response = client.chat.completions(
    
            model="sarvam-105b",
    
            messages=[
    
                {"role": "user", "content": "What is the capital of India?"}
    
            ],
    
        )
    
        print(response.choices[0].message.content)
    
    except ApiError as e:
    
        if e.status_code == 400:
    
            print(f"Bad request: {e.body}")
    
        elif e.status_code == 403:
    
            print("Invalid API key. Check your credentials.")
    
        elif e.status_code == 429:
    
            print("Rate limit exceeded. Wait and retry.")
    
        else:
    
            print(f"Error {e.status_code}: {e.body}")

## Limits

Limit| Value  
---|---  
Context window| 128K tokens (`sarvam-105b`) / 32K tokens (`sarvam-105b-conversations`)  
`max_tokens`| Starter 4096 / Pro 16384 / Business 128000  
(reasoning tokens count toward completion tokens)  
`temperature`| 0–2 (default 0.5 when reasoning is enabled, the default, and 0.2 when reasoning is disabled)  
`top_p`| 0–1  
`n` (completions per request)| 1–128  
`frequency_penalty` / `presence_penalty`| -2 to 2  
`stop`| Up to 4 sequences  
Rate limits| See [Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)  
  
Check out the [Chat Completion V1 API Reference](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1) to explore Chat Completion and all available options.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/platform/faq)[Responses APINext](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/responses-api)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
    * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
    * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
    * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
    * [Models](https://docs.sarvam.ai/api/getting-started/models)

    * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
    * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
    * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
    * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
    * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
    * Account & Billing

  * API Guides & Tutorials

    * Large Language Models
      * [Chat Completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
      * [Responses API](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/responses-api)
      * How-to

    * Speech to Text

    * Text to Speech

    * Text Processing

    * Document Intelligence

    * Document Translation

    * Dubbing

    * Instant Voice CloningBeta

  *     * Integration

    * Developer Tools

  * Cookbook

    * Guides

    * Example Voice Agents

  * Self-Hosted Deployments

    * Overview

    * AWS SageMaker

  *     * Migrations




  * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
  * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
  * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
  * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
  * [Models](https://docs.sarvam.ai/api/getting-started/models)
  * [Saaras](https://docs.sarvam.ai/api/getting-started/models/saaras)
  * [Bulbul](https://docs.sarvam.ai/api/getting-started/models/bulbul)
  * [Sarvam 105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)
  * [Open-Weight Models](https://docs.sarvam.ai/api/getting-started/models/openweight)
  * [GLM-5.3](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)
  * [Gemma 4 31B](https://docs.sarvam.ai/api/getting-started/models/openweight/gemma-4-31b)
  * [DeepSeek V4.1 Flash](https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash)
  * [Mayura](https://docs.sarvam.ai/api/getting-started/models/mayura)
  * [Sarvam Translate](https://docs.sarvam.ai/api/getting-started/models/sarvam-translate)
  * [Sarvam Vision](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)
  * [Sarvam 30B (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/sarvam-30b)
  * [Sarvam M (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/sarvam-m)
  * [Saarika (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/saarika)
  * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
  * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
  * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
  * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
  * [Organisations & workspaces](https://docs.sarvam.ai/api/platform/organisations-and-workspaces)
  * [Create an organisation](https://docs.sarvam.ai/api/platform/create-an-organisation)
  * [Create a workspace](https://docs.sarvam.ai/api/platform/create-a-workspace)
  * [Invite your team](https://docs.sarvam.ai/api/platform/invite-your-team)
  * [Billing & payments](https://docs.sarvam.ai/api/platform/billing)
  * [Platform FAQ](https://docs.sarvam.ai/api/platform/faq)
  * [Chat Completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * [Responses API](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/responses-api)
  * [List your chat messages](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/list-your-chat-messages)
  * [Control response randomness](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-response-randomness)
  * [Control response diversity](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-response-diversity)
  * [Adjust the model's thinking level](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/adjust-the-models-thinking-level)
  * [Encourage new topics in response](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/encourage-new-topics-in-response)
  * [Reduce repetition words or phrases in response](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/reduce-repetition-words-or-phrases-in-response)
  * [Get repeatable results](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/get-repeatable-results)
  * [Control the response length](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-the-response-length)
  * [Control where the model stops](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-where-the-model-stops)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)
  * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
  * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)
  * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
  * [Realtime Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming)
  * [Best Practices](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/best-practices)
  * [FAQs](https://docs.sarvam.ai/api/speech-to-text/faq)
  * [Select Output Mode](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/select-output-mode)
  * [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/specify-language-codes)
  * [Enable Speaker Diarization](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/enable-speaker-diarization)
  * [Keyterm Prompting](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/keyterms)
  * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/ivr-contact-center)
  * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/bfsi-voice-bots)
  * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
  * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services)
  * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/agri-rural)
  * [Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)
  * [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)
  * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/which-api-to-use)
  * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)
  * [HTTP Stream](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream)
  * [WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket)
  * [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
  * [Best Practice Guide for Bulbul v4 Flash](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices)
  * [Best Practices (Bulbul v3)](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices)
  * [Set the Language](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-the-language)
  * [Change the Speaker Voice](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/change-the-speaker-voice)
  * [Adjust the Tone](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-tone)
  * [Adjust the Speed](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-speed)
  * [Adjust the Loudness](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-loudness)
  * [Set the Sample rate](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-the-sample-rate)
  * [Enable Text Preprocessing](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/enable-text-preprocessing)
  * [Set audio format for output](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-audio-format-for-output)
  * [Set bitrate for output](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-bitrate-for-output)
  * [Set maximum length for sentence splitting](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-maximum-length-for-sentence-splitting)
  * [Set buffer size to start processing](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-buffer-size-to-start-processing)
  * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/ivr-contact-center)
  * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/bfsi-voice-bots)
  * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
  * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/government-services)
  * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview)
  * [Text Translation](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/translation)
  * [Transliteration](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/transliteration)
  * [Language Detection](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/language-detection)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview)
  * [Get your config_id](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/how-to/get-your-config-id)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)
  * [Set Style Guidelines](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/style-guidelines)
  * [Pick a Genre](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/genre-and-model-tier)
  * [Use Native Numerals](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/native-numerals)
  * [Poll Status and Export Results](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/poll-and-export)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/faq)
  * [Use Cases](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/use-cases)
  * [Translate a PDF](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/guides/translate-a-pdf)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)
  * [Job Lifecycle](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle)
  * [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/specify-language-codes)
  * [Control Translation Tone](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/control-translation-tone)
  * [Choose a Voice](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice)
  * [Choose Export Formats](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/faq)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview)
  * [Prepare Reference Audio](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/prepare-reference-audio)
  * [Clone Across Languages](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/clone-across-languages)
  * [Choose Audio Formats](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/choose-audio-formats)
  * [Use Quality Control](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/use-quality-control)
  * [HTTP Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/http-streaming)
  * [WebSocket Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/websocket-streaming)
  * [Supported Languages](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/supported-languages)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/faq)
  * [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)
  * [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)
  * [Twilio](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio)
  * [Exotel](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)
  * [Vobiz](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)
  * [Vapi](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)
  * [n8n](https://docs.sarvam.ai/api/integration/n8n)
  * [Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)
  * [LangChain](https://docs.sarvam.ai/api/integration/langchain)
  * [LiveKit in Production](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)
  * [Pipecat in Production](https://docs.sarvam.ai/api/integration/pipecat-production-guide)
  * [MCP Server](https://docs.sarvam.ai/api/developer-tools/mcp)
  * [Markdown & llms.txt](https://docs.sarvam.ai/api/developer-tools/llms-txt)
  * [Context7](https://docs.sarvam.ai/api/developer-tools/context7)
  * [Agent Skills](https://docs.sarvam.ai/api/developer-tools/agent-skills)
  * [Call Analytics Pipeline](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)
  * [Live Video Transcription](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)
  * [Podcast Generator](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator)
  * [WhatsApp Bot](https://docs.sarvam.ai/api/cookbook/guides/whats-app-bot)
  * [Collection Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/collection-agent)
  * [Government Scheme Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent)
  * [Tutor Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/tutor-agent)
  * [Loan Advisory Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/loan-advisory-agent)
  * [Introduction](https://docs.sarvam.ai/api/self-hosted/introduction)
  * [Managed vs Self-Hosted](https://docs.sarvam.ai/api/self-hosted/hosted-vs-self-hosted)
  * [How it works](https://docs.sarvam.ai/api/self-hosted/architecture)
  * [Get started](https://docs.sarvam.ai/api/self-hosted/sagemaker/get-started)
  * [Speech-to-Text (Saaras v3)](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-saaras)
  * [Sarvam Vision](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-vision)
  * [Text-to-Speech (Bulbul v3)](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-bulbul)
  * [Deploy with Terraform](https://docs.sarvam.ai/api/self-hosted/sagemaker/terraform)
  * [Speech-to-Text](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-saaras)
  * [Sarvam Vision](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-vision)
  * [Text-to-Speech](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-bulbul)
  * [Error handling](https://docs.sarvam.ai/api/self-hosted/sagemaker/errors)
  * [Configure & tune](https://docs.sarvam.ai/api/self-hosted/sagemaker/configure)
  * [Operations](https://docs.sarvam.ai/api/self-hosted/sagemaker/operations)
  * [Limitations](https://docs.sarvam.ai/api/self-hosted/sagemaker/limitations)
  * [Troubleshooting](https://docs.sarvam.ai/api/self-hosted/sagemaker/troubleshooting)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text)
  * [Instant Voice Cloning](https://docs.sarvam.ai/api/migrations/from-elevenlabs/voice-cloning)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-cartesia/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-cartesia/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-cartesia/speech-to-text)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-deepgram/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-deepgram/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-deepgram/speech-to-text)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-gemini/overview)
  * [Chat Completion](https://docs.sarvam.ai/api/migrations/from-gemini/chat-completion)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-gemini/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-gemini/speech-to-text)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


