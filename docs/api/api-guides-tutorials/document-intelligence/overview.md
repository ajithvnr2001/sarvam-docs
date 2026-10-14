---
url: https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview/
title: Document Intelligence Overview | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:16.382039+00:00
---

# Document Intelligence Overview | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview/

Skip to navigation

On this page

  * Two ways to process a document
  * What’s new
  * Key Features
  * Supported Languages
  * Supported Input Formats
  * Output Formats
  * Digitise
  * Extract
  * Quick Start: Digitise
  * Quick Start: Extract
  * Schema rules
  * Job Lifecycle
  * Job States
  * Status Response
  * Error Handling
  * Error Codes
  * Best Practices
  * Limits
  * Next Steps



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Document Intelligence](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview)

# Document Intelligence Overview

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview.md "View this page as plain text")|More actions

This page is for Model APIs.

Sarvam’s Document AI API provides enterprise-grade document processing powered by [Sarvam Vision 1.5](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision), our state-of-the-art multimodal model.

Turn any document into structured, searchable, machine-readable data, whether you need the full page digitized or specific fields extracted.

[Sarvam Vision 1.5An upgraded Sarvam Vision, trained to do both OCR and key-value extraction. SOTA performance on global and Indic document benchmarks.](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)

## Two ways to process a document

Document AI gives you two endpoints over the same job lifecycle. Pick based on what you need out the other end.

Digitise

Full-document OCR. Extracts all text, preserves layout and reading order, and parses tables into HTML, Markdown, or JSON. Use when you want the **whole document** as clean, structured content.

Extract

Schema-based key-value extraction. You define the fields you want; Sarvam Vision 1.5 returns them as structured JSON. Use when you want **specific fields** , not the whole page.

Aspect| Digitise| Extract  
---|---|---  
**Output**|  Full text + layout (HTML, Markdown, or JSON)| Just the fields you define (JSON / CSV / XLSX)  
**You provide**|  A document| A document + a schema (or saved `config_id`)  
**Best for**|  Archival, search, RAG ingestion, reading-order-faithful conversion| KYC, invoices, forms, structured data capture  
**Endpoint**| `POST /doc-ai/v1/job/digitise`| `POST /doc-ai/v1/job/extract`  
  
## What’s new

**Document AI supersedes the earlier Document Digitization API.** Two changes matter most:

  1. Processing is now powered by an **upgraded Sarvam Vision 1.5** , trained to do both OCR and key-value extraction.
  2. Alongside full-document **Digitise** (OCR), we now offer **Extract** for schema-based field extraction.



The API namespace is `doc_ai`, and jobs are created with a single `digitise()` or `extract()` call.

## Key Features

23 Language Support

Native support for all Constitutionally recognized Indian languages and English with script-native accuracy.

Digitise + Extract

Full-document digitization and targeted key-value extraction from one API and one job model.

Table Extraction

Intelligent table detection and conversion to structured HTML, Markdown, or JSON.

Schema-Based Fields

Define exactly the fields you want in Extract, returned as structured data.

Layout Preservation

Intelligent reading-order detection and complex layout handling.

Enterprise-Ready

Scalable API with job management, progress tracking, and error handling.

## Supported Languages

Document AI supports all 22 Constitutionally recognized Indian languages plus English:

Language| Code  
---|---  
Hindi| `hi-IN`  
Bengali| `bn-IN`  
Tamil| `ta-IN`  
Telugu| `te-IN`  
Marathi| `mr-IN`  
Gujarati| `gu-IN`  
Kannada| `kn-IN`  
Malayalam| `ml-IN`  
Odia| `od-IN`  
Punjabi| `pa-IN`  
Assamese| `as-IN`  
Bodo| `brx-IN`  
Dogri| `doi-IN`  
Kashmiri| `ks-IN`  
Konkani| `kok-IN`  
Maithili| `mai-IN`  
Manipuri| `mni-IN`  
Nepali| `ne-IN`  
Sanskrit| `sa-IN`  
Santali| `sat-IN`  
Sindhi| `sd-IN`  
Urdu| `ur-IN`  
English| `en-IN`  
  
## Supported Input Formats

Format| Extension| Description  
---|---|---  
PDF| `.pdf`| Multi-page PDF documents (max 10 pages)  
PNG| `.png`| Document page images  
JPEG| `.jpg`, `.jpeg`| Document page images  
ZIP| `.zip`| Flat archive of document page images (JPG or PNG, max 10 images)  
  
**Page Limit:** Both PDF and ZIP uploads are limited to a maximum of **10 pages**. Exceeding this limit returns a `400 Bad Request` with code `invalid_request_error`. Split larger documents into batches of 10 pages or fewer before uploading.

For ZIP files, include only JPG and PNG document pages in a flat structure (no nested folders). The API processes all pages in the archive and maintains page order based on filename.

## Output Formats

### Digitise

The `output_format` parameter controls the primary content format. Choose `html` (the default), `md` (Markdown), or `json`.

Format| `output_format` value| Description  
---|---|---  
HTML| `html`| Rich HTML output for web rendering (default)  
Markdown| `md`| Human-readable Markdown output  
JSON| `json`| Structured JSON with blocks containing text, tag, and bounding box  
  
The download is a ZIP archive holding the primary file, a `metadata/page_NNN.json` per page, and a `manifest.json`.

### Extract

Format| `output_format` value| Description  
---|---|---  
JSON| `json`| Structured field values (default)  
CSV| `csv`| Flat tabular output, one row per document  
XLSX| `xlsx`| Spreadsheet output  
  
## Quick Start: Digitise

**API parameter names:** Document AI uses `language` and `output_format` values `"md"`, `"html"`, or `"json"`. Do not use `language_code` (it’s ignored) or `"markdown"` (it returns `400`; use `"md"` instead). This differs from STT, translate, and LID endpoints.

PythonJavaScriptcURL
    
    
    import os, time
    
    from sarvamai import SarvamAI
    
    from sarvamai.core.api_error import ApiError
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    try:
    
        # Create and submit a digitise job in one call
    
        with open("./sample-document.pdf", "rb") as f:
    
            job = client.doc_ai.digitise(
    
                file=[("sample-document.pdf", f, "application/pdf")],
    
                language="en-IN",
    
                output_format="md",
    
            )
    
        print("job created:", job.job_id, "| status:", job.status)
    
        # Poll until the job reaches a terminal state
    
        TERMINAL = {"completed", "partially_completed", "failed", "rejected"}
    
        while True:
    
            st = client.doc_ai.get_status(job_id=job.job_id)
    
            print(f"status={st.status} pages={st.usage.pages_processed}/{st.usage.pages_total}")
    
            if st.status.lower() in TERMINAL:
    
                break
    
            time.sleep(5)
    
        # Fetch the output
    
        if st.status.lower() in ("completed", "partially_completed"):
    
            dl = client.doc_ai.get_download_url(job_id=job.job_id)
    
            print("download:", dl.method, dl.url)
    
    except FileNotFoundError:
    
        print("Document file not found: ./sample-document.pdf")
    
    except ApiError as e:
    
        print(f"API error {e.status_code}: {e.body}")

## Quick Start: Extract

Extract takes the same document input, plus a **schema** describing the fields you want (or a saved `config_id`). The result is structured JSON with the field values you defined.

PythonJavaScriptcURL
    
    
    import json, os, time
    
    from sarvamai import SarvamAI
    
    from sarvamai.core.api_error import ApiError
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    # Define the fields you want back
    
    schema = {
    
        "type": "object",
    
        "properties": {
    
            "policy_number": {"type": "string", "description": "Insurance policy number"},
    
            "insured_name":  {"type": "string", "description": "Name of the insured person"},
    
            "sum_insured":   {"type": "number", "description": "Total sum insured, in INR"},
    
        },
    
    }
    
    try:
    
        # Create and submit an extract job in one call
    
        with open("./insurance-policy.pdf", "rb") as f:
    
            job = client.doc_ai.extract(
    
                file=[("insurance-policy.pdf", f, "application/pdf")],
    
                schema=json.dumps(schema),   # or: config_id="cfg_abc123"
    
                language="en-IN",
    
                output_format="json",
    
            )
    
        print("job created:", job.job_id, "| status:", job.status)
    
        # Poll until the job reaches a terminal state
    
        TERMINAL = {"completed", "partially_completed", "failed", "rejected"}
    
        while True:
    
            st = client.doc_ai.get_status(job_id=job.job_id)
    
            print(f"status={st.status} pages={st.usage.pages_processed}/{st.usage.pages_total}")
    
            if st.status.lower() in TERMINAL:
    
                break
    
            time.sleep(5)
    
        # Fetch the extracted fields
    
        if st.status.lower() in ("completed", "partially_completed"):
    
            results = client.doc_ai.get_results(job_id=job.job_id)
    
            print(results.result)        # {"policy_number": ..., "insured_name": ..., "sum_insured": ...}
    
    except FileNotFoundError:
    
        print("Document file not found: ./insurance-policy.pdf")
    
    except ApiError as e:
    
        print(f"API error {e.status_code}: {e.body}")

**Provide exactly one of`schema` or `config_id`.** Use an inline `schema` for ad-hoc extraction, or a saved `config_id` for a schema you’ve set up on the platform. Sending both, or neither, returns a `400`.

**Pass`schema` as a JSON string, not an object.** It’s sent as a multipart form field, so both SDKs type it as a string. Use `json.dumps(schema)` in Python and `JSON.stringify(schema)` in JavaScript. Passing a dict in Python raises `AttributeError: 'dict' object has no attribute 'read'`.

Note also that the JavaScript SDK is generated without a serialization layer, so its request parameters and response fields use the wire names (`output_format`, `job_id`, `pages_processed`), not camelCase. `file` takes an **array** , and `job_id` is a **positional** argument, `getStatus(job_id)`, not `getStatus({ job_id })`.

### Schema rules

The inline schema is a JSON object with these constraints:

  * Root must be `type: "object"` with a non-empty `properties` map.
  * Every field needs a `type` and a non-empty `description`. The description guides the model, so make it specific.
  * Supported field types: `string`, `number`, `integer`, `boolean`, `object`, `array`.
  * An optional `enum` may be supplied to constrain values.
  * Maximum nesting depth is 4.



## Job Lifecycle

Both `digitise()` and `extract()` create and submit a job in a single call, returning a `job_id` and an initial status. You then poll `get_status()` until the job reaches a terminal state, and fetch output with `get_results()` (structured data) or `get_download_url()` (output file).
    
    
    digitise() / extract()  →  poll get_status()  →  get_results() / get_download_url()

### Job States

State| Description  
---|---  
`pending`| Job created, queued for processing  
`running`| Job is being processed  
`completed`| All pages processed successfully  
`partially_completed`| Some pages succeeded, some failed  
`failed`| All pages failed or a job-level error occurred  
`rejected`| Job rejected before processing (e.g. validation or entitlement)  
  
Terminal states are `completed`, `partially_completed`, `failed`, and `rejected`.

### Status Response
    
    
    {
    
      "job_id": "019fb81e-2543-70bd-a737-b5a2d62a3bb7",
    
      "status": "completed",
    
      "pipeline": "digitise",
    
      "usage": {
    
        "pages_total": 1,
    
        "pages_processed": 1,
    
        "pages_succeeded": 1,
    
        "pages_failed": 0
    
      },
    
      "created_at": "2026-07-31T12:20:11Z",
    
      "updated_at": "2026-07-31T12:20:15Z"
    
    }

## Error Handling

###### Error Handling Code Example
    
    
    import json, os
    
    from sarvamai import SarvamAI
    
    from sarvamai.core.api_error import ApiError
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    try:
    
        with open("./insurance-policy.pdf", "rb") as f:
    
            job = client.doc_ai.extract(
    
                file=[("insurance-policy.pdf", f, "application/pdf")],
    
                schema=json.dumps({
    
                    "type": "object",
    
                    "properties": {
    
                        "policy_number": {"type": "string", "description": "Insurance policy number"},
    
                    },
    
                }),
    
                output_format="json",
    
            )
    
        # ... poll get_status() until terminal ...
    
        results = client.doc_ai.get_results(job_id=job.job_id)
    
        print(results.result)
    
    except ApiError as e:
    
        if e.status_code == 400:
    
            print(f"Bad request or invalid schema: {e.body}")
    
        elif e.status_code in (402, 403):
    
            print("Billing or entitlement error")
    
        elif e.status_code == 409:
    
            print("Results requested before the job reached a terminal state")
    
        elif e.status_code == 413:
    
            print("File too large")
    
        elif e.status_code == 429:
    
            print("Rate limit exceeded")
    
        else:
    
            print(f"Error {e.status_code}: {e.body}")
    
    except FileNotFoundError:
    
        print("Document file not found: ./insurance-policy.pdf")

### Error Codes

The full error-code table, retry guidance, and SDK exception reference live on the central [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting) page. Errors specific to this API:

HTTP Status| Description  
---|---  
`400`| Invalid request or schema (includes documents exceeding the 10-page limit)  
`402` / `403`| Billing or entitlement error  
`404`| Resource unavailable (e.g. job not found)  
`409`| Results or download requested before the job reached a terminal state  
`413`| File too large  
`422`| Invalid file format or corrupted file  
`429`| Rate or admission limit  
`503`| Billing unavailable  
  
## Best Practices

Digitise vs. Extract

Reach for Digitise when you want the whole document, and Extract when you want specific fields. Don’t post-process a full digitise just to pull three fields; define a schema and let Extract do it.

Write Specific Descriptions

In Extract, each field’s `description` guides the model. “Insurance policy number, top-right, format ABC-1234” outperforms “policy number”.

Specify Language

Digitise defaults to Indic when `language` is omitted. Set `language` to `en-IN` to process English documents, and always pass the correct code for best accuracy. Sarvam Vision supports 22 Indian languages plus English — see the [Sarvam Vision model page](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision) for the full list.

Handle Large Documents

Monitor `usage` in the status response to track progress, and handle `partially_completed` jobs gracefully.

## Limits

Limit| Value  
---|---  
Max pages per PDF| 10 (`400 invalid_request_error` if exceeded)  
Max images per ZIP| 10  
Max file size| 200 MB  
Supported input formats| PDF, PNG, JPG, ZIP  
Rate limit| Varies by plan — see [Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)  
  
## Next Steps

[Sarvam Vision 1.5Learn about the upgraded model powering Document AI.](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)[API ReferenceComplete API documentation with all parameters and options.](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview)[Try in API DashboardUpload and process documents in the API Dashboard.](https://dashboard.sarvam.ai/)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/language-detection)[Get your config_idNext](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/how-to/get-your-config-id)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview)
      * How-to

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


