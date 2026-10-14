---
url: https://sarvam.ai/integrations/n8n/
title: Sarvam Integrations: Workflow Automation with n8n
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:49.046092+00:00
---

# Sarvam Integrations: Workflow Automation with n8n

> Source: https://sarvam.ai/integrations/n8n/

[Integrations](https://sarvam.ai/integrations) / n8n

![n8n logo](https://sarvam.ai/assets/integrations/n8n-logo.svg)

#  Sarvam + n8n 

Automation 

Drop speech to text, text to speech, and Indic-language chat capabilities into any workflow, without writing a backend. Connect Sarvam to your CRM, support stack, internal tools, or any of the 1,000+ apps n8n supports. 

[ Get started](https://indus.sarvam.ai) [ Read the docs](https://docs.sarvam.ai)

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

What you can build

### Transcribe audio in 23 Indian languages

Upload audio from a form, pull it from a webhook, or fetch it from storage. Sarvam's speech to text handles Hindi, Tamil, Bengali, Telugu, and 19 more, with modes for standard transcription, code-mixed output, Roman transliteration, or direct translation to English for downstream tools that only read one language.

### Synthesize speech that sounds right for Indian users

Turn any text into audio across 11 languages and dozens of speakers. Set the pace, pick the codec, and choose a voice that fits your product. The output goes directly into a Respond to Webhook node, an email, or a storage bucket, wherever your workflow sends audio next.

### Run Sarvam's language models on any text

Feed transcripts, form inputs, or scraped content into sarvam-105b for high-quality multilingual reasoning. Chain completions with speech to text and text to speech to build voice Q&A flows, automated call handling, or multilingual support automations, all in the node editor.

A workflow in four nodes

Most Sarvam automations follow the same shape.

1.

### Receive audio

A webhook, form, or file download brings audio into the workflow as a binary property.

2.

### Transcribe

Sarvam speech to text reads that binary and returns a transcript.

3.

### Process

The chat node takes the transcript as a user message and returns a reply.

4.

### Respond

Text to speech reads the reply and returns audio you can send, store, or stream back.

No custom backend. No glue code. The node editor wires it.

Popular workflows

### Transcribe a form audio upload

A Form Trigger captures the file. Sarvam transcribes it and returns text in JSON. Route it to a CRM, a support ticket, or a Google Sheet.

Form to transcript in seconds

Route to any downstream tool

### Webhook voice Q&A

An incoming POST with raw audio goes to Sarvam speech to text, then chat, then text to speech. Respond to Webhook returns the spoken answer. Full round-trip in four nodes.

Full voice round-trip

Four nodes, no backend

### Batch transcription from storage

Pull audio files from S3 or Google Drive. Loop through with Sarvam speech to text. Write transcripts to a database or sheet. Useful for call centres, field recordings, or interview archives.

Bulk processing at scale

Call centres & archives

### Multilingual support automation

Sarvam's Translate to English mode converts any Indic call to English text on transcription. Feed it straight to your existing English-only model or ticketing system. No language detection step, no translation middleware.

No translation middleware

Works with English-only tools

How to install

The Sarvam node is available as a community package on n8n. 

[ Get your API key](https://indus.sarvam.ai)

Self-hosted? `npm install n8n-nodes-sarvam`

1.

### Open Community Nodes

Go to Settings, then Community Nodes.

2.

### Install the package

Search for n8n-nodes-sarvam and install.

3.

### Restart n8n

Restart n8n if prompted.

4.

### Add credentials

Go to Credentials, create a new Sarvam AI API credential, and paste your API key from indus.sarvam.ai.

5.

### Start building

Add a Sarvam node to any workflow and pick your Resource and Operation.

Quick start

JSONCopy
    
    
    // n8n HTTP Request node configuration
    {
      "method": "POST",
      "url": EXTERNAL_LINKS.apiPublic.translate,
      "headers": {
        "API-Subscription-Key": "{{ $env.SARVAM_API_KEY }}"
      },
      "body": {
        "input": "{{ $json.text }}",
        "source_language_code": "en-IN",
        "target_language_code": "hi-IN"
      }
    }

Use cases

### Call

Call Transcription Pipelines

Automatically transcribe recorded calls and route transcripts to downstream systems.

### Document

Document Translation

Translate incoming documents across Indian languages as part of an automation flow.

### Voice-Powered

Voice-Powered Chatbots

Add speech input and output to existing chatbot workflows without writing code.

Resources & details

Type Open Source + Cloud

Language No-code (visual)

Maintained by n8n GmbH

Install Self-host or use n8n Cloud

[ n8n docs  → ](https://docs.n8n.io)[ HTTP Request node guide  → ](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)[ n8n community  → ](https://community.n8n.io)[ Sarvam API ref  → ](https://docs.sarvam.ai/api/integration/n8n)

Ready to automate? Get your Sarvam API key and connect to n8n in minutes. 

Ready to automate?

Get your Sarvam API key and connect to n8n in minutes.

[Get API Key](https://indus.sarvam.ai)
