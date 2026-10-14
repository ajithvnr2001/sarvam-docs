---
url: https://www.sarvam.ai/blogs/sarvam-edge/
title: Announcing Sarvam Edge | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:20.764249+00:00
---

# Announcing Sarvam Edge | Sarvam AI

> Source: https://www.sarvam.ai/blogs/sarvam-edge/

  1. [ Home ](https://www.sarvam.ai/)
  2. /
  3. [ Blog ](https://www.sarvam.ai/blogs)



# Announcing Sarvam Edge

Powering on-device intelligence

Research

* * *

Feb 14, 2026·9 min readShare

![Announcing Sarvam Edge](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/42d675e333219227dd0a6872d6405088722eb6e1-2400x1800.png)

Intelligence should work everywhere. Not summoned from distant servers, not gated behind connectivity, not metered by the query. Just there, immediate and local, working at the speed of thought. The devices in your hands have the compute power to run sophisticated models. What's been missing are models actually designed to run there.

Today, we’re announcing Sarvam Edge, our dedicated effort to bring intelligence to devices and remove barriers to access.

The question is no longer whether India can train powerful models. The question is whether they can run everywhere, every day. The next phase of AI will not be defined by model size, but by deployment at national scale, cost-efficient inference, domain adaptation, and integration into everyday devices. At its core, it comes down to access.

**Responses are instant.** There's no round trip to a data center, no queueing behind other users, no variance based on network conditions. The model is already there, ready to run the moment you need it.

**Your data never leaves your device.** When you process a document, translate a conversation, or ask a question, that information stays local. There's no server logging your queries, no database storing your conversations, no privacy policy to parse. The model runs, produces a result, and that's it.

**It works everywhere.** On a flight. In a rural area with intermittent connectivity. During a network outage. When you're bandwidth-constrained or when cloud services are unavailable. It works because your device works.

**The economics are different.** There is no per query cost, no usage based pricing, no scaling concerns as your user base grows. The inference cost is already paid. It is embedded in the device. This changes what becomes possible. AI can reach contexts where cloud costs would otherwise be prohibitive. Education tools for students, productivity software for small businesses, assistive technologies for underserved communities all become possible.

Sarvam Edge is being developed in close collaboration with leading global device manufacturers, bringing model design and hardware evolution into the same conversation. When inference moves to devices, something fundamental shifts. The model becomes part of your device, not a service you access. It is designed to run on the devices people already have. That means rethinking everything. Architecture choices that prioritize efficiency over raw parameter count. Training techniques that produce models that compress well without losing capability.

In this blog, we detail the models powering Sarvam Edge, including speech recognition, speech synthesis, and multilingual translation built for on-device inference.

## **Speech Models on the Edge**

### **Speech Recognition**

The speech recognition engine **delivers production-grade, on-device transcription specifically engineered for the Indian market.** By processing entirely at the edge, the system provides high-accuracy speech-to-text for the 10 most popular Indic languages without cloud dependency, ensuring absolute data privacy and operational reliability.

At the core of the system is a **single unified multilingual model** that supports 10 most popular Indian languages within one compact footprint. Instead of maintaining separate models per language, the system uses one efficient architecture capable of automatic language identification, eliminating manual user selection and enabling seamless multilingual interaction.

This compact model features a highly efficient architecture that delivers transcription accuracy competitive with leading server-side cloud systems:

  * Model parameters: 74M
  * On-device footprint: ~294MB (FP16)



#### **Cost, Latency and Memory**

Time-to-first-token is maintained under 300 milliseconds, enabling a responsive streaming experience suitable for real-time applications. The inference stack achieves a real-time factor of approximately 0.12 (RTFx 8.5) as measured on Qualcomm’s Snapdragon 8 Gen 3 mobile chip, allowing speech to be processed faster than real time.

Because inference runs entirely on device, there is no dependency on network availability and no per-query cloud cost.

#### **Accuracy**

The architecture was designed around real-world speech conditions. It maintains high accuracy on 8KHz audio typical of telephony systems and voice recorders. It handles multi-speaker environments, including overlapping speech, and remains resilient in noisy backgrounds rather than assuming controlled acoustic settings.

Accuracy extends beyond phonetic transcription. The system preserves Indian proper nouns, regional names, and entities with high fidelity. A built-in inverse text normalization engine converts spoken forms into correct written conventions, formatting numbers, dates, currencies, and temperature units appropriately. Punctuation and alphanumeric expressions remain grammatically consistent and readable, producing output that can be used directly.

The model has been rigorously benchmarked against the [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)Vistaar dataset](https://github.com/AI4Bharat/vistaar), a comprehensive suite of 59 test environments spanning diverse domains such as news, education, and tourism. This evaluation demonstrates competitive Word Error Rates (WER) and Character Error Rates (CER) across the supported Indic languages.

To establish a performance baseline, we compare our Edge ASR Model with cloud models Saarika v2.6 and Google Cloud STT, while native on-device support for Indian languages continues to develop.

### **Speech Synthesis**

Speech Synthesis provides reliable text-to-speech directly on device, without requiring an internet connection. It supports 10 Indian languages and 8 multilingual speakers using a single compact model, while maintaining low latency, intelligible realistic speech and consistent voice identity across languages. This is a single unified model, which supports multiple speakers and all the languages. While it allows for compact and easy deployment, it also improves the quality of outputs by allowing speakers to be multilingual.

The model specifications are given below

  * Model parameters: 24M
  * On-device footprint: ~60MB



The model is designed to remain compact enough for practical deployment. The model features the ability of all the speakers to maintain similar voice identity across languages, as shown by high speaker similarity, both for intra-language and cross lingual generations. This is measured by generating multiple audios for each speaker, using _[![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)Speechbrain ECAPA-TDNN](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) model to get embeddings for each audio, and calculating average cosine scores between these._

#### **Cost, Latency and Memory**

The model contains 24 million parameters, representing the total learned weights. The final deployable file size on the device is approximately 60MB.

Time to First Audio (TTFA) for the model is 260 milliseconds, measured from text input to the first audible output. The model achieves a Real-Time Factor (RTF) of 0.19, meaning audio is generated approximately 5.2× faster than real time. Streaming inference allows playback to begin before full sentence generation is complete.

All latency and throughput benchmarks were measured on a Samsung Galaxy S25 Ultra.

#### **Accuracy**

Character Error Rate (CER) measures transcription error after generated speech is re-evaluated using an automatic speech recognition system. Lower values indicate clearer, more intelligible output.

The model achieves an overall mean CER of 0.0173 on the [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)sarvamai/tts-general-benchmark ](https://huggingface.co/datasets/sarvamai/tts-general-benchmark)dataset from the Bulbul V3 release. Across all languages, CER remains consistently low, indicating that synthesized speech is reliably understood for all the languages.

This benchmark matters because it evaluates whether generated speech is not only natural-sounding, but also linguistically precise. Low CER indicates that the spoken output preserves the intended words and structure, reducing downstream errors in voice interfaces and assistive systems.

ASR evaluations were performed using Sarvam Audio.

#### **Custom Voice Cloning**

Speech Synthesis supports onboarding custom voices within the same unified multilingual model. With approximately one hour of curated speech data, a new speaker can be adapted to work across supported languages while maintaining consistent identity.

The adapted voice remains deployable on device within the same ~60MB footprint, preserving the same memory and latency characteristics as the base model.

### **Translation Models on the Edge**

Translation on the Edge provides high-performance multilingual neural machine translation directly on device. It supports 11 languages, including 10 Indian languages and English, enabling bidirectional translation across 110 language pairs without pivoting through an intermediate language.

The system runs from a single unified multilingual model rather than maintaining language-specific checkpoints. This simplifies deployment while allowing cross-lingual transfer learning across all supported languages.

#### **Cost, Latency and Memory**

The multilingual model is approximately 150 million parameters in size, with a memory footprint of about 334MB on-device. The design balances translation quality with deployability, making full multilingual translation practical on modern mobile hardware.

Benchmarked on a Qualcomm Snapdragon 8 Gen3 processor, Time to First Token (TTFT) is approximately 200 milliseconds, enabling near-instant responses in interactive settings. Streaming throughput reaches approximately 30 tokens per second, supporting smooth real-time translation even for longer sentences.

Tokenization efficiency plays a key role in latency. By minimizing fertility, or tokens per word, across all 11 languages, the system reduces decoder workload and lowers total inference time per sentence.

Because inference runs entirely on device, translation does not depend on network availability and incurs no per-query cloud cost.

#### **Accuracy**

The model is built to handle real-world inputs. It supports normalization of dates and currencies, processes noisy inputs such as spelling errors and chat-style language, and handles complex alphanumeric formatting. Code-mixed and colloquial expressions are supported natively.

Users can also control numeral style in the output, toggling between international Hindu-Arabic numerals, such as “100 रुपये,” and native Indic numerals, such as “१०० रुपये.” This allows translations to adapt to audience and context without retraining.

Evaluation demonstrates strong translation accuracy across supported languages. Compared to a 600M parameter state-of-the-art open-source multilingual edge model, this model achieves competitive or superior quality with a 4× smaller size.

This matters because translation quality must be maintained under strict memory and latency constraints. Reducing model size while preserving accuracy improves deployability without sacrificing user experience.

## Edge in Action

### Sarvam Vision OCR on a Macbook Pro

The demo begins by uploading an Odia image file, with transcription running entirely locally on a MacBook Pro. The system operates fully offline, with internet connectivity turned off. It sustains transcription speeds of over 40 tokens per second while maintaining peak memory usage below 10GB, demonstrating efficient on-device speech recognition within consumer hardware constraints.

### Stock Brokerage App on Android

The demo showcases the full spectrum of agentic capabilities in a voice-driven financial assistant, all running locally on the device. Users interact naturally through speech to retrieve their portfolio overview, check current stock holdings, view balances, execute transactions such as buying or selling specific stocks, conduct market research, assess overall market trends, and receive real-time stock price quotes.

All voice interactions, including speech recognition for understanding user commands and text to speech for delivering responses, are processed entirely on-device without cloud connectivity. This ensures fast response times, complete privacy, and reliable performance even when offline.

### Real-time Voice Translation

This demo shows real-time voice translation between Indian languages. You speak in your preferred language, and the system translates and responds in another, preserving both meaning and natural delivery. Speech recognition, translation, and expressive text-to-speech work together seamlessly.

## And the edge is where it begins

When intelligence is built into the core of the device, performance improves, latency drops, and privacy strengthens. AI becomes truly native. Built into the devices people already carry.

That foundation unlocks a new class of products. AI-enabled glasses. Intelligent audio systems. Assistive wearables. Devices where intelligence is not an app, but a property of the hardware itself.

Sarvam Edge is building toward that shift.

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
