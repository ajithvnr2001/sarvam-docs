---
url: https://sarvam.ai/integrations/langchain/
title: LangChain Integration | Sarvam
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:49.370090+00:00
---

# LangChain Integration | Sarvam

> Source: https://sarvam.ai/integrations/langchain/

[Integrations](https://sarvam.ai/integrations) / LangChain

![LangChain logo](https://sarvam.ai/assets/integrations/langchain-logo.svg)

#  Sarvam + LangChain 

Agent Framework 

Official LangChain integration for Sarvam AI. Use ChatSarvam as a drop-in BaseChatModel for chains, agents, tool calling, and structured output, exactly like ChatOpenAI or ChatAnthropic. 

[ Get Started](https://docs.sarvam.ai/api/integration/langchain) [ View on GitHub](https://github.com/sarvamai/langchain-sarvam)

Sarvam APIs Supported

sarvam-105b 

###  LLM 

Multilingual large language model with native proficiency across Indian languages for text generation and reasoning. 

How it works

1.

### Install langchain-sarvam

pip install langchain-sarvam python-dotenv

2.

### Add your API key

Set SARVAM_API_KEY in a .env file with a key from indus.sarvam.ai

3.

### Create a ChatSarvam instance

Use ChatSarvam in chains, agents, or tool-calling loops like any other BaseChatModel

Quick start

Install

BashCopy
    
    
    pip install langchain-sarvam python-dotenv

Code

PythonCopy
    
    
    from langchain_sarvam import ChatSarvam
    
    llm = ChatSarvam(model="sarvam-105b")
    
    response = llm.invoke("Translate this to malayalam: 'Keep cooking, guys'")
    print(response.content)  # പാചകം തുടരൂ, സുഹൃത്തുക്കളേ

Use cases

### Multilingual

Multilingual Chat Agents

Build LangChain agents that reason and respond natively in Indian languages.

### Tool-Calling

Tool-Calling Pipelines

Wire Sarvam models into bind_tools() workflows alongside retrievers and other LangChain components.

### Structured

Structured Output Chains

Use with_structured_output() to extract typed, schema-constrained data from Indic-language text.

Resources & details

Type Official Integration

Language Python

Maintained by Sarvam AI

Install pip install langchain-sarvam

[ langchain-sarvam on GitHub  → ](https://github.com/sarvamai/langchain-sarvam)[ PyPI package  → ](https://pypi.org/project/langchain-sarvam/)[ LangChain docs  → ](https://python.langchain.com/docs/concepts/chat_models/)[ Sarvam API ref  → ](https://docs.sarvam.ai/api/integration/langchain)

Ready to build? Start building with LangChain in minutes. 

Ready to build?

Start building with LangChain in minutes.

[Get API Key](https://indus.sarvam.ai)
