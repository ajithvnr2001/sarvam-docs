---
url: https://sarvam.ai/blogs/introducing-saaras-v4/
title: Introducing Saaras V4 speech recognition | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:19.620953+00:00
---

# Introducing Saaras V4 speech recognition | Sarvam AI

> Source: https://sarvam.ai/blogs/introducing-saaras-v4/

  1. [ Home ](https://sarvam.ai/)
  2. /
  3. [ Blog ](https://sarvam.ai/blogs)



# Introducing Saaras V4

The Next Leap in ASR for a Multilingual World

AnnouncementProduct

* * *

Sep 25, 2026·6 min readShare

![Introducing Saaras V4](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/e90bbe68a55d47ad208848a7b12a1b4c07378605-3840x2160.png)

We are releasing Saaras V4, the latest generation of our speech recognition model.

This post covers the work behind Saaras V4, including the data used to train it, our pre-training approach, the architectural and decoding changes that support multiple output modes, and the evaluation methodology behind our results. We also report benchmark performance across Indian languages, English, and challenging real-world speech conditions.

## Highlights

  * Saaras V4 uses an audio encoder, and an LLM decoder. The LLM decoder is a 3B hybrid state space model completely trained from scratch in-house
  * Saaras V4 achieved SOTA performance on all 22 Indian languages and reaffirms our commitment to even the most low-resource Indian languages
  * Saaras V4 achieves lowest WER on seven global English datasets, six being foreign English dialects and one being Indian English
  * You can choose the format that works best for you: Saaras V4 supports five transcript formats: transcribe, translate, verbatim, translit, and codemix
  * Saaras V4 is robust to noisy audios and code mixing. It also handles dialectical variation seamlessly
  * Its language identification is also best-in-class: a 2.9% error rate across the top ten Indian languages, and 5.22% across all 22



## Inside Saaras V4

Saaras V4 pairs an audio encoder with a 3B hybrid state-space language model that we trained from scratch in-house. 

We designed the system to handle the range of speech we see in practice, including code-mixing, dialectal variation, and noisy audio, while supporting five different ways of representing the same speech: verbatim transcription, normalized text, code-mixed text, transliteration, and translation.

Input waveform

Audio encoder

Self attention

MLP

Self attention

MLP

Audio embeddings

Temporal-downsampling adapter

shorter sequence, decoder embedding space

Emitted tokenstranscript tokens

और

जिस

तरह

से

टी

Autoregressive decoder backbonecausal LLM | 3B parameters

Audio features

+

pleasetranscribe

Text features · prompt

औरजिसतरहसे

Previously emitted tokens, fed back

Input waveform

Audio encoder

Self attention

MLP

Self attention

MLP

Audio embeddings

Temporal-downsampling adapter

shorter sequence, decoder embedding space

Audio features

+

pleasetranscribe

Text features · prompt

+

औरजिसतरहसे

Previously emitted tokens, fed back

Autoregressive decoder backbonecausal LLM | 3B parameters

Emitted tokenstranscript tokens

औरजिसतरहसेटी

Figure 1. Overview of our approach: The input audio waveform goes into an audio encoder, which produces audio embeddings that capture phonetic and acoustic detail. A temporal-downsampling adapter compresses these along the time axis and projects them into the language model's embedding space, so even long recordings stay within the context budget. The in-house Sarvam-3B autoregressive decoder then reads these audio features alongside the prompt as text features, and emits the transcript token by token, with each token fed back as input for the next.

### **Performance across English benchmarks**

We evaluated Saaras V4 across seven English speech recognition benchmarks covering Indian English, international accents, meetings, media, finance, and other real-world speech settings. Across these datasets, Saaras V4 achieves the lowest average word error rate.

AMI

Meeting rooms, far-field microphones

GigaSpeech

Podcast, audiobook, web video

LibriSpeech clean

Read speech, studio conditions

LibriSpeech others

Read speech, harder acoustics

SPGISpeech

Earning calls, financial vocabulary

VoxPopuli

European Parliament speeches

Svarah

Indian-accented English

  
**Evaluation methodology**

  * Six international: taken as published at HuggingFace's [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)Open ASR Leaderboard](https://huggingface.co/datasets/hf-audio/open-asr-leaderboard)
  * One Indian accented English: [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)Svarah](https://huggingface.co/datasets/ai4bharat/Svarah) published by AI4Bharat
  * Normalization and scoring follow the Open ASR Leaderboard's [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)code](https://github.com/huggingface/open_asr_leaderboard)



## Indic Benchmarks for Saaras V4:

### Vistaar

We evaluate Saaras V4 on [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)Vistaar](https://github.com/AI4Bharat/vistaar) across ten Indian languages and report both standard Word Error Rate (WER) and LLM-WER.

WER remains the standard deterministic measure for speech recognition, counting substitutions, deletions, and insertions between the reference and predicted transcript. In Indic-language settings, however, some of these differences can be orthographic or formatting variations that do not materially change the spoken content.

To account for this, we also report [![](https://www.google.com/s2/favicons?domain=www.sarvam.ai&sz=32)LLM-WER](https://www.sarvam.ai/blogs/evaluating-indian-language-asr), which adds a semantic adjudication step to determine whether a mismatch changes the meaning of the transcript or simply represents the same content differently.

The two metrics are therefore complementary. WER provides a reproducible baseline, while LLM-WER gives a more faithful view of errors that affect the underlying speech content.

### Detailed breakdown of various benchmarks:

### Benchmark WER by dataset

Lower is better

Common VoiceFleursGramvaaniIndicTTSKathbathKathbath NoisyMUCS

Contains crowd-sourced read speech from the Mozilla Foundation's Commonvoice.

#### Audio examples

BengaliGujaratiHindiKannadaTamilTelugu

BengaliCommon Voice

Saaras V4স্বামীকে প্রণাম করার পর তাকিয়ে দেখেন স্বামী আর সেখানে নেই.

11 Labs Scribe v2ছামকে প্রলাম করা সহজ। তাকে দেখেন ছামিয়া যেখানে.

Deepgram Nova3থামটি প্রদান করার পর তাকে ডাকেন থামিযা ফিফা নেই.

GPT-4o Transcribeসমকীয় পনাম কলার প্রাক আখিয়ান্যাপন.

BengaliIndicTTS

Saaras V4সিপিএমের রাজীববাবু বলেন আড়তে আমার পৈতৃক ব্যবসা.

11 Labs Scribe v2সিপিএমের রাজীব বাবু বলেন, আরতে আমার পৈত্রিক ব্যবসা.

Deepgram Nova3সিপিএমের রাজিববাবু বলেন আরতি আমার পৈতৃক ব্যবসা.

GPT-4o Transcribeসিপিএমে রাজীব বাবু বলেন, আরতে আমার পৈতৃক ব্যবসা.

### Five Modes, One Model

Different applications need different representations of the same speech. A compliance archive may need a verbatim transcript, while a CRM workflow may require normalized text and an analytics system may need an English translation. These transformations are often handled through separate post-processing steps, which add complexity and can introduce additional errors.

Saaras V4 handles these requirements within the model itself. From the same audio input, it can produce five transcript modes: verbatim, normalized, code-mixed, transliterated, and translated.

TranscribeNumerals normalized,  
punctuation restored

औरजिसतरहसेटी-20बैटिंगइवॉल्वकररहीहै,इससीज़नयहीदेखाहैहमलोगोंनेविराटकोहलीकेसाथभी।

Code-mixedNative script, English words  
in English

औरजिसतरहसेT20battingevolveकररहीहैइसseasonयहीदेखाहैहमलोगोंनेViratKohliकेसाथभी।

TransliterationThe whole utterance in  
English script

AurjistarahseT20battingevolvekarrahihai,isseasonyahidekhahaihumlogonneViratKohlikesaathbhi.

TranslationFaithful English  
translation

AndthewayT20battingisevolving,wehaveseenthesamethisseasonwithViratKohliaswell.

VerbatimEvery word  
as spoken

औरजिसतरहसेटीट्वेंटीबैटिंगइवॉल्वकररहीहैइससीज़नयहीदेखाहैहमलोगोंनेविराटकोहलीकेसाथभी

  * **Verbatim:** The exact transcription in the native script of the spoken language
  * **Transcribe:** The exact transcription in the native script of the spoken language with numbers and dates normalised
  * **Codemix:** Transcribe mode plus keeps native english words in english to improve legibility
  * **Translit:** Does transcription but in english script. Colloquially referred to as “WhatsApp language”
  * **Translate:** The English translation of the audio with numbers normalized



Because all five come from one model, there are no extra pre-processing steps that could lead to cascading of errors.

### Beyond the transcription

#### a. Best in class Language Identification

Saaras V4 can identify the spoken language directly from the audio and transcribe it in the corresponding native script, without requiring the language to be specified in advance. On verified IndicVoices utterances, language identification error is 5.22% across all 22 Indian languages, falling to 2.9% across the ten most widely spoken languages.

#### b. Keyterm prompting

Keyterm prompting lets you bias transcription toward words or phrases that are easy to miss, such as product names, people’s names, acronyms, or domain-specific terminology.

Validated as best on [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)ai4bharat/IndicContextEval](https://huggingface.co/datasets/ai4bharat/IndicContextEval) (Interspeech 2026): Saaras V4 reaches the lowest WER of **16.03%** in the L5 (keyword prompting) setting, where the domain-entity list is provided in native script along with the language. For dataset details and competitor scores, see the [![](https://www.google.com/s2/favicons?domain=arxiv.org&sz=32)paper](https://arxiv.org/pdf/2606.19157).

GujaratiHindi

Gujarati · field audio

Saaras 4 without keywords

ઢૂન માટે આંખનું કામ કરે છે અને દરેક વખતે

Saaras 4 with keywords

ડ્રોન માટે આંખનું કામ કરે છે અને દરેક વખતે

Reference keywords provided (24)

ડ્રોનસર્વેથ્રીડીમોડેલજનરેટરીઅલટાઇમકાઇનેટિક્સઆર ટી કેસ્કેલેબિલિટીમોડ્યુલારિટીસપોર્ટફ્યુચરએક્સપાન્શનઈઝીએડવાન્સપીએલસીટ્રાન્સડ્યુસરફ્લોમીટર્સલેવલસેન્સર્સપ્રોક્સિમિટીસેન્સર

#### c. Built For Real-World Audio

Field audio is compressed, clipped, and full of interference. These are conditions where systems trained on clean benchmarks often fall apart. Saaras V4 is designed to remain reliable under these conditions, including noisy audio, code-mixing, and dialectal variation.

Language| Condition| Format| Transcript  
---|---|---|---  
Hindi| Constant wind noise| Verbatim| ए एक बात सुनो ना मैडम दो दो दो दो दो दोनों मिलाकर  
Hindi| Distortion and clipping| Transcribe| सर आपको अपनी पॉलिसी के बारे में कुछ पूछना है? मैं आपसे ये पूछ रही थी कि।  
Hindi| Constant background| Codemix| होते हो। Nice to meet you brothers. Okay. Thank you. Bye. कुछ कुछ price तो ऐसा है कि जो  
Bengali| Heavy traffic| Translit| Maane ami ekta TV kinechilam ami ekta TV installmente niyechilam apnader bank hoyto erokom taka kate okhan theke ki koreche  
Kannada| Static noise| Translate| First, in our art, in our culture, first we built a temple. We used to live in huts. We built big, big temples. If you see it, it's a surprise even now. How they must have built it, for a thousand years, for two thousand years, this kind of thing, it's a surprise.  
English| Channel distortion| Transcribe| Oh, what a record to read! What a picture to gaze upon! How awful the fact!  
  
#### d. Low-latency streaming

For real-time voice applications, latency is as important as transcription quality. Saaras V4 supports streaming with time to first token below 150 ms, allowing downstream systems to begin responding with minimal delay and enabling more natural turn-taking.

It also handles long-form audio natively, with multi-minute recordings processed within a second.

## Integrating Saaras V4 into your platform

Integrate Saaras v4 into your application with a simple API key from the [![](https://www.google.com/s2/favicons?domain=indus.sarvam.ai&sz=32)Sarvam AI dashboard](https://indus.sarvam.ai/)

**Choose Your Integration Path:**

  * [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)**REST API**](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api) : Synchronous transcription for audio under 30 seconds
  * [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)**Batch API**](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) : Asynchronous processing for files up to 2 hours. Speaker Diarization can be enabled in batch mode
  * [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)**WebSocket (Real-time)**](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming) : Streaming transcription with partial results for live applications



**SDKs & Frameworks:**

Ready-to-use SDKs for Python 3.9+ and Node.js 18+. 

Framework integrations available for [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk), [![](https://www.google.com/s2/favicons?domain=docs.livekit.io&sz=32)LiveKit Agents](https://docs.livekit.io/agents/models/stt/sarvam/) and [![](https://www.google.com/s2/favicons?domain=docs.pipecat.ai&sz=32)Pipecat Agents](https://docs.pipecat.ai/api-reference/server/services/stt/sarvam)

**Output Modes:**

Configure transcription output: `transcribe` (default), `translate` (to English), `translit` (romanized), or `verbatim` or `codemix`

**Quick Start:**

See the [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)Developer Quickstart](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api) for code examples and authentication details

## One model across languages

With Saaras V4, you no longer have to trade off English performance against Indic language coverage. It delivers strong performance across both, while supporting low-latency streaming and reliable production workloads. This makes it possible to build multilingual voice applications with one ASR model.

Building voice agents?

End-to-end pricing with the models included, as low as ₹3 a minute. 

[ Explore Voice Agents pricing ](https://sarvam.ai/products/voice-agents/pricing)

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
