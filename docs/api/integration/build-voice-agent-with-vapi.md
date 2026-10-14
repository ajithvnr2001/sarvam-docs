---
url: https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi/
title: Build Your First Voice Agent using Vapi | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:41.050188+00:00
---

# Build Your First Voice Agent using Vapi | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi/

Skip to navigation

On this page

  * Overview
  * What You’ll Build
  * Quick Overview
  * Quick Start
  * 1\. Prerequisites
  * 2\. Create the Project
  * 3\. Create Environment File
  * 4\. Write the Bridge Server
  * 5\. Run and Expose the Server
  * 6\. Create Your Assistant
  * 7\. Test Your Agent
  * How a Call Flows
  * Going to Production
  * Customization Examples
  * Example 1: Hindi Voice Agent
  * Example 2: Multilingual Agent (Auto-detect)
  * Example 3: Speech-to-English Agent (Saaras)
  * Available Options
  * Language Codes
  * Speaker Voices (Bulbul v3)
  * Pro Tips
  * Troubleshooting
  * Additional Resources
  * Need Help?



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)

# Build Your First Voice Agent using Vapi

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi.md "View this page as plain text")|More actions

This page is for Model APIs.

Want a production voice agent without assembling the stack yourself? [Sarvam Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents) is a managed platform with speech recognition, reasoning, Indian-language voices, telephony, testing, and analytics included, from ₹3 per minute. This guide shows how to build your own pipeline on the APIs instead.

## Overview

This guide demonstrates how to build a **voice agent on[Vapi](https://vapi.ai/)** powered end-to-end by **Sarvam AI** : listening with Saaras v4, thinking with Sarvam-105B, and speaking with Bulbul v3. Perfect for bringing natural Indian-language conversations to Vapi’s hosted calling infrastructure (web calls, phone numbers, and SIP).

Vapi doesn’t ship Sarvam as a built-in provider, but it exposes **custom provider interfaces** for exactly this purpose:

Pipeline stage| Vapi provider| Sarvam model| How it connects  
---|---|---|---  
Transcriber (ears)| `custom-transcriber`| `saaras:v4`| WebSocket bridge (part of the server below)  
LLM (brain)| `custom-llm`| `sarvam-105b`| OpenAI-compatible proxy route (part of the server below)  
Voice (mouth)| `custom-voice`| `bulbul:v3`| HTTP webhook (part of the server below)  
  
All three run through **one small Node.js server** you’ll copy-paste below: a single process, a single deploy.

**Configure via API, not the dashboard.** Vapi’s dashboard dropdowns don’t list the `custom-transcriber` and `custom-voice` providers; they can only be set through the Vapi API. This guide creates the assistant with a single `curl` command in Step 6, and tests it with a small web page in Step 7 (the dashboard’s “Talk to Assistant” button has a known bug with custom-transcriber assistants).

## What You’ll Build

A Vapi voice agent that can:

  * Listen to users speaking (in multiple Indian languages!)
  * Understand and process their requests
  * Respond back in natural-sounding voices



## Quick Overview

  1. Get API keys (Vapi, Sarvam)
  2. Install packages: `npm install express ws sarvamai dotenv`
  3. Create `.env` file with your API keys
  4. Copy the bridge server (~150 lines of Node.js)
  5. Run: `node server.js` \+ expose with ngrok
  6. Create the assistant with one `curl` command
  7. Test from a browser test page



* * *

## Quick Start

### 1\. Prerequisites

  * Node.js 18 or higher
  * API keys from: 
    * [Sarvam AI](https://dashboard.sarvam.ai/) (get API key from dashboard)
    * [Vapi](https://dashboard.vapi.ai/), for which you need **both** keys from the API Keys page: 
      * **Private key** : for creating the assistant via API
      * **Public key** : for starting test calls from the browser
  * [ngrok](https://ngrok.com/) (free account) to expose your local server to Vapi’s cloud



Vapi keys are per-organization. If you have multiple Vapi orgs, copy both keys from the **same org** ; a key from another org is rejected with `401 Invalid Key` or `403 Key doesn't allow assistantId`.

### 2\. Create the Project
    
    
    mkdir vapi-sarvam-bridge
    
    cd vapi-sarvam-bridge
    
    npm init -y
    
    npm install express ws sarvamai dotenv

### 3\. Create Environment File

Create a file named `.env` in your project folder:
    
    
    SARVAM_API_KEY=YOUR_SARVAM_API_KEY
    
    PORT=3001
    
    # STT defaults
    
    STT_LANGUAGE=unknown        # auto-detect, or en-IN, hi-IN, ta-IN, ...
    
    # TTS defaults
    
    TTS_LANGUAGE=en-IN
    
    TTS_SPEAKER=shubh

Placeholders you must replace are written as `YOUR_*` throughout this guide. Swap in your Sarvam API key here.

### 4\. Write the Bridge Server

The server has three routes, one per pipeline stage:

  * **`/llm/chat/completions`** : forwards chat requests to Sarvam’s OpenAI-compatible API, adding your API key and disabling thinking mode (see the Note below).
  * **`/api/custom-transcriber`** : receives Vapi’s live call audio over WebSocket (2-channel PCM: caller + assistant), splits the channels, and streams each to a Saaras v4 session.
  * **`/api/synthesize`** : receives Vapi’s `voice-request` webhooks, synthesizes with Bulbul v3, and returns the raw PCM audio Vapi requires.



Create `sarvamTranscriber.js`:
    
    
    const { SarvamAIClient } = require("sarvamai");
    
    class SarvamTranscriber {
    
      constructor({ channel, sampleRate, language, onTranscript }) {
    
        this.channel = channel; // "customer" or "assistant"
    
        this.sampleRate = sampleRate;
    
        this.language = language;
    
        this.onTranscript = onTranscript;
    
        this.socket = null;
    
      }
    
      async connect() {
    
        const client = new SarvamAIClient({
    
          apiSubscriptionKey: process.env.SARVAM_API_KEY,
    
        });
    
        // Heads-up on naming: these keys mirror the WebSocket API's query
    
        // parameters, so "language-code" is hyphenated (quoted) while the
    
        // rest are snake_case. The SDK expects them as-is, so don't "fix" the names.
    
        this.socket = await client.speechToTextStreaming.connect({
    
          model: "saaras:v4",
    
          mode: "transcribe",
    
          "language-code": this.language,
    
          sample_rate: this.sampleRate,
    
          input_audio_codec: "pcm_s16le", // Vapi sends raw 16-bit PCM
    
          high_vad_sensitivity: "true",   // 0.5s silence boundary for snappier turns
    
        });
    
        this.socket.on("message", (message) => {
    
          if (message.type === "data" && message.data.transcript) {
    
            this.onTranscript(message.data.transcript, this.channel);
    
          }
    
        });
    
        this.socket.on("error", (err) => {
    
          console.error(`Sarvam STT error (${this.channel}):`, err);
    
        });
    
        await this.socket.waitForOpen();
    
        console.log(`Sarvam STT connected for ${this.channel} channel`);
    
      }
    
      sendAudio(pcmBuffer) {
    
        if (!this.socket) return;
    
        try {
    
          // encoding stays "audio/wav" even for raw PCM, since the codec was
    
          // already declared via input_audio_codec at connection time
    
          this.socket.transcribe({
    
            audio: pcmBuffer.toString("base64"),
    
            sample_rate: this.sampleRate,
    
            encoding: "audio/wav",
    
          });
    
        } catch (err) {
    
          console.error(`Sarvam STT send failed (${this.channel}):`, err);
    
        }
    
      }
    
      close() {
    
        this.socket?.close();
    
      }
    
    }
    
    module.exports = SarvamTranscriber;

Create `server.js`:
    
    
    require("dotenv").config();
    
    const express = require("express");
    
    const http = require("http");
    
    const { WebSocketServer } = require("ws");
    
    const { SarvamAIClient } = require("sarvamai");
    
    const SarvamTranscriber = require("./sarvamTranscriber");
    
    const app = express();
    
    app.use(express.json({ limit: "5mb" }));
    
    const sarvam = new SarvamAIClient({
    
      apiSubscriptionKey: process.env.SARVAM_API_KEY,
    
    });
    
    // ---------------------------------------------------------------
    
    // LLM proxy (custom-llm): forwards to Sarvam with reasoning off
    
    // ---------------------------------------------------------------
    
    // Sarvam enables thinking mode by default, which delays the first
    
    // spoken token and can consume the whole max_tokens budget. Vapi's
    
    // custom-llm config can't pass reasoning_effort, so inject it here.
    
    app.post("/llm/chat/completions", async (req, res) => {
    
      try {
    
        const body = { ...req.body, reasoning_effort: null };
    
        const upstream = await fetch("https://api.sarvam.ai/v1/chat/completions", {
    
          method: "POST",
    
          headers: {
    
            "api-subscription-key": process.env.SARVAM_API_KEY,
    
            "Content-Type": "application/json",
    
          },
    
          body: JSON.stringify(body),
    
        });
    
        res.status(upstream.status);
    
        res.setHeader(
    
          "Content-Type",
    
          upstream.headers.get("content-type") || "application/json"
    
        );
    
        // Stream SSE (or JSON) straight through
    
        const { Readable } = require("stream");
    
        Readable.fromWeb(upstream.body).pipe(res);
    
      } catch (error) {
    
        console.error("LLM proxy failed:", error);
    
        if (!res.headersSent) res.status(500).json({ error: "LLM proxy failed" });
    
      }
    
    });
    
    // ---------------------------------------------------------------
    
    // TTS endpoint (custom-voice): text in, raw PCM out
    
    // ---------------------------------------------------------------
    
    // Sarvam returns base64 WAV; Vapi needs headerless 16-bit mono PCM.
    
    // Locate the WAV "data" chunk and return everything after it.
    
    function wavToRawPcm(wavBuffer) {
    
      const dataIndex = wavBuffer.indexOf("data");
    
      if (dataIndex === -1) throw new Error("Invalid WAV: no data chunk");
    
      return wavBuffer.subarray(dataIndex + 8); // skip "data" tag + 4-byte size
    
    }
    
    app.post("/api/synthesize", async (req, res) => {
    
      try {
    
        const { message } = req.body;
    
        if (message?.type !== "voice-request" || !message.text) {
    
          return res.status(400).json({ error: "Expected a voice-request with text" });
    
        }
    
        const response = await sarvam.textToSpeech.convert({
    
          text: message.text,
    
          model: "bulbul:v4-flash",
    
          language_code: process.env.TTS_LANGUAGE || "en-IN",
    
          speaker: process.env.TTS_SPEAKER || "shubh",
    
          speech_sample_rate: message.sampleRate, // must match Vapi's request
    
        });
    
        const wav = Buffer.from(response.audios.join(""), "base64");
    
        const pcm = wavToRawPcm(wav);
    
        res.setHeader("Content-Type", "application/octet-stream");
    
        res.setHeader("Content-Length", pcm.length);
    
        res.end(pcm);
    
      } catch (error) {
    
        console.error("TTS synthesis failed:", error);
    
        if (!res.headersSent) {
    
          res.status(500).json({ error: "TTS synthesis failed" });
    
        }
    
      }
    
    });
    
    // ---------------------------------------------------------------
    
    // STT endpoint (custom-transcriber): WebSocket audio in, JSON out
    
    // ---------------------------------------------------------------
    
    // Vapi streams interleaved stereo PCM: channel 0 = customer, 1 = assistant
    
    function splitStereo(buffer) {
    
      const frames = Math.floor(buffer.length / 4); // 2 bytes x 2 channels
    
      const customer = Buffer.alloc(frames * 2);
    
      const assistant = Buffer.alloc(frames * 2);
    
      for (let i = 0; i < frames; i++) {
    
        buffer.copy(customer, i * 2, i * 4, i * 4 + 2);
    
        buffer.copy(assistant, i * 2, i * 4 + 2, i * 4 + 4);
    
      }
    
      return { customer, assistant };
    
    }
    
    const server = http.createServer(app);
    
    const wss = new WebSocketServer({ server, path: "/api/custom-transcriber" });
    
    wss.on("connection", (ws) => {
    
      console.log("Vapi connected to custom transcriber");
    
      const transcribers = {};
    
      const sendTranscript = (transcription, channel) => {
    
        if (ws.readyState !== ws.OPEN) return;
    
        console.log(`Transcript (${channel}): ${transcription}`);
    
        ws.send(
    
          JSON.stringify({
    
            type: "transcriber-response",
    
            transcription,
    
            channel,
    
            transcriptType: "final",
    
          })
    
        );
    
      };
    
      ws.on("message", async (data, isBinary) => {
    
        if (!isBinary) {
    
          let msg;
    
          try {
    
            msg = JSON.parse(data.toString());
    
          } catch (err) {
    
            console.error("Ignoring non-JSON control message from Vapi:", err);
    
            return;
    
          }
    
          if (msg.type === "start") {
    
            // One Sarvam session per audio channel
    
            const language = process.env.STT_LANGUAGE || "unknown";
    
            try {
    
              for (const channel of ["customer", "assistant"]) {
    
                transcribers[channel] = new SarvamTranscriber({
    
                  channel,
    
                  sampleRate: msg.sampleRate,
    
                  language,
    
                  onTranscript: sendTranscript,
    
                });
    
                await transcribers[channel].connect();
    
              }
    
            } catch (err) {
    
              // Most common cause: invalid SARVAM_API_KEY. Close the socket
    
              // so Vapi's fallback plan can take over instead of dead air.
    
              console.error("Failed to start Sarvam STT sessions:", err);
    
              ws.close(1011, "Transcriber startup failed");
    
            }
    
          }
    
          return;
    
        }
    
        if (!transcribers.customer) return;
    
        const { customer, assistant } = splitStereo(data);
    
        transcribers.customer.sendAudio(customer);
    
        transcribers.assistant.sendAudio(assistant);
    
      });
    
      ws.on("error", (err) => {
    
        console.error("Transcriber WebSocket error:", err);
    
      });
    
      ws.on("close", () => {
    
        console.log("Vapi disconnected");
    
        Object.values(transcribers).forEach((t) => t.close());
    
      });
    
    });
    
    const PORT = process.env.PORT || 3001;
    
    server.listen(PORT, () => {
    
      console.log(`Sarvam bridge listening on port ${PORT}`);
    
    });

**Why the LLM proxy instead of pointing Vapi straight at`https://api.sarvam.ai/v1`?** The direct connection works (Sarvam’s Chat Completions API is OpenAI-compatible and accepts the Bearer token Vapi sends), but Sarvam models have **thinking mode on by default** , so reasoning tokens stream before the reply, delaying the agent’s speech; with a small `max_tokens` the entire budget can be consumed by reasoning, leaving the reply empty. The proxy injects `reasoning_effort: null` on every request, which Vapi has no other way to pass. It also authenticates server-side, so you don’t need to configure a Custom LLM credential in Vapi at all.

### 5\. Run and Expose the Server
    
    
    node server.js

In a second terminal, expose it with ngrok:
    
    
    ngrok http 3001

Note the public URL (e.g. `https://your-id.ngrok-free.app`): you’ll use it in the next step.

### 6\. Create Your Assistant

Replace `YOUR_VAPI_PRIVATE_KEY` and the three `your-id.ngrok-free.app` URLs (model, transcriber, and voice) with your ngrok hostname, then run:
    
    
    curl -X POST https://api.vapi.ai/assistant \
    
      -H "Authorization: Bearer YOUR_VAPI_PRIVATE_KEY" \
    
      -H "Content-Type: application/json" \
    
      -d '{
    
        "name": "Sarvam Voice Agent",
    
        "firstMessage": "Hello! How can I help you today?",
    
        "model": {
    
          "provider": "custom-llm",
    
          "url": "https://your-id.ngrok-free.app/llm",
    
          "model": "sarvam-105b",
    
          "messages": [
    
            {
    
              "role": "system",
    
              "content": "You are a helpful voice assistant. Be friendly, concise, and conversational. Keep replies short - they will be spoken aloud."
    
            }
    
          ]
    
        },
    
        "transcriber": {
    
          "provider": "custom-transcriber",
    
          "server": {
    
            "url": "wss://your-id.ngrok-free.app/api/custom-transcriber"
    
          }
    
        },
    
        "voice": {
    
          "provider": "custom-voice",
    
          "server": {
    
            "url": "https://your-id.ngrok-free.app/api/synthesize",
    
            "timeoutSeconds": 45
    
          }
    
        }
    
      }'

The response contains your assistant’s `id`: copy it for the next step.

Vapi treats the model `url` as an OpenAI `baseURL` and appends `/chat/completions` itself, which is why the value ends at `/llm`. The transcriber URL uses `wss://` (WebSocket), the other two use `https://`.

### 7\. Test Your Agent

Create `test-call.html`, a minimal page that starts a web call using Vapi’s Web SDK:
    
    
    <!DOCTYPE html>
    
    <html>
    
    <body>
    
      <h1>Sarvam Voice Agent</h1>
    
      <button id="start">Start Call</button>
    
      <button id="stop">End Call</button>
    
      <pre id="log"></pre>
    
      <script type="module">
    
        import Vapi from "https://esm.sh/@vapi-ai/web";
    
        const vapi = new Vapi("YOUR_VAPI_PUBLIC_KEY");
    
        const log = (msg) =>
    
          (document.getElementById("log").textContent += msg + "\n");
    
        document.getElementById("start").onclick = () =>
    
          vapi.start("YOUR_ASSISTANT_ID");
    
        document.getElementById("stop").onclick = () => vapi.stop();
    
        vapi.on("call-start", () => log("Call started, speak now!"));
    
        vapi.on("call-end", () => log("Call ended"));
    
        vapi.on("message", (m) => {
    
          if (m.type === "transcript") log(`${m.role}: ${m.transcript}`);
    
        });
    
        vapi.on("error", (e) => log("ERROR: " + JSON.stringify(e)));
    
      </script>
    
    </body>
    
    </html>

Fill in your **public** key and the assistant `id`, serve it locally, and open it in your browser:
    
    
    python3 -m http.server 8080
    
    # open http://localhost:8080/test-call.html

Click **Start Call** , allow microphone access, and start speaking. You’ll see live transcripts on the page and in your server logs, and hear the agent reply in Bulbul’s voice.

That’s it! You’ve built a Vapi voice agent running entirely on Sarvam models!

Why a test page instead of the dashboard? Vapi’s dashboard has a known bug with custom-transcriber assistants: the “Talk to Assistant” button can fail with a 404 or a `Cannot read properties of undefined (reading 'cost')` error. The assistant itself is fine; calls made through the Web SDK, API, or a phone number work normally.

* * *

## How a Call Flows

  1. **Transcriber** : Vapi opens one WebSocket per call and streams raw 16-bit PCM with the caller on channel 0 and the assistant on channel 1. The bridge splits the channels and runs a separate Saaras v4 streaming session for each, so both sides of the conversation are transcribed.
  2. **LLM** : Vapi sends standard OpenAI-style chat completion requests. The proxy adds your Sarvam key, disables thinking mode, and streams the response back token by token.
  3. **Voice** : for every reply (including the `firstMessage`), Vapi POSTs a `voice-request` with the text and a target sample rate. The bridge synthesizes with Bulbul v3 at that exact sample rate and returns headerless mono PCM.



* * *

## Going to Production

  * **Deploy the bridge server** to any Node.js host and replace the ngrok URLs in your assistant (PATCH `https://api.vapi.ai/assistant/:id`). Host in an Indian region since Sarvam’s APIs are served from India, so proximity cuts round-trip latency on every STT chunk and TTS request.
  * **Secure the endpoints** : set `server.secret` in the transcriber/voice config and validate the `x-vapi-secret` header on every request, or use Vapi’s [Custom Credentials](https://docs.vapi.ai/customization/custom-voices/custom-tts#authentication-setup) with a `credentialId`.
  * **Add a fallback voice** so calls continue on a built-in Vapi voice if your TTS endpoint is ever unreachable:


    
    
    "voice": {
    
      "provider": "custom-voice",
    
      "server": { "url": "https://your-host.com/api/synthesize" },
    
      "fallbackPlan": {
    
        "voices": [{ "provider": "vapi", "voiceId": "Neha" }]
    
      }
    
    }

  * **Attach a phone number** : in the Vapi dashboard, create or import a phone number and assign your assistant to it, and the same bridge serves phone calls with no changes.



* * *

## Customization Examples

### Example 1: Hindi Voice Agent

Set the bridge’s `.env` to Hindi:
    
    
    STT_LANGUAGE=hi-IN
    
    TTS_LANGUAGE=hi-IN
    
    TTS_SPEAKER=simran

And make the LLM reply in Hindi via the assistant’s system message:
    
    
    {
    
      "role": "system",
    
      "content": "आप एक सहायक वॉयस असिस्टेंट हैं। हमेशा हिंदी में छोटे और स्पष्ट जवाब दें।"
    
    }

### Example 2: Multilingual Agent (Auto-detect)

Keep `STT_LANGUAGE=unknown`: Saaras v4 auto-detects the spoken language. Then tell the LLM:
    
    
    Reply in the same language the user speaks.

Bulbul v3 handles code-mixed text (e.g. Hinglish) out of the box; set `TTS_LANGUAGE` to your primary audience’s language.

### Example 3: Speech-to-English Agent (Saaras)

**Difference** : Saaras v4 handles both transcription (same-language output) and translation (English output) via the `mode` parameter. Use `mode="translate"` when users speak Indian languages but you want to process and respond in English.

In `sarvamTranscriber.js`, change the connection:
    
    
    this.socket = await client.speechToTextStreaming.connect({
    
      model: "saaras:v4",
    
      mode: "translate",              // Speech-to-English translation
    
      sample_rate: this.sampleRate,
    
      input_audio_codec: "pcm_s16le",
    
      high_vad_sensitivity: "true",
    
    });

**Note:** Saaras v4 with `mode="translate"` automatically detects the source language (Hindi, Tamil, etc.) and translates spoken content directly to English text, so the rest of your pipeline stays English-only.

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
Auto-detect (STT only)| `unknown`  
  
### Speaker Voices (Bulbul v3)

**Male (23):** Shubh (default), Aditya, Rahul, Rohan, Amit, Dev, Ratan, Varun, Manan, Sumit, Kabir, Aayan, Ashutosh, Advait, Anand, Tarun, Sunny, Mani, Gokul, Vijay, Mohit, Rehan, Soham

**Female (14):** Ritu, Priya, Neha, Pooja, Simran, Kavya, Ishita, Shreya, Roopa, Tanya, Shruti, Suhani, Kavitha, Rupali

* * *

## Pro Tips

  * Use `STT_LANGUAGE=unknown` to automatically detect the language. Great for multilingual scenarios!
  * Sarvam’s models understand code-mixing: your agent can naturally handle Hinglish, Tanglish, and other mixed languages.
  * For lower time-to-first-token on live calls, disable reasoning by passing `reasoning_effort=None` in your proxy’s chat completion call.
  * Keep LLM replies short: spoken responses feel best under a couple of sentences, so say so in the system prompt.
  * Vapi’s `sampleRate` in each `voice-request` maps directly to Bulbul’s `speech_sample_rate`: the bridge passes it through, so never hard-code a sample rate.



* * *

## Troubleshooting

**“Request failed with status code 404” or a`cost` error in the Vapi dashboard**: Known dashboard bug with custom-transcriber assistants: the assistant works; test via the web page from Step 7 instead of the dashboard’s “Talk to Assistant” button.

**`401 Invalid Key` / `403 Key doesn't allow assistantId`**: You’re mixing keys. Assistant creation needs the **private** key, browser calls need the **public** key, and both must come from the same Vapi organization. Verify with: `curl -s -o /dev/null -w "%{http_code}" https://api.vapi.ai/assistant -H "Authorization: Bearer YOUR_VAPI_PRIVATE_KEY"`, which should print `200`.

**Agent connects but never speaks (empty LLM replies)** : You’re likely bypassing the LLM proxy. With thinking mode on (Sarvam’s default), reasoning can consume the entire `max_tokens` budget and return an empty reply: route the model URL through `/llm` as shown, which disables reasoning.

**Garbled or distorted agent speech** : The TTS response isn’t matching Vapi’s PCM spec: most commonly a WAV header left in the response or a sample-rate mismatch. Use the `wavToRawPcm` helper as-is and always pass `message.sampleRate` through.

**No transcripts arriving** : Confirm the transcriber URL starts with `wss://` (not `https://`) and check the server logs for “Vapi connected to custom transcriber” and Sarvam auth errors (`SARVAM_API_KEY` missing or invalid).

**ngrok URL stopped working** : Free ngrok URLs change on every restart. Get the current URL from `http://localhost:4040` and PATCH your assistant with the new endpoints.

* * *

## Additional Resources

  * [Sarvam AI Documentation](https://docs.sarvam.ai/)
  * [Sarvam Streaming Speech-to-Text API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)
  * [Sarvam Chat Completions API](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * [Sarvam Text-to-Speech API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)
  * [Vapi Custom Transcriber Guide](https://docs.vapi.ai/customization/custom-transcriber)
  * [Vapi Custom LLM Guide](https://docs.vapi.ai/customization/custom-llm/using-your-server)
  * [Vapi Custom TTS Guide](https://docs.vapi.ai/customization/custom-voices/custom-tts)



* * *

## Need Help?

  * Sarvam Support: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Community: [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



* * *

**Happy Building!**

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)[Build workflows with Sarvam AI in n8nNext](https://docs.sarvam.ai/api/integration/n8n)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


