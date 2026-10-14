---
url: https://docs.sarvam.ai/api/integration/langchain/
title: Build with Sarvam AI in LangChain | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:41.802802+00:00
---

# Build with Sarvam AI in LangChain | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/langchain/

Skip to navigation

On this page

  * Overview
  * Quick start
  * 1\. Install
  * 2\. Set your API key
  * 3\. Create a chat model instance
  * 4\. Invoke
  * Streaming
  * Async
  * Tool calling
  * Structured output
  * Reasoning mode
  * Capabilities at a glance
  * Troubleshooting
  * Additional resources
  * Need help?



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

# Build with Sarvam AI in LangChain

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/langchain.md "View this page as plain text")|More actions

This page is for Model APIs.

## Overview

**[LangChain](https://python.langchain.com/)** is a Python framework for building LLM applications, giving you a single set of interfaces (`invoke`, `stream`, `bind_tools`, `with_structured_output`, and more) that work the same way across different model providers. Instead of learning each provider’s own SDK, you write your app logic once against LangChain’s `BaseChatModel` interface and swap providers by changing the model you instantiate.

**[langchain-sarvam](https://pypi.org/project/langchain-sarvam/)** is the official LangChain integration package for Sarvam AI. It wraps the `sarvamai` Python SDK’s **chat completion** API behind LangChain’s `ChatSarvam` class, so Sarvam’s `sarvam-105b` model works as a drop-in `BaseChatModel` that you can use in chains, agents, retrievers, tool-calling loops, and structured-output pipelines exactly like `ChatOpenAI` or `ChatAnthropic` (including LangSmith tracing support).

## Quick start

### 1\. Install
    
    
    pip install langchain-sarvam python-dotenv

Requires Python 3.10+. `python-dotenv` loads `SARVAM_API_KEY` from a local `.env` file, used throughout the examples below.

### 2\. Set your API key

Get an API key from **[dashboard.sarvam.ai](https://dashboard.sarvam.ai/)** and add it to your environment:

.env
    
    
    SARVAM_API_KEY="your_api_key"

### 3\. Create a chat model instance
    
    
    import os
    
    from dotenv import load_dotenv
    
    from langchain_sarvam import ChatSarvam
    
    load_dotenv()
    
    if not os.getenv("SARVAM_API_KEY"):
    
        raise RuntimeError("Set SARVAM_API_KEY in your environment or .env file before running.")
    
    llm = ChatSarvam(model="sarvam-105b")

`ChatSarvam` reads `SARVAM_API_KEY` from the environment automatically, so no explicit client setup is needed. Pass `api_key="..."` directly if you’d rather not use an environment variable.

### 4\. Invoke
    
    
    import os
    
    from dotenv import load_dotenv
    
    from langchain_sarvam import ChatSarvam
    
    load_dotenv()
    
    if not os.getenv("SARVAM_API_KEY"):
    
        raise RuntimeError("Set SARVAM_API_KEY in your environment or .env file before running.")
    
    llm = ChatSarvam(model="sarvam-105b")
    
    try:
    
        response = llm.invoke("Translate this to malayalam: 'Keep cooking, guys'")
    
        print(response.content)  # പാചകം തുടരൂ, സുഹൃത്തുക്കളേ
    
    except Exception as e:
    
        print(f"Error: {e}")

If longer completions come back truncated mid-sentence, the model is hitting its output token limit. Raise `max_tokens` and check `finish_reason` to confirm when a response was truncated:
    
    
    import os
    
    from dotenv import load_dotenv
    
    from langchain_sarvam import ChatSarvam
    
    load_dotenv()
    
    if not os.getenv("SARVAM_API_KEY"):
    
        raise RuntimeError("Set SARVAM_API_KEY in your environment or .env file before running.")
    
    llm = ChatSarvam(model="sarvam-105b", max_tokens=4096)
    
    try:
    
        response = llm.invoke("Write a detailed explanation of...")
    
        if response.response_metadata.get("finish_reason") == "length":
    
            print("Response was truncated; consider raising max_tokens further.")
    
    except Exception as e:
    
        print(f"Error: {e}")

* * *

## Streaming
    
    
    import os
    
    from dotenv import load_dotenv
    
    from langchain_sarvam import ChatSarvam
    
    load_dotenv()
    
    if not os.getenv("SARVAM_API_KEY"):
    
        raise RuntimeError("Set SARVAM_API_KEY in your environment or .env file before running.")
    
    llm = ChatSarvam(model="sarvam-105b", streaming=True)
    
    try:
    
        for chunk in llm.stream("Count from 1 to 5."):
    
            print(chunk.content, end="", flush=True)
    
    except Exception as e:
    
        print(f"Error: {e}")

Token usage is emitted on the final chunk, so `chunk.usage_metadata` is populated once streaming completes, no extra configuration needed.

## Async
    
    
    import asyncio
    
    import os
    
    from dotenv import load_dotenv
    
    from langchain_sarvam import ChatSarvam
    
    load_dotenv()
    
    if not os.getenv("SARVAM_API_KEY"):
    
        raise RuntimeError("Set SARVAM_API_KEY in your environment or .env file before running.")
    
    llm = ChatSarvam(model="sarvam-105b")
    
    async def main():
    
        try:
    
            response = await llm.ainvoke("What is the capital of India?")
    
            print(response.content)
    
            async for chunk in llm.astream("Count from 1 to 3."):
    
                print(chunk.content, end="", flush=True)
    
        except Exception as e:
    
            print(f"Error: {e}")
    
    asyncio.run(main())

## Tool calling

`ChatSarvam` supports LangChain’s standard `bind_tools()` interface:
    
    
    import os
    
    from dotenv import load_dotenv
    
    from langchain_core.tools import tool
    
    from langchain_sarvam import ChatSarvam
    
    load_dotenv()
    
    if not os.getenv("SARVAM_API_KEY"):
    
        raise RuntimeError("Set SARVAM_API_KEY in your environment or .env file before running.")
    
    @tool
    
    def get_weather(city: str) -> str:
    
        """Get the weather for a city."""
    
        return f"Sunny in {city}"
    
    llm = ChatSarvam(model="sarvam-105b")
    
    llm_with_tools = llm.bind_tools([get_weather])
    
    try:
    
        response = llm_with_tools.invoke("What is the weather in Mumbai?")
    
        print(response.tool_calls)
    
    except Exception as e:
    
        print(f"Error: {e}")

Pass `tool_choice="auto"` (model decides), `tool_choice="none"` (disabled), `tool_choice="required"` (must call a tool), or a tool name string to force a specific tool.

## Structured output
    
    
    import os
    
    from dotenv import load_dotenv
    
    from pydantic import BaseModel
    
    from langchain_sarvam import ChatSarvam
    
    load_dotenv()
    
    if not os.getenv("SARVAM_API_KEY"):
    
        raise RuntimeError("Set SARVAM_API_KEY in your environment or .env file before running.")
    
    class CapitalCity(BaseModel):
    
        city: str
    
        country: str
    
    llm = ChatSarvam(model="sarvam-105b")
    
    structured_llm = llm.with_structured_output(CapitalCity)
    
    try:
    
        result = structured_llm.invoke("What is the capital of France?")
    
        print(result)  # CapitalCity(city='Paris', country='France')
    
    except Exception as e:
    
        print(f"Error: {e}")

`with_structured_output()` sends an explicit `reasoning_effort=None` by default, unless the model or the call already sets `reasoning_effort`. Sarvam’s reasoning models default to `reasoning_effort="medium"` server-side, and the resulting `reasoning_content` competes with the structured JSON payload for the same completion token budget. Disabling reasoning by default keeps that budget free for the structured output. Pass `reasoning_effort="low"`, `"medium"`, or `"high"` explicitly (on the model or the call) to combine reasoning with structured output.

## Reasoning mode

Pass `reasoning_effort` to control how much effort the model puts into reasoning before responding: `"low"`, `"medium"`, or `"high"`. Leaving it unset lets the API apply its own default.
    
    
    import os
    
    from dotenv import load_dotenv
    
    from langchain_sarvam import ChatSarvam
    
    load_dotenv()
    
    if not os.getenv("SARVAM_API_KEY"):
    
        raise RuntimeError("Set SARVAM_API_KEY in your environment or .env file before running.")
    
    reasoning_llm = ChatSarvam(model="sarvam-105b", reasoning_effort="high")
    
    try:
    
        response = reasoning_llm.invoke("Explain the Riemann hypothesis.")
    
        print(response.additional_kwargs.get("reasoning_content"))
    
        print(response.content)
    
    except Exception as e:
    
        print(f"Error: {e}")

See [Reasoning effort](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/adjust-the-models-thinking-level) for details on the allowed values.

* * *

## Capabilities at a glance

`ChatSarvam` interface| LangChain concept| Underlying Sarvam capability  
---|---|---  
`invoke` / `ainvoke`| Sync/async single-turn completion| [Chat completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)  
`stream` / `astream`| Sync/async token streaming| Chat completion (streaming)  
`bind_tools`| Tool/function calling| Chat completion (tool calling)  
`with_structured_output`| Schema-constrained output| Chat completion ([Structured Outputs](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1) via `response_format`)  
`reasoning_effort` param| Extended reasoning| [Reasoning effort](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/adjust-the-models-thinking-level)  
  
Supported model: [Sarvam 105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b) (flagship, 128K context).

* * *

## Troubleshooting

###### ValueError: Sarvam API key not found

Set `SARVAM_API_KEY` in the environment the process actually reads (`.env` loaded, no stray whitespace in the key), or pass `api_key="..."` explicitly when constructing `ChatSarvam`.

###### 401/403 from Sarvam

Sarvam’s API returns `403` (not `401`) for auth failures; see [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting).

###### Calling a non-default environment

Set `SARVAM_API_BASE_URL`, or pass `base_url="..."` to `ChatSarvam`, to point at a different API base URL than `https://api.sarvam.ai/v1`.

###### Responses get cut off partway through

Output length is capped by `max_tokens` (unset by default, so the API’s own default applies). Raise it and check `response.response_metadata["finish_reason"] == "length"` to confirm truncation; see the [Invoke](https://docs.sarvam.ai/api/integration/langchain#4-invoke) section above.

###### ValueError: Got unknown message type

`ChatSarvam` only converts `SystemMessage`, `HumanMessage`, `AIMessage`, and `ToolMessage`. This surfaces when older-style `FunctionMessage`s or a generic `ChatMessage` end up in the history, commonly from a prebuilt agent or migrated codebase, since those aren’t converted. Map them to `ToolMessage`/`HumanMessage` before passing the history to `ChatSarvam`.

###### Catching a specific error type (e.g. rate limits) never triggers

`ChatSarvam` wraps every exception from the underlying `sarvamai` client, including auth, rate limit, and network errors, in a single `ChatSarvamError`. Catch `ChatSarvamError` rather than a provider-specific exception type, and inspect `str(e)` for the underlying cause.

* * *

## Additional resources

  * [langchain-sarvam on PyPI](https://pypi.org/project/langchain-sarvam/)
  * [LangChain chat models documentation](https://python.langchain.com/docs/concepts/chat_models/)
  * [Chat completion overview](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * [Build with Sarvam AI in the Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk) (same chat capability from a TypeScript app)
  * [Build workflows with Sarvam AI in n8n](https://docs.sarvam.ai/api/integration/n8n) (same Sarvam capabilities without writing code)



* * *

## Need help?

  * Sarvam Support: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Community: [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)[LiveKit in ProductionNext](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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

    * Speech to Text

    * Text to Speech

    * Text Processing

    * Document Intelligence

    * Document Translation

    * Dubbing

    * Instant Voice CloningBeta

  *     * Integration
      * [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)
      * [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)
      * [Twilio](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio)
      * [Exotel](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)
      * [Vobiz](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)
      * [Vapi](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)
      * [n8n](https://docs.sarvam.ai/api/integration/n8n)
      * [Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)
      * [LangChain](https://docs.sarvam.ai/api/integration/langchain)
      * Best Practices

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


