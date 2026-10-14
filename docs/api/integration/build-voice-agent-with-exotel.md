---
url: https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel/
title: Build Your First Voice Agent using Exotel | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:40.533191+00:00
---

# Build Your First Voice Agent using Exotel | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel/

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
  * 5\. Configure Exotel to Reach Your Agent
  * 6\. Run Your Agent
  * 7\. Test Your Agent
  * Customization Examples
  * Example 1: Hindi Voice Agent
  * Example 2: Tamil Voice Agent
  * Example 3: Multilingual Agent (Auto-detect)
  * Example 4: Speech-to-English Agent (Saaras)
  * Available Options
  * Language Codes
  * Speaker Voices (Bulbul v3)
  * TTS Additional Parameters
  * Understanding the Call Flow
  * Pro Tips
  * Troubleshooting
  * Additional Resources
  * Need Help?



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

# Build Your First Voice Agent using Exotel

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel.md "View this page as plain text")|More actions

This page is for Model APIs.

Want a production voice agent without assembling the stack yourself? [Sarvam Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents) is a managed platform with speech recognition, reasoning, Indian-language voices, telephony, testing, and analytics included, from ₹3 per minute. This guide shows how to build your own pipeline on the APIs instead.

## Overview

This guide shows you how to build a **real-time voice agent that answers phone calls**. It uses **Exotel** for telephony, **Pipecat** to orchestrate the real-time audio pipeline, and **Sarvam AI** for speech-to-text, the LLM, and text-to-speech. It’s a great starting point for IVR replacements, customer support lines, and conversational phone agents in Indian languages.

## What You’ll Build

A voice agent that can:

  * Answer inbound phone calls on an Exotel number
  * Listen to callers speaking, in multiple Indian languages
  * Understand and process what they say
  * Respond back in a natural-sounding voice, over the phone



## Quick Overview

  1. Get an API key (Sarvam). Exotel needs no API credentials for this flow.
  2. Install packages: `pip install "pipecat-ai[websocket,sarvam]" python-dotenv`
  3. Create a `.env` file with your API key
  4. Write about 80 lines of Python code
  5. Point an Exotel Voicebot Applet at your agent’s WebSocket URL
  6. Call your Exotel number



* * *

## Quick Start

### 1\. Prerequisites

  * Python 3.9 or higher
  * [ngrok](https://ngrok.com/download), to expose your local server during development
  * An [Exotel](https://my.exotel.com/) account with voice streaming enabled and a provisioned ExoPhone
  * A [Sarvam AI](https://dashboard.sarvam.ai/) API key from your dashboard



Unlike Twilio, Exotel’s dial-in flow doesn’t require an account SID or auth token in your bot code. Pipecat’s `ExotelFrameSerializer` only needs the stream and call identifiers Exotel sends over the WebSocket itself.

### 2\. Install Dependencies

###### macOS/Linux

###### Windows
    
    
    pip install "pipecat-ai[websocket,sarvam]" python-dotenv loguru

### 3\. Create Environment File

Create a file named `.env` in your project folder:
    
    
    SARVAM_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx

Replace the placeholder with your real key from the [Sarvam dashboard](https://dashboard.sarvam.ai/).

### 4\. Write Your Agent

Create `agent.py`:
    
    
    import os
    
    from dotenv import load_dotenv
    
    from loguru import logger
    
    from pipecat.frames.frames import LLMRunFrame
    
    from pipecat.pipeline.pipeline import Pipeline
    
    from pipecat.pipeline.runner import PipelineRunner
    
    from pipecat.pipeline.task import PipelineParams, PipelineTask
    
    from pipecat.processors.aggregators.llm_context import LLMContext
    
    from pipecat.processors.aggregators.llm_response_universal import (
    
        LLMContextAggregatorPair,
    
    )
    
    from pipecat.runner.types import RunnerArguments
    
    from pipecat.runner.utils import create_transport
    
    from pipecat.services.sarvam.stt import SarvamSTTService
    
    from pipecat.services.sarvam.tts import SarvamTTSService
    
    from pipecat.services.sarvam.llm import SarvamLLMService
    
    from pipecat.transports.websocket.fastapi import FastAPIWebsocketParams
    
    load_dotenv(override=True)
    
    async def bot(runner_args: RunnerArguments):
    
        """Main bot entry point."""
    
        # create_transport auto-detects Exotel's WebSocket handshake and builds
    
        # the matching ExotelFrameSerializer using the stream and call identifiers
    
        # Exotel sends when it connects. No Exotel credentials are needed here.
    
        transport = await create_transport(
    
            runner_args,
    
            {
    
                "exotel": lambda: FastAPIWebsocketParams(
    
                    audio_in_enabled=True, audio_out_enabled=True
    
                ),
    
            },
    
        )
    
        # Initialize AI services
    
        stt = SarvamSTTService(api_key=os.getenv("SARVAM_API_KEY"))
    
        tts = SarvamTTSService(api_key=os.getenv("SARVAM_API_KEY"))
    
        llm = SarvamLLMService(
    
            api_key=os.getenv("SARVAM_API_KEY"),
    
            settings=SarvamLLMService.Settings(model="sarvam-105b"),
    
        )
    
        # Set up conversation context
    
        messages = [
    
            {
    
                "role": "system",
    
                "content": "You are a friendly AI phone assistant. Keep your responses brief and conversational.",
    
            },
    
        ]
    
        context = LLMContext(messages)
    
        context_aggregator = LLMContextAggregatorPair(context)
    
        # Build pipeline
    
        pipeline = Pipeline(
    
            [
    
                transport.input(),
    
                stt,
    
                context_aggregator.user(),
    
                llm,
    
                tts,
    
                transport.output(),
    
                context_aggregator.assistant(),
    
            ]
    
        )
    
        # Exotel Voice Streaming sends and receives 8kHz mono audio
    
        task = PipelineTask(
    
            pipeline,
    
            params=PipelineParams(
    
                audio_in_sample_rate=8000,
    
                audio_out_sample_rate=8000,
    
            ),
    
        )
    
        @transport.event_handler("on_client_connected")
    
        async def on_client_connected(transport, client):
    
            logger.info("Caller connected")
    
            messages.append(
    
                {"role": "system", "content": "Greet the caller and briefly introduce yourself."}
    
            )
    
            await task.queue_frames([LLMRunFrame()])
    
        @transport.event_handler("on_client_disconnected")
    
        async def on_client_disconnected(transport, client):
    
            logger.info("Caller disconnected")
    
            await task.cancel()
    
        runner = PipelineRunner(handle_sigint=runner_args.handle_sigint)
    
        await runner.run(task)
    
    if __name__ == "__main__":
    
        from pipecat.runner.run import main
    
        main()

### 5\. Configure Exotel to Reach Your Agent

Exotel is different from Twilio here: it doesn’t fetch an XML webhook at call time. Instead, you paste your WebSocket URL directly into a Voicebot Applet inside a call flow, and Exotel opens that connection itself.

**Start ngrok:**
    
    
    ngrok http 7860

ngrok prints a forwarding URL that looks like `https://xxxx.ngrok-free.app`. Turn it into a `wss://` URL for the next step.

The domain suffix ngrok assigns varies per account. You may see `ngrok-free.app`, `ngrok-free.dev`, or the older `ngrok.io`, regardless of whether you’re on macOS, Windows, or Linux. Always use whatever URL ngrok actually prints, not the placeholder shown here.

Free ngrok URLs change every time you restart ngrok. If your agent stops receiving calls, check whether the URL in your Voicebot Applet still matches the one ngrok is currently printing.

**Build the App Bazaar flow:**

  1. In the [Exotel dashboard](https://my.exotel.com/), go to **App Bazaar**
  2. Create a new custom app (or edit an existing one)
  3. Add a **Voicebot** applet (not **Stream** or **Passthru**), and set its URL field to `wss://xxxx.ngrok-free.app/ws`
  4. Add a **Hangup** applet right after it, so the flow is: **Call Start → Voicebot Applet → Hangup Applet**
  5. Save the flow



For production use, Exotel recommends adding a **Passthru** applet between Voicebot and Hangup to capture session metadata (call SID, duration, recording URL) and detect disconnects. It’s optional for getting a call working.

**Assign the flow to your number:**

  1. Go to **ExoPhones** , and select your number
  2. Under **Installed App** , choose the flow you just built
  3. Confirm the change when prompted



### 6\. Run Your Agent
    
    
    python agent.py --transport exotel

No `--proxy` flag is needed here since Exotel doesn’t fetch a webhook, it just connects straight to `/ws`.

### 7\. Test Your Agent

Call your Exotel number from any phone. Your voice agent will pick up and start the conversation.

* * *

## Customization Examples

### Example 1: Hindi Voice Agent
    
    
    stt = SarvamSTTService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamSTTService.Settings(
    
            model="saaras:v4",
    
            language="hi-IN",  # Hindi
    
        ),
    
        mode="transcribe",
    
    )
    
    tts = SarvamTTSService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamTTSService.Settings(
    
            model="bulbul:v4-flash",
    
            voice="ishita_hi_devotional",  # v4 persona; v3 short names need model="bulbul:v3"
    
            language_code="hi-IN",
    
        ),
    
    )
    
    llm = SarvamLLMService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamLLMService.Settings(model="sarvam-105b"),
    
    )

`language`, `voice`, and `language_code` are `Settings` fields, not constructor keyword arguments. Passing them directly to `SarvamSTTService(...)` or `SarvamTTSService(...)` raises a `TypeError` on current versions of `pipecat-ai`. Only `mode` (STT) and `api_key` stay outside `settings`.

### Example 2: Tamil Voice Agent
    
    
    stt = SarvamSTTService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamSTTService.Settings(
    
            model="saaras:v4",
    
            language="ta-IN",
    
        ),
    
        mode="transcribe",
    
    )
    
    tts = SarvamTTSService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamTTSService.Settings(
    
            model="bulbul:v4-flash",
    
            voice="simran_en_customer",
    
            language_code="ta-IN",
    
        ),
    
    )
    
    llm = SarvamLLMService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamLLMService.Settings(model="sarvam-105b"),
    
    )

### Example 3: Multilingual Agent (Auto-detect)
    
    
    # Auto-detect the caller's language
    
    stt = SarvamSTTService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamSTTService.Settings(
    
            model="saaras:v4",
    
            language="unknown",  # Auto-detects language
    
        ),
    
        mode="transcribe",
    
    )
    
    tts = SarvamTTSService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamTTSService.Settings(
    
            model="bulbul:v4-flash",
    
            voice="simran_en_customer",
    
            language_code="en-IN",
    
        ),
    
    )
    
    llm = SarvamLLMService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamLLMService.Settings(model="sarvam-105b"),
    
    )

Use `language="unknown"` for support lines where callers might speak any of several languages. Sarvam auto-detects the spoken language per utterance, so the same agent can handle a Hindi caller followed by a Tamil caller without any code changes.

### Example 4: Speech-to-English Agent (Saaras)

`mode="transcribe"` converts speech to text in the same language. `mode="translate"` translates speech directly to English text. Use translate mode when the caller speaks an Indian language but you want to process and respond in English.
    
    
    # Caller speaks Hindi, Saaras converts it to English, the LLM processes it,
    
    # and the agent responds in English.
    
    stt = SarvamSTTService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamSTTService.Settings(model="saaras:v4"),
    
        mode="translate",  # Speech-to-English translation
    
    )
    
    tts = SarvamTTSService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamTTSService.Settings(
    
            model="bulbul:v4-flash",
    
            voice="shubh_en_narration",
    
            language_code="en-IN",
    
        ),
    
    )
    
    llm = SarvamLLMService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamLLMService.Settings(model="sarvam-105b"),
    
    )

Saaras auto-detects the source language (Hindi, Tamil, and so on) and translates spoken content directly to English text, which makes Indian-language speech usable by English-based LLMs.

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

### TTS Additional Parameters

You can customize the TTS service with additional parameters:
    
    
    tts = SarvamTTSService(
    
        api_key=os.getenv("SARVAM_API_KEY"),
    
        settings=SarvamTTSService.Settings(
    
            model="bulbul:v4-flash",
    
            voice="simran_en_customer",
    
            language_code="en-IN",
    
            pace=1.0,  # Range: 0.5 to 2.0
    
        ),
    
    )

Exotel Voice Streaming defaults to 8kHz mono audio when the Voicebot Applet’s WebSocket URL doesn’t specify a rate (this guide’s URL doesn’t). Exotel also supports 16kHz and 24kHz via a `?sample-rate=` query parameter on that URL, but if you use one, update `audio_in_sample_rate`/`audio_out_sample_rate` in `PipelineParams` to match. You don’t need to touch `sample_rate` on `SarvamTTSService` either way: Pipecat resamples the TTS output to match `audio_out_sample_rate` automatically.

* * *

## Understanding the Call Flow

  1. **Caller dials your Exotel number.** The App Bazaar flow reaches the Voicebot Applet, and Exotel opens a WebSocket directly to your agent, there’s no webhook fetch in between.
  2. **Transport Input:** Your Pipecat transport receives the caller’s audio over the WebSocket, and hands it to STT.
  3. **STT (Speech-to-Text):** Converts audio to text using Sarvam’s Saaras, and the context aggregator adds it to the conversation context.
  4. **LLM:** Generates a response using Sarvam.
  5. **TTS (Text-to-Speech):** Converts the response to audio using Sarvam’s Bulbul.
  6. **Transport Output:** Streams the audio back over the WebSocket, and Exotel plays it to the caller, while the context aggregator saves the assistant’s response to context. The **Hangup Applet** then ends the call once your agent closes the WebSocket.



* * *

## Pro Tips

  * Use `language="unknown"` to automatically detect the caller’s language. This works well for multilingual support lines.
  * Sarvam’s models understand code-mixing, so your agent can naturally handle Hinglish, Tanglish, and other mixed languages, which is common on real support calls.
  * Use `sarvam-105b` for the LLM step.



Log the transcript from `context_aggregator` if you want post-call analytics. Writing it to a file or database is cheap and won’t slow down the live pipeline.

* * *

## Troubleshooting

**Call connects but there’s no audio.** Confirm the Voicebot Applet’s URL uses `wss://`, not `ws://` or `https://`, and that it points at your current ngrok URL. Free ngrok URLs change on every restart.

**Call doesn’t reach your agent at all.** Double-check the flow order in App Bazaar: **Call Start → Voicebot Applet → Hangup Applet**. A missing or misordered applet is the most common cause.

**API key errors.** Make sure `SARVAM_API_KEY` is in your `.env` file and that the file sits in the same directory as `agent.py`.

**Module not found.** Re-run the install command for your operating system (see Step 2 above).

**Poor transcription.** Try `language="unknown"` for auto-detection, or set the exact language code (`en-IN`, `hi-IN`, and so on) if you already know it.

**Choppy or robotic audio.** Make sure `audio_in_sample_rate` and `audio_out_sample_rate` in `PipelineParams` match the rate Exotel is actually streaming: `8000` by default, or whatever you set via `?sample-rate=` on the Voicebot Applet’s WebSocket URL (Exotel also supports 16000 and 24000). A mismatch causes distorted playback.

**Call disconnects a few seconds after connecting.** Exotel expects your WebSocket server to accept the connection within about 10 seconds. Make sure ngrok and `agent.py` are both already running before you place the call.

**Long call cuts off unexpectedly.** Exotel caps a single streaming session at around 60 minutes (this can vary by plan), for calls that need to run longer, design your agent to end the conversation before that limit.

* * *

## Additional Resources

  * [Sarvam AI Documentation](https://docs.sarvam.ai/)
  * [Pipecat Documentation](https://docs.pipecat.ai/)
  * [Pipecat Sarvam LLM Service](https://docs.pipecat.ai/api-reference/server/services/llm/sarvam)
  * [Exotel Stream and Voicebot Applet Guide](https://support.exotel.com/support/solutions/articles/3000108630-working-with-the-stream-and-voicebot-applet)
  * [Exotel Updated Extension Guide (timeouts, session limits, Passthru)](https://support.exotel.com/support/solutions/articles/3000132302-updated-extension-guide-working-with-the-stream-and-voicebot-applet-beta-)
  * [Exotel Dashboard](https://my.exotel.com/)



* * *

## Need Help?

  * Sarvam Support: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Community: [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



* * *

**Happy Building!**

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio)[Build a Voice Agent using VobizNext](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


