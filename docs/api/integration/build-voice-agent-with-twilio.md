---
url: https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio/
title: Build a Voice Agent or WhatsApp Bot using Twilio | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:40.126686+00:00
---

# Build a Voice Agent or WhatsApp Bot using Twilio | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio/

Skip to navigation

On this page

  * Overview
  * What You’ll Build
  * Part 1: Phone Call Agent (Telephony)
  * Quick Overview
  * Quick Start
  * 1\. Prerequisites
  * 2\. Install Dependencies
  * 3\. Create Environment File
  * 4\. Write Your Agent
  * 5\. Configure Twilio to Reach Your Agent
  * 6\. Run Your Agent
  * 7\. Test Your Agent
  * Customization Examples
  * Example 1: Hindi Voice Agent
  * Example 2: Tamil Voice Agent
  * Example 3: Multilingual Agent (Auto-detect)
  * Example 4: Speech-to-English Agent (Saaras)
  * Available Options
  * Language Codes
  * Speaker voices (Bulbul v4 Flash)
  * TTS Additional Parameters
  * Understanding the Call Flow
  * Pro Tips
  * Troubleshooting
  * Part 2: WhatsApp Bot
  * WhatsApp Bot: Quick Overview
  * WhatsApp Bot: Quick Start
  * Step 1: Prerequisites
  * Step 2: Install Dependencies
  * Step 3: Create Environment File
  * Step 4: Write Your Agent
  * Step 5: Configure Twilio to Reach Your Agent
  * Step 6: Run and Test Your Agent
  * Reply with a Voice Note (Optional)
  * Understanding the Message Flow
  * WhatsApp Bot: Pro Tips
  * WhatsApp Bot: Troubleshooting
  * Additional Resources
  * Need Help?



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

# Build a Voice Agent or WhatsApp Bot using Twilio

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio.md "View this page as plain text")|More actions

This page is for Model APIs.

Want a production voice agent without assembling the stack yourself? [Sarvam Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents) is a managed platform with speech recognition, reasoning, Indian-language voices, telephony, testing, and analytics included, from ₹3 per minute. This guide shows how to build your own pipeline on the APIs instead.

## Overview

This guide shows you how to build a **real-time conversational agent with Twilio and Sarvam AI** , on either of two channels: a **phone voice agent** that answers inbound calls, or a **WhatsApp bot** that replies to text and voice messages. Both use Sarvam AI for speech-to-text, the LLM, and text-to-speech, and are a great starting point for IVR replacements, customer support lines, and conversational agents in Indian languages.

## What You’ll Build

Pick the channel that matches your use case:

[Phone Call AgentAnswers inbound phone calls on a Twilio number, listens to callers in multiple Indian languages, and responds back in a natural-sounding voice, in real time. Built with Twilio Media Streams and Pipecat.](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio#part-1-phone-call-agent-telephony)[WhatsApp BotReplies to WhatsApp text messages and voice notes on a Twilio WhatsApp number, transcribing voice notes and replying with text (or optionally, a spoken voice note).](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio#part-2-whatsapp-bot)

* * *

## Part 1: Phone Call Agent (Telephony)

A voice agent that can:

  * Answer inbound phone calls on a Twilio number
  * Listen to callers speaking, in multiple Indian languages
  * Understand and process what they say
  * Respond back in a natural-sounding voice, over the phone



## Quick Overview

  1. Get API keys (Twilio, Sarvam)
  2. Install packages: `pip install "pipecat-ai[websocket,sarvam]" python-dotenv`
  3. Create a `.env` file with your API keys
  4. Write about 80 lines of Python code
  5. Point a Twilio phone number at your agent using TwiML
  6. Call your Twilio number



* * *

## Quick Start

### 1\. Prerequisites

  * Python 3.9 or higher
  * [ngrok](https://ngrok.com/download), to expose your local server during development
  * Accounts and keys from: 
    * [Twilio](https://console.twilio.com/): an Account SID, an Auth Token, and a phone number with voice capability
    * [Sarvam AI](https://dashboard.sarvam.ai/): an API key from your dashboard



### 2\. Install Dependencies

###### macOS/Linux

###### Windows
    
    
    pip install "pipecat-ai[websocket,sarvam]" python-dotenv loguru

### 3\. Create Environment File

Create a file named `.env` in your project folder:
    
    
    SARVAM_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx
    
    TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Then replace each placeholder with your real credentials from the [Sarvam dashboard](https://dashboard.sarvam.ai/) and the [Twilio Console](https://console.twilio.com/).

`TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` aren’t optional here. Pipecat’s Twilio transport uses them to authenticate with Twilio’s REST API and to hang up the call cleanly when your agent ends the conversation.

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
    
        # create_transport auto-detects Twilio's WebSocket handshake and builds
    
        # the matching TwilioFrameSerializer, using TWILIO_ACCOUNT_SID and
    
        # TWILIO_AUTH_TOKEN from the environment.
    
        transport = await create_transport(
    
            runner_args,
    
            {
    
                "twilio": lambda: FastAPIWebsocketParams(
    
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
    
                "content": (
    
                    "You are Sarvam AI Agent, a multilingual voice assistant powered by Sarvam AI. "
    
                    "You can understand and respond fluently in English and 10+ Indian languages. "
    
                    "Keep your responses brief and conversational."
    
                ),
    
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
    
        # Twilio Media Streams send and receive 8kHz mono audio
    
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

There’s no manual `try`/`except` around `stt`, `tts`, or `llm` here on purpose. Those lines just construct pipeline processors; the actual Sarvam API calls happen later, streamed frame-by-frame while the pipeline runs, and Pipecat already catches failures at that layer and surfaces them as `ErrorFrame`s (logged via `loguru`) instead of raising into your code. Wrapping the setup code in `try`/`except` wouldn’t protect anything a real call could fail on.

### 5\. Configure Twilio to Reach Your Agent

Twilio needs a public `wss://` URL to stream call audio to. For local development, expose your agent with ngrok.

**Start ngrok:**
    
    
    ngrok http 7860

ngrok prints a forwarding URL that looks like `https://xxxx.ngrok-free.app`. You’ll turn this into a `wss://` URL in the next step.

The domain suffix ngrok assigns varies per account. You may see `ngrok-free.app`, `ngrok-free.dev`, or the older `ngrok.io`, regardless of whether you’re on macOS, Windows, or Linux. Always use whatever URL ngrok actually prints, not the placeholder shown here.

Free ngrok URLs change every time you restart ngrok. If your agent stops receiving calls, check whether the URL in your TwiML Bin still matches the one ngrok is currently printing.

**Create a TwiML Bin:**

TwiML Bins aren’t in the Twilio Console’s left sidebar by default. The fastest way to reach them is to click the search bar at the top of the console and type “TwiML Bins”.

  1. Open the [Twilio Console](https://console.twilio.com/) and search for **TwiML Bins** using the search bar at the top (or find it under **Developer Tools** in the sidebar)
  2. Click **Create new TwiML Bin** , give it a friendly name, and paste the following, replacing the domain with your own ngrok URL:


    
    
    <?xml version="1.0" encoding="UTF-8"?>
    
    <Response>
    
      <Connect>
    
        <Stream url="wss://xxxx.ngrok-free.app/ws" />
    
      </Connect>
    
    </Response>

  3. Click **Create** to save the bin



**Assign it to your phone number:**

  1. Go to **Numbers & Senders**, then **Phone Numbers** , and select your number
  2. Open its configuration/voice settings tab
  3. Find the setting for what happens when **a call comes in** , and set it to use your TwiML Bin (Twilio has labeled this option **TwiML** , **TwiML Bin** , or similar depending on your console version)
  4. Save



Twilio has redesigned this page’s tabs and section names more than once (you may see **Configuration** , **Configure** , or **Configuration Details** ; **Voice & Fax**, **Voice Configuration** , or **Voice and emergency calling**). The setting you want is always the one controlling what happens when a call comes in. If you can’t find it, Twilio’s own [Getting Started with TwiML Bins](https://www.twilio.com/docs/serverless/twiml-bins/getting-started) guide has current screenshots.

### 6\. Run Your Agent
    
    
    python agent.py --transport twilio

This starts a local FastAPI server, via Pipecat’s development runner, that accepts Twilio’s Media Streams WebSocket connection at `/ws`.

### 7\. Test Your Agent

Call your Twilio phone number from any phone. Your voice agent will pick up and start the conversation.

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
  
### Speaker voices (Bulbul v4 Flash)

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

Twilio Media Streams always carry 8kHz mono audio. You don’t need to touch `sample_rate` on `SarvamTTSService` for this: Pipecat resamples the TTS output to match the `audio_out_sample_rate` set in `PipelineParams` automatically.

* * *

## Understanding the Call Flow

  1. **Caller dials your Twilio number.** Twilio answers using the TwiML Bin and opens a WebSocket (Media Stream) to your agent.
  2. **Transport Input:** Your Pipecat transport receives the caller’s audio over the WebSocket, and hands it to STT.
  3. **STT (Speech-to-Text):** Converts audio to text using Sarvam’s Saaras, and the context aggregator adds it to the conversation context.
  4. **LLM:** Generates a response using Sarvam.
  5. **TTS (Text-to-Speech):** Converts the response to audio using Sarvam’s Bulbul.
  6. **Transport Output:** Streams the audio back over the WebSocket, and Twilio plays it to the caller, while the context aggregator saves the assistant’s response to context.



* * *

## Pro Tips

  * Use `language="unknown"` to automatically detect the caller’s language. This works well for multilingual support lines, but transcription accuracy is slightly lower than when you specify the exact language code, so prefer an explicit code whenever you already know which language the caller will use.
  * Sarvam’s models understand code-mixing, so your agent can naturally handle Hinglish, Tanglish, and other mixed languages, which is common on real support calls.
  * Use `sarvam-105b` for the LLM step.



Log the transcript from `context_aggregator` if you want post-call analytics. Writing it to a file or database is cheap and won’t slow down the live pipeline.

* * *

## Troubleshooting

**Call connects but there’s no audio.** Confirm the TwiML `<Stream url>` uses `wss://`, not `wss:/` or `https://`, and that it points at your current ngrok URL. Free ngrok URLs change on every restart.

**Call drops immediately.** Check that `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` are set correctly in `.env`. The Twilio serializer needs both to manage the call.

**API key errors.** Make sure all keys are in your `.env` file and that the file sits in the same directory as `agent.py`.

**Module not found.** Re-run the install command for your operating system (see Step 2 above).

**Poor transcription.** Try `language="unknown"` for auto-detection, or set the exact language code (`en-IN`, `hi-IN`, and so on) if you already know it.

**Choppy or robotic audio.** Make sure `audio_in_sample_rate` and `audio_out_sample_rate` are both set to `8000` in `PipelineParams`. Twilio Media Streams don’t support other rates, and a mismatch causes distorted playback.

* * *

## Part 2: WhatsApp Bot

A WhatsApp bot that can:

  * Receive inbound WhatsApp messages, text or voice notes, on a Twilio WhatsApp number
  * Transcribe voice notes in multiple Indian languages
  * Understand and process what the user said or typed
  * Reply with text, or optionally, a spoken voice note



Unlike the phone agent, this path doesn’t use Pipecat. WhatsApp messages arrive as one-off HTTP webhook requests rather than a continuous audio stream, so a small web server (Flask) that calls Sarvam’s APIs directly is all you need.

### WhatsApp Bot: Quick Overview

  1. Get API keys (Twilio, Sarvam)
  2. Install packages: `pip install flask twilio sarvamai python-dotenv requests`
  3. Create a `.env` file with your API keys
  4. Write about 50 lines of Python code
  5. From WhatsApp, send the Sandbox’s join code to opt your number in
  6. Point the Sandbox’s webhook at your agent
  7. Message your Twilio WhatsApp number



### WhatsApp Bot: Quick Start

#### Step 1: Prerequisites

  * Python 3.9 or higher
  * [ngrok](https://ngrok.com/download), to expose your local server during development
  * Accounts and keys from: 
    * [Twilio](https://console.twilio.com/): an Account SID and an Auth Token
    * [Sarvam AI](https://dashboard.sarvam.ai/): an API key from your dashboard



This guide uses the **Twilio Sandbox for WhatsApp** , a free, instant way to test WhatsApp messaging in development. Moving to production requires registering a WhatsApp Sender, which involves Meta Business verification and can take a few days. See [Twilio’s WhatsApp docs](https://www.twilio.com/docs/whatsapp) when you’re ready to go live.

#### Step 2: Install Dependencies
    
    
    pip install flask twilio sarvamai python-dotenv requests

#### Step 3: Create Environment File

Create a file named `.env` in your project folder:
    
    
    SARVAM_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx
    
    TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Then replace each placeholder with your real credentials from the [Sarvam dashboard](https://dashboard.sarvam.ai/) and the [Twilio Console](https://console.twilio.com/).

`TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` are used to authenticate when downloading voice-note media from Twilio, which requires HTTP Basic Auth with these credentials.

#### Step 4: Write Your Agent

Create `whatsapp_agent.py`:
    
    
    import logging
    
    import os
    
    from pathlib import Path
    
    import requests
    
    from dotenv import load_dotenv
    
    from flask import Flask, Response, request
    
    from sarvamai import SarvamAI
    
    from twilio.twiml.messaging_response import MessagingResponse
    
    load_dotenv(override=True)
    
    logging.basicConfig(level=logging.INFO)
    
    logger = logging.getLogger(__name__)
    
    app = Flask(__name__)
    
    sarvam = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))
    
    SYSTEM_PROMPT = (
    
        "You are Sarvam AI Agent, a multilingual assistant powered by Sarvam AI, "
    
        "chatting over WhatsApp. You can understand and respond fluently in "
    
        "English and 10+ Indian languages. Keep replies short (2-3 sentences) "
    
        "and conversational."
    
    )
    
    @app.route("/whatsapp", methods=["POST"])
    
    def whatsapp_webhook():
    
        num_media = int(request.form.get("NumMedia", 0))
    
        twiml = MessagingResponse()
    
        try:
    
            if num_media > 0 and "audio" in request.form.get("MediaContentType0", ""):
    
                # Sender sent a voice note - download and transcribe it.
    
                # Twilio media URLs require your account credentials to fetch.
    
                media_url = request.form["MediaUrl0"]
    
                media_response = requests.get(
    
                    media_url,
    
                    auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")),
    
                    timeout=10,
    
                )
    
                media_response.raise_for_status()
    
                audio_file = Path("/tmp/voice_note.ogg")
    
                audio_file.write_bytes(media_response.content)
    
                transcript = sarvam.speech_to_text.transcribe(
    
                    file=open(audio_file, "rb"),
    
                    model="saaras:v4",
    
                    language_code="unknown",  # auto-detects the sender's language
    
                )
    
                user_text = transcript.transcript
    
            else:
    
                user_text = request.form.get("Body", "")
    
            completion = sarvam.chat.completions(
    
                model="sarvam-105b",
    
                messages=[
    
                    {"role": "system", "content": SYSTEM_PROMPT},
    
                    {"role": "user", "content": user_text},
    
                ],
    
            )
    
            reply_text = completion.choices[0].message.content
    
        except Exception:
    
            # Network hiccups, a failed download, or an API error shouldn't crash
    
            # the webhook - Twilio would just get a 500 and the sender gets silence.
    
            logger.exception("Failed to process incoming WhatsApp message")
    
            reply_text = "Sorry, I couldn't process that. Please try again in a moment."
    
        twiml.message(reply_text)
    
        return Response(str(twiml), mimetype="application/xml")
    
    if __name__ == "__main__":
    
        app.run(port=7861)

WhatsApp voice notes arrive as OGG/Opus audio, and Sarvam’s speech-to-text REST API accepts that format directly, no transcoding needed. Voice notes longer than 30 seconds will fail on this endpoint; for longer audio, switch to the [Batch STT API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api).

The `try`/`except` around the webhook body exists because this endpoint is a system boundary, it calls two external services (Twilio’s media download, Sarvam’s API) over the network, either of which can fail independently of your code. Replying with a short apology keeps the conversation alive instead of leaving the sender with no response at all.

This example trusts every request to `/whatsapp`. Before going to production, validate the `X-Twilio-Signature` header on each request (using `twilio.request_validator.RequestValidator`) so that requests can’t be spoofed as coming from Twilio.

#### Step 5: Configure Twilio to Reach Your Agent

**Start ngrok:**
    
    
    ngrok http 7861

ngrok prints a forwarding URL that looks like `https://xxxx.ngrok-free.app`.

**5a. Register your WhatsApp number with the Sandbox (required first)**

The Sandbox is a shared Twilio number (`+1 XXX XXX XXXX`, shown on the console page below), used by every developer testing WhatsApp. Twilio only forwards messages from phone numbers that have explicitly opted in to _your_ sandbox, nothing reaches your webhook until this step is done, no matter how correctly your code or webhook URL is set up.

  1. Open the [Twilio Console](https://console.twilio.com/) and go to **Messaging** → **Try it out** → **Send a WhatsApp message** (or search for “WhatsApp sandbox” in the console search bar). This page shows the sandbox number and your account’s unique join code, for example `join happy-elephant`.
  2. From the WhatsApp app on your phone, send that exact `join <your-code>` message as a normal WhatsApp text to the sandbox number shown on that page (or scan the QR code Twilio shows, which pre-fills this message for you).
  3. Twilio replies confirming you’re connected. Your number is now opted in to your sandbox.



This opt-in is per phone number, not per account. Anyone else who wants to message your bot (a teammate, a demo user) must send the same `join <code>` message from their own WhatsApp number first, there’s no way around this for the Sandbox.

The opt-in expires 3 days after joining (or after the last message exchanged). If your bot suddenly stops receiving messages from a number that worked before, re-send the `join <code>` message from that WhatsApp number.

**5b. Point the Sandbox at your webhook**

  1. Still on the Sandbox settings page, find **When a message comes in**
  2. Set it to your ngrok URL plus `/whatsapp` (for example, `https://xxxx.ngrok-free.app/whatsapp`), with the method set to **HTTP POST**
  3. Save



Free ngrok URLs change every time you restart ngrok. If your bot stops responding, check whether the webhook URL in the sandbox settings still matches the one ngrok is currently printing.

#### Step 6: Run and Test Your Agent
    
    
    python whatsapp_agent.py

Send a text message, or a voice note, to your Twilio WhatsApp number from any phone. Your bot will transcribe and reply within a few seconds.

* * *

### Reply with a Voice Note (Optional)

To have your bot speak its reply back as a voice note instead of (or alongside) text, synthesize the reply with Sarvam’s text-to-speech API, serve the audio file from your own Flask app, and attach it to the TwiML response as media:
    
    
    import uuid
    
    from flask import send_from_directory
    
    from sarvamai.play import save
    
    AUDIO_DIR = Path("audio_replies")
    
    AUDIO_DIR.mkdir(exist_ok=True)
    
    @app.route("/audio/<filename>")
    
    def serve_audio(filename):
    
        return send_from_directory(AUDIO_DIR, filename, mimetype="audio/wav")
    
    # Inside whatsapp_webhook(), replace the final `twiml.message(reply_text)` with:
    
    message = twiml.message(reply_text)
    
    try:
    
        audio = sarvam.text_to_speech.convert(
    
            text=reply_text,
    
            language_code="en-IN",
    
            model="bulbul:v4-flash",
    
            speaker="simran_en_customer",
    
        )
    
        filename = f"{uuid.uuid4().hex}.wav"
    
        save(audio, AUDIO_DIR / filename)
    
        message.media(f"{request.host_url}audio/{filename}")
    
    except Exception:
    
        # If TTS fails, the sender still gets the text reply above.
    
        logger.exception("Text-to-speech failed, sending text-only reply")
    
    return Response(str(twiml), mimetype="application/xml")

`request.host_url` resolves to your current ngrok URL automatically, since ngrok forwards the original `Host` header, so you don’t need to hardcode it here.

Synthesizing the voice note is wrapped in its own `try`/`except`, separate from the outer one, so a TTS failure only drops the audio attachment, the sender still gets the text reply instead of the generic apology.

WhatsApp only renders a native, waveform voice-note bubble for OGG/Opus audio. A `.wav` reply still plays back fine, just as a regular audio attachment rather than a voice-note bubble.

You can use the same [language codes](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio#language-codes) and [speaker voices](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio#speaker-voices-bulbul-v4-flash) listed above for the phone agent when customizing STT and TTS for your WhatsApp bot.

* * *

### Understanding the Message Flow

  1. **User sends a message.** Text or a voice note, to your Twilio WhatsApp number. Twilio POSTs it to your `/whatsapp` webhook.
  2. **STT (Speech-to-Text):** If the message is a voice note, your agent downloads it and converts it to text using Sarvam’s Saaras.
  3. **LLM:** Generates a reply using Sarvam.
  4. **TTS (Text-to-Speech, optional):** Converts the reply to audio using Sarvam’s Bulbul, if you’ve added voice-note replies.
  5. **Response:** Your agent returns TwiML, and Twilio delivers the reply, text and/or audio, back to the user on WhatsApp.



### WhatsApp Bot: Pro Tips

  * Use `language_code="unknown"` in STT to auto-detect whichever language the sender types or speaks in.
  * Keep system prompts explicit about reply length (as in the example), WhatsApp messages are capped at 1600 characters by Twilio, and short replies also read better in a chat window.
  * For production traffic, move off the Sandbox to a verified WhatsApp Sender, and validate Twilio’s request signature on every webhook call.



WhatsApp’s Business Platform only allows free-form replies within 24 hours of the user’s last message. Outside that window, you need a pre-approved template message. This is a WhatsApp policy that neither Sarvam nor Twilio can bypass.

### WhatsApp Bot: Troubleshooting

**Webhook never gets called.** First confirm the sending number actually joined the sandbox (Step 5a), Twilio silently drops messages from numbers that haven’t opted in, and this is the most common reason nothing reaches your server. Then check that the sandbox’s “When a message comes in” URL matches your current ngrok URL exactly, ends in `/whatsapp`, and uses HTTPS.

**Works for a few days, then stops.** The sandbox opt-in expires 3 days after joining (or after the last message exchanged). Re-send the `join <code>` message from that WhatsApp number to reconnect.

**No response outside a fresh conversation.** WhatsApp’s 24-hour session-messaging window has closed; you’ll need a pre-approved template message to reach the user again.

**Voice note transcription fails or comes back empty.** Confirm `MediaContentType0` starts with `audio/`, and that you’re passing your Twilio Account SID and Auth Token as Basic Auth when downloading `MediaUrl0` (Twilio media URLs return 401 without it).

**Voice notes over 30 seconds fail.** The synchronous speech-to-text endpoint caps input at 30 seconds. Switch to the Batch STT API for longer voice notes.

**Module not found.** Re-run the install command from Step 2 above.

* * *

## Additional Resources

  * [Sarvam AI Documentation](https://docs.sarvam.ai/)
  * [Pipecat Documentation](https://docs.pipecat.ai/)
  * [Pipecat Sarvam LLM Service](https://docs.pipecat.ai/api-reference/server/services/llm/sarvam)
  * [Pipecat Twilio Serializer Reference](https://reference-server.pipecat.ai/en/latest/api/pipecat.serializers.twilio.html)
  * [Twilio Media Streams Documentation](https://www.twilio.com/docs/voice/twiml/stream)
  * [Twilio Getting Started with TwiML Bins](https://www.twilio.com/docs/serverless/twiml-bins/getting-started)
  * [Twilio Sandbox for WhatsApp](https://www.twilio.com/docs/whatsapp/sandbox)
  * [Twilio WhatsApp API Overview](https://www.twilio.com/docs/whatsapp)
  * [Twilio Python Helper Library](https://www.twilio.com/docs/libraries/python)
  * [Twilio Console](https://console.twilio.com/)



* * *

## Need Help?

  * Sarvam Support: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Community: [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



* * *

**Happy Building!**

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)[Build Your First Voice Agent using ExotelNext](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


