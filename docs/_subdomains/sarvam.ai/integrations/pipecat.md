---
url: https://sarvam.ai/integrations/pipecat/
title: Pipecat Integration | Sarvam
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:49.294934+00:00
---

# Pipecat Integration | Sarvam

> Source: https://sarvam.ai/integrations/pipecat/

[Integrations](https://sarvam.ai/integrations) / Pipecat

![Pipecat logo](https://sarvam.ai/assets/integrations/pipecat-logo.svg)

#  Sarvam + Pipecat 

Agent Framework 

Open-source Python framework for building real-time voice and multimodal conversational AI agents. Sarvam STT and LLM are built-in services. 

[ Get Started](https://docs.pipecat.ai) [ View on GitHub](https://github.com/pipecat-ai/pipecat)

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

### Install Pipecat

pip install "pipecat-ai[daily,sarvam]" python-dotenv loguru

2.

### Add Sarvam API key

Set SARVAM_API_KEY in a .env file in your project directory

3.

### Build your pipeline

Use SarvamSTTService, SarvamLLMService, and SarvamTTSService in your pipeline

Quick start

Install

BashCopy
    
    
    pip install "pipecat-ai[daily,sarvam]" python-dotenv loguru

Code

PythonCopy
    
    
    from pipecat.services.sarvam.stt import SarvamSTTService
    from pipecat.services.sarvam.tts import SarvamTTSService
    from pipecat.services.sarvam.llm import SarvamLLMService
    
    stt = SarvamSTTService(
        api_key=os.getenv("SARVAM_API_KEY"),
        language="hi-IN",
        model="saaras:v3",
        mode="transcribe",
    )
    
    tts = SarvamTTSService(
        api_key=os.getenv("SARVAM_API_KEY"),
        target_language_code="en-IN",
        model="bulbul:v3",
        speaker="shubh",
    )
    
    llm = SarvamLLMService(
        api_key=os.getenv("SARVAM_API_KEY"),
        settings=SarvamLLMService.Settings(model="sarvam-105b"),
    )
    
    pipeline = Pipeline([transport.input(), stt, llm, tts, transport.output()])

Run

BashCopy
    
    
    python agent.py

Runs the pipeline. With Daily transport, this creates a room and prints a URL. Open it in a browser to start talking to the agent.

Use cases

### IVR

IVR & Call Centres

Build conversational IVR systems with Indic-language understanding.

### Voice

Voice Assistants

Create multimodal voice assistants with real-time streaming.

### Rapid

Rapid Prototyping

Go from idea to working voice agent in under an hour.

Resources & details

Type Open Source

Language Python

Maintained by Daily.co

Install pip install "pipecat-ai[daily,sarvam]"

[ Pipecat docs  → ](https://docs.pipecat.ai/api-reference/server/services/llm/sarvam#sarvam)[ PyPI  → ](https://pypi.org/project/pipecat-ai/)[ GitHub  → ](https://github.com/pipecat-ai/pipecat/tree/main/src/pipecat/services/sarvam)[ Sarvam API ref  → ](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)

Ready to build? Start building with Pipecat in minutes. 

Ready to build?

Start building with Pipecat in minutes.

[Get API Key](https://indus.sarvam.ai)
