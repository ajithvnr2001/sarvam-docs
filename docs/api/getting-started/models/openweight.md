---
url: https://docs.sarvam.ai/api/getting-started/models/openweight/
title: Open-Weight Models | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:33.933774+00:00
---

# Open-Weight Models | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/getting-started/models/openweight/

Skip to navigation

On this page

  * Choose a model
  * Which model should I use?
  * Quickstart
  * Common patterns
  * Reasoning
  * Troubleshooting
  * Production tips
  * Platform details
  * Next steps



Scroll to top

[Getting Started](https://docs.sarvam.ai/api/getting-started/welcome)[Models](https://docs.sarvam.ai/api/getting-started/models)

# Open-Weight Models

Beta

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/getting-started/models/openweight.md "View this page as plain text")|More actions

This page is for Model APIs.

Run leading **open-weight models** on Sarvam infrastructure through the same OpenAI-compatible `/v2` API, with your existing Sarvam API key and credits. Switching models is a one-line change to the `model` field.

**Available in beta.** Your API key must be [whitelisted for beta access](https://docs.sarvam.ai/api-reference/beta-apis) before these models respond. [Contact us](https://docs.sarvam.ai/api/getting-started/help) to request access.

## Choose a model

[GLM-5.3**`glm5.3`**  
Software engineering and long-horizon agents. Reasoning, 1M context.](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)[Gemma 4 31B**`gemma4`**  
Fast direct answers and image understanding. 131K context.](https://docs.sarvam.ai/api/getting-started/models/openweight/gemma-4-31b)[DeepSeek V4.1 Flash**`deepseekv4.1-flash`**  
Low-cost reasoning for long documents and agents. 1M context.](https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash)

| GLM-5.3| Gemma 4 31B| DeepSeek V4.1 Flash  
---|---|---|---  
**Best for**|  Coding and long-horizon agents| Images and low-latency answers| Long documents and cost-sensitive reasoning  
**Model ID**| `glm5.3`| `gemma4`| `deepseekv4.1-flash`  
**Context window**|  1,048,576| 131,072| 1,048,576  
**Input**|  Text| Text + image| Text  
**Reasoning**| `low` · `high` · `max`| | `low` · `high` · `max`  
**Tool calling**| | |   
**Streaming**| | |   
**Log probabilities**| | |   
**Multiple choices (`n`)**| `1` only| |   
**Disable parallel tool calls**| | |   
**Input / output price** (per 1M tokens)| ₹126 / ₹390| ₹35 / ₹90| ₹25 / ₹105  
  
### Which model should I use?

If you need…| Use| Why  
---|---|---  
Hardest coding and multi-step agent tasks| `glm5.3`| Strongest reasoning, 1M context  
Cheapest reasoning over long documents| `deepseekv4.1-flash`| Lowest per-token price, 1M context  
Image input, or the lowest latency| `gemma4`| No reasoning pass, accepts images  
Log probabilities or `n > 1` with fast answers| `gemma4`| Not supported on `glm5.3`  
  
## Quickstart

[1](https://docs.sarvam.ai/api/getting-started/models/openweight#get-access)

### Get access

Create an API key in the [dashboard](https://dashboard.sarvam.ai/) and [request beta access](https://docs.sarvam.ai/api-reference/beta-apis) for it.

[2](https://docs.sarvam.ai/api/getting-started/models/openweight#set-your-key)

### Set your key
    
    
    export SARVAM_API_KEY="your-api-key"

[3](https://docs.sarvam.ai/api/getting-started/models/openweight#make-your-first-call)

### Make your first call

Open-weight models are served on `POST /v2/chat/completions`. Pick your SDK:

###### Python (Sarvam SDK)

###### Python (OpenAI SDK)

###### JavaScript

###### cURL
    
    
    import os
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    response = client.chat.completions_v2(
    
        model="glm5.3",  # or "gemma4", "deepseekv4.1-flash"
    
        messages=[
    
            {"role": "user", "content": "Summarise the causes of the 2008 financial crisis."}
    
        ],
    
        max_tokens=1000,
    
    )
    
    print(response.choices[0].message.content)

**Already use the OpenAI SDK?** Point `base_url` at `https://api.sarvam.ai/v2` and pass your Sarvam key as `api_key`. The endpoint also accepts `Authorization: Bearer <key>`. Native Sarvam clients use the `api-subscription-key` header. See [Authentication](https://docs.sarvam.ai/api-reference/authentication).

## Common patterns

###### Streaming

###### Reasoning

###### Tool calling

###### Images (Gemma)

Set `stream=True` to receive server-sent events. Reasoning models stream `reasoning_content` deltas first, then the final `content`.
    
    
    stream = client.chat.completions.create(
    
        model="glm5.3",
    
        messages=[{"role": "user", "content": "What is 17 * 23?"}],
    
        reasoning_effort="low",
    
        max_tokens=1000,
    
        stream=True,
    
    )
    
    for chunk in stream:
    
        if not chunk.choices:
    
            continue
    
        delta = chunk.choices[0].delta
    
        if getattr(delta, "reasoning_content", None):
    
            print(delta.reasoning_content, end="", flush=True)  # thinking
    
        if delta.content:
    
            print(delta.content, end="", flush=True)  # answer

## Reasoning

`glm5.3` and `deepseekv4.1-flash` think before answering. When `reasoning_effort` is omitted, the default is **`max`**.

API| Field| Values  
---|---|---  
[Chat Completion V2](https://docs.sarvam.ai/api-reference/chat/chat-completions-v2)| `reasoning_effort`| `low`, `high`, `max` (omit for `max`)  
[Responses](https://docs.sarvam.ai/api-reference/responses/create)| `reasoning.effort`| `low`, `high`, or omit for `max`  
  
On the Responses API, do **not** send the string `"max"` to `glm5.3`. It returns `400`. Omit the `reasoning` field instead.

Reasoning tokens count toward `max_tokens` and are billed as output. If you see empty `content` with `finish_reason: "length"`, the model spent the whole budget thinking. Raise `max_tokens` or lower the effort. On `glm5.3`, `max_tokens` defaults to `2048`.

## Troubleshooting

Symptom| Likely cause| Fix  
---|---|---  
`400 invalid_request_error` before the model runs| Key not whitelisted for beta| [Request access](https://docs.sarvam.ai/api-reference/beta-apis)  
`403 invalid_api_key_error`| Missing or wrong key header| Check `api-subscription-key` or the Bearer token  
`404 not_found_error`| Unknown or wrongly cased model ID| IDs are case-sensitive. List them with [`GET /v2/models`](https://docs.sarvam.ai/api-reference/chat/models-v2)  
Empty `content`, `finish_reason: "length"`| Reasoning used the token budget| Raise `max_tokens` or lower `reasoning_effort`  
`400` on `logprobs` or `n > 1`| Unsupported on `glm5.3`| See the comparison table above  
`402 insufficient_quota_error`| No credits left| Add credits in the [dashboard](https://dashboard.sarvam.ai/)  
`429 rate_limit_exceeded_error` or `503`| Rate limit or overload| Retry with exponential backoff  
  
## Production tips

###### Retry on 429 and 503

Rate limits and temporary overload are retryable. The OpenAI SDK retries these automatically with backoff when you raise `max_retries`:
    
    
    client = OpenAI(
    
        base_url="https://api.sarvam.ai/v2",
    
        api_key=os.environ["SARVAM_API_KEY"],
    
        max_retries=4,
    
        timeout=120,  # reasoning at high effort can take a while
    
    )

###### Budget tokens for reasoning

Set `max_tokens` well above your expected answer length, at least a few thousand for `high` or `max` effort, because thinking tokens share the same budget.

###### Match effort to the task

Use `low` for extraction, classification and chat. Reserve `high` and `max` for math, debugging and multi-step planning, where extra thinking improves quality at higher latency and cost.

###### Switch models without code changes

Read the model ID from configuration, for example `model=os.environ.get("SARVAM_MODEL", "glm5.3")`, so you can compare models on your own prompts. Only change parameters the target model supports, see the comparison table above.

## Platform details

###### Endpoints and model discovery

  * **Chat:** `POST https://api.sarvam.ai/v2/chat/completions`, see the [API reference](https://docs.sarvam.ai/api-reference/chat/chat-completions-v2).
  * **Responses:** `POST https://api.sarvam.ai/v2/responses`, see the [API reference](https://docs.sarvam.ai/api-reference/responses/create).
  * **Models:** [`GET /v2/models`](https://docs.sarvam.ai/api-reference/chat/models-v2) lists the IDs enabled for your key.



###### Billing and rate limits

Usage is metered per token against your Sarvam credits, see [Pricing](https://docs.sarvam.ai/api/getting-started/pricing). Reasoning is billed as output. Limits apply per API key, see [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits).

###### Beta access

Access is granted per API key. See [Access to Beta APIs](https://docs.sarvam.ai/api-reference/beta-apis).

## Next steps

[Chat Completions guideStreaming, tool calling and structured outputs.](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Responses APIStateless responses with reasoning and tools.](https://docs.sarvam.ai/api-reference/responses/create)[PricingPer-token rates for every model.](https://docs.sarvam.ai/api/getting-started/pricing)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)[GLM-5.3Next](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
    * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
    * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
    * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
    * [Models](https://docs.sarvam.ai/api/getting-started/models)
      * [Saaras](https://docs.sarvam.ai/api/getting-started/models/saaras)
      * [Bulbul](https://docs.sarvam.ai/api/getting-started/models/bulbul)
      * [Sarvam 105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)
      * [Open-Weight ModelsBeta](https://docs.sarvam.ai/api/getting-started/models/openweight)
        * [GLM-5.3Beta](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)
        * [Gemma 4 31BBeta](https://docs.sarvam.ai/api/getting-started/models/openweight/gemma-4-31b)
        * [DeepSeek V4.1 FlashBeta](https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash)

      * [Mayura](https://docs.sarvam.ai/api/getting-started/models/mayura)
      * [Sarvam Translate](https://docs.sarvam.ai/api/getting-started/models/sarvam-translate)
      * [Sarvam Vision](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)
      * Deprecated Models

    * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
    * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
    * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
    * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
    * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
    * Account & Billing

  * API Guides & Tutorials

    * Large Language Models

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


