---
url: https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/faq/
title: FAQs | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:15.976320+00:00
---

# FAQs | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/faq/

Skip to navigation

On this page

  * Pricing and billing
  * Getting started
  * Languages
  * Voices and speakers
  * Translation quality
  * Exports and downloads
  * Statuses and polling
  * Troubleshooting
  * Related



Scroll to top

[API Guides & Tutorials](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)[Dubbing](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)

# FAQs

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/faq.md "View this page as plain text")|More actions

This page is for Model APIs.

Common questions about the [Dubbing API](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview). If yours isn’t here, reach out on [Discord](https://discord.com/invite/5rAsykttcs).

## Pricing and billing

###### How much does dubbing cost?

Dubbing is billed per whole second of source media, multiplied by the number of target languages. On Starter, the default API rate is **₹40/min** when `editor_flow` is `false` (the default). See [Pricing](https://docs.sarvam.ai/api/getting-started/pricing#dubbing) for Pro, Enterprise, and the full rate table.

Why does `editor_flow: true` cost more?

`editor_flow: true` enables the interactive editor workflow (manual review, chunk edits, and manual export triggers in Creator Studio). It is billed at the **editor-flow rate, ₹80/min on Starter** , which is **double** the standard API rate. It also suppresses auto-export, so `export-status` stays empty until exports are triggered manually. For programmatic integrations that just need dubbed files back, keep `editor_flow` at its default of `false`.

###### How do I estimate credits before starting a job?

Multiply source duration in whole seconds by the number of target languages, then apply the per-second rate for your plan and whether `editor_flow` is enabled. Example: a 60-second file into two languages at the Starter API rate (₹40/min) costs about ₹80 in credits (60 × 2 × ₹40/60).

## Getting started

###### Which host and auth header does dubbing use?

See the [API Reference](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/create-dub) for the current base URL. Send your key in the `api-subscription-key` header, not `Authorization: Bearer`. Generate a key at [Key Management](https://dashboard.sarvam.ai/key-management) using the same email as your Sarvam account.

If you’re using the Python SDK, none of this needs configuring: the client resolves the dubbing endpoint from its default environment, so `SarvamAI(api_subscription_key=...)` is enough. You do not need to pass a custom `SarvamAIEnvironment`.

###### Is there a single call that takes a file and returns a dub?

No. Dubbing runs as an asynchronous pipeline, so it’s split across five steps: create the job, upload the media to the signed `upload_url`, `POST /start`, poll `live-status`, then read `export-status` for download URLs. In the Python SDK the upload step is `client.dubbing.upload()`. See the [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview#how-it-works) for the flow, and the [API Reference](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/create-dub) for runnable code for each call.

###### What files can I upload?

Video as MP4, MOV, MKV, WebM, AVI, FLV, or WMV, and audio as WAV, MP3, or M4A. The file needs to be at least one second long and contain audible speech. The format is detected from the file’s contents rather than its name, so the `.mp4` ending the signed upload URL does not constrain what you send.

###### How large or long can my media be?

It depends on your plan: 2 GB and 1 hour on Starter, 3 GB and 1 hour on Pro, and 4 GB and 4 hours on Business. Starter is the default, so assume those limits unless your account is on a higher plan; on Enterprise, check with your account team. Media over the limit is rejected when processing starts, not at upload time. See [What you can upload](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview#what-you-can-upload).

## Languages

###### Which languages are supported?

Twelve: English (`en-IN`), Hindi (`hi-IN`), Bengali (`bn-IN`), Gujarati (`gu-IN`), Kannada (`kn-IN`), Malayalam (`ml-IN`), Marathi (`mr-IN`), Odia (`or-IN`), Punjabi (`pa-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), and Assamese (`as-IN`). The same set is valid for both `src_lang` and `target_langs`.

###### Do I need one job per target language?

No, and you shouldn’t. `target_langs` is an array and a single job dubs into every language in it, from one upload and one `job_id`. See [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/specify-language-codes).

## Voices and speakers

###### Does the dub keep the original speaker's voice?

Yes, by default. `voice_cloning` defaults to `true`, which preserves each original speaker’s vocal identity in the target language. See [Choose a Voice](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice).

###### How does Sarvam handle multiple speakers?

Set `num_speakers` to the number of distinct voices in the source (1 to 10, or `-1` to auto-detect); each is separated and cloned independently. The default is `1`, so a conversation left at the default is flattened into one voice. If you’re unsure, round your estimate **up** , because under-specifying is audible and can only be fixed with a new job.

###### Can I use a preset voice instead of cloning?

Yes. Set `voice_cloning: false` and name a `voice_id` from the 15 preset voices, optionally with a `pace_preset`. This is single-speaker only, so multi-speaker jobs always clone. See [Choose a Voice](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice).

## Translation quality

###### How do I control how formal the translation sounds?

Pass `register`. Accepted values are `formal`, `common-indic`, `classic-colloquial`, `modern-colloquial`, `academic`, and `auto`. See [Control Translation Tone](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/control-translation-tone).

###### What's the fastest way to review translation quality?

Add `srt` to `export_options` and read the subtitle file. It takes seconds versus watching the full dub, and it surfaces register and phrasing problems before you publish.

###### Can I change the register on an existing job?

No. Every setting is fixed at creation, and there is no update endpoint. To compare registers on the same source, create two jobs.

## Exports and downloads

###### What formats can I get back?

`export_options` accepts any combination of `video`, `audio`, and `srt`, produced for **each** target language. Omit it and you get video, audio, and MP3, but never SRT, which you have to request explicitly. Pass it and only the formats you list are produced. Note that `audio` is uncompressed `.wav`; entries may also report an `export_type` of `mp3`, which is the same track re-encoded. See [Choose Export Formats](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats).

###### I only asked for SRT. Can I get the video later?

Yes, and without re-dubbing or re-uploading. The translated audio already exists, so `POST /jobs/{job_id}/export-all?target_lang=...` produces the full video + audio + MP3 set for that language, and `POST /jobs/{job_id}/export` adds one specific format. Both reuse valid existing exports. See [Choose Export Formats](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats#getting-a-format-you-didnt-request).

###### How long do download URLs stay valid?

Roughly 24 hours. They’re signed and time-limited, so store the `job_id` and re-poll `export-status` for a fresh link rather than caching the URL.

What does `is_stale` mean?

The translation chunks for that language were modified after the export completed, so the downloadable file no longer reflects the latest edits. Re-export before publishing.

###### How do I remove the watermark?

Pass `disable_watermark: true` at job creation. It defaults to `false`, applies to video exports only, and cannot be changed after the job exists. See [the watermark section](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats#the-watermark-on-video-exports).

## Statuses and polling

###### What are the possible job statuses?

`not_started`, `queued`, `in_progress`, `completed`, `failed`, `partial_failure`, and `deleted`. A freshly created job is `not_started` until you call `start`. Individual exports carry their own separate status: `in_progress`, `completed`, or `failed`. See [Job Lifecycle](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle).

What is `partial_failure`?

Some target languages succeeded and others didn’t. It’s uncommon, but treat it as a terminal state alongside `completed` and `failed`, so the languages that did work still get published. Inspect per-language state in `live-status` and per-entry `status` in `export-status`.

###### How often should I poll?

The API does not specify a required polling interval, so pick one that suits your workload and back off for long files. As general guidance: always cap total wait time, and poll from a background worker rather than an HTTP request handler. If you need a value to start from, treat something like 15 seconds as an example to tune against your own file lengths, not a recommended setting.

## Troubleshooting

Why is my job still `not_started` or `queued`?

Both mean a step is still outstanding on your side. `not_started` means `POST /jobs/{job_id}/start` was never called, creating a job does not start it. `queued` means it was started but the media was never uploaded to `upload_url`, so there is nothing to process. See [Job Lifecycle](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle).

###### Why did my job fail soon after starting?

Media is checked once processing begins rather than while it uploads, so an unsupported format, a corrupt or truncated file, or one with no audible audio only surfaces at that point, storage accepts the bytes either way. Read `error_message` on the job for the specific reason.

###### What causes a 422 on language codes?

Check Odia. The dubbing service uses **`or-IN`** , and `od-IN` is rejected. Also confirm every code is in the list of twelve above, and that `src_lang` does not also appear in `target_langs`.

I set `voice_id` but the dub came back in the original voice. Why?

Because cloning is on by default and takes precedence. A preset voice needs `voice_cloning: false` alongside `voice_id`; without it both `voice_id` and `pace_preset` are discarded without an error. Multi-speaker jobs always clone, since one preset voice cannot represent several speakers. See [Choose a Voice](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice).

Why would `export-status` be empty on a completed job?

Usually timing: the job reaches `completed` when the dubbing pipeline finishes, and exports are triggered at that moment rather than before it, so a poll that lands in between sees nothing yet. Keep polling. Auto-export is best-effort per language, so if entries never appear for one language you can trigger them yourself with `POST /jobs/{job_id}/export-all?target_lang=...`.

###### Why would some exports be missing from the response?

Check `limit`. It defaults to `5`, and entries beyond the limit are not returned, so a job with 2 languages × 3 formats gets only five of its six entries. Pass an explicit `limit` above `languages × formats` (maximum `100`).

What causes a 403 when uploading to `upload_url`?

The signed URL expired. Check `data.expires_in_hours` from the create response and upload promptly; if it’s lapsed, create a new job for a fresh URL. Also make sure you’re sending `x-ms-blob-type: BlockBlob` and a correct `Content-Type`, and **not** sending your API key to that URL.

###### What should I include in a support request?

The `job_id`. It’s how a dub is traced end to end, so log it on every call for the job.

## Related

  * [Dubbing Overview](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)
  * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats)[Instant Voice Cloning APINext](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


