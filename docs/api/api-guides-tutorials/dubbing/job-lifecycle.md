---
url: https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle/
title: Job Lifecycle | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:17.581305+00:00
---

# Job Lifecycle | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle/

Skip to navigation

On this page

  * Job statuses
  * How a job moves
  * Reading live-status
  * Reading export-status
  * A complete run
  * Troubleshooting
  * Related



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Dubbing](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)

# Job Lifecycle

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle.md "View this page as plain text")|More actions

This page is for Model APIs.

Dubbing runs asynchronously: you start a job, then follow it until the files are ready to download. This page covers every state a job passes through and the two status endpoints you read along the way.

If you just want the five calls in order, start with the [Dubbing Overview](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview).

## Job statuses

Status| Meaning| Terminal  
---|---|---  
`not_started`| Created, but `start` has not been called. This is the status immediately after `create()`.| No  
`queued`| `start` accepted; waiting for a worker.| No  
`in_progress`| The job is being processed.| No  
`completed`| Every target language finished processing.| Yes  
`partial_failure`| Some target languages succeeded, others failed. **Real outputs exist** for the ones that worked.| Yes  
`failed`| The job could not be completed. Read `error_message`.| Yes  
`deleted`| The job was deleted.| Yes  
  
`partial_failure` is uncommon, but treat it as terminal alongside `completed`. It carries real output for the languages that succeeded, so code that waits only for `completed` will poll until its own timeout and leave those files uncollected.

## How a job moves

[1](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#create--not_started)

### create() → not_started

The job row exists and you hold a `job_id` plus a signed `upload_url`. Nothing is processing yet.

[2](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#start--queued)

### start() → queued

Starting is idempotent in practice: calling it on a job that is already `queued`, `in_progress`, or `completed` returns without re-queueing.

[3](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#processing--in_progress)

### Processing → in_progress

The job flips to `in_progress` once processing begins, and stays there for the bulk of the run.

[4](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#finished--completed-partial_failure-or-failed)

### Finished → completed, partial_failure, or failed

Exports are then triggered automatically for the formats in `export_options`.

`completed` means the dub itself finished. The exported files may still be rendering, and `progress` can sit just short of 100 while they do, so confirm in `export-status` before downloading.

## Reading `live-status`

Alongside `status`, this endpoint reports a `progress` percentage and a human-readable `current_step_label` you can surface directly in a UI.
    
    
    {
    
      "data": {
    
        "job_id": "3f9a...",
    
        "job_name": "keynote.mp4",
    
        "status": "in_progress",
    
        "current_step": "translate",
    
        "current_step_label": "Translating",
    
        "progress": 50,
    
        "export": null,
    
        "exports": null,
    
        "error_message": null
    
      }
    
    }

**`export` and `exports` swap depending on language count.** A job with one target language populates `export` (an object) and leaves `exports` `null`; a job with two or more does the reverse. An integration written against a single-language job therefore reads `null` the first time someone asks for two, so handle both keys.

Both are `null` until the job reaches `completed`. Note also that this block only ever carries a `dubbed_video_url`, there are no audio or SRT links here, which is why `export-status` is the endpoint to use for downloads.

## Reading `export-status`

`export-status` is the authoritative source for downloads. It returns a **flat array with one entry per (language, format)** , so a two-language, three-format job returns six entries in a single poll.
    
    
    {
    
      "data": {
    
        "exports": [
    
          { "id": "a1...", "target_language": "hi-IN", "export_type": "video", "status": "completed", "is_stale": false, "created_at": "...", "completed_at": "...", "download_url": "https://..." },
    
          { "id": "b2...", "target_language": "hi-IN", "export_type": "srt", "status": "completed", "is_stale": false, "created_at": "...", "completed_at": "...", "download_url": "https://..." },
    
          { "id": "c3...", "target_language": "ta-IN", "export_type": "video", "status": "in_progress", "is_stale": false, "created_at": "...", "completed_at": null }
    
        ]
    
      }
    
    }

Group by `target_language` on your side, and take only entries whose own `status` is `completed`.

`download_url` is **absent** rather than `null` until an export completes, as in the third entry above. If you are reading the raw JSON, access it defensively; the Python SDK exposes it as an optional field, so it reads as `None`.

**Set`limit` deliberately.** It defaults to `5`, so a job with 2 languages × 3 formats returns only the first five of its six entries, with no indication that more exist. Pass a value comfortably above `languages × formats` (maximum `100`).

Each entry also carries `is_stale`, which becomes `true` when translation chunks for that language were edited after the export finished, the file you would download no longer matches the latest text. Re-export before publishing. Download URLs are signed and expire in roughly 24 hours, so persist the `job_id` and re-poll for a fresh link rather than caching the URL.

## A complete run

Here is one job carried from an empty script to downloaded files, a block at a time. Paste the blocks into a single file in order and you have a working program; each one explains what it does and why it is needed.

[1](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#install-the-sdk-and-set-your-key)

### Install the SDK and set your key
    
    
    pip install sarvamai
    
    export SARVAM_API_KEY="your-key-here"

Reading the key from an environment variable keeps it out of your source code, so you can share the script without sharing your credentials. Generate a key at [Key Management](https://dashboard.sarvam.ai/key-management).

[2](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#set-up-the-client-and-your-inputs)

### Set up the client and your inputs
    
    
    import os, time
    
    from pathlib import Path
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    media = Path("sample.mp4")
    
    target_language_codes = ["hi-IN", "ta-IN"]
    
    export_options = ["video", "srt"]

`client` is the object every call goes through. The three values below it are the only things you would normally change: the file to dub, the languages to dub it into, and the formats you want back. Naming them once here matters, because later steps reuse them to work out exactly what to wait for.

[3](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#create-the-job)

### Create the job
    
    
    created = client.dubbing.create(
    
        source_language_code="en-IN",
    
        target_language_codes=target_language_codes,
    
        export_options=export_options,
    
        voice_cloning=True,
    
        num_speakers=1,
    
        job_name=media.name,
    
    )
    
    job_id = created.data.job_id

This registers the job and reserves somewhere to put your file. Nothing is processing yet and the file has not been sent. What comes back is a `job_id`, which identifies this job in every later call, and an `upload_url`, which is a temporary link to upload the file to.

`voice_cloning=True` keeps each original speaker’s voice, and `num_speakers=1` says the source has one person talking. Both are covered in [Choose a Voice](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice).

[4](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#upload-the-media-then-start-the-job)

### Upload the media, then start the job
    
    
    client.dubbing.upload(created.data.upload_url, media)
    
    client.dubbing.start(job_id=job_id)

Uploading sends the file straight to storage rather than through the API, which is why it is a separate call from `create`. Starting then tells the service the file is in place and work can begin.

Order matters: starting before the file is uploaded leaves the job sitting at `queued` with nothing to process.

[5](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#wait-for-the-dub-to-finish)

### Wait for the dub to finish
    
    
    TERMINAL = {"completed", "partial_failure", "failed", "deleted"}
    
    deadline = time.monotonic() + 3600
    
    while True:
    
        job = client.dubbing.get_live_status(job_id=job_id).data
    
        print(f"{job.progress:>3}%  {job.current_step_label}")
    
        if job.status in TERMINAL:
    
            break
    
        if time.monotonic() > deadline:
    
            raise TimeoutError(f"{job_id} did not finish in time")
    
        time.sleep(15)

Dubbing takes minutes rather than seconds, so instead of waiting on one long request you ask for the status every 15 seconds until the job stops changing.

The loop exits on any status in `TERMINAL`, not just `completed`. That matters for `partial_failure`, which means some languages finished and others did not, there are still real files to collect, so it counts as done. The `deadline` is a safety net so the loop cannot run forever.

[6](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#stop-if-the-job-failed-outright)

### Stop if the job failed outright
    
    
    if job.status == "failed":
    
        raise RuntimeError(job.error_message or "job failed")

`failed` is the only terminal status with nothing to collect. Everything else, `partial_failure` included, has output worth fetching, so the script continues.

[7](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#wait-for-the-exported-files)

### Wait for the exported files
    
    
    wanted = {(lang, fmt) for lang in target_language_codes for fmt in export_options}
    
    deadline = time.monotonic() + 3600
    
    while True:
    
        exports = client.dubbing.get_export_status(job_id=job_id, limit=100).data.exports or []
    
        settled = {
    
            (e.target_language, e.export_type)
    
            for e in exports
    
            if e.status in {"completed", "failed"}
    
        }
    
        if wanted <= settled:
    
            break
    
        if time.monotonic() > deadline:
    
            raise TimeoutError(f"{job_id} exports did not settle in time")
    
        time.sleep(15)

A finished job does not yet mean finished files, because each output is rendered after the dub itself completes. This is a second wait, for the files rather than the dub.

`wanted` is every combination you asked for: two languages times two formats is four files. The loop keeps polling until each of those has settled, meaning it either completed or failed, so one slow file cannot make you miss the others. `limit=100` is deliberate, the default of `5` would not return every entry.

[8](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle#collect-the-download-links)

### Collect the download links
    
    
    downloads = {
    
        (e.target_language, e.export_type): e.download_url
    
        for e in exports
    
        if e.status == "completed" and not e.is_stale
    
    }
    
    for (lang, fmt), url in sorted(downloads.items()):
    
        print(f"{lang} {fmt}: {url}")

This keeps only the files that actually completed, and skips any marked `is_stale`, which means the translation was edited after that file was made. The links are signed and valid for roughly 24 hours, so download them now or re-poll `export-status` later for fresh ones.

`client.dubbing.upload()` requires `sarvamai` 0.1.31a1 or newer.

Poll from a background worker rather than an HTTP request handler, and always cap total wait time as above. The API does not mandate an interval; the 15 seconds here is a starting point to tune against your own file lengths, not a recommended setting.

You do not need to add retry logic for server errors. The SDK already retries `429`, `408`, `409`, and `5xx` responses with exponential backoff, honouring `Retry-After`, twice by default. Raise it per call with `request_options={"max_retries": 5}`. A dropped connection is not retried, so wrap the calls in your own `try` / `except httpx.TransportError` if the script runs unattended.

###### The whole script in one piece
    
    
    import os, time
    
    from pathlib import Path
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    media = Path("sample.mp4")
    
    target_language_codes = ["hi-IN", "ta-IN"]
    
    export_options = ["video", "srt"]
    
    created = client.dubbing.create(
    
        source_language_code="en-IN",
    
        target_language_codes=target_language_codes,
    
        export_options=export_options,
    
        voice_cloning=True,
    
        num_speakers=1,
    
        job_name=media.name,
    
    )
    
    job_id = created.data.job_id
    
    client.dubbing.upload(created.data.upload_url, media)
    
    client.dubbing.start(job_id=job_id)
    
    TERMINAL = {"completed", "partial_failure", "failed", "deleted"}
    
    deadline = time.monotonic() + 3600
    
    while True:
    
        job = client.dubbing.get_live_status(job_id=job_id).data
    
        print(f"{job.progress:>3}%  {job.current_step_label}")
    
        if job.status in TERMINAL:
    
            break
    
        if time.monotonic() > deadline:
    
            raise TimeoutError(f"{job_id} did not finish in time")
    
        time.sleep(15)
    
    if job.status == "failed":
    
        raise RuntimeError(job.error_message or "job failed")
    
    # partial_failure still has usable outputs, so keep going either way.
    
    wanted = {(lang, fmt) for lang in target_language_codes for fmt in export_options}
    
    deadline = time.monotonic() + 3600
    
    while True:
    
        exports = client.dubbing.get_export_status(job_id=job_id, limit=100).data.exports or []
    
        settled = {
    
            (e.target_language, e.export_type)
    
            for e in exports
    
            if e.status in {"completed", "failed"}
    
        }
    
        if wanted <= settled:
    
            break
    
        if time.monotonic() > deadline:
    
            raise TimeoutError(f"{job_id} exports did not settle in time")
    
        time.sleep(15)
    
    downloads = {
    
        (e.target_language, e.export_type): e.download_url
    
        for e in exports
    
        if e.status == "completed" and not e.is_stale
    
    }
    
    for (lang, fmt), url in sorted(downloads.items()):
    
        print(f"{lang} {fmt}: {url}")

## Troubleshooting

Almost everything below is a configuration detail rather than a dub that went wrong: a call that was never made, a URL that has aged out, or a parameter the API rejected up front.

Symptom| Cause| Fix  
---|---|---  
Stuck in `not_started`| `start` was never called.| Call `start` after uploading.  
Stuck in `queued`| The media was never uploaded, so there is nothing to process.| Upload to `upload_url`, then start.  
`403` on upload| The signed URL expired, or the request is missing `x-ms-blob-type: BlockBlob`.| Check `expires_in_hours` and upload promptly; create a new job for a fresh URL. Never send your API key to the storage URL.  
`422` on create| An invalid language code (Odia is `or-IN`, not `od-IN`), the source language repeated in `target_langs`, an unknown `voice_id`, or `voice_cloning: false` without a `voice_id`.| See [Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/specify-language-codes) and [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice).  
`export-status` empty on a `completed` job| `editor_flow: true` suppresses auto-export, leaving exports for a human to trigger in Creator Studio. It also bills at the **editor-flow rate (₹80/min on Starter, double the default API rate)**.| Keep `editor_flow` at its default of `false` for API integrations. See [Pricing](https://docs.sarvam.ai/api/getting-started/pricing#dubbing).  
Fewer exports than expected| `limit` defaults to `5`.| Pass an explicit `limit` above `languages × formats`.  
  
Log the `job_id` on every call. It is how a dub is traced end to end, and it is the first thing to include in a support request.

## Related

[Dubbing OverviewThe five calls that make up an integration.](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)[Choose Export FormatsDecide which formats each language produces.](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)[How to specify language codesNext](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/specify-language-codes)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)
      * [Job Lifecycle](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle)
      * How-to

      * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/faq)

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


