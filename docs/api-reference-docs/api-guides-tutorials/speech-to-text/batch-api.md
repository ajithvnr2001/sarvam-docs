---
url: https://docs.sarvam.ai/api-reference-docs/api-guides-tutorials/speech-to-text/batch-api/
title: Batch Speech-to-Text API | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:42.110356+00:00
---

# Batch Speech-to-Text API | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference-docs/api-guides-tutorials/speech-to-text/batch-api/

Skip to navigation

On this page

  * Supported Modes (Saaras v3 and v4)
  * Features
  * Input audio codec (batch)
  * Code Examples
  * Choosing a Mode
  * REST download note
  * Full Example
  * Speaker Diarization
  * Capabilities
  * Output Format
  * Polling Defaults
  * Webhook Support
  * Setting Up Webhooks
  * Webhook Payload
  * Webhook Server Example
  * Next Steps



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Speech to Text](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)

# Batch Speech-to-Text API

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api.md "View this page as plain text")|More actions

This page is for Model APIs.

Process long audio files (up to 2 hours) using synchronous or asynchronous methods. Ideal for meetings, interviews, call center recordings, and large-scale content processing pipelines.

  * Supports files up to 2 hours long
  * Advanced transcription and translation
  * Speaker diarization and timestamp support



**Note:** You can upload up to `20` audio files per job.

**Model Availability:** The Batch API supports **Saaras v4** (default, recommended, latest) and **Saaras v3** , both with multiple output modes via the `mode` parameter.

Using `saaras:v4`? Pass a `keyterms` list inside `job_parameters` to bias recognition toward specific names, places, brands, or technical terms. See [Keyterm Prompting](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/keyterms).

### Supported Modes (Saaras v3 and v4)

Mode| Description| Output  
---|---|---  
`transcribe`| Standard transcription in the original language| Text in source language  
`translate`| Transcribe and translate to English| English text  
`verbatim`| Word-for-word transcription including filler words and repetitions| Verbatim text in source language  
`translit`| Transcribe and transliterate to Roman script| Romanized text  
`codemix`| Transcribe code-mixed speech (e.g., Hindi-English) naturally| Code-mixed text  
  
## Features

Processing

  * Supports up to 2 hours audio
  * Synchronous and asynchronous job-based API
  * Upload multiple files per job



Audio & Language Support

  * Indian languages and English
  * Automatic language detection
  * Diarization and timestamp support



Timestamps

  * **Chunk-level** timestamps only (not word-level)
  * Each chunk covers a sentence or phrase segment
  * Provides start and end times for each chunk of text
  * Useful for subtitle alignment and audio navigation



Speaker Diarization

  * Identify multiple speakers
  * Output includes speaker labels (SPEAKER_00, etc.)
  * Ideal for meetings and interviews



**Word-level timestamps are not supported.** The Batch API returns **chunk-level** timestamps only. Each timestamp entry covers a sentence or phrase, not an individual word. If your use case requires per-word timing, this is not currently available.

## Input audio codec (batch)

When you call **init job** (`POST /speech-to-text/job/v1`), set `input_audio_codec` inside `job_parameters` when needed. Behavior matches the REST upload APIs: most formats are auto-detected; for **raw PCM** (`pcm_s16le`, `pcm_l16`, `pcm_raw`) you **must** set this field. PCM must be **16 kHz** sample rate. See [supported formats and MIME types](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview) for the full list.

Use the same field on **speech-to-text translate** bulk jobs when translate job parameters include `input_audio_codec`.

PythonJavaScript
    
    
    # input_audio_codec is set via the low-level init-job API
    
    job = client.speech_to_text_job.initialise(
    
        job_parameters={
    
            "model": "saaras:v4",
    
            "mode": "transcribe",
    
            "language_code": "hi-IN",
    
            "input_audio_codec": "pcm_s16le",  # required for raw PCM uploads in the batch
    
        },
    
    )

## Code Examples

### Choosing a Mode

To switch between modes, simply change the `mode` parameter in your job creation call. The rest of the workflow (upload, start, wait, download) remains the same.

###### Saaras v3

###### Saaras v4

Still available. All five output modes across 22 Indian languages plus Indian English.

###### Transcribe

###### Translate

###### Verbatim

###### Translit

###### Codemix

Transcribe audio in the original language.

PythonJavaScript
    
    
    job = client.speech_to_text_job.create_job(
    
        model="saaras:v3",
    
        mode="transcribe",         # Standard transcription
    
        language_code="hi-IN",
    
        with_diarization=True,
    
        num_speakers=2,
    
    )

### REST download note

If you call **Batch - Download Results** (`POST /speech-to-text/job/v1/download-files`) directly, the body must include both `job_id` and a `files` array (for example `["0.json"]`). Output filenames come from the [Batch - Get Status](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) response (`job_details[].outputs[].file_name`). The SDK `download_outputs()` method supplies these automatically.

### Full Example

Once you’ve created a job with your chosen mode, the upload, processing, and download workflow is the same for all modes:

Python (Sync)Python (Async)JavaScript
    
    
    from sarvamai import SarvamAI
    
    def main():
    
        client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
        # Create batch job: change mode as needed
    
        job = client.speech_to_text_job.create_job(
    
            model="saaras:v4",
    
            mode="transcribe",
    
            language_code="en-IN",
    
            with_diarization=True,
    
            num_speakers=2
    
        )
    
        # Upload and process files
    
        audio_paths = ["path/to/audio1.mp3", "path/to/audio2.mp3"]
    
        job.upload_files(file_paths=audio_paths)
    
        job.start()
    
        # Wait for completion
    
        job.wait_until_complete()
    
        # Check file-level results
    
        file_results = job.get_file_results()
    
        print(f"\nSuccessful: {len(file_results['successful'])}")
    
        for f in file_results['successful']:
    
            print(f"  ✓ {f['file_name']}")
    
        print(f"\nFailed: {len(file_results['failed'])}")
    
        for f in file_results['failed']:
    
            print(f"  ✗ {f['file_name']}: {f['error_message']}")
    
        # Download outputs for successful files
    
        if file_results['successful']:
    
            job.download_outputs(output_dir="./output")
    
            print(f"\nDownloaded {len(file_results['successful'])} file(s) to: ./output")
    
    if __name__ == "__main__":
    
        main()

## Speaker Diarization

Speaker diarization automatically identifies and separates different speakers in an audio recording. This feature is ideal for meetings, interviews, and multi-speaker conversations where you need to know who said what.

### Capabilities

  * Identify multiple speakers in a single audio file
  * Assign unique speaker IDs (speaker 1, speaker 2, etc.)
  * Provide timestamps for each speaker segment
  * Works with up to 20 speakers per audio file



### Output Format

When `with_diarization=True` is passed in the request, the response includes a `diarized_transcript` field with detailed speaker information:
    
    
    {
    
      "request_id": "20260130_d8d2c0e6-1eb6-4982-8045-b267d5165c44",
    
      "transcript": "Full transcript text...",
    
      "timestamps": {
    
        "chunks": ["Hello, how can I help you today?", "I have a question."],
    
        "start_time_seconds": [0.01, 2.8],
    
        "end_time_seconds": [2.5, 4.2]
    
      },
    
      "diarized_transcript": {
    
        "entries": [
    
          {
    
            "transcript": "Hello, how can I help you today?",
    
            "start_time_seconds": 0.01,
    
            "end_time_seconds": 2.5,
    
            "speaker_id": "0"
    
          },
    
          {
    
            "transcript": "I have a question.",
    
            "start_time_seconds": 2.8,
    
            "end_time_seconds": 4.2,
    
            "speaker_id": "1"
    
          }
    
        ]
    
      },
    
      "language_code": "en-IN"
    
    }

Each entry contains:

  * `transcript`: The text spoken by the speaker
  * `start_time_seconds`: When the speaker started speaking (float)
  * `end_time_seconds`: When the speaker stopped speaking (float)
  * `speaker_id`: Unique identifier for the speaker (e.g., “0”, “1”)



The SarvamAI SDK supports both synchronous and asynchronous programming in Python. This refers to how your code interacts with the SDK, not how the server handles the processing of requests.

## Polling Defaults

`job.wait_until_complete()` polls `GET /speech-to-text/job/v1/{job_id}/status` in a loop until the job reaches a terminal state:
    
    
    def wait_until_complete(self, poll_interval: int = 5, timeout: int = 600) -> JobStatusResponse

Parameter| Default| Meaning  
---|---|---  
`poll_interval`| **5 seconds**|  Time between status checks  
`timeout`| **600 seconds** (10 minutes)| Raises `TimeoutError` if the job hasn’t reached `Completed`/`Failed` by then  
  
Both are overridable, for example `job.wait_until_complete(poll_interval=10, timeout=1800)`, if your files are large enough that 10 minutes isn’t enough headroom.

The legacy `document_intelligence` API’s `wait_until_complete()` uses different defaults (2-second poll interval, no timeout by default). Its successor, [Document AI](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview), has no such helper. You poll `get_status()` yourself.

## Webhook Support

For long-running batch jobs, you can use webhooks to receive notifications when jobs complete instead of polling for status updates.

### Setting Up Webhooks

When creating a job, include a `callback` parameter with your webhook URL and authentication token:

Python (Async)Python (Sync)
    
    
    from sarvamai import AsyncSarvamAI, BulkJobCallbackParams
    
    client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    job = await client.speech_to_text_job.create_job(
    
        model="saaras:v4",
    
        mode="transcribe",
    
        with_diarization=True,
    
        callback=BulkJobCallbackParams(
    
            url="https://your-server.com/webhook-endpoint",
    
            auth_token="your-secret-token"
    
        )
    
    )

### Webhook Payload

When a job finishes (or fails), Sarvam AI sends a **POST** to your callback URL. The body matches the same `JobStatusResponse` schema returned by [`GET /speech-to-text/job/v1/{job_id}/status`](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/status). It is a **status notification** , not the transcript text itself.

Sarvam includes your `auth_token` in the **`X-SARVAM-JOB-CALLBACK-TOKEN`** request header (validate this on every request).
    
    
    {
    
      "job_id": "job_12345",
    
      "job_state": "Completed",
    
      "created_at": "2026-05-27T10:30:00Z",
    
      "updated_at": "2026-05-27T10:35:12Z",
    
      "total_files": 2,
    
      "successful_files_count": 2,
    
      "failed_files_count": 0,
    
      "storage_container_type": "Azure",
    
      "error_message": "",
    
      "job_details": [
    
        {
    
          "inputs": [{ "file_name": "meeting.mp3", "file_id": "input-0" }],
    
          "outputs": [{ "file_name": "0.json", "file_id": "output-0" }],
    
          "state": "Success",
    
          "error_message": null,
    
          "exception_name": null
    
        }
    
      ]
    
    }

Field| Meaning  
---|---  
`job_state`| One of `Accepted`, `Pending`, `Running`, `Completed`, or `Failed` (title case)  
`job_details`| Per-file status: input/output file names, processing `state`, and errors  
`successful_files_count` / `failed_files_count`| How many files succeeded vs failed  
  
**Transcripts are not in the webhook.** Each successful file’s transcript lives in a **downloaded JSON** (for example `0.json` listed under `job_details[].outputs`). After `job_state` is `Completed`, call [`POST /speech-to-text/job/v1/download-files`](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/download) (or use `job.download_outputs()` in the SDK) and parse those files. See [Speaker Diarization → Output Format](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#speaker-diarization) for the JSON shape (`transcript`, `language_code`, optional `diarized_transcript`, etc.).

### Webhook Server Example

Here’s a simple FastAPI server to handle webhook callbacks:
    
    
    from fastapi import FastAPI, Request, HTTPException
    
    import uvicorn
    
    app = FastAPI()
    
    VALID_TOKEN = "your-secret-token"
    
    @app.post("/webhook-endpoint")
    
    async def handle_webhook(request: Request):
    
        # Validate authentication
    
        token = request.headers.get("X-SARVAM-JOB-CALLBACK-TOKEN")
    
        if token != VALID_TOKEN:
    
            raise HTTPException(status_code=403, detail="Invalid token")
    
        
    
        # Process the webhook data
    
        data = await request.json()
    
        job_id = data.get("job_id")
    
        job_state = data.get("job_state")
    
        
    
        if job_state == "Completed":
    
            print(f"Job {job_id} completed successfully!")
    
            # Fetch transcripts: download output JSON files (see job_details[].outputs)
    
        elif job_state == "Failed":
    
            print(f"Job {job_id} failed: {data.get('error_message')}")
    
            # Handle failure
    
        
    
        return {"status": "success"}
    
    if __name__ == "__main__":
    
        uvicorn.run(app, host="0.0.0.0", port=8000)

Your webhook server must respond with a 200 status code within 30 seconds. Make sure your webhook URL is publicly accessible and uses HTTPS in production.

## Next Steps

[1](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#choose-your-api)

### Choose Your API

Select the appropriate API type based on your use case.

[2](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#get-api-key)

### Get API Key

Sign up and get your API key from the [dashboard](https://dashboard.sarvam.ai/).

[3](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#go-live)

### Go Live

Deploy your integration and monitor usage in the dashboard.

Need help choosing the right API? Contact us on [discord](https://discord.com/invite/5rAsykttcs) for guidance.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)[Realtime Streaming Speech-to-Text APINext](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


