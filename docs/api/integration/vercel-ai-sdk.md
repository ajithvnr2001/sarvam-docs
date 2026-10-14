---
url: https://docs.sarvam.ai/api/integration/vercel-ai-sdk/
title: Build with Sarvam AI in the Vercel AI SDK | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:43.298422+00:00
---

# Build with Sarvam AI in the Vercel AI SDK | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/vercel-ai-sdk/

Skip to navigation

On this page

  * Overview
  * Quick start
  * 1\. Install
  * 2\. Set your API key
  * 3\. Create a provider instance
  * 4\. Generate text
  * Text-to-speech
  * Speech-to-text
  * Translation
  * Transliteration
  * Language identification
  * Tool calling
  * Structured output
  * All APIs at a glance
  * Troubleshooting
  * Additional resources
  * Need help?



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

# Build with Sarvam AI in the Vercel AI SDK

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/vercel-ai-sdk.md "View this page as plain text")|More actions

This page is for Model APIs.

## Overview

The **[Vercel AI SDK](https://ai-sdk.dev/)** is a TypeScript toolkit for building AI-powered applications, giving you a single set of functions (`generateText`, `streamText`, `generateObject`, and more) that work the same way across different model providers. Instead of learning each provider’s own API, you write your app logic once against the AI SDK and swap providers by changing the `model` you pass in.

**[sarvam-ai-sdk](https://github.com/sarvamai/sarvam-ai-sdk)** is a community provider for the Vercel AI SDK that wraps Sarvam’s **chat completion** , **text-to-speech** , **speech-to-text** , **translation** , **transliteration** , and **language identification** APIs behind the AI SDK’s standard functions: `generateText`, `generateObject`, `generateSpeech`, and `transcribe`.

If you already build with the AI SDK, this lets you swap in Sarvam models without changing how you call `generateText` or stream responses, and it works alongside tool calling and structured output the same way any other AI SDK provider does.

`sarvam-ai-sdk` versions track a specific major version of `ai`. Install matching versions or you will hit type and runtime mismatches.

Sarvam AI SDK version| Vercel AI SDK version  
---|---  
`0.5.x` (beta)| `8.x.x` (beta)  
`0.4.x` (current)| `7.x.x` (current)  
`0.3.x`| `6.x.x`  
`0.2.x`| `5.x.x`  
`0.1.x`| `4.x.x`  
  
## Quick start

### 1\. Install
    
    
    npm install sarvam-ai-sdk ai@7

`sarvam-ai-sdk` currently tracks AI SDK v7; installing `ai@latest` can silently pull in an incompatible future major version, so pin the major version shown in the compatibility table above.

### 2\. Set your API key

Get an API key from **[dashboard.sarvam.ai](https://dashboard.sarvam.ai/)** and add it to your environment:

.env
    
    
    SARVAM_API_KEY="your_api_key"

### 3\. Create a provider instance
    
    
    import { sarvam } from "sarvam-ai-sdk";

`sarvam` reads `SARVAM_API_KEY` from the environment automatically, so no explicit client setup is needed.

### 4\. Generate text
    
    
    import { sarvam } from "sarvam-ai-sdk";
    
    import { generateText } from "ai";
    
    try {
    
      const { text } = await generateText({
    
        model: sarvam("sarvam-105b"),
    
        prompt: "Translate this to malayalam: 'Keep cooking, guys'",
    
      });
    
      console.log(text); // പാചകം തുടരൂ, സുഹൃത്തുക്കളേ
    
    } catch (error) {
    
      console.error("generateText failed:", error);
    
    }

If longer completions come back truncated mid-sentence, the model is hitting its output token limit. Raise the limit and check the finish reason to confirm when a response was truncated. Through the AI SDK this is `maxOutputTokens` / `finishReason`; calling Sarvam directly (Python or REST) it’s the underlying `max_tokens` / `finish_reason`:

JavaScriptPythonBash
    
    
    const result = await generateText({
    
      model: sarvam("sarvam-105b"),
    
      prompt: "Write a detailed explanation of...",
    
      maxOutputTokens: 4096,
    
    });
    
    if (result.finishReason === "length") {
    
      console.warn("Response was truncated; consider raising maxOutputTokens further.");
    
    }

* * *

## Text-to-speech

Use `generateSpeech` with `sarvam.speech(model, targetLanguage)`:
    
    
    import { sarvam } from "sarvam-ai-sdk";
    
    import { generateSpeech } from "ai";
    
    import { writeFile } from "fs/promises";
    
    try {
    
      const { audio } = await generateSpeech({
    
        model: sarvam.speech("bulbul:v3", "ml-IN"),
    
        text: "പാചകം തുടരൂ, സുഹൃത്തുക്കളേ",
    
      });
    
      const audioBuffer = Buffer.from(audio.base64, "base64");
    
      await writeFile("./output.wav", audioBuffer);
    
    } catch (error) {
    
      console.error("generateSpeech failed:", error);
    
    }

See [Text to Speech](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview) for supported languages, speakers, and audio options available on the underlying API.

## Speech-to-text

Use `transcribe` with `sarvam.transcription(model, language)`:
    
    
    import { sarvam } from "sarvam-ai-sdk";
    
    import { transcribe } from "ai";
    
    import { readFile } from "fs/promises";
    
    try {
    
      const { text } = await transcribe({
    
        model: sarvam.transcription("saaras:v4", "en-IN"),
    
        audio: await readFile("./input.wav"),
    
      });
    
      console.log(text); // Pachakam thudaroo, suhruthukkale.
    
    } catch (error) {
    
      console.error("transcribe failed:", error);
    
    }

See [Saaras](https://docs.sarvam.ai/api/getting-started/models/saaras) for model details.

## Translation
    
    
    import { sarvam } from "sarvam-ai-sdk";
    
    import { generateText } from "ai";
    
    try {
    
      const result = await generateText({
    
        model: sarvam.translation("mayura:v1", {
    
          from: "ml-IN",
    
          to: "en-IN",
    
        }),
    
        prompt: "ഇതൊക്കെ ശ്രദ്ധിക്കണ്ടേ അംബാനെ?",
    
      });
    
      console.log(result.text); // Shouldn't we be careful about this, Ambane?
    
    } catch (error) {
    
      console.error("Translation failed:", error);
    
    }

Only `prompt` and `role: user` messages are translated; `system` and `assistant` messages pass through unchanged.

## Transliteration
    
    
    import { sarvam } from "sarvam-ai-sdk";
    
    import { generateText } from "ai";
    
    try {
    
      const result = await generateText({
    
        model: sarvam.transliterate({
    
          to: "ml-IN",
    
          from: "en-IN", // optional
    
        }),
    
        prompt: "eda mone, happy alle?",
    
      });
    
      console.log(result.text); // എടാ മോനെ, ഹാപ്പി അല്ലേ?
    
    } catch (error) {
    
      console.error("Transliteration failed:", error);
    
    }

## Language identification
    
    
    import { sarvam } from "sarvam-ai-sdk";
    
    import { generateText } from "ai";
    
    try {
    
      const result = await generateText({
    
        model: sarvam.languageIdentification(),
    
        prompt: "ബുദ്ധിയാണ് സാറേ ഇവൻ്റെ മെയിൻ",
    
      });
    
      console.log(result.text); // ml-IN
    
    } catch (error) {
    
      console.error("Language identification failed:", error);
    
    }

* * *

## Tool calling

Sarvam chat models support the AI SDK’s standard `tool()` interface:
    
    
    import { z } from "zod";
    
    import { generateText, tool } from "ai";
    
    import { sarvam } from "sarvam-ai-sdk";
    
    try {
    
      const result = await generateText({
    
        model: sarvam("sarvam-105b"),
    
        tools: {
    
          weather: tool({
    
            description: "Get the weather in a location",
    
            inputSchema: z.object({
    
              location: z.string(),
    
            }),
    
            execute: async ({ location }) => ({
    
              location,
    
              temperature: 72 + Math.floor(Math.random() * 21) - 10,
    
            }),
    
          }),
    
        },
    
        instructions: "You are a helpful AI",
    
        prompt: "കൊച്ചിയിലെ കാലാവസ്ഥ എന്താണ്?",
    
      });
    
      console.log(result.toolResults);
    
    } catch (error) {
    
      console.error("Tool call failed:", error);
    
    }

## Structured output

Prefer `generateText` with `Output.object`; `generateObject` still works but is deprecated in the AI SDK:
    
    
    import { z } from "zod";
    
    import { sarvam } from "sarvam-ai-sdk";
    
    import { generateText, Output } from "ai";
    
    try {
    
      const { output } = await generateText({
    
        model: sarvam("sarvam-105b"),
    
        output: Output.object({
    
          name: "Recipe",
    
          description: "A recipe with a name, ingredients and steps",
    
          schema: z.object({
    
            recipe: z.object({
    
              name: z.string(),
    
              ingredients: z.array(z.string()),
    
              steps: z.array(z.string()),
    
            }),
    
          }),
    
        }),
    
        prompt: "Generate a South Indian recipe, in Malayalam",
    
      });
    
      console.log(output);
    
    } catch (error) {
    
      console.error("Structured output generation failed:", error);
    
    }

* * *

## All APIs at a glance
    
    
    import { sarvam } from "sarvam-ai-sdk";
    
    // Chat completion
    
    sarvam("sarvam-105b");
    
    sarvam.languageModel("sarvam-105b");
    
    // Transliteration
    
    sarvam.transliterate({ to: "ml-IN", from: "en-IN" });
    
    // Translation
    
    sarvam.translation("mayura:v1", { from: "en-IN", to: "ml-IN" });
    
    // Language identification
    
    sarvam.languageIdentification();
    
    // Text-to-speech
    
    sarvam.speech("bulbul:v3", "ml-IN");
    
    // Speech-to-text
    
    sarvam.transcription("saaras:v4");

Function| AI SDK entry point| Underlying Sarvam capability  
---|---|---  
`sarvam("sarvam-105b")` / `sarvam.languageModel(...)`| `generateText`, `generateObject`, `streamText`| [Chat completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)  
`sarvam.translation(model, { from, to })`| `generateText`| [Translation](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/translation)  
`sarvam.transliterate({ from, to })`| `generateText`| Transliteration  
`sarvam.languageIdentification()`| `generateText`| [Language identification](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/language-detection)  
`sarvam.speech(model, targetLanguage)`| `generateSpeech`| [Text to Speech](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)  
`sarvam.transcription(model, language)`| `transcribe`| [Speech to Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)  
  
* * *

## Troubleshooting

**Type or runtime errors after install:** Your `sarvam-ai-sdk` and `ai` versions are mismatched. Check the version table above and pin `ai` to the major version your `sarvam-ai-sdk` version expects (for example `ai@6` with `sarvam-ai-sdk@0.3.x`).

**401/403 from Sarvam:** Confirm `SARVAM_API_KEY` is set in the environment the process actually reads (`.env` loaded, no stray whitespace in the key). Sarvam’s REST API returns `403` (not `401`) for auth failures; see [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting).

**Translation/transliteration/LID returns the input unchanged:** These wrappers only act on `prompt` and `role: user` messages; `system` and `assistant` messages are passed through as-is by design.

**`generateObject` deprecation warnings:** Migrate to `generateText` with `Output.object(...)` as shown above; `generateObject` still works but is deprecated upstream in the AI SDK.

**Responses get cut off partway through:** Output length is capped by default (`maxOutputTokens` in the AI SDK, `max_tokens` when calling Sarvam directly from Python or REST), so long completions can stop mid-sentence. Raise the limit and check the finish reason (`finishReason` / `finish_reason` equals `"length"`) to confirm when a response was truncated; see the [Generate text](https://docs.sarvam.ai/api/integration/vercel-ai-sdk#4-generate-text) section above for examples in JavaScript, Python, and cURL.

* * *

## Additional resources

  * [sarvam-ai-sdk on GitHub](https://github.com/sarvamai/sarvam-ai-sdk) (source, issues, changelog)
  * [sarvam-ai-sdk on npm](https://npmjs.com/sarvam-ai-sdk)
  * [Sarvam provider on the AI SDK docs](https://v7.ai-sdk.dev/providers/community-providers/sarvam)
  * [Chat completion overview](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * [Text to Speech overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)
  * [Speech to Text overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)
  * [Build workflows with Sarvam AI in n8n](https://docs.sarvam.ai/api/integration/n8n) (same Sarvam capabilities without writing code)
  * [Build with Sarvam AI in LangChain](https://docs.sarvam.ai/api/integration/langchain) (same chat capability from a Python app)



* * *

## Need help?

  * Sarvam Support: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Community: [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/n8n)[Build with Sarvam AI in LangChainNext](https://docs.sarvam.ai/api/integration/langchain)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


