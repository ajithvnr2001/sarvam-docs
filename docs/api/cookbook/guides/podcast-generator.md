---
url: https://docs.sarvam.ai/api/cookbook/guides/podcast-generator/
title: Podcast Generator | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:30.913568+00:00
---

# Podcast Generator | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/cookbook/guides/podcast-generator/

Skip to navigation

On this page

  * Overview
  * Business Value
  * How It Works
  * 1\. Prerequisites
  * 2\. Clone and Install
  * 3\. Configure Environment Variables
  * 4\. Run It
  * 5\. Pipeline Walkthrough
  * Step 1: Parse the PDF
  * Step 2: Generate the script
  * Step 3: Voice each line
  * Step 4: Orchestrate with Inngest
  * Available Options
  * Supported Languages
  * Default Voices (Bulbul v4 Flash)
  * Customization
  * Use different voices per language
  * Change how long the podcast is
  * Move off the in-memory stubs
  * Tips & Best Practices
  * Error Handling
  * Additional Resources
  * Final Notes



Scroll to top

[Cookbook](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)[Guides](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)

# Podcast Generator

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator.md "View this page as plain text")|More actions

This page is for Model APIs.

## **Overview**

This cookbook builds a full-stack app that turns any PDF into a listenable, two-host audio podcast. It chains together three Sarvam AI APIs, **Document Digitization** to extract the document’s text, a **Sarvam chat model** to turn that text into a conversational script, and **Bulbul v4 Flash TTS (latest)** to voice each line, and runs the whole pipeline as a background job so the UI stays responsive while a long document is processed.

**What you’ll build:**

  * A Next.js app where a user uploads a PDF and picks a target language
  * A background pipeline (PDF → text → script → audio) that runs as durable, resumable steps
  * A host/guest podcast script generated directly in the target language
  * Per-line audio segments stitched into a playable episode with a transcript view
  * Support for 11 languages (10 Indian + English), including auto-summarization for documents too long to fit in a single prompt



[View on GitHubBrowse the full source for this app in the sarvam-ai-cookbook repo.](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/examples/sarvam-podcast-generator)[Run Code LocallyJump to Clone and Install to set this demo up on your machine.](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator#2-clone-and-install)

### Business Value

  * Turn reports, research papers, and policy documents into audio for commuting or accessibility
  * Localize long-form written content into regional languages without a human translator
  * Repurpose existing documentation or course material into a more engaging audio format



###### EdTech

###### Enterprise Knowledge

###### Publishing & Media

Convert textbook chapters or study notes into a podcast-style discussion, in the student’s preferred language.

## **How It Works**

[1](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator#parse-the-pdf)

### Parse the PDF

The uploaded PDF is sent to Sarvam’s **Document Digitization** API, which extracts its text as Markdown, preserving reading order and table structure.

[2](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator#summarize-if-needed)

### Summarize if needed

If the extracted text is too long to fit in a single prompt, it’s split into chunks and each chunk is summarized by a Sarvam chat model before moving on, so very large documents don’t break the pipeline.

[3](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator#generate-a-two-host-script)

### Generate a two-host script

The (possibly summarized) text is sent to a Sarvam chat model with a prompt that asks for a natural **host/guest** conversation, returned as structured JSON, directly in the target language.

[4](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator#voice-every-line)

### Voice every line

Each line of the script is converted to speech with **Bulbul v4 Flash TTS (latest)** , using a distinct voice for the host and the guest, then assembled into a single playable episode with a synced transcript.

All four steps run inside a background job orchestrated by [Inngest](https://inngest.com/), so a slow TTS call or a large document doesn’t block the request or time out the browser.

## **1\. Prerequisites**

  * Node.js 18 or higher
  * A Sarvam API key, sign up on the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/) to get one
  * A free [Inngest](https://inngest.com/) account, used to run the PDF-to-podcast pipeline as a durable background job
  * A PDF you want to turn into a podcast



Redis and UploadThing are also referenced in the app’s configuration but are optional for local development. See [Configure Environment Variables](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator#3-configure-environment-variables) below for what each one actually does out of the box.

## **2\. Clone and Install**

###### macOS/Linux

###### Windows
    
    
    git clone https://github.com/sarvamai/sarvam-ai-cookbook.git
    
    cd sarvam-ai-cookbook/examples/sarvam-podcast-generator
    
    npm install

## **3\. Configure Environment Variables**

Create a `.env` file in the project root:
    
    
    SARVAM_API_KEY=your_sarvam_api_key_here
    
    REDIS_URL=your_redis_url
    
    UPLOADTHING_TOKEN=your_uploadthing_token
    
    INNGEST_SIGNING_KEY=your_inngest_signing_key

As shipped, the app’s job store always keeps job state in an in-memory map, and its audio upload helper always stores generated audio as in-memory base64 data URLs, regardless of what you set for `REDIS_URL` or `UPLOADTHING_TOKEN`. This is fine for local, single-process development, but it won’t survive a server restart or work across multiple serverless instances. Wire up real Redis and UploadThing clients in `lib/job-store.ts` and `lib/upload-audio.ts` before deploying.

Because audio is stored as raw base64 instead of a real file URL, each TTS segment’s “URL” is actually several hundred KB of inline data, and Inngest persists that as the step’s return value. On long podcasts this can occasionally hit Inngest’s per-step output size limit (`output_too_large` in the `inngest dev` logs); Inngest’s automatic step retry recovers from it with no data loss, just extra latency. A real UploadThing token resolves this at the source, since steps would then store a short URL instead of the raw audio.

## **4\. Run It**

Start the Next.js app and the Inngest dev server in two terminals:
    
    
    npm run dev
    
    
    npm run inngest

Open [http://localhost:3000](http://localhost:3000/), pick a target language, upload a PDF, and watch the status update as the pipeline runs. The Inngest dev dashboard at [http://localhost:8288](http://localhost:8288/) shows every step, script generation, each TTS call, retries, in real time, which is the fastest way to see what the pipeline is actually doing.

## **5\. Pipeline Walkthrough**

### Step 1: Parse the PDF

`app/api/parse-pdf/route.ts` drives Document Digitization’s job API directly: create a job, get a presigned upload URL, upload the PDF, start the job, poll until it completes, then download and unzip the Markdown output.
    
    
    try {
    
      const createRes = await fetch(BASE_URL, {
    
        method: 'POST',
    
        headers: HEADERS,
    
        body: JSON.stringify({
    
          job_parameters: { output_format: 'md', language: 'en-IN' },
    
        }),
    
      });
    
      if (!createRes.ok) {
    
        throw new Error(`Failed to create job: ${await createRes.text()}`);
    
      }
    
      const { job_id } = await createRes.json();
    
      // Get a presigned URL and upload the PDF to it
    
      await fetch(`${BASE_URL}/upload-files`, {
    
        method: 'POST',
    
        headers: HEADERS,
    
        body: JSON.stringify({ job_id, files: [file.name] }),
    
      });
    
      // ... PUT the file to the presigned URL ...
    
      // Start the job
    
      const startRes = await fetch(`${BASE_URL}/${job_id}/start`, {
    
        method: 'POST',
    
        headers: HEADERS,
    
        body: JSON.stringify({}),
    
      });
    
      if (!startRes.ok) {
    
        throw new Error(`Failed to start job: ${await startRes.text()}`);
    
      }
    
      // Poll until the job reaches a terminal state, then download the result
    
      await pollStatus(job_id);
    
      const downloadRes = await fetch(`${BASE_URL}/${job_id}/download-files`, {
    
        method: 'POST',
    
        headers: HEADERS,
    
        body: JSON.stringify({}),
    
      });
    
      if (!downloadRes.ok) {
    
        throw new Error(`Failed to get download URLs: ${await downloadRes.text()}`);
    
      }
    
      const downloadData = await downloadRes.json();
    
    } catch (error) {
    
      console.error('Document Intelligence error:', error);
    
      return NextResponse.json(
    
        { error: error instanceof Error ? error.message : 'Failed to process PDF' },
    
        { status: 500 }
    
      );
    
    }

`pollStatus` throws if the job reaches a `Failed` state, so that failure is caught here too. The route returns the caught error as a `500` with a JSON `error` field instead of crashing the request.

This app calls the REST endpoints directly so it can unzip the output itself. The legacy `document_intelligence` SDK wraps the same job lifecycle behind `create_job()` / `upload_file()` / `start()` / `wait_until_complete()` / `download_output()`. If you’re starting a pipeline from scratch, use [Document AI](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview#quick-start-digitise) instead, `doc_ai.digitise()` creates and submits the job in one call.

Sarvam’s role: This step runs entirely on Sarvam’s Document Digitization API. Sarvam does the actual PDF parsing, layout analysis, table structure, and reading order, and hands back clean Markdown; the route above is just a REST client driving that job’s create → upload → start → poll → download lifecycle.

### Step 2: Generate the script

`inngest/podcast-generation.ts` sends the extracted text to `sarvam-105b` via the Chat Completion API, with a prompt that requests a JSON object containing a `script` array of `{speaker, text}` turns:
    
    
    try {
    
      const response = await fetch('https://api.sarvam.ai/v1/chat/completions', {
    
        method: 'POST',
    
        headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    
        body: JSON.stringify({
    
          messages: [{ role: 'user', content: prompt }],
    
          model: 'sarvam-105b',
    
          temperature: 0.7,
    
          max_tokens: 4096,
    
        }),
    
      });
    
      if (!response.ok) {
    
        throw new Error(`Sarvam API error: ${response.status} - ${await response.text()}`);
    
      }
    
      const data = await response.json();
    
      if (!data.choices?.[0]?.message?.content) {
    
        throw new Error('No content received from Sarvam API');
    
      }
    
      return data.choices[0].message.content;
    
    } catch (error) {
    
      console.error('Error calling Sarvam API:', error);
    
      throw error;
    
    }

This is itself wrapped in a helper (`callSarvamChat`) that also retries on a `429` with exponential backoff and retries once more on a bare network failure before giving up, so a transient rate limit or dropped connection doesn’t fail the whole pipeline run. The prompt asks for at least 10-15 host/guest exchanges and instructs the model to reply with **only** JSON, no Markdown code fences, which the app strips defensively anyway before calling `JSON.parse`. If the document’s text is too large for a single prompt, it’s chunked and each chunk is summarized by the same chat model first, and the summaries (not the raw text) become the input to script generation.

This is the same [Chat Completion API](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview) used for regular conversational completions, there’s no separate “structured output” endpoint. The app gets JSON back by asking for it in the prompt and defensively parsing the response.

Sarvam’s role: Sarvam’s `sarvam-105b` chat model is what actually writes the podcast. It turns the (possibly summarized) document text into a host/guest conversation in the target language and returns the structured JSON the app parses; the same model also produces the chunk summaries for oversized documents earlier in the pipeline.

### Step 3: Voice each line

Every script line is sent to Bulbul v4 Flash, with the host and guest mapped to different speakers:
    
    
    try {
    
      const response = await fetch('https://api.sarvam.ai/text-to-speech', {
    
        method: 'POST',
    
        headers: {
    
          'Content-Type': 'application/json',
    
          'Accept': 'application/json',
    
          'api-subscription-key': apiKey,
    
        },
    
        body: JSON.stringify({
    
          text,
    
          language_code: language,
    
          speaker: selectedVoice,
    
          pace: 1.0,
    
          temperature: 0.6,
    
          speech_sample_rate: 22050,
    
          model: 'bulbul:v4-flash',
    
        }),
    
      });
    
      if (!response.ok) {
    
        throw new Error(`TTS API error: ${response.status} - ${await response.text()}`);
    
      }
    
      const data = await response.json();
    
      if (!data.audios?.[0]) {
    
        throw new Error('No audio data received from TTS API');
    
      }
    
      return data.audios[0];
    
    } catch (error) {
    
      console.error('Error calling TTS API:', error);
    
      throw error;
    
    }

Like the chat call above, this is wrapped in a helper (`textToSpeech`) that also retries on `429`s with backoff. The app maps `host` to the `priya` voice and `guest` to `shubh` for every supported language, so the two speakers stay distinguishable throughout the episode. See [Available Options](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator#available-options) below for the full voice list if you want to customize this.

Sarvam’s role: Every audio segment is synthesized by Sarvam’s Bulbul v4 Flash text-to-speech model. Sarvam handles the actual voice generation for each line, host and guest included, this step is what turns the written script into the podcast’s audio.

### Step 4: Orchestrate with Inngest

The three steps above run inside one Inngest function (`generatePodcastFunction`), with each unit of work wrapped in `step.run(...)` so Inngest can retry it independently on failure without redoing the rest of the pipeline:
    
    
    for (let i = 0; i < script.length; i++) {
    
      const segment = script[i];
    
      const audioResult = await step.run(`generate-audio-segment-${i + 1}`, async () => {
    
        try {
    
          const audioBase64 = await textToSpeech(segment.text, targetLanguage, segment.speaker);
    
          // Upload the generated audio and get back a short-lived URL
    
          const { url: uploadThingUrl } = await uploadBase64Audio(audioBase64);
    
          return {
    
            speaker: segment.speaker,
    
            text: segment.text,
    
            audioUrl: uploadThingUrl,
    
            success: true,
    
          };
    
        } catch (error) {
    
          console.error(`Error generating audio for segment ${i + 1}:`, error);
    
          // Don't rethrow: mark this segment as failed so the whole job doesn't fail.
    
          // Inngest still retries the step on its own for transient/network errors.
    
          return {
    
            speaker: segment.speaker,
    
            text: segment.text,
    
            audioUrl: '',
    
            success: false,
    
          };
    
        }
    
      });
    
      audioGenerationResults.push(audioResult);
    
      // A durable sleep between calls, resumable, unlike a plain setTimeout
    
      if (i < script.length - 1) {
    
        await step.sleep(`wait-after-segment-${i + 1}`, '1.2s');
    
      }
    
    }

`step.sleep` and per-segment `step.run` calls are what make the pipeline resilient: if the process restarts mid-podcast, Inngest resumes from the last completed step instead of starting over. The inner `try/catch` deliberately swallows a single segment’s failure instead of rethrowing it, marking that segment `success: false` so the episode still assembles with a few dropped lines rather than failing the whole job. (After the loop, the function does still throw if literally zero segments came back.)

## **Available Options**

### Supported Languages

Language| Code  
---|---  
English (India)| `en-IN`  
Hindi| `hi-IN`  
Tamil| `ta-IN`  
Telugu| `te-IN`  
Bengali| `bn-IN`  
Gujarati| `gu-IN`  
Marathi| `mr-IN`  
Malayalam| `ml-IN`  
Kannada| `kn-IN`  
Punjabi| `pa-IN`  
Odia| `od-IN`  
  
### Default Voices (Bulbul v4 Flash)

Role| Voice  
---|---  
Host| `priya`  
Guest| `shubh`  
  
Bulbul v4 Flash supports a much larger set of speakers. See [Text-to-Speech](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview) for the full list if you want each language to use a different voice pair instead of the same one across all 11.

## **Customization**

### Use different voices per language

`VOICE_MAPPINGS` in `inngest/podcast-generation.ts` maps every language to the same `{ host: 'priya', guest: 'shubh' }` pair. Give a language its own entry to use a different voice for it:
    
    
    const VOICE_MAPPINGS: { [key: string]: { host: string; guest: string } } = {
    
      'hi-IN': { host: 'priya', guest: 'shubh' },
    
      'ta-IN': { host: 'ishita', guest: 'karun' },
    
      // ...
    
    };

### Change how long the podcast is

The script-generation prompt in `generatePodcastScript` asks for an “8-10 minute” conversation with “10-15 dialog exchanges.” Adjust that wording, and the `script.length < 10` padding logic just below it, to target a shorter or longer episode.

### Move off the in-memory stubs

Before deploying beyond local testing, replace the in-memory `Map` in `lib/job-store.ts` with a real Redis client, and the base64 stub in `lib/upload-audio.ts` / `lib/uploadthing.ts` with a real UploadThing client. Both files are already structured around `REDIS_URL` and `UPLOADTHING_TOKEN`, they’re just not wired up to real clients in the version shipped in the repo.

## **Tips & Best Practices**

  * **Document length** : Very large PDFs can push the extracted text past what fits in a single script-generation prompt. The app automatically chunks and summarizes in that case, but extremely long documents may still lose detail in the process, consider trimming to the most relevant sections first.
  * **Rate limiting** : TTS and chat completion calls are spaced out with durable `step.sleep` calls (1.2s between TTS calls, 1.5s between chunk summaries) to stay under rate limits. If you see `429` errors anyway, increase these delays.
  * **API key security** : Load `SARVAM_API_KEY` from an environment variable rather than hardcoding it, especially outside local experimentation.
  * **Production storage** : Don’t ship the in-memory job store or base64 audio stub to production, see [Move off the in-memory stubs](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator#move-off-the-in-memory-stubs) above.



## **Error Handling**

You may encounter these errors while using the underlying APIs:

  * **403 Forbidden** (`invalid_api_key_error`), invalid API key. Use a valid key from the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/).
  * **429 Too Many Requests** (`insufficient_quota_error` / `rate_limit_exceeded_error`), credits exhausted or rate limit hit. The app already retries both chat completion and TTS calls with exponential backoff; if it still fails, slow down the pipeline further.
  * **400 Bad Request** (`invalid_request_error`), the uploaded PDF exceeds Document Digitization’s page limit for a single job.
  * **500 Internal Server Error** (`internal_server_error`), issue on our servers. Try again later; contact support if persistent.



For the full error-code table and SDK exception reference, see [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting).

## **Additional Resources**

  * **Documentation** : [docs.sarvam.ai](https://docs.sarvam.ai/)
  * **Related APIs** : [Document Digitization](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview) · [Chat Completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview) · [Text-to-Speech](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)
  * **Full source** : [sarvam-podcast-generator on GitHub](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/examples/sarvam-podcast-generator)
  * **Community** : [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



## **Final Notes**

  * Keep your API key secure, prefer environment variables over hardcoding.
  * The in-memory job store and audio stub are fine for trying the app locally, but need to be swapped for Redis and UploadThing before deploying.
  * The pipeline’s chunking, retries, and durable sleeps mean it degrades gracefully rather than failing outright on large documents or transient rate limits.



**Keep Building!** 🚀

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)[WhatsApp BotNext](https://docs.sarvam.ai/api/cookbook/guides/whats-app-bot)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Call Analytics Pipeline](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)
      * [Live Video Transcription](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)
      * [Podcast Generator](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator)
      * [WhatsApp Bot](https://docs.sarvam.ai/api/cookbook/guides/whats-app-bot)
      * [Example Projects on GitHub](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/examples "Example Projects on GitHub")

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


