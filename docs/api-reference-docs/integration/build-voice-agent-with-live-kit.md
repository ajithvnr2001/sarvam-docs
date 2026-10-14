---
url: https://docs.sarvam.ai/api-reference-docs/integration/build-voice-agent-with-live-kit/
title: Build Your First Voice Agent using LiveKit | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:17.289170+00:00
---

# Build Your First Voice Agent using LiveKit | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference-docs/integration/build-voice-agent-with-live-kit/

Skip to navigation

On this page

  * Overview
  * What You’ll Build
  * Quick Overview
  * Quick Start
  * 1\. Prerequisites
  * 2\. Install Dependencies
  * 3\. Create Environment File
  * 4\. Write Your Agent
  * 5\. Run Your Agent
  * 6\. Test Your Agent
  * Customization Examples
  * Example 1: Hindi Voice Agent
  * Example 2: Tamil Voice Agent
  * Example 3: Multilingual Agent (Auto-detect)
  * Example 4: Speech-to-English Agent (Saaras)
  * Available Options
  * Language Codes
  * Speaker Voices (Bulbul v3)
  * Pro Tips
  * Best Practices
  * 1\. Do Not Pass VAD to AgentSession
  * 2\. Enable Flush Signal in STT
  * 3\. Set Turn Detection to STT
  * 4\. Configure Min Endpointing Delay
  * Complete Optimized Example
  * Troubleshooting
  * Going to Production?
  * Additional Resources
  * Need Help?



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

# Build Your First Voice Agent using LiveKit

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit.md "View this page as plain text")|More actions

This page is for Model APIs.

Want a production voice agent without assembling the stack yourself? [Sarvam Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents) is a managed platform with speech recognition, reasoning, Indian-language voices, telephony, testing, and analytics included, from ₹3 per minute. This guide shows how to build your own pipeline on the APIs instead.

## Overview

This guide demonstrates how to build a **real-time voice agent** that can listen, understand, and respond naturally using **LiveKit** for real-time communication and **Sarvam AI** for speech processing. Perfect for building voice assistants, customer support bots, and conversational AI applications for Indian languages.

Use the [Sarvam voice-agents skill](https://github.com/sarvamai/skills/tree/main/voice-agents) to generate correct LiveKit integration code from your AI coding assistant:
    
    
    npx skills add sarvamai/skills --skill voice-agents

See [Agent Skills](https://docs.sarvam.ai/api/developer-tools/agent-skills) for the full list.

## What You’ll Build

A voice agent that can:

  * Listen to users speaking (in multiple Indian languages!)
  * Understand and process their requests
  * Respond back in natural-sounding voices



## Quick Overview

  1. Get API keys (LiveKit, Sarvam)
  2. Install packages: `pip install livekit-agents[sarvam,silero] python-dotenv`
  3. Create `.env` file with your API keys
  4. Write ~40 lines of Python code
  5. Run: `python agent.py dev`
  6. Test: `python agent.py console`



* * *

## Quick Start

### 1\. Prerequisites

  * Python 3.9 or higher
  * API keys from: 
    * [LiveKit Cloud](https://cloud.livekit.io/) (free account)
    * [Sarvam AI](https://dashboard.sarvam.ai/) (get API key from dashboard)



### 2\. Install Dependencies

###### macOS/Linux

###### Windows
    
    
    pip install "livekit-agents[sarvam,silero]" python-dotenv

### 3\. Create Environment File

Create a file named `.env` in your project folder and add your API keys:
    
    
    LIVEKIT_URL=wss://your-project-xxxxx.livekit.cloud
    
    LIVEKIT_API_KEY=APIxxxxxxxxxxxxx
    
    LIVEKIT_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    SARVAM_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx

Replace the values with your actual API keys.

### 4\. Write Your Agent

Create `agent.py`:
    
    
    import logging
    
    from dotenv import load_dotenv
    
    from livekit.agents import JobContext, WorkerOptions, cli
    
    from livekit.agents.voice import Agent, AgentSession
    
    from livekit.plugins import sarvam
    
    # Load environment variables
    
    load_dotenv()
    
    # Set up logging
    
    logger = logging.getLogger("voice-agent")
    
    logger.setLevel(logging.INFO)
    
    class VoiceAgent(Agent):
    
        def __init__(self) -> None:
    
            super().__init__(
    
                # Your agent's personality and instructions
    
                instructions="""
    
                    You are a helpful voice assistant.
    
                    Be friendly, concise, and conversational.
    
                    Speak naturally as if you're having a real conversation.
    
                """,
    
                
    
                # Saaras v4 STT - Converts speech to text
    
                stt=sarvam.STT(
    
                    language="unknown",  # Auto-detect language, or use "en-IN", "hi-IN", etc.
    
                    model="saaras:v4",
    
                    mode="transcribe"
    
                ),
    
                
    
                # Sarvam LLM - The "brain" that processes and generates responses
    
                llm=sarvam.LLM(model="sarvam-105b-conversations"),
    
                
    
                # Bulbul TTS - Converts text to speech
    
                tts=sarvam.TTS(
    
                    language_code="en-IN",
    
                    model="bulbul:v4-flash",
    
                    speaker="simran_en_customer"  # Female: priya, simran, ishita, kavya | Male: aditya, anand, rohan
    
                ),
    
            )
    
        
    
        async def on_enter(self):
    
            """Called when user joins - agent starts the conversation"""
    
            self.session.generate_reply()
    
    async def entrypoint(ctx: JobContext):
    
        """Main entry point - LiveKit calls this when a user connects"""
    
        logger.info(f"User connected to room: {ctx.room.name}")
    
        
    
        # Create and start the agent session
    
        session = AgentSession()
    
        await session.start(
    
            agent=VoiceAgent(),
    
            room=ctx.room
    
        )
    
    if __name__ == "__main__":
    
        # Run the agent
    
        cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

### 5\. Run Your Agent
    
    
    python agent.py dev

### 6\. Test Your Agent

In a new terminal, run:
    
    
    python agent.py console

That’s it! You’ve built your first voice agent!

* * *

## Customization Examples

### Example 1: Hindi Voice Agent
    
    
    stt=sarvam.STT(
    
        language="hi-IN",  # Hindi
    
        model="saaras:v4",
    
        mode="transcribe"
    
    ),
    
    tts=sarvam.TTS(
    
        language_code="hi-IN",
    
        model="bulbul:v4-flash",
    
        speaker="simran"  # Or: priya, ishita, kavya, aditya, anand, rohan
    
    )

### Example 2: Tamil Voice Agent
    
    
    stt=sarvam.STT(language="ta-IN", model="saaras:v4", mode="transcribe"),
    
    tts=sarvam.TTS(
    
        language_code="ta-IN",
    
        model="bulbul:v4-flash",
    
        speaker="simran_en_customer"
    
    )

### Example 3: Multilingual Agent (Auto-detect)
    
    
    stt=sarvam.STT(language="unknown", model="saaras:v4", mode="transcribe"),  # Auto-detects language
    
    tts=sarvam.TTS(language_code="en-IN", model="bulbul:v4-flash", speaker="anand")

### Example 4: Speech-to-English Agent (Saaras)

**Difference** : Saaras v4 handles both transcription (same-language output) and translation (English output) via the `mode` parameter. Use `mode="translate"` when user speaks Indian languages but you want to process/respond in English.
    
    
    # User speaks Hindi → Saaras converts to English → LLM processes → Responds in English
    
    stt=sarvam.STT(model="saaras:v4", mode="translate"),  # Speech-to-English translation
    
    llm=sarvam.LLM(model="sarvam-105b-conversations"),
    
    tts=sarvam.TTS(language_code="en-IN", model="bulbul:v4-flash", speaker="aditya")

**Note:** Saaras v4 with `mode="translate"` automatically detects the source language (Hindi, Tamil, etc.) and translates spoken content directly to English text, making Indian language speech comprehensible to English-based LLMs.

* * *

## Available Options

### Language Codes

Language| Code  
---|---  
English (India)| `en-IN`  
Hindi| `hi-IN`  
Bengali| `bn-IN`  
Tamil| `ta-IN`  
Telugu| `te-IN`  
Gujarati| `gu-IN`  
Kannada| `kn-IN`  
Malayalam| `ml-IN`  
Marathi| `mr-IN`  
Punjabi| `pa-IN`  
Odia| `od-IN`  
Auto-detect| `unknown`  
  
### Speaker Voices (Bulbul v3)

**Male (23):** Shubh (default), Aditya, Rahul, Rohan, Amit, Dev, Ratan, Varun, Manan, Sumit, Kabir, Aayan, Ashutosh, Advait, Anand, Tarun, Sunny, Mani, Gokul, Vijay, Mohit, Rehan, Soham

**Female (14):** Ritu, Priya, Neha, Pooja, Simran, Kavya, Ishita, Shreya, Roopa, Tanya, Shruti, Suhani, Kavitha, Rupali

* * *

## Pro Tips

  * Use `language="unknown"` to automatically detect the language. Great for multilingual scenarios!
  * Sarvam’s models understand code-mixing - your agent can naturally handle Hinglish, Tanglish, and other mixed languages.



* * *

## Best Practices

When using Sarvam AI plugins with LiveKit, follow these recommendations for optimal performance:

### 1\. Do Not Pass VAD to AgentSession

The `vad` parameter should **not** be passed to `AgentSession` as Voice Activity Detection is handled internally by the Sarvam plugin.
    
    
    # ❌ Avoid this
    
    session = AgentSession(vad=silero.VAD.load())
    
    # ✅ Do this instead
    
    session = AgentSession()

### 2\. Enable Flush Signal in STT

Add `flush_signal=True` to the STT configuration. This enables the plugin to emit start and end of speech events, which is essential for proper turn-taking.
    
    
    stt=sarvam.STT(
    
        language="unknown",
    
        model="saaras:v4",
    
        mode="transcribe",
    
        flush_signal=True  # Enables speech start/end events
    
    )

### 3\. Set Turn Detection to STT

Add `turn_detection="stt"` to the `AgentSession` configuration. This ensures turn detection is handled by the Sarvam plugin, which emits start and end of speech signals.
    
    
    session = AgentSession(turn_detection="stt")

### 4\. Configure Min Endpointing Delay

Set `min_endpointing_delay=0.07` in your `AgentSession`. The Sarvam STT plugin has a processing latency of approximately 70ms. This setting ensures the agent transitions to the next pipeline step (LLM) as soon as STT finishes processing, minimizing response delay.
    
    
    session = AgentSession(
    
        turn_detection="stt",
    
        min_endpointing_delay=0.07
    
    )

### Complete Optimized Example

Here’s a complete example incorporating all best practices:
    
    
    # STT with flush_signal enabled
    
    stt=sarvam.STT(
    
        language="unknown",
    
        model="saaras:v4",
    
        mode="transcribe",
    
        flush_signal=True
    
    )
    
    # AgentSession with optimized settings (no VAD parameter)
    
    session = AgentSession(
    
        turn_detection="stt",
    
        min_endpointing_delay=0.07
    
    )

* * *

## Troubleshooting

**API key errors** : Check that all keys are in your `.env` file and the file is in the same directory as your script.

**Module not found** : Run the installation command again based on your operating system (see Step 2 above).

**Poor transcription** : Try `language="unknown"` for auto-detection, or specify the correct language code (`en-IN`, `hi-IN`, etc.).

* * *

## Going to Production?

This guide gets a demo agent talking. Before you ship it, see [LiveKit in Production](https://docs.sarvam.ai/api/integration/livekit-production-best-practices) for the defaults you need to change: VAD and turn detection, endpointing delays, barge-in tuning, latency measurement, and a full caveats list derived from the Sarvam LiveKit plugin source.

* * *

## Additional Resources

  * [Sarvam AI Documentation](https://docs.sarvam.ai/)
  * [LiveKit Documentation](https://docs.livekit.io/)
  * [LiveKit Sarvam LLM Plugin](https://docs.livekit.io/agents/models/llm/sarvam/)
  * [LiveKit Sarvam STT Plugin](https://docs.livekit.io/agents/models/stt/plugins/sarvam/)
  * [LiveKit Sarvam TTS Plugin](https://docs.livekit.io/agents/models/tts/plugins/sarvam/)



* * *

## Need Help?

  * Sarvam Support: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Community: [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



* * *

**Happy Building!**

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/faq)[Build Your First Voice Agent using PipecatNext](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


