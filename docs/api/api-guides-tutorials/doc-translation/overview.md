---
url: https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview/
title: Document Translation API Overview | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:15.519176+00:00
---

# Document Translation API Overview | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview/

Skip to navigation

On this page

  * What you get from one job
  * How it works
  * Quickstart
  * Page-granular vs document-granular responses
  * Response shapes at a glance
  * Shared fields (both response types)
  * Job states
  * Request parameters
  * Supported file formats
  * Supported languages
  * Response examples
  * Errors
  * Best Practices
  * Limits
  * Pricing
  * Next Steps



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Document Translation](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)

# Document Translation API Overview

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview.md "View this page as plain text")|More actions

This page is for Model APIs.

The Document Translation API takes a source document and returns it translated into one or more Indian languages, in its original file format. The layout, formatting, and structure of the source file are preserved.

Authentication: send your API key in the `api-subscription-key` header. Generate a key from [Key Management](https://dashboard.sarvam.ai/key-management) in the dashboard.

## What you get from one job

A single job translates into up to 12 target languages (out of 23 total supported) from one uploaded document. You upload once, and each target language is translated independently and exported separately.

## How it works

Document translation is asynchronous by design: you create a job, upload the file, start the pipeline, poll it, and then export each language’s result, rather than getting a translated file back from a single request. Every integration follows the same five steps:

[1](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview#create-the-job)

### Create the job

`POST /translate/document/jobs` with your source/target languages and the original filename. Returns a `job_id` and a short-lived signed `upload_url`, with status `201 Created`.

[2](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview#upload-the-document)

### Upload the document

`PUT` the file bytes to `upload_url`. This step is required; the create call only accepts metadata, not the file itself.

[3](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview#start-the-pipeline)

### Start the pipeline

`POST /translate/document/jobs/{job_id}/start`, no request body. Runs file validation, then parsing (OCR for PDFs, structural extraction for Office and web formats), then translation, one independent branch per target language. Idempotent: calling `start` again on the same job returns the current job state instead of erroring.

[4](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview#poll-progress)

### Poll progress

`GET /translate/document/jobs/{job_id}/live-status` for an overall progress percentage and per-language translation state. Poll every 10-15 seconds.

[5](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview#export-each-language)

### Export each language

`POST /translate/document/jobs/{job_id}/export?lang={code}` to enqueue an async export for one target language (defaults to the uploaded file’s format), then poll `GET /translate/document/jobs/{job_id}/export/status` until `export_state` is `Completed` and download from `download_url`.

Export is per language, not one call for the whole job. Loop over your `target_language_codes` and call `export` once for each, only after that language’s own `state` in `live-status` is `Completed`. Calling `export` before that returns `409 Conflict`.

## Quickstart

Install the SDK (`pip install sarvamai` or `npm install sarvamai`), set `SARVAM_API_KEY`, and point `document` at a local PDF or Office file. The client uses `https://api.sarvam.ai` by default, so your API key is the only configuration it needs.

Document translation does not include an SDK upload helper yet. After `create`, `PUT` the file bytes to `upload_url` with `Content-Type` and `x-ms-blob-type: BlockBlob`, then call `start`. See [Poll and Export](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/poll-and-export) for the polling and download loop.

PythonJavaScript
    
    
    import os
    
    from pathlib import Path
    
    import httpx
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    document = Path("chapter1.pdf")
    
    # 1. Create job (job_name is optional: defaults to original_filename)
    
    job = client.document_translation.create(
    
        job_name="chapter1",
    
        source_language_code="en-IN",
    
        target_language_codes=["hi-IN", "ta-IN"],
    
        original_filename=document.name,
    
    )
    
    # 2. Upload to the signed URL (required: not handled by the SDK)
    
    with document.open("rb") as f:
    
        httpx.put(
    
            job.upload_url,
    
            content=f.read(),
    
            headers={
    
                "Content-Type": "application/pdf",
    
                "x-ms-blob-type": "BlockBlob",
    
            },
    
            timeout=120.0,
    
        )
    
    # 3. Start the pipeline
    
    client.document_translation.start(job_id=job.job_id)
    
    # 4–5. Poll translation, then export: see Poll and Export guide
    
    print(job.job_id)

That job is now running. See [Poll and Export](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/poll-and-export) for the polling loop and per-language download flow.

## Page-granular vs document-granular responses

The response format depends on the uploaded file type:

  * PDFs are tracked per page.
  * Word, spreadsheets, and presentations are tracked per text segment (roughly a paragraph).



Both response formats share the same base fields. Only the progress-related fields differ.

### Response shapes at a glance

| PDF uploads (per page)| Word / Spreadsheet / Presentation uploads (per segment)  
---|---|---  
Tracking unit| Page| Segment (paragraph-sized chunk of text)  
Start response| `num_pages`| -  
Live status| `page_metrics`| `translation_metrics`  
Per-language progress| `pages_completed`, `pages_failed`| `progress`, `segments_completed`, `segments_total`  
Other metrics| `total_pages`, `pages_processed`, `pages_succeeded`, `pages_failed`| `languages_total`, `languages_completed`, `languages_failed`  
  
### Shared fields (both response types)

`job_id` `job_state` `job_name` `source_language_code` `progress` `translations[]` `created_at` `updated_at`

Optional| On failure  
---|---  
`warnings`| `error_message`  
  
## Job states

State| Description  
---|---  
`Accepted`| Job created, queued for processing  
`Running`| Job is being processed  
`Completed`| All languages translated successfully  
`PartiallyCompleted`| Some languages succeeded, some failed  
`Failed`| All languages failed or a job-level error occurred  
  
Terminal states are `Completed`, `PartiallyCompleted`, and `Failed`.

Each language in `translations[]` has its own `state` (`Pending`, `Running`, `Completed`, `Failed`), independent of the others. A language is exportable as soon as its own entry reads `Completed`, even while other languages in the same job are still `Running`. Treat `PartiallyCompleted` as a terminal state alongside `Completed`, and check each language’s own `state` before deciding what to export.

## Request parameters

Required:

Field| Description  
---|---  
`source_language_code`| BCP-47 code identifying the original document’s language  
`target_language_codes`| Array of destination languages, 1 to 12 entries per job (out of 23 total supported); one translated document is produced per language  
`original_filename`| File name with extension; validated against the supported format list  
  
Optional:

Field| Description  
---|---  
`job_name`| Human-readable job name, 1-255 characters. Defaults to `original_filename` when omitted  
`genre`| Content category: `NON_FICTION`, `ADULT_FICTION`, `CHILDREN_FICTION`, `RELIGIOUS`, `LEGAL`, or `ACADEMIC`, used to tune the translation prompt  
`use_native_numerals`| When `true`, numerals render in the target script; when `false`, uses international numerals (0-9). `null` uses the application default. See [Use Native Numerals](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/native-numerals)  
`style_guidelines`| Up to ~4000 characters of global tone, terminology, and formatting instructions  
`language_specific_guidelines`| Per-language overrides (~4000 characters each); keys must match entries in `target_language_codes`  
  
## Supported file formats

Category| Extensions  
---|---  
PDF| `.pdf`  
Word| `.doc`, `.docx`, `.odt`  
Spreadsheets| `.xls`, `.xlsx`, `.ods`  
Presentations| `.ppt`, `.pptx`, `.odp`  
Web pages| `.html`, `.xhtml`, `.mhtml`  
  
## Supported languages

23 languages: English plus 22 Indic languages.

Language| Code| Language| Code  
---|---|---|---  
Assamese| `as-IN`| Manipuri| `mni-IN`  
Bengali| `bn-IN`| Marathi| `mr-IN`  
Bodo| `brx-IN`| Nepali| `ne-IN`  
Dogri| `doi-IN`| Odia| `or-IN`  
English| `en-IN`| Punjabi| `pa-IN`  
Gujarati| `gu-IN`| Sanskrit| `sa-IN`  
Hindi| `hi-IN`| Santali| `sat-IN`  
Kannada| `kn-IN`| Sindhi| `sd-IN`  
Kashmiri| `ks-IN`| Tamil| `ta-IN`  
Konkani| `kok-IN`| Telugu| `te-IN`  
Maithili| `mai-IN`| Urdu| `ur-IN`  
Malayalam| `ml-IN`| |   
  
## Response examples

`POST /translate/document/jobs` returns `201 Created`:
    
    
    {
    
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
    
      "upload_url": "https://api.sarvam.ai/translate/document/uploads/550e8400-e29b-41d4-a716-446655440000?sig=...",
    
      "expires_in_hours": 24,
    
      "source_language_code": "en-IN",
    
      "target_language_codes": ["hi-IN", "ta-IN"]
    
    }

`GET /translate/document/jobs/{job_id}/live-status` returns:
    
    
    {
    
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
    
      "job_name": "chapter1",
    
      "job_state": "Running",
    
      "source_language_code": "en-IN",
    
      "progress": 55,
    
      "page_metrics": {
    
        "total_pages": 42,
    
        "pages_processed": 23,
    
        "pages_succeeded": 23,
    
        "pages_failed": 0
    
      },
    
      "translations": [
    
        {
    
          "target_language_code": "hi-IN",
    
          "state": "Running",
    
          "pages_completed": 12,
    
          "pages_failed": 0
    
        },
    
        {
    
          "target_language_code": "ta-IN",
    
          "state": "Pending",
    
          "pages_completed": 0,
    
          "pages_failed": 0
    
        }
    
      ],
    
      "created_at": "2026-08-04T10:00:00Z",
    
      "updated_at": "2026-08-04T10:05:00Z"
    
    }

`GET /translate/document/jobs/{job_id}/export/status` returns, once the export is `Completed`:
    
    
    {
    
      "export_id": "exp_1a2b3c4d",
    
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
    
      "target_language_code": "hi-IN",
    
      "format": "pdf",
    
      "export_state": "Completed",
    
      "download_url": "https://api.sarvam.ai/translate/document/exports/550e8400-e29b-41d4-a716-446655440000/hi-IN?sig=...",
    
      "filename": "chapter1_hi-IN.pdf",
    
      "expires_in_hours": 24,
    
      "file_size": 1048576,
    
      "created_at": "2026-08-04T10:10:00Z",
    
      "completed_at": "2026-08-04T10:12:30Z"
    
    }

## Errors

HTTP Status| Description  
---|---  
`400`| Invalid request, invalid language code, genre, filename, or export format  
`401`| Unauthorized. Send a valid `api-subscription-key`  
`402`| Payment required, insufficient credits to complete this operation  
`404`| Not found, no job exists for this `job_id`, or no export for the given `export_id` or `lang`  
`409`| Conflict, export already in progress for this language and format, or translation not yet `Completed`  
`500`| Internal server error  
`503`| Service unavailable, export enqueue failed. Please retry  
  
## Best Practices

Poll, Don't Block

Poll `live-status` every 10-15 seconds from a background worker, not an HTTP request handler. Cap total wait time and handle timeouts gracefully.

Export Per Language

Export is per language, not one call for the whole job. Loop over your `target_language_codes` and call `export` once for each, only after that language’s own `state` is `Completed`.

Check Per-Language State

Don’t gate the export loop on `job_state` alone. A job at `PartiallyCompleted` can still have individual languages ready to export. Check each language’s own `state` in `translations[]`.

Pick the Right Genre

Use `genre` to tune the translation prompt for your content type. `LEGAL` for contracts, `CHILDREN_FICTION` for children’s books, `ACADEMIC` for research papers.

## Limits

Limit| Value  
---|---  
Target languages per job| 1 to 12 (out of 23 total supported languages)  
`job_name` length| 1-255 characters when provided; defaults to `original_filename`  
`style_guidelines` / `language_specific_guidelines` length| ~4000 characters each  
Signed upload URL validity| `expires_in_hours` on the create response (24 hours)  
Signed export URL validity| `expires_in_hours` on the export response (24 hours); call `export/status` again for a fresh link  
Poll interval| Every 10-15 seconds against `live-status`  
  
## Pricing

Billed at **₹5 per 1,000 billable characters** per target language, counted after the document is parsed (not from the raw file size). Charges round up; minimum **₹1** when there is billable text. See [Pricing](https://docs.sarvam.ai/api/getting-started/pricing#document-translation) and [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits).

## Next Steps

[Poll and ExportComplete code examples for polling and exporting in Python, JavaScript, and curl.](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/poll-and-export)[Pick a GenreHow to use genre for different content types.](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/genre-and-model-tier)[Use Native NumeralsControl whether numbers appear as international digits or native script numerals.](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/native-numerals)[API ReferenceEndpoint-level schemas for every request and response field.](https://docs.sarvam.ai/api-reference/translate-document/create-doc-translation)

Need help scoping a document translation integration? Reach out on [Discord](https://discord.com/invite/5rAsykttcs).

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/how-to/get-your-config-id)[How to set style guidelinesNext](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/style-guidelines)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)
      * How-to

      * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/faq)
      * [Use Cases](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/use-cases)
      * [Translate a PDF](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/guides/translate-a-pdf)

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


