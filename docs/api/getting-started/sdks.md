---
url: https://docs.sarvam.ai/api/getting-started/sdks/
title: Libraries & SDKs | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:38.343518+00:00
---

# Libraries & SDKs | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/getting-started/sdks/

Skip to navigation

On this page

  * Initialize the client
  * Async usage
  * Timeouts and retries
  * Handling errors
  * Exception reference
  * Streaming support
  * Document AI (file uploads)
  * Versioning
  * Resources



Scroll to top

[Getting Started](https://docs.sarvam.ai/api/getting-started/welcome)

# Libraries & SDKs

Official Python and JavaScript clients for the Sarvam AI API: with async, retries, timeouts, streaming, and typed errors.

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/getting-started/sdks.md "View this page as plain text")|More actions

This page is for Model APIs.

The official SDKs wrap every Sarvam AI API — Speech-to-Text, Text-to-Speech, Instant Voice Cloning, Translation, Chat Completion, and Document AI — behind a typed, ergonomic client. They handle auth, serialization, multipart uploads, and error mapping so you don’t have to hand-roll HTTP calls.

Language| Package| Install  
---|---|---  
Python| [`sarvamai` on PyPI](https://pypi.org/project/sarvamai/)| `pip install sarvamai`  
JavaScript / TypeScript| [`sarvamai` on npm](https://www.npmjs.com/package/sarvamai)| `npm install sarvamai`  
  
**Official SDKs vs. generated request snippets.** The Python and JavaScript SDKs above are hand-tested, fully supported clients. The per-endpoint snippets you see in other languages (cURL, Go, Swift, etc.) on API Reference pages are auto-generated request examples, useful as a starting point, but only Python and JavaScript are first-class SDKs.

## Initialize the client

Pass your API key directly, or let the SDK read it from the `SARVAM_API_KEY` environment variable.

PythonJavaScript
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    response = client.text.translate(
    
        input="Hello, how are you?",
    
        source_language_code="auto",
    
        target_language_code="hi-IN",
    
    )
    
    print(response)

## Async usage

Both SDKs support fully asynchronous calls. Use them when you need concurrency (e.g. fanning out many requests, or inside an async web server or voice agent).

Python: AsyncSarvamAIJavaScript
    
    
    import asyncio
    
    from sarvamai import AsyncSarvamAI
    
    client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    async def main():
    
        # Run several translations concurrently
    
        inputs = ["Good morning", "How are you?", "Thank you"]
    
        results = await asyncio.gather(*[
    
            client.text.translate(
    
                input=text,
    
                source_language_code="en-IN",
    
                target_language_code="hi-IN",
    
            )
    
            for text in inputs
    
        ])
    
        for r in results:
    
            print(r)
    
    asyncio.run(main())

In JavaScript, every method is already `Promise`-based, `await` it directly. In Python, the synchronous `SarvamAI` and asynchronous `AsyncSarvamAI` expose the exact same method names and arguments, so you can switch with a one-line change.

## Timeouts and retries

Configure timeouts and automatic retries either globally (on the client) or per request. Per-request options override the client defaults.

PythonJavaScript
    
    
    from sarvamai import SarvamAI
    
    # Client-level: applies to every request
    
    client = SarvamAI(
    
        api_subscription_key="YOUR_SARVAM_API_KEY",
    
        timeout=30.0,  # seconds
    
    )
    
    # Per-request: override timeout and set automatic retries
    
    response = client.text.translate(
    
        input="Hello, how are you?",
    
        source_language_code="auto",
    
        target_language_code="hi-IN",
    
        request_options={
    
            "timeout_in_seconds": 60,
    
            "max_retries": 3,
    
        },
    
    )

Retries use exponential backoff and apply to transient failures (HTTP `429`, `5xx`, and connection errors). For a full retry/backoff helper and idempotency guidance, see [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting).

## Handling errors

The SDKs raise typed exceptions mapped to HTTP status codes, so you can catch exactly the failure you care about. Catch the base class to handle everything.

PythonJavaScript
    
    
    from sarvamai import SarvamAI, TooManyRequestsError
    
    from sarvamai.core.api_error import ApiError
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    try:
    
        response = client.text.translate(
    
            input="Hello, how are you?",
    
            source_language_code="auto",
    
            target_language_code="hi-IN",
    
        )
    
    except TooManyRequestsError:
    
        print("Rate limited, back off and retry")
    
    except ApiError as e:
    
        # Base class for every API error
    
        print(f"API error {e.status_code}: {e.body}")

### Exception reference

HTTP status| Python exception| JavaScript exception  
---|---|---  
`400` Bad request| `BadRequestError`| `SarvamAI.BadRequestError`  
`403` Forbidden / invalid key¹| `ForbiddenError`| `SarvamAI.ForbiddenError`  
`404` Not found| `NotFoundError`| `SarvamAI.NotFoundError`  
`413` Payload too large| `ContentTooLargeError`| `SarvamAI.ContentTooLargeError`  
`422` Unprocessable entity| `UnprocessableEntityError`| `SarvamAI.UnprocessableEntityError`  
`429` Rate limited / quota| `TooManyRequestsError`| `SarvamAI.TooManyRequestsError`  
`500` Server error| `InternalServerError`| `SarvamAI.InternalServerError`  
`503` Service unavailable| `ServiceUnavailableError`| `SarvamAI.ServiceUnavailableError`  
Any of the above (base)| `ApiError`| `SarvamAIError`  
Client-side timeout| `httpx.TimeoutException`| `SarvamAITimeoutError`  
  
¹ Auth failures return **HTTP 403** (`invalid_api_key_error`), not 401. See the [auth status-code note](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting).

## Streaming support

Several APIs stream results instead of returning a single response. Here’s what each SDK supports:

Capability| Method| Python| JavaScript  
---|---|---|---  
TTS over HTTP stream| `text_to_speech.convert_stream` / `textToSpeech.convertStream`| |   
TTS over WebSocket| `text_to_speech_streaming` / `textToSpeechStreaming`| |   
Instant Voice Cloning (REST)| `voice_cloning.convert` / `voiceCloning.convert`| |   
Instant Voice Cloning over HTTP stream| `voice_cloning.convert_stream` / `voiceCloning.convertStream`| |   
Instant Voice Cloning over WebSocket| `voice_cloning_streaming` / `voiceCloningStreaming`| |   
Instant Voice Cloning — voice library (REST)| `voice_cloning.create_voice` / `voiceCloning.createVoice`, plus list/get/delete| |   
STT over WebSocket| `speech_to_text_streaming` / `speechToTextStreaming`| |   
STT-translate over WebSocket _(legacy. Prefer STT WebSocket with`mode="translate"`)_| `speech_to_text_translate_streaming` / `speechToTextTranslateStreaming`| |   
  
  * **HTTP streaming** returns an iterable/`BinaryResponse` of raw audio bytes. See the [TTS HTTP Streaming guide](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream) and [Instant Voice Cloning HTTP streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/http-streaming).
  * **WebSocket streaming** uses the async clients (`AsyncSarvamAI` / `SarvamAIClient`) with an event-driven connection. See the [TTS WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket), [Instant Voice Cloning WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/websocket-streaming), and [STT WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api) guides.



## Document AI (file uploads)

Document AI is the one group that takes **file uploads** rather than JSON, so its call shape differs from the rest of the SDK. Both clients expose it as a `doc_ai` / `docAi` group, and a job is created in a single `digitise()` or `extract()` call.

Capability| Python| JavaScript  
---|---|---  
Digitise a document (full-page OCR)| `doc_ai.digitise`| `docAi.digitise`  
Extract schema-defined fields| `doc_ai.extract`| `docAi.extract`  
Poll job status| `doc_ai.get_status`| `docAi.getStatus`  
Fetch extracted fields| `doc_ai.get_results`| `docAi.getResults`  
Get a download URL for the output| `doc_ai.get_download_url`| `docAi.getDownloadUrl`  
Pre-upload a file, then reference it| `doc_ai.create_upload_url`| `docAi.createUploadUrl`  
  
PythonJavaScript
    
    
    import os, time
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    # `file` takes a list of (filename, fileobj, content_type) tuples
    
    with open("document.pdf", "rb") as f:
    
        job = client.doc_ai.digitise(
    
            file=[("document.pdf", f, "application/pdf")],
    
            language="hi-IN",
    
            output_format="md",   # "html" (default) or "md"
    
        )
    
    TERMINAL = {"completed", "partially_completed", "failed", "rejected"}
    
    while True:
    
        st = client.doc_ai.get_status(job_id=job.job_id)
    
        if st.status.lower() in TERMINAL:
    
            break
    
        time.sleep(5)
    
    dl = client.doc_ai.get_download_url(job_id=job.job_id)
    
    print("download:", dl.method, dl.url)

**Three call-shape gotchas, all specific to this group:**

  1. **`file` is a list**, even for a single document. In JavaScript a bare stream fails with `TypeError: request.file is not iterable`.
  2. **`job_id` is positional**: `getStatus(job_id)`, not `getStatus({ job_id })`. Passing an object sends `[object Object]` as the path segment and the service rejects it as a non-UUID.
  3. **`schema` is a JSON string**, not an object, because it’s sent as a multipart form field, `json.dumps(schema)` in Python, `JSON.stringify(schema)` in JavaScript.



The JavaScript SDK is generated without a serialization layer, so request parameters and response fields use wire names (`output_format`, `job_id`, `pages_processed`), not camelCase. This is unlike the rest of the SDK.

See the [Document AI overview](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview) for schema rules, output formats, and the full job lifecycle. The older `document_intelligence` group (`create_job()` / `upload_file()` / `start()` / `wait_until_complete()` / `download_output()`) is still present for existing integrations, but new work should use `doc_ai`.

## Versioning

The SDKs follow [semantic versioning](https://semver.org/). Pin a version in production and review the [API changelog](https://docs.sarvam.ai/changelog) before upgrading across a major version. Always develop against the latest release:

PythonJavaScript
    
    
    pip install --upgrade sarvamai

## Resources

Resource| Link  
---|---  
Example notebooks & agents| [GitHub cookbook](https://github.com/sarvamai/sarvam-ai-cookbook)  
Errors, retries & exceptions| [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)  
Builder community, early access & challenges| [Discord](https://discord.com/invite/5rAsykttcs)  
Machine-readable API schema| `https://docs.sarvam.ai/openapi.json` · `https://docs.sarvam.ai/asyncapi.json`  
  
Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/getting-started/quickstart)[Building for Indian LanguagesThe concepts that make Indian-language speech and document apps work in production: code-mixing, scripts, telephony audio, voices, and Indic OCR.Next](https://docs.sarvam.ai/api/getting-started/building-for-india)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


