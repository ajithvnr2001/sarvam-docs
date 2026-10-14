---
url: https://sarvam.ai/integrations/vercel-ai-sdk/
title: Vercel AI SDK Integration | Sarvam
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:49.157529+00:00
---

# Vercel AI SDK Integration | Sarvam

> Source: https://sarvam.ai/integrations/vercel-ai-sdk/

[Integrations](https://sarvam.ai/integrations) / Vercel AI SDK

![Vercel AI SDK logo](https://sarvam.ai/assets/integrations/vercel-logo.svg)

#  Sarvam + Vercel AI SDK 

Developer Tools 

Community provider for the Vercel AI SDK. Call Sarvam chat, text-to-speech, speech-to-text, translation, transliteration, and language identification through the standard generateText, generateSpeech, and transcribe functions. 

[ Get Started](https://docs.sarvam.ai/api/integration/vercel-ai-sdk) [ View on GitHub](https://github.com/sarvamai/sarvam-ai-sdk)

Sarvam APIs Supported

saaras:v3 

###  Speech-to-Text 

Accurate transcription built for Indian accents, dialects, and real-world audio with speaker diarisation. 

bulbul:v3 

###  Text-to-Speech 

Natural, expressive voices across 11+ Indian languages for conversational AI, dubbing, and accessibility. 

sarvam-105b 

###  LLM 

Multilingual large language model with native proficiency across Indian languages for text generation and reasoning. 

Sarvam Translate 

###  Translation 

High-quality translation across 12+ Indian languages, optimised for conversational and enterprise content. 

How it works

1.

### Install the provider

npm install sarvam-ai-sdk ai@7

2.

### Add your API key

Set SARVAM_API_KEY in a .env file with a key from indus.sarvam.ai

3.

### Call the standard AI SDK functions

Import { sarvam } from "sarvam-ai-sdk" and pass it to generateText, generateSpeech, or transcribe

Quick start

Install

BashCopy
    
    
    npm install sarvam-ai-sdk ai@7

Code

JavaScriptCopy
    
    
    import { sarvam } from "sarvam-ai-sdk";
    import { generateText } from "ai";
    import { EXTERNAL_LINKS } from "@/config/links.config";
    
    const { text } = await generateText({
      model: sarvam("sarvam-105b"),
      prompt: "Translate this to malayalam: 'Keep cooking, guys'",
    });
    
    console.log(text); // പാചകം തുടരൂ, സുഹൃത്തുക്കളേ

Use cases

### Full-Stack

Full-Stack AI Apps

Add multilingual chat, TTS, and STT to Next.js and Vercel-hosted TypeScript apps without switching SDKs.

### Tool-Calling

Tool-Calling Agents

Build agents with function calling and structured output using the standard AI SDK interfaces.

### Multilingual

Multilingual Voice Features

Combine speech-to-text, translation, and text-to-speech behind one provider for Indic-language products.

Resources & details

Type Community Provider

Language TypeScript

Maintained by Sarvam AI

Install npm install sarvam-ai-sdk

[ Vercel AI SDK docs  → ](https://ai-sdk.dev)[ sarvam-ai-sdk on GitHub  → ](https://github.com/sarvamai/sarvam-ai-sdk)[ npm package  → ](https://npmjs.com/sarvam-ai-sdk)[ Sarvam API ref  → ](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)

Ready to build? Start building with Vercel AI SDK in minutes. 

Ready to build?

Start building with Vercel AI SDK in minutes.

[Get API Key](https://indus.sarvam.ai)
