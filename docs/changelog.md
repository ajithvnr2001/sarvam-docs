---
url: https://docs.sarvam.ai/changelog/
title: Change Log | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:51.043778+00:00
---

# Change Log | Sarvam API Docs

> Source: https://docs.sarvam.ai/changelog/

Skip to navigation

This page is for Changelog.

# [Change Log](https://docs.sarvam.ai/changelog)

Subscribe via RSS

Track new features, model updates, and breaking changes across Sarvam AI’s APIs and products. Use the filters below to narrow the timeline to a single product - Model APIs, Voice Agents, Doc Agents, Content Studio, or Cowork.

Subscribe to updates: append `.rss`, `.atom`, or `.json` to this page’s URL - e.g. `https://docs.sarvam.ai/changelog.rss`.

[Request a feature](mailto:support@sarvam.ai?subject=Sarvam%20feature%20request)

Select filters

Oct 14, 2026

### [Volume Adjustment for Voice Agents](https://docs.sarvam.ai/changelog/2026/10/14)

You can now control how loud your voice agent sounds. A new **Volume** slider in the agent’s voice settings (Sarvam / Bulbul voices) sets the loudness of the agent’s speech, from `0.7` (quieter) to `2.0` (louder), with `1.0` as the natural level. The volume is stored with the agent’s voice configuration and applied on every call, so it can be set once and manipulated later. See [Speakers & voice](https://docs.sarvam.ai/voice-agents/build/voice-language#volume).

Voice Agents

Oct 12, 2026

### [Instant Voice Cloning in the Python and TypeScript SDKs](https://docs.sarvam.ai/changelog/2026/10/12)

The [`sarvamai`](https://pypi.org/project/sarvamai/) Python and TypeScript SDKs now expose **Instant Voice Cloning** (beta) with the same call shape as Bulbul Text-to-Speech: `voice_cloning.convert` / `voiceCloning.convert` for one-shot synthesis, `convert_stream` / `convertStream` for HTTP streaming, and `voice_cloning_streaming` / `voiceCloningStreaming` for WebSocket sessions (`configure` → `convert` → `flush`). Voice lifecycle helpers (`create_voice`, `list_voices`, `get_voice`, `delete_voice`) live on the same `voice_cloning` client. Paths stay under `/voices/*`. Requires the `text_to_speech_voice_cloning` capability. See the [Instant Voice Cloning overview](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview) and install `sarvamai` ≥ `0.1.37` (Python) or `sarvamai` ≥ `1.1.12` (TypeScript). Older alphas such as `0.1.31a7` do not include the full streaming APIs.

Model APIs

Oct 10, 2026

### [Updated Pricing for Language Models](https://docs.sarvam.ai/changelog/2026/10/10)

Language model prices have changed. `sarvam-105b` and `sarvam-105b-conversations` now cost ₹15 input, ₹5 cached input, and ₹60 output per 1M tokens. `gemma4` is now ₹35 / ₹10 / ₹90. `glm5.3` cached input and output drop to ₹20 and ₹390, and input stays at ₹126. `deepseekv4.1-flash` is now ₹25 / ₹0.5 / ₹105. See [Pricing](https://docs.sarvam.ai/api/getting-started/pricing) for the full table.

Model APIs

### [Session Affinity for Chat Completion V2](https://docs.sarvam.ai/changelog/2026/10/10#2026-10-10-session-affinity-for-chat-completion-v2)

`POST /v2/chat/completions` now accepts an optional `x-session-affinity` header on the `gemma4` model. Send the same session ID on every turn of a conversation, and later turns can reuse cached prompt context for lower latency. Session IDs are scoped to your API subscription, and requests without the header work as before. See [Session affinity](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview#session-affinity-for-multi-turn-conversations).

Model APIs

Oct 6, 2026

### [Bulbul V4 for Voice Agents](https://docs.sarvam.ai/changelog/2026/10/6)

Bulbul V4 is now available for Voice Agents, alongside Bulbul V3. The voice picker is now a filterable catalog: browse and preview voices, filter the list to find the right fit, and choose between Bulbul V3 and Bulbul V4 per agent. See [Speakers & voice](https://docs.sarvam.ai/voice-agents/build/voice-language).

Voice Agents

### [New Voice Names in Bulbul V4](https://docs.sarvam.ai/changelog/2026/10/6#2026-10-06-new-voice-names-in-bulbul-v4)

Voices in Bulbul V4 carry new, more descriptive display names: **Shubh** is now **Shubh - Hinglish Ad Voice** and **Ritu** is now **Ritu - Hindi Support Agent**. The full V3-to-V4 name mapping is in [Speakers & voice](https://docs.sarvam.ai/voice-agents/build/voice-language#voice-name-changes-from-v3-to-v4).

Voice Agents

Oct 4, 2026

### [New and Improved Extract](https://docs.sarvam.ai/changelog/2026/10/4)

Extract is now more accurate across Indic, English, and mixed-language documents, with lower latency and support for longer documents. Every extracted value now includes a citation to its source, viewable in the UI, so each field can be verified at a glance. Extract rate limits have also been increased. Get started with the [Document AI overview](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview).

Doc Agents

Oct 1, 2026

### [Instant Voice Cloning Streaming](https://docs.sarvam.ai/changelog/2026/10/1)

Instant Voice Cloning (beta) now supports streaming audio. Use `POST /voices/clone/stream` for a single binary HTTP stream, or `GET /voices/clone/ws` for a persistent WebSocket that accepts incremental text. See the [HTTP streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/http-streaming) and [WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/websocket-streaming) guides, or the [API Reference](https://docs.sarvam.ai/api-reference/voice-cloning/clone-stream).

Model APIs

Sep 26, 2026

### [Dubbing API Now Available](https://docs.sarvam.ai/changelog/2026/9/26)

The Dubbing API is now available for programmatically localizing audio and video while preserving each speaker’s voice. Learn how to create and manage dubbing jobs in the [Dubbing API documentation](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview), or explore the endpoints in the [API Reference](https://docs.sarvam.ai/api-reference/creative-agents-dubbing/create-dub).

Content Studio

### [Voice Cloning API Now Available](https://docs.sarvam.ai/changelog/2026/9/26#2026-09-26-voice-cloning-api-now-available)

The Voice Cloning API is now available for generating speech in a cloned voice from a short reference recording. Get started with the [Voice Cloning API documentation](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview), or explore the endpoints in the [API Reference](https://docs.sarvam.ai/api-reference/voice-cloning).

Content Studio

Sep 23, 2026

### [Invite Teammates from Workspace Settings](https://docs.sarvam.ai/changelog/2026/9/23)

Workspace owners can now invite people directly from the workspace members page, with the workspace pre-selected, instead of going through organisation-level settings.

Cowork

### [Slack Connect Made Simple](https://docs.sarvam.ai/changelog/2026/9/23#2026-09-23-slack-connect-made-simple)

Connecting an agent to Slack no longer means creating a Slack app by hand and pasting secrets into a form. Copy one command into your Slack workspace, approve the permissions, and you are done - no Slack dashboard required.

Cowork

### [Live Voice Input](https://docs.sarvam.ai/changelog/2026/9/23#2026-09-23-live-voice-input)

Added live voice input: words appear on screen while you are still speaking, instead of recording a clip and waiting for it to be transcribed. The 30-second limit is gone; you can speak for up to five minutes in one go.

Cowork

Sep 22, 2026

### [Share Files by Link](https://docs.sarvam.ai/changelog/2026/9/22)

You can now share any file your agent creates with a link - from the chat card, the Files panel, or the preview. Choose who can open it (your workspace, your organisation, or anyone with the link) and change the audience later without breaking the link. Recipients see a clean page with just the file, and public links need no account.

Cowork

### [Faster, Complete Outputs on Big Tasks](https://docs.sarvam.ai/changelog/2026/9/22#2026-09-22-faster-complete-outputs-on-big-tasks)

Agents now finish multi-step jobs faster by batching their work into a single pass instead of one step at a time. Long results from sub-tasks, such as a full report or a long rewrite, now arrive complete instead of being cut off and redone from scratch.

Cowork

### [Keyterm Prompting on Streaming WebSockets](https://docs.sarvam.ai/changelog/2026/9/22#2026-09-22-keyterm-prompting-on-streaming-websockets)

`keyterms` is now supported on the streaming WebSocket endpoints — `/speech-to-text/ws` (legacy) and `/speech-to-text-realtime/ws` (realtime) — with `model="saaras:v4"`, matching the existing REST and Batch behaviour. Pass a JSON-encoded list of up to 50 terms (64 characters each) as the `keyterms` query parameter when opening the connection. See [Keyterm Prompting](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/keyterms).

Model APIs

Sep 21, 2026

### [Scheduled Agents Deliver Their Files](https://docs.sarvam.ai/changelog/2026/9/21)

Fixed an issue where agents on a schedule, such as a daily report, posted their text but dropped the files they created. Files now arrive with the message, every time. See [Scheduled Tasks](https://docs.sarvam.ai/cowork/build/scheduled-tasks).

Cowork

Sep 18, 2026

### [Edit Parts of an Artifact by Commenting](https://docs.sarvam.ai/changelog/2026/9/18)

You can now change a specific part of an artifact your agent built by commenting on it directly. Turn on Comment in the preview, click the block or button you want changed, and type your feedback. Each comment attaches to that element and reaches the agent with your next message, so you no longer have to describe where the problem is.

Cowork

### [A Richer Message Composer](https://docs.sarvam.ai/changelog/2026/9/18#2026-09-18-a-richer-message-composer)

The message box now has two quick commands: @ to mention an agent, and / to pull in skills, knowledge bases, and connectors. What you pick is attached right where you are typing, so the agent gets what it needs without you configuring it elsewhere.

Cowork

Sep 17, 2026

### [Tests for Voice Agents](https://docs.sarvam.ai/changelog/2026/9/17)

Agents can now be regression-tested with [Tests](https://docs.sarvam.ai/voice-agents/build/tests): describe the conversations that matter as test cases, and the platform plays a simulated user against a committed version of your agent while an AI judge grades each expected behavior `Pass` or `Fail`. Suites carry shared variables and global guardrails, runs execute each case up to 20 times to expose flakiness, and every execution returns the full transcript with per-behavior reasoning. The same suites can be created, run, and read over REST — see the [Tests API overview](https://docs.sarvam.ai/voice-agents/api/tests/overview) and [Best practices](https://docs.sarvam.ai/voice-agents/api/tests/best-practices).

Voice Agents

[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  *     * [Changelog](https://docs.sarvam.ai/changelog "Last updated today at 12:00 AM")



  * [Changelog](https://docs.sarvam.ai/changelog)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


