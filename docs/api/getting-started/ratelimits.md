---
url: https://docs.sarvam.ai/api/getting-started/ratelimits/
title: Credits & Rate Limits | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:38.527054+00:00
---

# Credits & Rate Limits | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/getting-started/ratelimits/

Skip to navigation

On this page

  * Credits
  * How Rate Limits Work
  * Per-API Rate Limits by Plan
  * Speech to Text
  * Real-time REST
  * WebSocket Streaming
  * Batch
  * Text to Speech
  * Real-time REST
  * WebSocket Streaming
  * Instant Voice Cloning
  * Translation & Text Services
  * Text translation (POST /translate)
  * Document Translation
  * Chat Completion (LLM)
  * Default models
  * Sarvam-105B model
  * Document AI
  * Digitise
  * Extract
  * Exceeding Your Limits
  * REST rate limits (429 / 503)
  * WebSocket connection limits
  * Plan Overview
  * Upgrading Your Limits
  * Managing Your Credits



Scroll to top

[Getting Started](https://docs.sarvam.ai/api/getting-started/welcome)

# Credits & Rate Limits

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/getting-started/ratelimits.md "View this page as plain text")|More actions

This page is for Model APIs.

## Credits

Sarvam offers **₹100 worth of free credits** for every user on signup. These credits can be used across any of our APIs, explore, prototype, and build without upfront cost.

Credits are universal and never expire. Once exhausted, add more credits or upgrade your plan from the [Sarvam Dashboard](https://dashboard.sarvam.ai/billing).

For commercial production rights when you ship generated audio (Bulbul v3, Content Studio exports, cloned voices), see [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing).

* * *

## How Rate Limits Work

Rate limits restrict the number of API requests your account can make within a given time window. Key points:

  * **Per-account enforcement** : limits apply to your account as a whole, not individual API keys. All keys share the same rate limit pool.
  * **Continuous replenishment** : capacity refills steadily over the window period rather than resetting all at once (token bucket model).
  * **Per-API granularity** : each API has its own independent rate limits. WebSocket, Document AI, and LLM APIs have different limits from standard REST APIs. Check your specific API below.



* * *

## Per-API Rate Limits by Plan

Rate limits vary significantly by API type and plan. Review the limits for each API below before building your integration.

### Speech to Text

#### Real-time REST

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  60 req/min| 100 req/min| 4,000 req/min  
  
#### WebSocket Streaming

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  20 concurrent| 100 concurrent| 100 concurrent  
  
#### Batch

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  20 req/min| 100 req/min| 500 req/min  
  
For batch endpoints, avoid tight polling loops. Poll no faster than your plan’s rate limit allows, for example every 3 seconds on Starter’s 20 req/min.

The SDK’s `wait_until_complete()` uses safe defaults out of the box:

  * **Batch STT / Speech-to-Text-Translate:** 5-second poll interval. See [Polling Defaults](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api#polling-defaults).
  * **Document Digitization (legacy`document_intelligence`):** 2-second poll interval.



[Document AI](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview) has no `wait_until_complete()` helper. You poll `get_status()` yourself, so pick your own interval (the examples use 5 seconds).

If you poll manually instead of using the SDK helper, match or exceed these intervals.

* * *

### Text to Speech

#### Real-time REST

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  60 req/min| 200 req/min| 1,000 req/min  
  
For `bulbul:v3` model specifically, Starter rate limit is **30 req/min**. Pro and Business limits are the same as the default above.

#### WebSocket Streaming

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  60 concurrent| 200 concurrent| 1,000 concurrent  
  
For `bulbul:v3` model specifically, Starter rate limit is **30 concurrent**. Pro and Business limits are the same as the default above.

### Instant Voice Cloning

| Starter| Pro| Business  
---|---|---|---  
**Sustained**|  10 req/min| 50 req/min| 500 req/min  
**Burst**|  50 req| 100 req| 600 req  
  
Instant Voice Cloning limits are lower than Text to Speech because each request runs the full cloning pipeline (transcription, generation, quality control). The sustained figure is the steady-state rate; short spikes are allowed up to the burst figure before requests are rejected with a `429`. Limits are subject to change.

* * *

### Translation & Text Services

#### Text translation (`POST /translate`)

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  60 req/min| 200 req/min| 1,000 req/min  
  
#### Document Translation

Job lifecycle endpoints (`POST /translate/document/jobs`, `start`, `live-status`, `export`, `export/status`):

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  60 req/min| 200 req/min| 1,000 req/min  
  
Document Translation is asynchronous. Poll `live-status` every **10–15 seconds** (see the [overview](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview#how-it-works)) rather than tight loops that burn your per-minute quota.

* * *

### Chat Completion (LLM)

#### Default models

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  60 req/min| 200 req/min| 1,000 req/min  
  
#### Sarvam-105B model

This large model has lower limits due to its compute requirements.

| Starter| Pro| Business  
---|---|---|---  
**Rate Limit**|  40 req/min| 60 req/min| 120 req/min  
  
Applies to: `sarvam-105b`, `sarvam-105b-conversations`

* * *

### Document AI

Document AI limits scale with your plan.

#### Digitise

Rate limits assume **20 pages per request**.

| Pay as you go| Pro| Growth  
---|---|---|---  
**Rate Limit**|  200 req/min| 300 req/min| 400 req/min  
  
#### Extract

Rate limits assume **30 pages per request**.

| Pay as you go| Pro| Growth  
---|---|---|---  
**Rate Limit**|  30 req/min| 50 req/min| 60 req/min  
  
* * *

## Exceeding Your Limits

### REST rate limits (429 / 503)

When your account exceeds a rate limit, the API returns a `429 Too Many Requests` response:
    
    
    {
    
      "error": {
    
        "message": "Rate limit exceeded",
    
        "code": "rate_limit_exceeded_error"
    
      }
    
    }

A `503 Service Unavailable` can also occur under high backend load. Retry it the same way you would a 429, using a fixed exponential backoff. See [Retry with exponential backoff](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting#retry-with-exponential-backoff) for a reference implementation.

### WebSocket connection limits

The limiter reacts to how fast new connections are opened, not how many are held open at once:

  * Connections opened in a fast burst can be rejected well below the concurrent ceilings listed above.
  * The same number of connections opened gradually (for example, 300ms apart) and held open simultaneously can succeed past those ceilings.



A rejected connection is closed, not queued. The close code is `1003`, with this reason text:
    
    
    Rate limit exceeded. Visit the API Dashboard to review and manage your subscription.

This differs from the `4xxx` range described elsewhere on this site for application-specific closures.

The burst threshold is not a fixed number and can vary between runs at the same burst size. Space out new connections rather than relying on a specific count.

* * *

## Plan Overview

| Starter| Pro| Business| Enterprise  
---|---|---|---|---  
**Price**|  Pay as you go| ₹10,000| ₹50,000| Custom  
**Bonus Credits**|  —| ₹100| ₹7,500| Custom  
**Support**|  Community| Email| Email| Dedicated  
**Best For**|  Prototyping & testing| Startups & POCs| Production workloads| Scale deployments  
  
Rate limits are measured per account, not per API key. All keys under an account share the same limit pool. Your current limits are visible on the [Dashboard → Rate Limits](https://dashboard.sarvam.ai/rate-limits) page.

* * *

## Upgrading Your Limits

[1](https://docs.sarvam.ai/api/getting-started/ratelimits#check-your-current-limits)

### Check your current limits

Visit the [Dashboard → Rate Limits](https://dashboard.sarvam.ai/rate-limits) to see your exact per-API limits.

[2](https://docs.sarvam.ai/api/getting-started/ratelimits#upgrade-your-plan)

### Upgrade your plan

Purchase a higher plan directly from the dashboard. Your rate limits increase immediately after upgrade, no downtime.

[3](https://docs.sarvam.ai/api/getting-started/ratelimits#need-custom-limits)

### Need custom limits?

For limits beyond Business tier, contact our team for an Enterprise arrangement.

[Upgrade PlanView plans and upgrade directly from the dashboard. Rate limits update instantly.](https://dashboard.sarvam.ai/pricing)[Enterprise & Custom LimitsNeed higher rate limits, dedicated infrastructure, or custom SLAs? Talk to our team.](https://docs.sarvam.ai/api/getting-started/help)

* * *

## Managing Your Credits

If your credits are exhausted, API requests will return errors. You can add credits at any time, adding credits does **not** change your plan or rate limits.

  1. **Add Credits** : Top up from the [Billing page](https://dashboard.sarvam.ai/billing) at any time. Credits never expire.
  2. **Upgrade Your Plan** : Higher plans include bonus credits and increased rate limits.
  3. **Enterprise** : For volume discounts and custom billing arrangements, email [support@sarvam.ai](mailto:support@sarvam.ai?subject=Enterprise%20API%20Access%20Request&body=Hi%20Sarvam%20Team%2C%0A%0AI'm%20reaching%20out%20from%20%5BYour%20Company%20Name%5D%20to%20explore%20enterprise%20access%20to%20Sarvam%20AI%20APIs.%0A%0ACompany%20Details%3A%0A-%20Company%20Name%3A%20%5BYour%20Company%5D%0A-%20Industry%3A%20%5BYour%20Industry%5D%0A-%20Website%3A%20%5BYour%20Website%5D%0A%0AUse%20Case%3A%0A%5BDescribe%20your%20use%20case%20and%20how%20you%20plan%20to%20use%20our%20APIs%5D%0A%0AAPIs%20of%20Interest%3A%0A%5B%5D%20Speech-to-Text%0A%5B%5D%20Text-to-Speech%0A%5B%5D%20Translation%0A%5B%5D%20Chat%20Completion%0A%5B%5D%20Other%20\(please%20specify\)%0A%0AExpected%20Usage%3A%0A-%20Estimated%20API%20calls%20per%20month%3A%20%5BNumber%5D%0A-%20Expected%20audio%20duration%2Ftext%20volume%3A%20%5BDetails%5D%0A-%20Languages%20needed%3A%20%5BList%20languages%5D%0A%0ASpecific%20Requirements%3A%0A%5BShare%20any%20specific%20features%2C%20SLAs%2C%20or%20support%20needs%5D%0A%0ATimeline%3A%0A%5BWhen%20do%20you%20plan%20to%20start%20testing%2Fdeployment%3F%5D%0A%0ALooking%20forward%20to%20discussing%20this%20further.%0A%0ABest%20regards%2C%0A%5BYour%20Name%5D%0A%5BYour%20Title%5D%0A%5BContact%20Information%5D).



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/getting-started/models/saarika)[Commercial LicensingNext](https://docs.sarvam.ai/api/getting-started/commercial-licensing)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


