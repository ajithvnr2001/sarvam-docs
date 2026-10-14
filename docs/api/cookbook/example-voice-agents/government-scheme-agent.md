---
url: https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent/
title: Government Scheme Awareness Agent using LiveKit | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:29.352267+00:00
---

# Government Scheme Awareness Agent using LiveKit | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent/

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
  * Example 1: Hindi-focused Agent
  * Example 2: Tamil Agent for Rural Tamil Nadu
  * Example 3: Bengali Agent for West Bengal
  * Example 4: Multilingual Agent (Auto-detect)
  * Example 5: Speech-to-English Agent (Saaras)
  * Available Options
  * Language Codes
  * Speaker Voices (Bulbul v3)
  * Pro Tips
  * Troubleshooting
  * Additional Resources
  * Need Help?



Scroll to top

[Cookbook](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)[Example Voice Agents](https://docs.sarvam.ai/api/cookbook/example-voice-agents/collection-agent)

# Government Scheme Awareness Agent using LiveKit

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent.md "View this page as plain text")|More actions

This page is for Model APIs.

Want a production voice agent without assembling the stack yourself? [Sarvam Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents) is a managed platform with speech recognition, reasoning, Indian-language voices, telephony, testing, and analytics included, from ₹3 per minute. This guide shows how to build your own pipeline on the APIs instead.

## Overview

This guide demonstrates how to build a **government scheme awareness agent** that helps citizens discover, understand, and learn how to apply for various government welfare schemes using **LiveKit** for real-time communication and **Sarvam AI** for speech processing. Ideal for government digital initiatives, NGOs, and citizen service centers.

For the broader architecture pattern this agent fits into, accessibility, grounding scheme facts, latency targets, see the [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services) use-case guide. For a closely related rural/farmer audience, see [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/agri-rural).

## What You’ll Build

A voice agent that can:

  * Explain various government schemes in simple language
  * Help citizens understand eligibility criteria
  * Guide users through application processes
  * Answer questions about benefits, documents required, and deadlines
  * Communicate in multiple Indian languages for maximum accessibility



## Quick Overview

  1. Get API keys (LiveKit, Sarvam)
  2. Install packages
  3. Create `.env` file with your API keys
  4. Write the agent code
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

Create `scheme_awareness_agent.py`:
    
    
    import logging
    
    from dotenv import load_dotenv
    
    from livekit.agents import JobContext, WorkerOptions, cli
    
    from livekit.agents.voice import Agent, AgentSession
    
    from livekit.plugins import sarvam
    
    # Load environment variables
    
    load_dotenv()
    
    # Set up logging
    
    logger = logging.getLogger("scheme-awareness-agent")
    
    logger.setLevel(logging.INFO)
    
    class GovernmentSchemeAgent(Agent):
    
        def __init__(self) -> None:
    
            super().__init__(
    
                # Government scheme awareness agent personality and instructions
    
                instructions="""
    
                    You are a helpful government scheme awareness assistant designed to help Indian citizens 
    
                    understand and access various government welfare schemes and programs.
    
                    
    
                    Your responsibilities:
    
                    - Explain government schemes in simple, easy-to-understand language
    
                    - Help citizens determine their eligibility for various schemes
    
                    - Provide information about required documents for applications
    
                    - Guide users through the application process step by step
    
                    - Answer questions about scheme benefits, deadlines, and procedures
    
                    - Suggest relevant schemes based on user's situation (farmer, student, senior citizen, etc.)
    
                    
    
                    Key government schemes you should know about:
    
                    - PM Kisan Samman Nidhi (farmer income support)
    
                    - Ayushman Bharat (health insurance)
    
                    - PM Awas Yojana (housing for all)
    
                    - Sukanya Samriddhi Yojana (girl child savings)
    
                    - PM Ujjwala Yojana (LPG connections)
    
                    - MGNREGA (rural employment guarantee)
    
                    - PM Jan Dhan Yojana (financial inclusion)
    
                    - Atal Pension Yojana (pension scheme)
    
                    - PM Mudra Yojana (small business loans)
    
                    - Skill India Mission (skill development)
    
                    
    
                    Communication guidelines:
    
                    - Use simple language avoiding complex jargon
    
                    - Be patient and willing to repeat or explain again
    
                    - Speak slowly and clearly
    
                    - Be encouraging and supportive
    
                    - If you don't know something, honestly say so and suggest where they can get accurate information
    
                    - Always mention official government portals for verification
    
                    - Be sensitive to the fact that many users may have limited formal education
    
                    
    
                    Start by greeting the user warmly and asking how you can help them today with government schemes.
    
                """,
    
                
    
                # Saaras v4 STT - Converts speech to text
    
                stt=sarvam.STT(
    
                    language="unknown",  # Auto-detect language for accessibility
    
                    model="saaras:v4",
    
                    mode="transcribe"
    
                ),
    
                
    
                # Sarvam LLM - The "brain" that processes and generates responses
    
                llm=sarvam.LLM(model="sarvam-105b"),
    
                
    
                # Bulbul TTS - Converts text to speech
    
                tts=sarvam.TTS(
    
                    language_code="hi-IN",  # Hindi as default for wider reach
    
                    model="bulbul:v4-flash",
    
                    speaker="simran"  # Warm and friendly female voice
    
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
    
            agent=GovernmentSchemeAgent(),
    
            room=ctx.room
    
        )
    
    if __name__ == "__main__":
    
        # Run the agent
    
        cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

### 5\. Run Your Agent
    
    
    python scheme_awareness_agent.py dev

### 6\. Test Your Agent

In a new terminal, run:
    
    
    python scheme_awareness_agent.py console

* * *

## Customization Examples

### Example 1: Hindi-focused Agent

For Hindi-speaking citizens:
    
    
    stt=sarvam.STT(
    
        language="hi-IN",  # Hindi
    
        model="saaras:v4",
    
        mode="transcribe"
    
    ),
    
    tts=sarvam.TTS(
    
        language_code="hi-IN",
    
        model="bulbul:v4-flash",
    
        speaker="simran"  # Warm and friendly voice
    
    )

### Example 2: Tamil Agent for Rural Tamil Nadu
    
    
    stt=sarvam.STT(language="ta-IN", model="saaras:v4", mode="transcribe"),
    
    tts=sarvam.TTS(
    
        language_code="ta-IN",
    
        model="bulbul:v4-flash",
    
        speaker="priya"
    
    )

### Example 3: Bengali Agent for West Bengal
    
    
    stt=sarvam.STT(language="bn-IN", model="saaras:v4", mode="transcribe"),
    
    tts=sarvam.TTS(
    
        language_code="bn-IN",
    
        model="bulbul:v4-flash",
    
        speaker="ishita"
    
    )

### Example 4: Multilingual Agent (Auto-detect)

For citizen service centers serving diverse populations:
    
    
    stt=sarvam.STT(language="unknown", model="saaras:v4", mode="transcribe"),  # Auto-detects language
    
    tts=sarvam.TTS(language_code="hi-IN", model="bulbul:v4-flash", speaker="simran")

### Example 5: Speech-to-English Agent (Saaras)

When you need to process regional language input but generate English reports. Saaras v4 handles both transcription (same-language output) and translation (English output) via the `mode` parameter: use `mode="translate"` for speech-to-English.
    
    
    # User speaks in any Indian language → Saaras converts to English → LLM processes
    
    stt=sarvam.STT(model="saaras:v4", mode="translate"),  # Speech-to-English translation
    
    llm=sarvam.LLM(model="sarvam-105b"),
    
    tts=sarvam.TTS(language_code="en-IN", model="bulbul:v4-flash", speaker="priya")

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

  * Use `language="unknown"` to serve citizens who speak different languages
  * Use warm, friendly voices like `simran` for citizen-facing services
  * Sarvam’s models handle code-mixing naturally - citizens often mix Hindi with English or regional languages
  * Consider deploying region-specific agents for better language accuracy
  * Keep responses simple and avoid bureaucratic jargon



* * *

## Troubleshooting

**API key errors** : Check that all keys are in your `.env` file and the file is in the same directory as your script.

**Module not found** : Run the installation command again based on your operating system.

**Poor transcription** : Try `language="unknown"` for auto-detection, or specify the correct language code.

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

[Previous](https://docs.sarvam.ai/api/cookbook/example-voice-agents/collection-agent)[Tutor Agent using PipecatNext](https://docs.sarvam.ai/api/cookbook/example-voice-agents/tutor-agent)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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

    * Developer Tools

  * Cookbook

    * Guides

    * Example Voice Agents
      * [Collection Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/collection-agent)
      * [Government Scheme Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent)
      * [Tutor Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/tutor-agent)
      * [Loan Advisory Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/loan-advisory-agent)

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


