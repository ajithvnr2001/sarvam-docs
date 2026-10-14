---
url: https://docs.sarvam.ai/api/integration/n8n/
title: Build workflows with Sarvam AI in n8n | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:44.715466+00:00
---

# Build workflows with Sarvam AI in n8n | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/n8n/

Skip to navigation

On this page

  * Video walkthrough
  * Overview
  * What you’ll build
  * Quick overview
  * Quick start
  * 1\. Prerequisites
  * 2\. Install the community node
  * 3\. Create your Sarvam credential
  * 4\. Run your first node (manual test)
  * 5\. Read outputs in the next node
  * 6\. Optional: import a starter workflow
  * Import sample workflows
  * Transcribe an audio upload (form)
  * Text to speech → speech to text → chat
  * Understanding the workflow
  * Build a full voice Q&A (webhook sketch)
  * Customization examples
  * Example 1: Hindi STT and TTS
  * Example 2: Tamil STT and TTS
  * Example 3: Multilingual input (auto language)
  * Example 4: Indian-language speech → English text for downstream tools
  * Operations reference
  * Speech to Text: modes
  * Chat: models (node UI)
  * Available options
  * Language codes (common)
  * TTS: output codec and sample rate
  * Speaker voices (names as in node)
  * Expressions and multiple Sarvam nodes
  * Best practices
  * 1\. Match binary property names exactly
  * 2\. Prefer unique node names before writing expressions
  * 3\. Pin sample data while building
  * 4\. Keep execution order predictable
  * 5\. Treat credentials like environment secrets
  * 6\. Use Sarvam as an AI tool where supported
  * Pro tips
  * Troubleshooting
  * Additional resources
  * Need help?



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

# Build workflows with Sarvam AI in n8n

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/n8n.md "View this page as plain text")|More actions

This page is for Model APIs.

## Video walkthrough

Watch this first for a full click-through: installing the **n8n-nodes-sarvam** community node, creating **Sarvam AI API** credentials in n8n, and wiring a **TTS → STT → Chat** sample chain.

Your browser does not support embedded video.

Then continue with **Overview** and **Quick start** for prerequisites, install commands, and importable JSON.

* * *

## Overview

This guide shows how to use **n8n** as your automation layer and **Sarvam AI** for **speech-to-text** , **text-to-speech** , and **chat completions** across Indian languages, without maintaining a custom backend. It follows the same flow as our **LiveKit** and **Pipecat** integration pages: what you will build, a quick path to a first success, then customization, reference tables, best practices, and troubleshooting.

If you already use n8n for CRM, support, or internal tools, you can add Sarvam nodes wherever you need audio or Indic-language text intelligence.

## What you’ll build

You will be able to:

  * **Transcribe** uploaded or downloaded audio (23 Indian languages plus English, with several transcript modes).
  * **Synthesize speech** from text (11 languages, many speakers, codecs, and pace).
  * **Run Sarvam chat models** on transcripts or any text, then chain TTS or downstream systems.
  * **Compose full flows** such as form → transcript, webhook → STT → chat → TTS, or sheet → batch transcribe, all in the node editor.



## Quick overview

  1. **Watch** the [video walkthrough](https://docs.sarvam.ai/api/integration/n8n#video-walkthrough) at the top of this page, community node install, credentials, and a **TTS → STT → Chat** demo.
  2. Create a [Sarvam AI](https://dashboard.sarvam.ai/) account and copy an **API key**.
  3. Install the community package **`n8n-nodes-sarvam`** from **Settings → Community Nodes** (or npm on self-hosted).
  4. Create a **Sarvam AI API** credential in n8n and attach it to each Sarvam node.
  5. Add a **Sarvam AI** node: pick **Resource** (Speech or Chat) and **Operation** , then map **binary** or **text** fields from upstream nodes.
  6. **Execute workflow** and inspect each node’s **OUTPUT** panel to verify `transcript`, binary `data`, or `choices[0].message.content`.
  7. Optionally **import** one of the JSON templates below to skip manual wiring.
  8. Iterate using the **customization** and **best practices** sections when you go to production.



* * *

## Quick start

### 1\. Prerequisites

  * **n8n** : [n8n Cloud](https://n8n.io/cloud/) or self-hosted **v1.x / v2.x** (with permission to install **community nodes** if you are not the admin).
  * **Sarvam AI API key** : from [dashboard.sarvam.ai](https://dashboard.sarvam.ai/) (includes credits for new accounts).
  * Basic familiarity with n8n: **triggers** , **connections** , and opening the **JSON** tab on a node’s output.



### 2\. Install the community node

###### n8n Cloud / UI (recommended)

###### Self-hosted (npm)

  1. In n8n, open **Settings** (gear) → **Community nodes**.
  2. Under **Install** , enter the package name:


    
    
    n8n-nodes-sarvam

  3. Accept the prompt, wait for install to finish, then **restart** n8n if the UI asks you to.
  4. In the canvas, press **+** and search **Sarvam AI** : the node should appear.



**Tip:** Package and install docs also live on [npm, n8n-nodes-sarvam](https://www.npmjs.com/package/n8n-nodes-sarvam) and [n8n community nodes](https://docs.n8n.io/integrations/community-nodes/installation/).

### 3\. Create your Sarvam credential

  1. Go to **Credentials** → **New**.
  2. Search for **Sarvam AI API**.
  3. Paste your **API key** from the dashboard and **Save**.



You reuse this credential on every Sarvam AI node in the workspace.
    
    
    Credential type : Sarvam AI API
    
    API Key         : <your-key-from-dashboard.sarvam.ai>

### 4\. Run your first node (manual test)

  1. Create a new workflow and add **Manual Trigger**.
  2. Add **Sarvam AI** → connect Manual Trigger → Sarvam.
  3. Configure: 
     * **Credential:** your Sarvam AI API.
     * **Resource:** Speech.
     * **Operation:** Text to Speech.
     * **Text:** `Hello from Sarvam in n8n.`
     * **Target Language:** e.g. `en-IN` or `hi-IN`.
  4. Click **Execute workflow** on the Manual Trigger.
  5. Open the Sarvam node **OUTPUT** : you should see **binary** data (often property name **`data`**) containing generated audio.



That confirms install, credentials, and outbound calls to Sarvam.

### 5\. Read outputs in the next node

  * After **Speech to Text** , the transcript is typically in **`{{ $json.transcript }}`**.
  * After **Chat → Complete** , the assistant text is **`{{ $json.choices[0].message.content }}`**.
  * After **Text to Speech** , audio is in **binary** ; the default property name is usually **`data`** : set **Input Binary Field** on the next STT node to match exactly.



### 6\. Optional: import a starter workflow

If you prefer to start from JSON, skip to **[Import sample workflows](https://docs.sarvam.ai/api/integration/n8n#import-sample-workflows)** below, import one template, then **re-attach** your credential on each Sarvam node (n8n may show a warning until you do).

* * *

## Import sample workflows

Use the workflow menu **⋯** → **Import from URL / File** , or **File → Import from File** , then paste JSON. After import:

  1. Open **each** Sarvam AI node and select your **Sarvam AI API** credential (replace any placeholder).
  2. **Execute** once from the trigger to confirm binary and JSON fields look correct.



### Transcribe an audio upload (form)

Flow: **Form Trigger** → **Sarvam AI (Speech → Speech to Text)** → transcript in JSON.
    
    
    {
    
      "name": "Sarvam: Transcribe form upload",
    
      "nodes": [
    
        {
    
          "parameters": {
    
            "formTitle": "Sample audio",
    
            "formDescription": "Upload a short clip to transcribe",
    
            "formFields": {
    
              "values": [
    
                {
    
                  "fieldLabel": "audio",
    
                  "fieldType": "file",
    
                  "acceptFileTypes": ".mp3,.wav"
    
                }
    
              ]
    
            },
    
            "options": {}
    
          },
    
          "type": "n8n-nodes-base.formTrigger",
    
          "typeVersion": 2.5,
    
          "position": [-200, 0],
    
          "id": "form-trigger-sarvam-stt",
    
          "name": "On form submission"
    
        },
    
        {
    
          "parameters": {
    
            "resource": "speech",
    
            "operation": "speechToText",
    
            "binaryPropertyName": "audio",
    
            "sttMode": "transcribe",
    
            "speechToTextOptions": {}
    
          },
    
          "type": "n8n-nodes-sarvam.sarvam",
    
          "typeVersion": 1,
    
          "position": [80, 0],
    
          "id": "sarvam-stt-form",
    
          "name": "Transcribe audio",
    
          "credentials": {
    
            "sarvamApi": {
    
              "id": "__REPLACE_WITH_YOUR_CREDENTIAL_ID__",
    
              "name": "Sarvam AI API"
    
            }
    
          }
    
        }
    
      ],
    
      "pinData": {},
    
      "connections": {
    
        "On form submission": {
    
          "main": [
    
            [
    
              {
    
                "node": "Transcribe audio",
    
                "type": "main",
    
                "index": 0
    
              }
    
            ]
    
          ]
    
        }
    
      },
    
      "active": false,
    
      "settings": {
    
        "executionOrder": "v1",
    
        "binaryMode": "separate"
    
      },
    
      "tags": []
    
    }

**Sarvam node fields**

UI field| Value  
---|---  
Resource| Speech  
Operation| Speech to Text  
Input Binary Field| `audio` (must match the form file field **label**)  
Mode| Transcribe (or another mode from the table below)  
  
### Text to speech → speech to text → chat

Same pattern as the sample **`fern/n8n.json`** : proves **binary handoff** (`data`) and **`{{ $json.transcript }}`** into chat.
    
    
    {
    
      "name": "Sarvam: TTS, STT, then chat",
    
      "nodes": [
    
        {
    
          "parameters": {},
    
          "type": "n8n-nodes-base.manualTrigger",
    
          "typeVersion": 1,
    
          "position": [0, 0],
    
          "id": "manual-trigger-demo",
    
          "name": "When clicking 'Execute workflow'"
    
        },
    
        {
    
          "parameters": {
    
            "resource": "speech",
    
            "operation": "textToSpeech",
    
            "text": "What is the capital of India?",
    
            "ttsTargetLanguage": "en-IN",
    
            "textToSpeechOptions": {}
    
          },
    
          "type": "n8n-nodes-sarvam.sarvam",
    
          "typeVersion": 1,
    
          "position": [220, 0],
    
          "id": "sarvam-tts-demo",
    
          "name": "Text to speech",
    
          "credentials": {
    
            "sarvamApi": {
    
              "id": "__REPLACE_WITH_YOUR_CREDENTIAL_ID__",
    
              "name": "Sarvam AI API"
    
            }
    
          }
    
        },
    
        {
    
          "parameters": {
    
            "resource": "speech",
    
            "operation": "speechToText",
    
            "binaryPropertyName": "data",
    
            "sttMode": "transcribe",
    
            "speechToTextOptions": {}
    
          },
    
          "type": "n8n-nodes-sarvam.sarvam",
    
          "typeVersion": 1,
    
          "position": [440, 0],
    
          "id": "sarvam-stt-demo",
    
          "name": "Speech to text",
    
          "credentials": {
    
            "sarvamApi": {
    
              "id": "__REPLACE_WITH_YOUR_CREDENTIAL_ID__",
    
              "name": "Sarvam AI API"
    
            }
    
          }
    
        },
    
        {
    
          "parameters": {
    
            "resource": "chat",
    
            "operation": "complete",
    
            "userMessage": "={{ $json.transcript }}",
    
            "chatOptions": {}
    
          },
    
          "type": "n8n-nodes-sarvam.sarvam",
    
          "typeVersion": 1,
    
          "position": [660, 0],
    
          "id": "sarvam-chat-demo",
    
          "name": "Complete chat",
    
          "credentials": {
    
            "sarvamApi": {
    
              "id": "__REPLACE_WITH_YOUR_CREDENTIAL_ID__",
    
              "name": "Sarvam AI API"
    
            }
    
          }
    
        }
    
      ],
    
      "pinData": {},
    
      "connections": {
    
        "When clicking 'Execute workflow'": {
    
          "main": [[{ "node": "Text to speech", "type": "main", "index": 0 }]]
    
        },
    
        "Text to speech": {
    
          "main": [[{ "node": "Speech to text", "type": "main", "index": 0 }]]
    
        },
    
        "Speech to text": {
    
          "main": [[{ "node": "Complete chat", "type": "main", "index": 0 }]]
    
        }
    
      },
    
      "active": false,
    
      "settings": {
    
        "executionOrder": "v1",
    
        "binaryMode": "separate"
    
      },
    
      "tags": []
    
    }

* * *

## Understanding the workflow

Unlike a single Python pipeline, n8n runs **discrete nodes**. Think in terms of **JSON** (text fields) and **binary** (files / audio).

**Typical voice Q &A path**
    
    
    Webhook / Form / File  →  [binary audio]  →  Sarvam STT  →  {{ $json.transcript }}
    
                                                          ↓
    
                                                Sarvam Chat (User message)
    
                                                          ↓
    
                                  {{ $json.choices[0].message.content }}  →  Sarvam TTS  →  binary audio  →  Email / HTTP / Storage

  1. **Trigger** produces binary (e.g. `data` or a custom name like `audio`).
  2. **Speech to Text** reads that binary property and writes **`transcript`** on the JSON item.
  3. **Chat → Complete** consumes text (expression from STT or static prompt).
  4. **Text to Speech** reads **Text** from chat output and writes **audio** back to binary (default often **`data`**).



When multiple Sarvam nodes exist, disambiguate with **`$('Exact node name').item.json...`** if `{{ $json }}` is ambiguous.

* * *

## Build a full voice Q&A (webhook sketch)

Use this when you want **HTTP POST with raw audio** → transcript → Sarvam model → spoken answer.

  1. Add **Webhook** : method **POST** , **Binary data** enabled so the body becomes a binary property (often **`data`**).
  2. Add **Sarvam AI** : **Speech** / **Speech to Text** : **Input Binary Field:** `data`, **Mode:** Transcribe (or Translate to English if the model should only see English).
  3. Add **Sarvam AI** : **Chat** / **Complete** : **User Message:** `={{ $json.transcript }}`, optional **System Message** with tone and safety rules, **Model:** `sarvam-105b`.
  4. Add **Sarvam AI** : **Speech** / **Text to Speech** : **Text:** `={{ $('Sarvam AI').item.json.choices[0].message.content }}` (adjust the node name to match your **Chat** node’s label in the canvas).
  5. Add **Respond to Webhook** : respond with **binary** from the TTS node (binary field **`data`** unless you renamed it).



**Naming tip:** Give each Sarvam node a **unique, descriptive name** (for example `Sarvam STT`, `Sarvam Chat`, `Sarvam TTS`) so expressions and logs stay readable.

* * *

## Customization examples

These mirror the **“Hindi / Tamil / multilingual / translate”** progression from our LiveKit and Pipecat guides, expressed as **node fields** instead of Python.

### Example 1: Hindi STT and TTS

  * **Speech to Text** → **Options → Language:** `hi-IN`, **Mode:** Transcribe.
  * **Text to Speech** → **Target Language:** `hi-IN`, **Options → Speaker:** e.g. `simran`, `shubh`, or any voice from the list below.



### Example 2: Tamil STT and TTS

  * STT **Language:** `ta-IN`, **Mode:** Transcribe.
  * TTS **Target Language:** `ta-IN`, pick a **Speaker** that fits your UX tests.



### Example 3: Multilingual input (auto language)

  * STT **Options → Language:** **Auto Detect** (value `unknown` in the API) when callers may switch languages.
  * **Mode:** Transcribe for same-language script output, or **Code Mixed** when you want English words Latin and Indic words in native script.



### Example 4: Indian-language speech → English text for downstream tools

**Difference:** use **Mode: Translate to English** on STT when the rest of the workflow (CRM, ticketing, English-only LLM) should only consume **English** text. Then wire **User Message** on Chat to `={{ $json.transcript }}` as usual.

* * *

## Operations reference

Resource| Operation| Purpose  
---|---|---  
Speech| Speech to Text| Binary audio in → `transcript` (plus mode / language options)  
Speech| Text to Speech| Text in → binary audio out (codec, pace, speaker, sample rate)  
Chat| Complete| User (+ optional system) message → Sarvam chat completion JSON  
  
### Speech to Text: modes

Mode| When to use  
---|---  
**Transcribe**|  Normal transcript in the spoken language and script  
**Translate to English**|  Spoken Indic (or mix) → **English** text for English-only steps  
**Transliterate (Roman)**|  Latin letters representing pronunciation  
**Code Mixed**|  English stays Latin; Indic words in native script  
**Verbatim**|  Minimal normalization, closest to raw recognition  
  
### Chat: models (node UI)

Model value| When to use  
---|---  
**`sarvam-105b`** (default in node)| Higher quality, richer reasoning options  
  
Under **Options** you can tune **temperature** , **max tokens** , **top p** , penalties, **reasoning effort** (where applicable), and **seed** : the same concepts covered in the [Chat completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview) docs.

* * *

## Available options

### Language codes (common)

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
Auto-detect (STT)| Use **Auto Detect** in the node (`unknown` in API terms)  
  
STT supports **23** Indian languages (full list in the node’s language dropdown). TTS **Target language** supports **11** languages (also listed in the UI).

### TTS: output codec and sample rate

Under **Options** on **Text to Speech** :

  * **Output Audio Codec:** `wav` (default), `mp3`, `aac`, `flac`, `opus`, `mulaw`, `alaw`, `linear16`.
  * **Sample Rate:** `8000`–`48000` Hz (see dropdown).
  * **Pace:** `0.5`–`2.0` (default `1.0`).
  * **Speaker:** many Indian-language voices (default `shubh`). Try a few in the UI to match your brand.



### Speaker voices (names as in node)

**Male:** aayan, aditya, advait, amit, anand, ashutosh, dev, gokul, kabir, manan, mani, mohit, rahul, rehan, rohan, ratan, shubh, soham, sumit, sunny, tarun, varun, vijay.

**Female:** amelia, ishita, kavitha, kavya, neha, pooja, priya, ritu, roopa, rupali, shreya, shruti, simran, sophia, suhani, tanya.

* * *

## Expressions and multiple Sarvam nodes

  * **`{{ $json.transcript }}`** : transcript from the **immediately previous** node when that node outputs it on the same item.
  * **`{{ $json.choices[0].message.content }}`** : assistant reply from **Chat → Complete**.
  * **`$('Node display name').item.json...`** : use when several nodes ran before the current one or when you need a **specific** upstream node. The string must match the **node name on the canvas** exactly.



Always turn on **“Execute previous nodes”** (or run the whole workflow) so the expression editor can **resolve** previews.

* * *

## Best practices

### 1\. Match binary property names exactly

The **Input Binary Field** on STT must equal the **binary field name** from the upstream node (`data`, `audio`, etc.). Inspect the **Binary** tab on the previous node’s output. Do not guess.

### 2\. Prefer unique node names before writing expressions

Rename nodes from generic **Sarvam AI** to **Sarvam STT – inbound** , **Sarvam Chat – support** , and so on. It prevents broken **`$('...')`** references after copy-paste.

### 3\. Pin sample data while building

Use **Pin data** on a trigger or HTTP node with a small sample file so you can iterate on STT options without re-uploading each run.

### 4\. Keep execution order predictable

Imported samples use **`executionOrder: v1`**. For multi-branch workflows, understand n8n’s execution model so STT always runs **after** the node that fetches audio.

### 5\. Treat credentials like environment secrets

Do not embed API keys in expressions or static JSON exports you commit to git. Use **Credentials** and n8n’s **external secrets** integrations for production.

### 6\. Use Sarvam as an AI tool where supported

The community node is built **`usableAsTool: true`** : on n8n versions that support it, you can expose Sarvam operations to **AI Agent** -style workflows as tools.

* * *

## Pro tips

  * **Auto Detect** on STT is ideal for mixed or unknown caller languages.
  * Sarvam handles **code-mixed** speech (for example Hinglish); pair that with **Code Mixed** mode when you care about script split.
  * **`sarvam-105b`** is the model used by the Chat node for chat-heavy automations.
  * Chain **Translate to English** early if downstream services are English-only, simpler than translating later in the graph.



* * *

## Troubleshooting

**Node does not appear after install** : Restart n8n. On self-hosted, confirm the package is installed in the **same** environment n8n loads and check server logs for install errors.

**Community nodes disabled** : Your admin may block installs. Ask for **`n8n-nodes-sarvam`** to be allow-listed or pre-baked into the image.

**`Binary data not found` on STT**: Wrong **Input Binary Field** name, or the previous node did not output binary on that execution (e.g. GET returned JSON instead of file). For **HTTP Request** , set response to **File** when downloading audio.

**Empty or nonsense transcript** : Check audio format (wav, mp3, ogg, flac), duration, and corruption. Try a fixed **Language** instead of auto-detect for debugging.

**Chat returns errors** : Verify **User Message** is non-empty (expressions must evaluate to text). Confirm **Model** is set and the Sarvam API is reachable from your host.

**403 from Sarvam** (`invalid_api_key_error`): Sarvam returns `403` (not `401`) for auth failures. Rotate the key in the dashboard and update the **Sarvam AI API** credential; ensure no stray spaces in the key field.

**Expressions show “undefined”** : Prior node did not run in this execution, or the JSON path is wrong. Open **OUTPUT** on each upstream node and copy paths from the **JSON** view.

* * *

## Additional resources

  * [Sarvam AI documentation](https://docs.sarvam.ai/)
  * [npm, n8n-nodes-sarvam](https://www.npmjs.com/package/n8n-nodes-sarvam)
  * [n8n-nodes-sarvam on GitHub](https://github.com/vinayak-sarvam/n8n-sarvam-node) (source and issues)
  * [n8n community nodes, installation](https://docs.n8n.io/integrations/community-nodes/installation/)
  * [Speech to Text, REST](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)
  * [Text to Speech, REST](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)
  * [Chat completion, overview](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * [Build Voice Agent with LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit): same Sarvam capabilities in real-time code
  * [Build Voice Agent with Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat): pipeline-style voice agent
  * [Build with Sarvam AI in LangChain](https://docs.sarvam.ai/api/integration/langchain): same Sarvam capabilities in Python code



* * *

## Need help?

  * Sarvam Support: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Community: [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



* * *

**Happy building!**

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)[Build with Sarvam AI in the Vercel AI SDKNext](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


