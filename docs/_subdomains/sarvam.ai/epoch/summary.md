---
url: https://sarvam.ai/epoch/summary/
title: Everything we announced at Sarvam Epoch | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:20.329739+00:00
---

# Everything we announced at Sarvam Epoch | Sarvam AI

> Source: https://sarvam.ai/epoch/summary/

![Sarvam Epoch](https://sarvam.ai/assets/epoch/epoch-logo.svg)

# Everything we announced

Last week, we held the first edition of Sarvam Epoch. It was energising to see the community come together at Epoch with such a strong sense of possibility.

The Builder Edition brought together developers and researchers for technical sessions and live demos. The Enterprise Edition brought together leaders from banking, government, and industry to explore what it takes to deploy AI across large organisations.

Across the two days, we shipped across the entire stack: model updates, an inference layer hosted in India, a self-serve agent platform, and partnerships designed to carry these capabilities into institutions across the country. This post covers everything we announced.

## Models and products

### Sarvam 105B

We released the first Sarvam 105B checkpoint in February. At Epoch, we released updated variants for conversational agents and work agents, the two use cases where we are seeing the most traction in India.

For conversational agents, standard public benchmarks are incomplete. They do not capture ambiguous messages, ASR noise, code-mixed speech, long policy documents, or instructions that must be followed many turns later.

We therefore evaluated the model on a production benchmark built from hundreds of millions of minutes of Indian conversations.

Capability| Sarvam 105B| GPT 5.4 Mini| Gemini 3.5 Flash  
---|---|---|---  
Voice-call capability| 82.1| 74.7| 78.9  
Instruction following| 63.4| 37.4| 52.4  
Tool calling| 78.8| 57.6| 71.8  
Linguistic quality, win rate| 61.3| 6.0| 32.7  
  
Scroll

Scroll

Sarvam 105B leads GPT 5.4 Mini and Gemini 3.5 Flash on all four measures, with the widest gaps in instruction following and linguistic quality, the two capabilities that decide whether a voice agent survives a real customer call. It does this at $0.80 per million blended tokens, against $4.50 for GPT 5.4 Mini and $9.00 for Gemini 3.5 Flash. Better on every measure, at a fraction of the price.

For work agents, we tuned a reasoning variant and evaluated it on HarnessBench: 106 sandboxed tasks across software engineering, data and finance, knowledge retrieval, office workflows, tool use, SRE, and long-running autonomy.

Against GLM 5.2, a 753B model, Sarvam 105B performs close enough that the most useful product decision is routing. In our own agent configuration, 36% of tasks route to Sarvam 105B and 64% to GLM 5.2, reducing serving cost by roughly 40%.

Both variants are available through the Sarvam API: one optimised for low-latency conversations, the other for complex tasks inside an agent harness.

### Sarvam Vision 2.0

Sarvam Vision 1.0 launched in February and has since digitised more than 35 million pages.

Vision 2.0 extends the model with native key-value extraction from tables and forms, Indic handwriting recognition, stronger complex-table parsing, and improved general OCR.

We also released Sarvam Vision Edge to bring these capabilities into customer environments through models customised for specific workflows. In a land-record digitisation workflow for the Government of Odisha, a custom model achieved 50% higher accuracy than the best general-purpose model tested on the same task.

### Saaras V4

Saaras V4 extends Sarvam's speech-recognition stack with five output modes from one model: verbatim transcription, normalised transcription, code-mixed output, transliteration, and translation.

It also adds multi-speaker ASR in a single pass, combining diarisation and transcription rather than running separate sequential systems. This is useful for call recordings, meetings, and interviews, where speaker attribution matters as much as the transcript.

Saaras V4 supports 22 Indian languages. And the best English ASR is now an Indian one: across seven standard suites, from LibriSpeech and GigaSpeech to Svarah for Indian-accented speech, it records the lowest average word error rate of any system tested.

### Bulbul V4 (Research preview)

Bulbul V4 is our most expressive text-to-speech model yet. Developers can shape how each line is spoken, guiding emotion, emphasis, pacing, and cues such as laughter as the audio is generated.

This brings more control to voice agents, creator tools, dubbing, education, accessibility, and media. It is especially valuable in enterprise settings, where names, amounts, product terms, and tone must be delivered clearly and accurately.

### Custom Model Training

We're introducing Custom Model Training for organisations that want models specialised on their own data, policies, and workflows. We manage training on infrastructure in India and deliver the trained weights to the organisation, bringing our experience in managing GPU fleets efficiently and running optimised model training pipelines.

We work with organisations to train smaller, task-specific models that can reduce latency and inference costs compared with using a larger general-purpose model for every request.

Throughout the engagement, the organisation's training data stays isolated and is never used to train Sarvam's own models. Once training is complete, the resulting weights are delivered to and owned by the organisation, which retains full control over how the model is deployed and modified.

### Sarvam Inference

Sarvam Inference is our serving layer for Sarvam models and frontier open-weight models, run from data centres in India. Developers get access to the best open models. Enterprises get data residency and compliance with Indian regulations by default.

The lineup includes GLM 5.2 and Gemma 4 31B, served at price-performance competitive with any global provider. GLM 5.2 runs at up to 80 tokens per second, and Gemma 4 31B at 0.63 seconds p50 time to first token.

The performance comes from the systems work underneath. Our inference team optimises kernels, disaggregates prefill and decode, manages KV cache across workload types, and trains speculator models.

All of it runs on the first fleet of Blackwell GPUs in India, and the fleet is growing over the coming months. As new open models release, we will serve them from day one, with the reliability and pricing enterprises plan around.

Gemma 4 31B

Output tokens per second per stream | faster upward

Blended 7:2:1 price per million tokens | cheaper to the left

Same story on every open-model board · OpenRouter P50 of real traffic

  * GLM 5.2

#1 speed · #1 TTFT

160 t/s · 0.75 s TTFT · next best 64 t/s

  * Kimi K3

#1 speed · #1 TTFT

71 t/s · 0.62 s TTFT




> We can absorb latest OSS models & optimize its inference within 3 days of launch.

## Indus

Indus is one platform for all your AI work. A single workspace, multiple agents. Voice Agents for conversations, Work Agents for employees, Document Agents for paperwork, Content Studio for media, and Coding Agents for engineering.

### Voice Agents

Our voice agents have spoken over 325 million minutes, delivering business outcomes at a fraction of the cost of human agents.

A business team can describe the goal of an agent in plain language, simulate a thousand calls against it, and be live on a phone number in under two hours, with the entire stack deployable inside the enterprise's own VPC where compliance demands it.

Agents can also run as an orchestrated fleet toward a goal, one explaining, one negotiating, one closing, and they improve with every conversation. The analytics go past call summaries into deep business insights: which offer converted, which cohort slipped, where the next crore of collections will come from. All of it at a cost and latency built for Indian volumes.

Voice Agents are now generally available, with no waitlist, at ₹3.50 per minute with authoring, simulation, phone numbers, evaluation, and analytics included.

![Voice Agents analytics dashboard with call distributions, conversation insights, and language breakdown](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/pages/epoch-recap/voice-agents-ui.png)

### Work Agents

Work Agents give an enterprise a fleet of AI coworkers it can build, manage, and integrate with its existing systems and data. Each one drafts, researches, analyses, and runs processes alongside a marketing, data, or developer team. It executes code in a sandboxed environment, produces finished artifacts, a report, a dashboard, a working application, and operates under enterprise-grade security and compliance. Work Agents are live now.

### Content Studio

Content Studio brings together multilingual content creation and transformation in one platform.

Content Studio includes AI voices, voice cloning, transcription, video dubbing and live translation. These capabilities can be used independently or combined into larger content workflows.

For dubbing, the system is designed to preserve emotion, maintain speaker consistency and produce native-sounding, lip-sync-ready audio.

### Sarvam Code

Introducing Sarvam Code, now in early beta. We are entering a category with many great products, with a specific view: code generation is improving quickly, but code velocity is not consistently translating into product outcomes. Duplicate code is accumulating, code review is becoming a bottleneck, and long-running tasks on frontier models can become expensive.

Sarvam Code is built to optimise cost per completed task. It routes work across 100B, 700B, and 3T-scale models, stays on complex tasks until they are complete, uses tooling designed for each model, and manages context without repeatedly processing the same codebase.

It includes skills for frontend development, data and ML, and cybersecurity, alongside custom skills for systems such as Finacle, SAP, and internal systems of record. The harness builds on Codex, while the broader stack learns from workflows and traces inside your infrastructure to improve routing and support specialised models for ITOps, NetworkOps, and CloudOps. It can run in India, in your VPC, or on-premises.

### Sarvam Cyber

At Epoch, we previewed Sarvam Cyber, an AI security agent that helps teams find, investigate, and remediate vulnerabilities across complex systems. It traces issues across environments and connects related findings, giving security teams a clearer path from discovery to resolution.

We are also building security skills and tools, working with startups and domain experts in cybersecurity. The same harness that plans and verifies coding work turns out to investigate well: it maintains a hypothesis ledger, finds vulnerabilities, and chains findings together to prove exploitability, rather than just flagging possibilities.

Working this way, we have already found vulnerabilities in widely used consumer platforms in India. We are working with the affected teams under responsible disclosure to get them patched quickly.

### Anvaya in a Box

Anvaya is an investigation agent for defence, intelligence, government, and financial institutions, where accuracy, deployment control, and data security are non-negotiable.

It runs on-premise, in air-gapped environments, and across varied hardware. Point it at documents, audio, video, images, and structured data, and it builds a unified data layer over all of it, with an ontology, entity schema, and knowledge graph that track provenance.

### Kivi

Kivi is a voice app that lets you speak to your computer and get things done across any application. Write messages in WhatsApp, draft documents in Docs, work through spreadsheets, build apps in Sarvam Code, or direct AI in Sarvam Work, all by speaking naturally. Kivi understands 22+ Indian languages, including code-switching, and turns what you say into clear, accurate text or action. It is voice as an interface for everything you do on your computer.

[Kivi for Mac is now available. Windows, Android, API, and MCP access are next.](https://heykivi.ai)

### Smart Glasses

Kaze is a smart-glasses system that brings Sarvam's speech, vision, and language models into a wearable interface. It supports 22 Indian languages, including code-switching, and uses cloud and edge models to work in low-network environments.

## After Epoch

Much of what we announced is open to try now, and the rest is rolling out in the weeks ahead. Start at docs.sarvam.ai, and if something in this post is not available yet, it will be soon.

![Sarvam Epoch gift box on stage at the Bengaluru conference](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/pages/epoch-recap/epoch-box-on-stage.jpg)

[Go to Sarvam Dashboard](https://indus.sarvam.ai)[Go to docs.sarvam.ai](https://docs.sarvam.ai)
