---
url: https://docs.sarvam.ai/api/speech-to-text/faq/
title: FAQs | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:50.809884+00:00
---

# FAQs | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/speech-to-text/faq/

Skip to navigation

On this page

  * General Questions
  * Indian Languages
  * REST API
  * Batch API
  * WebSocket API (Streaming)
  * Typical Accuracy Rates
  * Technical Questions
  * Duration Limits
  * 1\. Authentication Errors (403)
  * 2\. Rate Limit / Quota Errors (429)
  * 3\. Invalid Input (400)
  * 4\. Failed to read the file (400)
  * Billing & Support
  * Still Have Questions?



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Speech to Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)

# FAQs

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/speech-to-text/faq.md "View this page as plain text")|More actions

This page is for Model APIs.

# 

Frequently Asked Questions

Find answers to common questions about our speech-to-text services

## General Questions

###### What audio formats are supported?

**REST and Batch APIs** support a wide range of audio formats including:

  * WAV
  * MP3
  * M4A
  * AAC
  * OGG
  * FLAC
  * WebM
  * PCM (pcm_s16le, pcm_l16, pcm_raw)



**WebSocket/Streaming APIs** only support:

  * WAV
  * Raw PCM (pcm_s16le, pcm_l16, pcm_raw)



For optimal results, we recommend:

  * Sample rate: 16kHz or higher
  * Bit depth: 16-bit
  * Channels: Mono or Stereo



###### What languages are supported?

Our models support English and multiple Indian languages:

### Indian Languages

  * Hindi
  * English (Indian)
  * Bengali
  * Tamil
  * Telugu
  * Kannada
  * Malayalam
  * Marathi
  * Gujarati
  * Punjabi
  * Odia



`saaras:v3` extends coverage to 23 languages total (22 Indian languages + English), adding Assamese, Urdu, Nepali, Konkani, Kashmiri, Sindhi, Sanskrit, Santali, Manipuri, Bodo, Maithili, and Dogri.

Check our [models page](https://docs.sarvam.ai/api/getting-started/models) for the complete list and specific model capabilities.

###### What is the maximum duration?

The limits vary by API endpoint:

### REST API

  * Maximum duration: 30 seconds per request



### Batch API

  * Maximum duration: 2 hours per file
  * Maximum files per job: 20



### WebSocket API (Streaming)

  * Continuous streaming with chunked audio, no duration limit
  * Concurrency limits apply per plan (see [Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits))



For audio longer than 30 seconds, use the [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api). For files longer than 2 hours, we recommend:

  1. Splitting into smaller segments
  2. Contacting support for custom solutions



###### How accurate is the transcription?

Accuracy varies based on several factors:

### Typical Accuracy Rates

  * Clear speech, minimal background noise: 95-98%
  * Multiple speakers, moderate noise: 90-95%
  * Heavy accent or background noise: 85-90%



Factors affecting accuracy:

  * Audio quality
  * Background noise
  * Speaker accent
  * Speaking speed
  * Domain-specific terminology



Use our [interactive API reference](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe) to test with your specific audio.

## Technical Questions

###### How does speaker diarization work?

Speaker diarization identifies and labels different speakers in the audio:

  1. **Process** :

     * Voice activity detection
     * Speaker segmentation
     * Speaker clustering
     * Speaker labeling
  2. **Usage** (via Batch API):



    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    # Speaker diarization is available through the Batch API
    
    # See: https://docs.sarvam.ai/api/speech-to-text/batch
    
    job = client.speech_to_text_job.create_job(
    
        model="saaras:v4",
    
        mode="transcribe",
    
        with_diarization=True,
    
    )
    
    job.upload_files(file_paths=["audio.mp3"])
    
    job.start()
    
    job.wait_until_complete()
    
    job.download_outputs(output_dir="./output")

  3. **Output** : 
         
         {
         
           "segments": [
         
             {
         
               "speaker": "Speaker 1",
         
               "text": "Hello, how are you?",
         
               "start": 0.0,
         
               "end": 1.5
         
             },
         
             {
         
               "speaker": "Speaker 2",
         
               "text": "I'm doing well, thanks!",
         
               "start": 1.8,
         
               "end": 3.2
         
             }
         
           ]
         
         }




###### What are the rate limits?

Rate limits are applied per account based on your subscription plan and vary by endpoint. For the real-time REST API:

Plan| Rate Limit  
---|---  
**Starter**|  60 requests/min  
**Pro**|  100 requests/min  
**Business**|  4,000 requests/min  
**Enterprise**|  Custom limits  
  
Batch and WebSocket Streaming have their own, different limits. See the per-endpoint tables on the [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits) page.

### Duration Limits

  * **REST API** : Max 30 seconds of audio per request
  * **Batch API** : Up to 2 hours per file, 20 files per job
  * **Streaming API** : Continuous (chunked) streaming; concurrency limits per plan



For batch endpoints, avoid tight polling loops, poll no faster than your plan’s rate limit allows (e.g. every 3 seconds on Starter’s 20 req/min). The SDK’s `wait_until_complete()` already polls at a safe 5-second interval by default.

View the full [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits) page for details on HTTP headers, error handling, and upgrade paths.

###### How do I handle errors?

Common errors and solutions:

### 1\. Authentication Errors (403)
    
    
    {
    
      "error": {
    
        "code": "invalid_api_key_error",
    
        "message": "API key is invalid or expired"
    
      }
    
    }

Solution: Check API key validity and proper configuration. **Note:** Sarvam returns HTTP `403` (not `401`) for invalid/missing API keys. See the [Authentication](https://docs.sarvam.ai/api-reference/authentication) page.

### 2\. Rate Limit / Quota Errors (429)
    
    
    {
    
      "error": {
    
        "code": "insufficient_quota_error",
    
        "message": "API quota exceeded"
    
      }
    
    }

Solution: Implement exponential backoff or upgrade plan. A `429` with `rate_limit_exceeded_error` means too many requests; `insufficient_quota_error` means credits are exhausted. See [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting).

### 3\. Invalid Input (400)
    
    
    {
    
      "error": {
    
        "code": "invalid_request_error",
    
        "message": "Unsupported audio format"
    
      }
    
    }

Solution: Check supported formats and requirements

### 4\. Failed to read the file (400)
    
    
    {
    
      "error": {
    
        "message": "Failed to read the file, please check the audio format.",
    
        "code": "invalid_request_error"
    
      }
    
    }

This almost always means the uploaded bytes are not a readable audio file, not that the format is unsupported. Common causes:

  * **Empty or zero-length file** : the upload contains no bytes, or a buffer of all zeros
  * **Empty WebM blob from a browser recorder** : `MediaRecorder` produced a header with no audio frames (see “How do I record audio in the browser?” below)
  * **Junk or placeholder bytes** : the payload isn’t a real audio container
  * **Truncated or incomplete container** : the file was cut off during recording, download, or copy
  * **Passing a filename string instead of a file object** : use `file=open("audio.wav", "rb")` in Python, not `file="audio.wav"`



Solution: before uploading, verify the file exists, its size is greater than 0, and you’re passing a file handle/stream (not a path string).

See our [error handling guide](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting) for more details.

###### How do I record audio in the browser and transcribe it?

All the Node.js examples in these docs read audio with `fs.createReadStream(...)`, which doesn’t exist in the browser. To transcribe microphone audio from a web page, record with `MediaRecorder` and upload the resulting blob.

The most common mistake is uploading an **empty WebM blob** (a container header with no audio frames), which the API rejects with `"Failed to read the file, please check the audio format."` The recipe below avoids that by stopping the recorder cleanly, waiting for the final `dataavailable` event, and checking `blob.size > 0` before uploading:
    
    
    async function recordAndTranscribe(durationMs = 5000) {
    
      // 1. Capture the microphone
    
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
      // 2. Pick a supported mimeType (WebM/Opus is widely supported and accepted by the API)
    
      const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
    
        ? "audio/webm;codecs=opus"
    
        : "audio/webm";
    
      const recorder = new MediaRecorder(stream, { mimeType });
    
      const chunks = [];
    
      recorder.ondataavailable = (event) => {
    
        if (event.data.size > 0) chunks.push(event.data);
    
      };
    
      // 3. Stop cleanly: the final dataavailable fires before "stop" resolves
    
      const stopped = new Promise((resolve) => (recorder.onstop = resolve));
    
      recorder.start();
    
      setTimeout(() => recorder.stop(), durationMs);
    
      await stopped;
    
      stream.getTracks().forEach((track) => track.stop());
    
      // 4. Never upload an empty recording
    
      const blob = new Blob(chunks, { type: mimeType });
    
      if (blob.size === 0) {
    
        throw new Error("Recording is empty, no audio frames were captured.");
    
      }
    
      // 5. Upload to the Speech-to-Text API
    
      const formData = new FormData();
    
      formData.append("file", blob, "recording.webm");
    
      formData.append("model", "saaras:v4");
    
      formData.append("mode", "transcribe");
    
      const response = await fetch("https://api.sarvam.ai/speech-to-text", {
    
        method: "POST",
    
        headers: { "api-subscription-key": SARVAM_API_KEY },
    
        body: formData,
    
      });
    
      return await response.json();
    
    }

Pre-flight checklist before any upload:

  * The recording/file exists and `size > 0`
  * You’re sending the blob/file object, not a path or filename string
  * Audio longer than 30 seconds goes to the [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) instead of the sync REST endpoint



Don’t ship your API key in client-side code. In production, upload the recording to your own backend and call the Sarvam API from there.

###### How do I optimize for real-time transcription?

Tips for optimal real-time performance:

  1. **Audio Settings**


    
    
    const config = {
    
      sampleRate: 16000,
    
      encoding: 'LINEAR16',
    
      channels: 1
    
    }

  2. **Chunk Size**


  * Optimal: 100ms - 500ms chunks
  * Balance between latency and accuracy


  3. **WebSocket Connection**


    
    
    const ws = new WebSocket('wss://api.sarvam.ai/v1/stt/stream')
    
    ws.binaryType = 'arraybuffer'

  4. **Error Handling**


    
    
    ws.onerror = (error) => {
    
      console.error('WebSocket Error:', error)
    
      // Implement reconnection logic
    
    }

View our [real-time streaming guide](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api) for detailed examples.

## Billing & Support

###### How is usage calculated?

Usage is calculated based on:

  1. **Audio Duration**


  * Rounded up to the nearest second
  * Minimum charge: 1 second


  2. **Features Used**


  * Base transcription
  * Speaker diarization (+20%)
  * Language detection (+10%)
  * Chunk-level timestamps (included; **word-level timestamps are not supported**)



Example calculation:
    
    
    5 minutes audio × Base rate
    
    + Speaker diarization (20%)
    
    = Total cost

###### How do I check my credit usage?

You can check your credit usage directly on the [Billing page](https://indus.sarvam.ai/billing) in your Sarvam dashboard. It shows your total credits, how much has been consumed, and the remaining balance.

###### How do I get support?

Multiple support channels available:

  1. **Documentation**


  * [API Reference](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)
  * [Guides](https://docs.sarvam.ai/api/getting-started/quickstart)
  * [Examples](https://github.com/sarvamai/sarvam-ai-cookbook)


  2. **Direct Support**


  * Email: [support@sarvam.ai](mailto:support@sarvam.ai)
  * Enterprise: Dedicated support manager


  3. **Builder Community**


  * [Join our Discord](https://discord.com/invite/5rAsykttcs) for early access to new releases, biweekly challenges, office hours with the team, and India’s AI builder community.



## Still Have Questions?

### 

Can’t find what you’re looking for?

Our team is here to help! Reach out via email, or join our Discord to connect with the builder community.

[Email Support](mailto:support@sarvam.ai)[Join Discord](https://discord.com/invite/5rAsykttcs)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/best-practices)[How to select output modeNext](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/select-output-mode)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)
      * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
      * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)
      * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
      * [Realtime Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming)
      * [Best Practices](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/best-practices)
      * [FAQs](https://docs.sarvam.ai/api/speech-to-text/faq)
      * How-to

      * Use Cases

      * Legacy

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


