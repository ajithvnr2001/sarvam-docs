---
url: https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural/
title: Agri & Rural Voice Agents | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:45.131663+00:00
---

# Agri & Rural Voice Agents | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural/

Skip to navigation

On this page

  * Architecture
  * Recommended models & params
  * Latency targets
  * Pitfalls
  * Full example



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Text to Speech](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)[Use Cases](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/ivr-contact-center)

# Agri & Rural Voice Agents

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural.md "View this page as plain text")|More actions

This page is for Model APIs.

Want a production voice agent without assembling the stack yourself? [Sarvam Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents) is a managed platform with speech recognition, reasoning, Indian-language voices, telephony, testing, and analytics included, from ₹3 per minute. This guide shows how to build your own pipeline on the APIs instead.

Farmer-advisory bots (crop guidance, mandi/market prices, weather alerts, government scheme status) serve users who are frequently on 2G/3G connections, basic phones, and regional-language-only speech. Voice is often the _only_ accessible interface here, not a convenience layer on top of an app. This vertical shares a lot with [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services), the same accessibility bar and the same need to avoid stating unverified facts as certain, but adds connectivity constraints and domain content (crops, weather, mandi prices) that the other guides don’t cover.

There’s no dedicated example agent for this vertical yet in the cookbook, so this guide includes a full one, built on the same pattern as the [Government Scheme Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent), which already covers PM-Kisan and other farmer-relevant schemes.

**In short:** design for a bad connection first, ground every price/weather answer with a live tool call instead of the model’s memory, and reuse the Government Services pattern for scheme questions instead of duplicating it.

## Architecture
    
    
    Farmer Audio (often PSTN/2G) → STT (streaming, 8kHz-tolerant) → LLM (simple language, tool-grounded facts) → TTS (streaming, mulaw for low-bandwidth) → Farmer

  * **Tool calls from the LLM step:** mandi price lookup, weather API, scheme status



[1](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural#design-for-the-connection-youll-actually-get)

### Design for the connection you'll actually get

Assume PSTN or low-bandwidth mobile data, not a stable broadband WebRTC session. Use 8kHz telephony-friendly audio formats (`mulaw`/`alaw` for PSTN legs) and design conversations to survive occasional dropped audio: short turns and a willingness to repeat.

[2](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural#ground-time-sensitive-facts-with-tools-not-the-models-memory)

### Ground time-sensitive facts with tools, not the model's memory

Mandi prices, weather, and pest advisories are exactly the kind of facts that are wrong the moment they’re not live. Use [tool calling](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview#tool-calling-function-calling) to hit a real prices/weather API rather than letting the LLM guess from training data. This matters even more here than in Government Services, because a number like today’s mandi price goes stale in hours, not months.

[3](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural#keep-the-conversational-turn-short-and-concrete)

### Keep the conversational turn short and concrete

Same principle as citizen-services bots: short, plain-language turns beat long explanations for a low-literacy, audio-only interface.

[4](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural#cross-reference-scheme-content-instead-of-duplicating-it)

### Cross-reference scheme content instead of duplicating it

Questions about PM-Kisan status or other scheme eligibility should route to the same grounded-answer pattern as [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services) rather than maintaining a second, possibly inconsistent copy of scheme knowledge.

## Recommended models & params

Layer| Setting| Why  
---|---|---  
STT| `saaras:v3`, `mode="transcribe"`, `language="unknown"`| Regional-language-first callers. Auto-detect avoids forcing Hindi on a Tamil- or Telugu-speaking farmer  
LLM| `sarvam-105b`, `reasoning_effort=None` for routine advisory turns| Most turns are lookup-and-explain (price, weather, basic crop guidance), not deep reasoning. Keep latency low over an already-slow connection  
Tool calling| Wire mandi price and weather lookups as [tools](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview#tool-calling-function-calling) rather than prompting for “current” data| The model has no live data access. Tool calling is the only way to get an actually-current mandi price into the response  
TTS| `bulbul:v4-flash` (or `bulbul:v3`), `pace=0.85–0.9`, warm speaker matched to the [v4 use-case voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices#recommended-voices-by-use-case) or [v3 speakers](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices#speaker-selection-by-language)| Same accessibility reasoning as Government Services: slower, warmer, and in the farmer’s own language beats a brisk, generic voice  
TTS format| `wav` at 8 kHz for PSTN/IVR delivery; fall back gracefully if the connection can’t sustain WebSocket streaming| Matches [output formats](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices#output-formats-and-sample-rates) for telephony  
  
## Latency targets

The connection is usually the bottleneck here, not the model. Use streaming STT and TTS as the default, but design your retry/reconnect logic assuming the network will drop mid-call more often than in an urban contact-center deployment.

  * Keep tool-call round-trips (mandi price, weather) fast and cached where possible. For example, cache a mandi’s price for the trading day so a live lookup doesn’t stack latency on top of an already-slow connection.
  * Default to `reasoning_effort=None` here, specifically because added reasoning latency compounds with network latency in a way it doesn’t on a stable connection.



## Pitfalls

###### Quoting stale prices or weather as current

This is the biggest risk in this vertical. A farmer acting on yesterday’s mandi price or a stale weather forecast has real financial consequences. Always ground these answers with a live tool call, and never let the LLM state a specific number from memory.

###### Assuming smartphone-level connectivity

Test against 8kHz telephony audio and degraded network conditions, not just a WebRTC demo on office wifi. What works in a browser tab doesn’t necessarily survive a real rural PSTN call.

###### Over-relying on one language

A single hardcoded `language_code` will exclude farmers outside that language’s region. Auto-detect on STT and pick the TTS voice/language per caller, rather than shipping a single-language deployment and calling it done.

###### Agronomic or governmental jargon

Pesticide/fertilizer names, scheme acronyms, and technical crop terminology need the same plain-language treatment as [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services#pitfalls) content. Don’t assume agricultural literacy any more than you’d assume digital literacy.

###### Duplicating scheme content instead of reusing it

If your agri bot also answers PM-Kisan or scheme questions, reuse the grounded, verification-pointing pattern from the [Government Scheme Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent) rather than writing a second, possibly drifting version of the same facts.

## Full example

There’s no published cookbook example for this vertical yet. Here’s a complete agent following the same LiveKit pattern as the [Government Scheme Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent), with agri-specific instructions and a tool-calling stub for live mandi prices:
    
    
    import logging
    
    from dotenv import load_dotenv
    
    from livekit.agents import JobContext, WorkerOptions, cli, function_tool
    
    from livekit.agents.llm import RunContext
    
    from livekit.agents.voice import Agent, AgentSession
    
    from livekit.plugins import sarvam
    
    load_dotenv()
    
    logger = logging.getLogger("krishi-mitra")
    
    logger.setLevel(logging.INFO)
    
    class KrishiMitraAgent(Agent):
    
        def __init__(self) -> None:
    
            super().__init__(
    
                instructions="""
    
                    You are Krishi Mitra, a voice assistant that helps Indian farmers with
    
                    crop advisory, mandi (market) prices, weather, and government scheme queries.
    
                    Your responsibilities:
    
                    - Answer questions about crop care, sowing/harvest timing, and common pest/disease symptoms in simple terms
    
                    - Use the get_mandi_price tool for any current price question. Never state a price from memory
    
                    - Use the get_weather_forecast tool for any weather question. Never guess conditions
    
                    - For government scheme questions (PM-Kisan, crop insurance, etc.), give general guidance and
    
                      always direct the farmer to their nearest Krishi Vigyan Kendra or the official portal to confirm details
    
                    - If you don't know something, say so plainly rather than guessing
    
                    Communication guidelines:
    
                    - Use simple, everyday language. Avoid technical agronomic or bureaucratic jargon
    
                    - Speak slowly and clearly. Be willing to repeat
    
                    - Be patient and respectful. Many callers may have limited formal education
    
                    - Keep answers short and concrete: a specific action, not a lecture
    
                    Start by greeting the farmer warmly and asking what they need help with today.
    
                """,
    
                stt=sarvam.STT(
    
                    language="unknown",  # Auto-detect across regional languages
    
                    model="saaras:v4",
    
                    mode="transcribe",
    
                ),
    
                llm=sarvam.LLM(model="sarvam-105b"),
    
                tts=sarvam.TTS(
    
                    language_code="hi-IN",  # Set per deployment region
    
                    model="bulbul:v4-flash",
    
                    speaker="simran",
    
                    pace=0.9,
    
                ),
    
            )
    
        @function_tool
    
        async def get_mandi_price(self, context: RunContext, crop: str, mandi: str) -> dict:
    
            """Look up today's price for a crop at a given mandi. Replace with a real market-price API call."""
    
            # TODO: call your mandi price provider (e.g. Agmarknet) here
    
            return {"crop": crop, "mandi": mandi, "price_per_quintal": None, "as_of": "today"}
    
        @function_tool
    
        async def get_weather_forecast(self, context: RunContext, location: str) -> dict:
    
            """Look up the weather forecast for a location. Replace with a real weather API call."""
    
            # TODO: call your weather provider here
    
            return {"location": location, "forecast": None}
    
        async def on_enter(self):
    
            self.session.generate_reply()
    
    async def entrypoint(ctx: JobContext):
    
        logger.info(f"Farmer connected to room: {ctx.room.name}")
    
        session = AgentSession()
    
        await session.start(agent=KrishiMitraAgent(), room=ctx.room)
    
    if __name__ == "__main__":
    
        cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

`get_mandi_price` and `get_weather_forecast` above are stubs. Wiring them to real data sources is what makes this agent safe to deploy. Without that, don’t let the LLM answer price/weather questions from its own knowledge. See [Tool Calling](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview#tool-calling-function-calling) for the full request/response flow.

Install the same dependencies as the other LiveKit examples:
    
    
    pip install "livekit-agents[sarvam,silero]" python-dotenv

**See also:** [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services) for the scheme-awareness portion of this audience.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/government-services)[Text Processing OverviewNext](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)
      * [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)
      * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/which-api-to-use)
      * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)
      * Streaming API

      * [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
      * [Best Practice Guide for Bulbul v4 Flash](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices)
      * [Best Practices (Bulbul v3)](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices)
      * How-to

      * Use Cases
        * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/ivr-contact-center)
        * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/bfsi-voice-bots)
        * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
        * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/government-services)
        * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural)

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


