---
url: https://sarvam.ai/integrations/livekit/
title: LiveKit Integration | Sarvam
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:48.953653+00:00
---

# LiveKit Integration | Sarvam

> Source: https://sarvam.ai/integrations/livekit/

[Integrations](https://sarvam.ai/integrations) / LiveKit

![LiveKit logo](https://sarvam.ai/assets/integrations/livekit-logo.svg)

#  Sarvam + LiveKit 

Voice Infra 

Real-time voice infrastructure for building production-grade voice AI agents. Telephony, SIP, and global scaling handled automatically. 

[ Get Started](https://docs.livekit.io/agents/plugins/sarvam/) [ View on GitHub](https://github.com/livekit/agents)

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

How it works

1.

### Install LiveKit Agents SDK

pip install "livekit-agents[sarvam,silero]" python-dotenv

2.

### Add Sarvam as provider

Create a .env file with LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and SARVAM_API_KEY

3.

### Deploy your agent

Run locally with the dev or console command, or deploy to LiveKit Cloud

Quick start

Install

BashCopy
    
    
    pip install "livekit-agents[sarvam,silero]" python-dotenv

Code

PythonCopy
    
    
    from livekit.agents import AgentSession
    from livekit.plugins import sarvam
    
    session = AgentSession(
        stt=sarvam.STT(
            language="unknown",
            model="saaras:v3",
            mode="transcribe",
            flush_signal=True,
        ),
        llm=sarvam.LLM(model="sarvam-105b"),
        tts=sarvam.TTS(
            target_language_code="en-IN",
            model="bulbul:v3",
            speaker="shubh",
        ),
        turn_detection="stt",
    )

Run

BashCopy
    
    
    python agent.py dev

Starts the agent in development mode and connects it to your LiveKit room. Use `python agent.py console` to test the agent locally in your terminal without a LiveKit Cloud project.

Use cases

### IVR

IVR & Call Centres

Automate inbound and outbound calls with Indic-language voice agents.

### Voice

Voice Assistants

Build voice-first assistants that understand and speak Indian languages.

### Telephony

Telephony Bots

Deploy SIP-connected bots for telecoms with real-time transcription and synthesis.

Resources & details

Type Open Source + Cloud

Language Python

Maintained by LiveKit Inc.

Install pip install "livekit-agents[sarvam,silero]"

[ LiveKit docs  → ](https://docs.livekit.io)[ Sarvam plugin ref  → ](https://docs.livekit.io/agents/models/tts/sarvam/)[ GitHub  → ](https://github.com/livekit/agents/tree/main/livekit-plugins/livekit-plugins-sarvam)[ Sarvam API ref  → ](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

Ready to build? Start building with LiveKit in minutes. 

Ready to build?

Start building with LiveKit in minutes.

[Get API Key](https://indus.sarvam.ai)
