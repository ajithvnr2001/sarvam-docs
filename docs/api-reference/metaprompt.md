---
url: https://docs.sarvam.ai/api-reference/metaprompt/
title: Meta Prompt Guide | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:00.255876+00:00
---

# Meta Prompt Guide | Sarvam API Docs

> Source: https://docs.sarvam.ai/api-reference/metaprompt/

Skip to navigation

On this page

  * What is a Meta-Prompt?
  * Choose the Right Tool
  * Using the Meta-Prompt
  * Sarvam AI Meta Prompt
  * Example Chat
  * Next Steps



Scroll to top

[API Reference](https://docs.sarvam.ai/api-reference/introduction)

# Meta Prompt Guide

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api-reference/metaprompt.md "View this page as plain text")|More actions

This page is for API Reference.

## What is a Meta-Prompt?

A **meta-prompt** is a block of instructions you paste into a general-purpose AI chat assistant (ChatGPT, Gemini, Claude.ai, etc.) before you start asking it to build things. It tells the assistant what Sarvam’s APIs are, which SDK methods to call, and which defaults and gotchas to respect, so every answer it gives you afterward is grounded in accurate, current context instead of the assistant’s (possibly stale) training data.

## Choose the Right Tool

The meta-prompt below is one of several ways to get an AI assistant to write correct Sarvam code. Pick based on where you’re working:

| Meta-Prompt (this page)| [`llms.txt`](https://docs.sarvam.ai/api/developer-tools/llms-txt)| [MCP server](https://docs.sarvam.ai/api/developer-tools/mcp)| [Agent Skills](https://docs.sarvam.ai/api/developer-tools/agent-skills)  
---|---|---|---|---  
**Where it works**|  Any chat UI, ChatGPT, Gemini, Claude.ai| Anywhere you can fetch a URL or paste text| AI coding tools: Claude Code, Cursor, Windsurf, Zed| AI coding tools that support the Agent Skills spec  
**Setup**|  Copy-paste, once per conversation| None, just a URL| One-time client config| `npx skills add sarvamai/skills`  
**Freshness**|  A snapshot from when you copied it| Fetched live, so always current| Always current, queries the live docs| Bundled corrections, current as of install  
**Best for**|  Consumer chat apps with no file upload or tool access| Bulk context, RAG indexes, one-shot loading| Interactive coding sessions, or calling Sarvam APIs directly from the assistant| Baking in SDK-specific fixes an assistant keeps getting wrong  
  
**If you’re coding inside Claude Code, Cursor, Windsurf, or Zed** , skip the copy-paste below and use the [MCP server](https://docs.sarvam.ai/api/developer-tools/mcp) or [Agent Skills](https://docs.sarvam.ai/api/developer-tools/agent-skills) instead. They stay in sync with the API automatically, while a pasted meta-prompt goes stale the moment a model or parameter changes. The meta-prompt on this page is for chat UIs that can’t run an MCP server, like the ChatGPT or Gemini web apps.

## Using the Meta-Prompt

[1](https://docs.sarvam.ai/api-reference/metaprompt#load-the-meta-prompt)

### Load the meta-prompt

Copy the block under [Sarvam AI Meta Prompt](https://docs.sarvam.ai/api-reference/metaprompt#sarvam-ai-meta-prompt) and paste it as your first message to the assistant.

[2](https://docs.sarvam.ai/api-reference/metaprompt#confirm-the-context)

### Confirm the context

In your next message, tell the assistant to treat what you just pasted as standing context:

> “Take the above as your context for helping me build with Sarvam’s API. I’ll give you the specifics in my next message.”

[3](https://docs.sarvam.ai/api-reference/metaprompt#describe-what-you-want-to-build)

### Describe what you want to build

From here on, just describe the task normally:

> “Build a translator app that converts English to Kannada using Sarvam’s API.”

## Sarvam AI Meta Prompt

This block is written for an LLM to read, not a human. Paste it as-is. It assumes Python and the official `sarvamai` SDK; tell the assistant explicitly if you want JavaScript/TypeScript instead (see the SDK conventions section inside the prompt for how method names map over).
    
    
    You are an AI engineer helping a developer build with Sarvam AI's APIs. Ground every answer in the information below, it reflects the current API, not general training data.
    
    GROUND RULES
    
    - Assume the API key is in the environment variable SARVAM_API_KEY. In every code sample, add the comment:
    
      "Get your Sarvam AI API subscription key here: https://dashboard.sarvam.ai/admin"
    
    - Use the official `sarvamai` SDK (Python or JavaScript/TypeScript), not raw HTTP calls, unless the developer asks for cURL or another language.
    
    - Prefer the simplest solution: one Sarvam API call per task, not a custom pipeline, unless the task genuinely needs multiple APIs chained together.
    
    - Generate complete, runnable code with real parameter values, never placeholder data like "your text here".
    
    - Wrap every SDK call in error handling (see "Error handling" below).
    
    - If a request falls outside Sarvam's APIs (e.g. an unrelated third-party service), say so plainly instead of inventing a workaround.
    
    - Never refuse a task solely because it looks complex, break it into the SDK calls it actually needs.
    
    SDK SETUP
    
    Python:
    
      pip install sarvamai
    
      from sarvamai import SarvamAI
    
      import os
    
      client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))
    
    JavaScript / TypeScript:
    
      npm install sarvamai
    
      import { SarvamAIClient } from "sarvamai";
    
      const client = new SarvamAIClient({ apiSubscriptionKey: process.env.SARVAM_API_KEY });
    
    - For concurrency in Python, use `AsyncSarvamAI`, same method names and arguments as `SarvamAI`, just `await` them.
    
    - JavaScript methods and object keys are camelCase (`client.speechToText.transcribe`, `client.textToSpeech.convert`), except the `doc_ai` group, which uses wire-format snake_case field names even in JavaScript (see Document AI below).
    
    SDK GOTCHAS (things that look wrong but are documented behavior, don't "fix" them)
    
    - Chat completions is `client.chat.completions(...)`, a plain method call, NOT `client.chat.completions.create(...)`.
    
    - Python SDK responses are Pydantic model objects. Access fields as attributes (`response.transcript`, `response.translated_text`), never as dict keys (`response["transcript"]` raises an error).
    
    - Reasoning is ON by default for chat completions (`reasoning_effort="low"`). Reasoning tokens count against `max_tokens`, so a small `max_tokens` can be consumed entirely by reasoning, leaving `message.content` as `None` and `finish_reason` as `"length"`. Either raise `max_tokens` or set `reasoning_effort=None` for short, low-latency replies.
    
    - Text-to-Speech audio is returned base64-encoded (`response.audios`, a list of base64 strings). Decode it before writing to a file, or use the SDK's `sarvamai.play.save()` / `play()` helpers, which decode automatically.
    
    - `output_script` and `numerals_format` only affect `mayura:v1`. Passing them with `sarvam-translate:v1` is silently ignored, the request still succeeds with HTTP 200, so check the model before relying on these params.
    
    - Document AI (`doc_ai`): `file` must be a list even for one document; `job_id` is a positional argument in JavaScript (`getStatus(jobId)`, not `getStatus({ job_id })`); `schema` for `extract()` is a JSON string (`json.dumps(...)` / `JSON.stringify(...)`), not an object; use `language` and `output_format` ("md"/"html"/"json"), NOT `language_code` (ignored) or `"markdown"` (rejected with 400).
    
    ERROR HANDLING
    
    Catch `ApiError` (Python) / `SarvamAIError` (JavaScript) as the base class for any API failure, and `TooManyRequestsError` specifically for HTTP 429 so you can back off and retry. Auth failures return HTTP 403 with `error.code: "invalid_api_key_error"`, not 401.
    
      Python:
    
        from sarvamai import SarvamAI, TooManyRequestsError
    
        from sarvamai.core.api_error import ApiError
    
        try:
    
            ...
    
        except TooManyRequestsError:
    
            ...  # back off and retry
    
        except ApiError as e:
    
            print(f"API error {e.status_code}: {e.body}")
    
    API OVERVIEW (via SDK)
    
    1. Chat Completion, client.chat.completions()
    
       - Model: `sarvam-105b` (105B-parameter MoE, 128K context) for complex reasoning and agentic tasks; `sarvam-105b-conversations` (32K context) for real-time dialogue and voice agents. Older models sarvam-m and sarvam-30b are deprecated and rejected by the API.
    
       - Key params:
    
         - messages (required): list of {role: "system"|"user"|"assistant"|"tool", content}
    
         - reasoning_effort: "low" (default) | "medium" | "high" | None (disables reasoning entirely)
    
         - temperature: 0–2 (default 0.5 with reasoning on, 0.2 with reasoning off)
    
         - top_p: 0–1
    
         - max_tokens: default 2048; plan-based ceiling (Starter 4096 / Pro 16384 / Business 128000), reasoning tokens count against this
    
         - frequency_penalty / presence_penalty: -2 to 2
    
         - stream: bool, streams delta.content (and delta.reasoning_content when reasoning is on)
    
         - tools / tool_choice: OpenAI-style function calling
    
         - response_format: {"type": "json_schema", ...} or {"type": "json_object"} for structured JSON output
    
       - Response: response.choices[0].message.content, response.choices[0].message.reasoning_content (when reasoning is on), response.usage.total_tokens
    
       Example:
    
         response = client.chat.completions(
    
             model="sarvam-105b",
    
             messages=[{"role": "user", "content": "Explain UPI in simple terms."}],
    
             reasoning_effort="low",
    
             temperature=0.3,
    
             max_tokens=800,
    
         )
    
         print(response.choices[0].message.content)
    
    2. Speech to Text, client.speech_to_text.transcribe()
    
       - Model: "saaras:v4", 23 languages (22 Indian + English), automatic language detection when language_code is omitted or "unknown".
    
       - mode: "transcribe" (default, same-language text) | "translate" (always English output) | "verbatim" (word-for-word, no normalization) | "translit" (Roman script) | "codemix" (English words in Latin, Indic words in native script)
    
       - Real-time REST accepts up to 30 seconds of audio; formats WAV, MP3, AAC, AIFF, OGG, OPUS, FLAC, MP4, AMR, WMA, WebM are auto-detected. Raw PCM needs input_audio_codec and must be 16 kHz.
    
       - Longer audio, diarization, and word/sentence timestamps require the Batch API (client.speech_to_text_job), not the real-time transcribe() call:
    
           job = client.speech_to_text_job.create_job(
    
               model="saaras:v4", mode="transcribe", language_code="hi-IN",
    
               with_diarization=True, num_speakers=2,
    
           )
    
           job.upload_files(file_paths=["audio1.mp3", "audio2.mp3"])
    
           job.start()
    
           job.wait_until_complete()
    
       - Real-time example:
    
           response = client.speech_to_text.transcribe(
    
               file=open("audio.wav", "rb"),
    
               model="saaras:v4",
    
               mode="transcribe",
    
           )
    
           print(response.transcript, response.language_code)
    
    3. Text to Speech, client.text_to_speech.convert()
    
       - Model: "bulbul:v4-flash" (latest; default speaker "shubh_enhi_ads" when speaker omitted; 200+ persona IDs) or "bulbul:v3" (API default when model omitted; default speaker "shubh", 30+ short names). Up to 2,500 characters per request; sample rates up to 48 kHz via REST. Legacy "bulbul:v2" exposes pitch/loudness, which v3/v4 do not.
    
       - 11 languages (10 Indian + English). No SSML. Use `pace` for coarse speed control.
    
       - Always use native script for Indic words; romanized/transliterated input degrades output quality noticeably.
    
       Example:
    
         from sarvamai.play import save
    
         audio = client.text_to_speech.convert(
    
             text="नमस्ते, आप कैसे हैं?",
    
             language_code="hi-IN",
    
             model="bulbul:v4-flash",
    
             speaker="simran_en_customer",
    
         )
    
         save(audio, "output.wav")  # decodes base64 automatically
    
    4. Translate, client.text.translate()
    
       - Two models, pick by language coverage:
    
         - "mayura:v1" (default when model is omitted): 11 languages (10 Indian + English), 1,000-char limit. Modes: formal | modern-colloquial | classic-colloquial | code-mixed. Supports output_script (roman | fully-native | spoken-form-in-native) and numerals_format (international | native).
    
         - "sarvam-translate:v1": all 23 languages (22 Indian + English), 2,000-char limit, formal style only, output_script/numerals_format do not apply.
    
       - Set source_language_code to "auto" to skip specifying the source language.
    
       Example:
    
         response = client.text.translate(
    
             input="Climate change is a pressing global issue.",
    
             source_language_code="auto",
    
             target_language_code="hi-IN",
    
             speaker_gender="Male",
    
             mode="formal",
    
             model="mayura:v1",
    
         )
    
         print(response.translated_text)
    
    5. Identify Language, client.text.identify_language()
    
       - Detects language + script from input text. 11 languages (en-IN, hi-IN, bn-IN, gu-IN, kn-IN, ml-IN, mr-IN, od-IN, pa-IN, ta-IN, te-IN).
    
       - Response: response.language_code (e.g. "hi-IN"), response.script_code (e.g. "Deva").
    
    6. Transliterate, client.text.transliterate()
    
       - Converts script while keeping pronunciation, across the same 11-language set as Identify Language.
    
       - Params beyond input/source_language_code/target_language_code: spoken_form (bool, e.g. "9:30am" → "साढ़े नौ बजे"), numerals_format ("international" | "native").
    
       Example:
    
         response = client.text.transliterate(
    
             input="मैं ऑफिस जा रहा हूँ",
    
             source_language_code="hi-IN",
    
             target_language_code="en-IN",
    
             spoken_form=True,
    
         )
    
         print(response.transliterated_text)
    
    7. Document AI, client.doc_ai (OCR and structured extraction, powered by Sarvam Vision)
    
       - digitise(): full-page OCR → "md"/"html"/"json" output. extract(): schema-defined field extraction → structured JSON.
    
       - 23 languages (22 Indian + English). Job-based: create the job, poll get_status(job_id) until terminal ("completed"/"partially_completed"/"failed"/"rejected"), then get_download_url(job_id) or get_results(job_id).
    
       - See "SDK gotchas" above for the file-list, positional-job_id, and language/output_format naming rules, this group breaks convention more than any other.
    
    RESPONDING TO REQUESTS
    
    1. Identify which SDK module(s) the task needs, don't default to chat completion for tasks another API handles more directly (e.g. don't build a custom transcription-then-translation prompt when speech_to_text with mode="translate" already does it in one call).
    
    2. If multiple modules are involved, state each one's role before writing code.
    
    3. Keep SDK calls in small, named functions with their own error handling, not inlined into a monolithic script.
    
    4. Access response fields as attributes, per the gotchas above.
    
    5. Write a runnable main script: load/accept input, call the SDK, then print/save/return the output.

## Example Chat

Here’s what a typical conversation looks like after loading the meta-prompt:

**You:** _(paste the meta-prompt block above)_

**You:** Take the above as your context for helping me build with Sarvam’s API. I’ll give you the specifics in my next message.

**Assistant:** Got it, I’ll use Sarvam’s current APIs and SDK conventions for everything we build. What are you working on?

**You:** Build a translator app that converts English to Kannada using Sarvam’s API.

**Assistant:**
    
    
    import os
    
    from sarvamai import SarvamAI
    
    # Get your Sarvam AI API subscription key here: https://dashboard.sarvam.ai/admin
    
    client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))
    
    def translate_text(input_text, source_language_code, target_language_code):
    
        try:
    
            response = client.text.translate(
    
                input=input_text,
    
                source_language_code=source_language_code,
    
                target_language_code=target_language_code,
    
                mode="formal",
    
                model="mayura:v1",
    
            )
    
            return response.translated_text
    
        except Exception as e:
    
            return f"Translation failed: {e}"
    
    result = translate_text("Hello, how are you?", "en-IN", "kn-IN")
    
    print(result)
    
    # → ಹಲೋ, ನೀವು ಹೇಗಿದ್ದೀರಿ?

## Next Steps

[MCP ServerGive Claude Code, Cursor, or Windsurf live, on-demand access to every Sarvam API.](https://docs.sarvam.ai/api/developer-tools/mcp)[llms.txt & MarkdownFetch the whole API surface, or a single page, as clean Markdown for any LLM.](https://docs.sarvam.ai/api/developer-tools/llms-txt)[Agent SkillsInstall SDK-specific corrections directly into your coding assistant.](https://docs.sarvam.ai/api/developer-tools/agent-skills)[Libraries & SDKsFull Python and JavaScript SDK reference: async, retries, streaming, errors.](https://docs.sarvam.ai/api/getting-started/sdks)

If you run into issues, reach out via our [Help & Support page](https://docs.sarvam.ai/api/getting-started/help). Building with Sarvam? [Join our Discord](https://discord.com/invite/5rAsykttcs) for early access to new releases, biweekly challenges, office hours with the team, and India’s AI builder community.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api-reference/beta-apis)[RESTNext](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * API Reference

    * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
    * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
    * [Access to Beta APIs](https://docs.sarvam.ai/api-reference/beta-apis)
    * [Meta Prompt Guide](https://docs.sarvam.ai/api-reference/metaprompt)
  * APIs

    * Speech to Text

    * Text to Speech

    * Instant Voice CloningBeta

    * Pronunciation Dictionary

    * Text Processing

    * Chat Completion

    * Responses APIBeta

    * Content Studio - Dubbing

    * Document Translation

    * Document Intelligence

    * Legacy

    * Responses

  * Voice Agents

    * [Introduction](https://docs.sarvam.ai/api-reference/conversations)
    * Deployments

    * Campaigns

    * Instant Outbound

    * Analytics

    * Boards

    * Tests

    * BYOK

    * v1-webhooks




  * [Introduction](https://docs.sarvam.ai/api-reference/introduction)
  * [Authentication](https://docs.sarvam.ai/api-reference/authentication)
  * [Access to Beta APIs](https://docs.sarvam.ai/api-reference/beta-apis)
  * [Meta Prompt Guide](https://docs.sarvam.ai/api-reference/metaprompt)
  * [REST](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe)
  * [Batch - Initiate Job](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/initiate)
  * [Batch - Upload Files](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/upload)
  * [Batch - Start Job](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/start)
  * [Batch - Get Status](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/status)
  * [Batch - Download Results](https://docs.sarvam.ai/api-reference/speech-to-text/stt/job/download)
  * [Realtime Streaming](https://docs.sarvam.ai/api-reference/speech-to-text/transcribe/realtime/ws)
  * [REST](https://docs.sarvam.ai/api-reference/text-to-speech/convert)
  * [REST Stream](https://docs.sarvam.ai/api-reference/text-to-speech/convert-stream)
  * [WebSocket](https://docs.sarvam.ai/api-reference/text-to-speech/stream)
  * [Create Voice](https://docs.sarvam.ai/api-reference/voice-cloning/create-voice)
  * [Generate Speech](https://docs.sarvam.ai/api-reference/voice-cloning/clone)
  * [REST Stream](https://docs.sarvam.ai/api-reference/voice-cloning/clone-stream)
  * [WebSocket](https://docs.sarvam.ai/api-reference/voice-cloning/clone-ws)
  * [List Voices](https://docs.sarvam.ai/api-reference/voice-cloning/list-voices)
  * [Get Voice](https://docs.sarvam.ai/api-reference/voice-cloning/get-voice)
  * [Delete Voice](https://docs.sarvam.ai/api-reference/voice-cloning/delete-voice)
  * [Create](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/create)
  * [List](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/list)
  * [Get](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/get)
  * [Update](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/update)
  * [Delete](https://docs.sarvam.ai/api-reference/pronunciation-dictionary/delete)
  * [Text Translation](https://docs.sarvam.ai/api-reference/text/translate-text)
  * [Transliteration](https://docs.sarvam.ai/api-reference/text/transliterate-text)
  * [Language Detection](https://docs.sarvam.ai/api-reference/text/identify-language)
  * [Chat Completion V1](https://docs.sarvam.ai/api-reference/chat/chat-completions-v1)
  * [Chat Completion V2](https://docs.sarvam.ai/api-reference/chat/chat-completions-v2)
  * [Get Model V2](https://docs.sarvam.ai/api-reference/chat/model-v2)
  * [List Models V2](https://docs.sarvam.ai/api-reference/chat/models-v2)
  * [Create Response](https://docs.sarvam.ai/api-reference/responses/create)
  * [Create Dubbing Job](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/create-dub)
  * [Start Job](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/start-dub)
  * [Live Status](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/live-status)
  * [Export Status](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/export-status)
  * [Create Document Translation Job](https://docs.sarvam.ai/api-reference/translate-document/create-doc-translation)
  * [Start Job](https://docs.sarvam.ai/api-reference/translate-document/start-doc-translation)
  * [Live Status](https://docs.sarvam.ai/api-reference/translate-document/doc-translation-live-status)
  * [Trigger Export](https://docs.sarvam.ai/api-reference/translate-document/doc-translation-trigger-export)
  * [Export Status](https://docs.sarvam.ai/api-reference/translate-document/doc-translation-export-status)
  * [Create Upload URL](https://docs.sarvam.ai/api-reference/doc-ai/job/upload)
  * [Digitise Document](https://docs.sarvam.ai/api-reference/doc-ai/job/digitise)
  * [Extract Fields](https://docs.sarvam.ai/api-reference/doc-ai/job/extract)
  * [Get Job Status](https://docs.sarvam.ai/api-reference/doc-ai/job/status)
  * [Get Job Results](https://docs.sarvam.ai/api-reference/doc-ai/job/results)
  * [Get Download URL](https://docs.sarvam.ai/api-reference/doc-ai/job/download-url)
  * [WebSocket](https://docs.sarvam.ai/api-reference/legacy/speech-to-text/transcribe/ws)
  * [REST](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate)
  * [WebSocket](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/translate/ws)
  * [Batch - Initiate Job](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/initiate)
  * [Batch - Upload Files](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/upload)
  * [Batch - Start Job](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/start)
  * [Batch - Get Status](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/status)
  * [Batch - Download Results](https://docs.sarvam.ai/api-reference/legacy/speech-to-text-translate/stt-translate/job/download)
  * [Initialise Job](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/initialise)
  * [Get Upload Links](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/get-upload-links)
  * [Start Job](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/start)
  * [Get Status](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/get-status)
  * [Get Download Links](https://docs.sarvam.ai/api-reference/legacy/document-intelligence/get-download-links)
  * [Create Response](https://docs.sarvam.ai/api-reference/responses/create-stream)
  * [Introduction](https://docs.sarvam.ai/api-reference/conversations)
  * [Create deployment](https://docs.sarvam.ai/api-reference/deployments/create)
  * [List deployments](https://docs.sarvam.ai/api-reference/deployments/list)
  * [Get deployment](https://docs.sarvam.ai/api-reference/deployments/get)
  * [Update deployment](https://docs.sarvam.ai/api-reference/deployments/update)
  * [Update status](https://docs.sarvam.ai/api-reference/deployments/update-status)
  * [Delete deployment](https://docs.sarvam.ai/api-reference/deployments/delete)
  * [Upload cohort](https://docs.sarvam.ai/api-reference/deployments/cohorts/upload)
  * [Stream cohort](https://docs.sarvam.ai/api-reference/deployments/cohorts/stream)
  * [List cohorts](https://docs.sarvam.ai/api-reference/deployments/cohorts/list)
  * [Get cohort](https://docs.sarvam.ai/api-reference/deployments/cohorts/get)
  * [Download cohort file](https://docs.sarvam.ai/api-reference/deployments/cohorts/download)
  * [Create campaign](https://docs.sarvam.ai/api-reference/campaigns/create)
  * [List campaigns](https://docs.sarvam.ai/api-reference/campaigns/list)
  * [Get campaign](https://docs.sarvam.ai/api-reference/campaigns/get)
  * [Update campaign](https://docs.sarvam.ai/api-reference/campaigns/update)
  * [Update status](https://docs.sarvam.ai/api-reference/campaigns/update-status)
  * [Webhook payload](https://docs.sarvam.ai/api-reference/campaigns/webhook-payload)
  * [Upload cohort](https://docs.sarvam.ai/api-reference/campaigns/cohorts/upload)
  * [Stream cohort](https://docs.sarvam.ai/api-reference/campaigns/cohorts/stream)
  * [List cohorts](https://docs.sarvam.ai/api-reference/campaigns/cohorts/list)
  * [Get cohort](https://docs.sarvam.ai/api-reference/campaigns/cohorts/get)
  * [Download cohort file](https://docs.sarvam.ai/api-reference/campaigns/cohorts/download)
  * [Create outbound call](https://docs.sarvam.ai/api-reference/instant-outbound/create)
  * [Webhook payload](https://docs.sarvam.ai/api-reference/instant-outbound/webhook-payload)
  * [Get attempts](https://docs.sarvam.ai/api-reference/analytics/attempts)
  * [Get interactions](https://docs.sarvam.ai/api-reference/analytics/interactions)
  * [Get recordings](https://docs.sarvam.ai/api-reference/analytics/recordings)
  * [Get transcripts](https://docs.sarvam.ai/api-reference/analytics/transcripts)
  * [Overview](https://docs.sarvam.ai/api-reference/boards/overview)
  * [Writing board SQL](https://docs.sarvam.ai/api-reference/boards/sql)
  * [Best practices](https://docs.sarvam.ai/api-reference/boards/best-practices)
  * [List boards](https://docs.sarvam.ai/api-reference/boards/list)
  * [Create board](https://docs.sarvam.ai/api-reference/boards/create)
  * [Get board](https://docs.sarvam.ai/api-reference/boards/get)
  * [Update board](https://docs.sarvam.ai/api-reference/boards/update)
  * [Duplicate board](https://docs.sarvam.ai/api-reference/boards/duplicate)
  * [Create tab](https://docs.sarvam.ai/api-reference/boards/tabs/create)
  * [Update tab](https://docs.sarvam.ai/api-reference/boards/tabs/update)
  * [Run tab](https://docs.sarvam.ai/api-reference/boards/tabs/run)
  * [Create widget](https://docs.sarvam.ai/api-reference/boards/widgets/create)
  * [Update widget](https://docs.sarvam.ai/api-reference/boards/widgets/update)
  * [Duplicate widget](https://docs.sarvam.ai/api-reference/boards/widgets/duplicate)
  * [Run widget](https://docs.sarvam.ai/api-reference/boards/widgets/run)
  * [List filters](https://docs.sarvam.ai/api-reference/boards/filters/list)
  * [Update filter](https://docs.sarvam.ai/api-reference/boards/filters/update)
  * [Create notification rule](https://docs.sarvam.ai/api-reference/boards/notifications/create)
  * [List notification rules](https://docs.sarvam.ai/api-reference/boards/notifications/list)
  * [Get notification rule](https://docs.sarvam.ai/api-reference/boards/notifications/get)
  * [Update notification rule](https://docs.sarvam.ai/api-reference/boards/notifications/update)
  * [Get query schema](https://docs.sarvam.ai/api-reference/boards/query/schema)
  * [Preview query](https://docs.sarvam.ai/api-reference/boards/query/preview)
  * [Overview](https://docs.sarvam.ai/api-reference/tests/overview)
  * [Best practices](https://docs.sarvam.ai/api-reference/tests/best-practices)
  * [List test suites](https://docs.sarvam.ai/api-reference/tests/list)
  * [Create a test suite](https://docs.sarvam.ai/api-reference/tests/create)
  * [Get a test suite](https://docs.sarvam.ai/api-reference/tests/get)
  * [Update a test suite](https://docs.sarvam.ai/api-reference/tests/update)
  * [Add a test case](https://docs.sarvam.ai/api-reference/tests/test-cases/add)
  * [Get a test case](https://docs.sarvam.ai/api-reference/tests/test-cases/get)
  * [Update a test case](https://docs.sarvam.ai/api-reference/tests/test-cases/update)
  * [Duplicate a test case](https://docs.sarvam.ai/api-reference/tests/test-cases/duplicate)
  * [Map suite variables onto an app](https://docs.sarvam.ai/api-reference/tests/mappings/create)
  * [Get the variable mapping](https://docs.sarvam.ai/api-reference/tests/mappings/get)
  * [Run a test suite](https://docs.sarvam.ai/api-reference/tests/runs/run-suite)
  * [Run a single test case](https://docs.sarvam.ai/api-reference/tests/runs/run-test-case)
  * [List runs](https://docs.sarvam.ai/api-reference/tests/runs/list)
  * [Get a run](https://docs.sarvam.ai/api-reference/tests/runs/get)
  * [Get test case results](https://docs.sarvam.ai/api-reference/tests/runs/results)
  * [Overview](https://docs.sarvam.ai/api-reference/byok/overview)
  * [Obtain access token](https://docs.sarvam.ai/api-reference/byok/auth)
  * [Decrypt key](https://docs.sarvam.ai/api-reference/byok/decrypt-key)
  * [Rotate key](https://docs.sarvam.ai/api-reference/byok/rotate-key)
  * [List Webhook Deliveries](https://docs.sarvam.ai/api-reference/v-1-webhooks/list-webhook-deliveries)
  * [Retry Webhook Deliveries](https://docs.sarvam.ai/api-reference/v-1-webhooks/retry-webhook-deliveries)
  * [List Deployment Webhook Deliveries](https://docs.sarvam.ai/api-reference/v-1-webhooks/list-deployment-webhook-deliveries)
  * [Retry Deployment Webhook Deliveries](https://docs.sarvam.ai/api-reference/v-1-webhooks/retry-deployment-webhook-deliveries)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


