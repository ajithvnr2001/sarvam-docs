---
url: https://sarvam.ai/blogs/indic-diarbench/
title: Indic DiarBench: joint diarization-ASR benchmark | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:20.170655+00:00
---

# Indic DiarBench: joint diarization-ASR benchmark | Sarvam AI

> Source: https://sarvam.ai/blogs/indic-diarbench/

  1. [ Home ](https://sarvam.ai/)
  2. /
  3. [ Blog ](https://sarvam.ai/blogs)



# Indic DiarBench: A Joint Diarization-ASR Benchmark Dataset for Indian Languages

The first open benchmark dataset for joint ASR and speaker diarization across all 22 scheduled Indian languages.

ResearchOpen source

[Explore on 🤗](https://huggingface.co/datasets/sarvamai/indic-diarbench)[Read the paper](https://arxiv.org/abs/2607.23808)

* * *

Aug 11, 2026·5 min readShare

![Indic DiarBench: A Joint Diarization-ASR Benchmark Dataset for Indian Languages](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/e00f774b891123262917618947365156c3ddeaa5-2016x1260.png)

Speech recognition benchmark datasets have evolved significantly in recent years, but there is still a gap. Most major datasets, especially for Indian languages, contain audio where only one person speaks at a time. Real conversations look very different. Meetings, podcasts, debates, and customer-support calls often involve interruptions, rapid turn-taking, and overlapping speech. As a result, a model can perform well on a single-speaker dataset but struggle when people are speaking over each other.

This becomes even more important as speech systems move towards **joint speaker-attributed ASR** , systems that need to determine both **who spoke** and **what they said**.

Traditionally, these have been treated as two separate problems. Diarization identifies who spoke when, while ASR transcribes the speech.

But evaluating them separately can hide how errors in one affect the other. A system may transcribe the words correctly but assign them to the wrong speaker, or produce poor transcriptions when speech becomes short, choppy, and overlapping.

A conventional ASR benchmark dataset provides transcripts but not speaker attribution, while a diarization benchmark dataset provides speaker turns but not verified transcripts. Neither can tell us whether the two work together on the same audio.

### The Missing Benchmark Dataset

AMI established a foundation for English meetings, while datasets such as CALLHOME, DIHARD, VoxConverse, AliMeeting, AISHELL-4, and NOTSOFAR-1 expanded coverage to more languages and increasingly realistic conversational settings.

But Indian languages have lacked a comparable open benchmark dataset for **joint ASR and diarization**.

**Sarvam, along with AI4Bharat, built Indic DiarBench to fill this gap.** It is the first open benchmark dataset for speaker-attributed ASR across all 22 scheduled Indian languages, built around natural multi-speaker conversations and designed to evaluate transcription output and speaker attribution together.

Dataset| Languages| Hours| Domain| Speakers| ASR  
---|---|---|---|---|---  
IndicDiarBench| 22 Indic| ~108| Mixed| 2–9| ✓  
CALLHOME| 6 languages| 20| Telephone| 2–6| ✓  
AMI| English| 100| Meeting| 3–5| ✓  
DIHARD III| Multiple| 33| Mixed| 1–10| –  
VoxConverse| Multiple| 70| YouTube| 1–21| –  
LibriCSS| English| 10| Simulated| 8| ✓  
AliMeeting| Mandarin| 118| Meeting| 2–4| ✓  
NOTSOFAR-1| English| 28| Distant meeting| 4–8| ✓  
DISPLACE '24| 5 Indic| 38| Conversation| 3–5| –  
  
Scroll

Scroll

Comparison of diarization evaluation datasets. Indic DiarBench is the first benchmark to cover all 22 scheduled Indian languages with jointly annotated ASR and diarization labels

### What Indic DiarBench Covers

The benchmark contains **108 hours of natural, spontaneous speech** across 22 Indian languages, covering:

  * **2-9 speakers** per recording, with rapid turn-taking, backchanneling, interruptions, and substantial speech overlap in the conversation
  * **Near-field and far-field meetings** , capturing both close mic and more challenging acoustic conditions
  * **In the wild conversations** from YouTube. This adds more noise and variability as found in real-world recordings
  * **Human-verified transcripts and speaker-attributed timestamps.** This is crucial for enabling joint evaluation of ASR and diarization



### How we built the Dataset

The goal was to capture conversations that sound less scripted and more natural.

Participants were given debate topics and quiz questions rather than scripts for the conversations. Warm-up discussions were discarded from the dataset. We kept the same-gender sessions deliberately to make speaker identification harder. All the recordings retained natural ambient sound and minimal noise cancellation was done. Language experts reviewed sessions for vocabulary diversity, overlap, and spontaneity as well.

For the in-the-wild portion of the dataset, we selected public multi-speaker conversations and filtered out content with sustained ads or music. This way we only kept recordings where speakers were visibly active and the conversation could be reliably annotated.

### What's in the Dataset

**Meeting conversations: ~81 hours**

These recordings include a lot of diversity. **485 unique speakers from 189 districts** across urban and rural India are present, covering a range of dialects and educational backgrounds.

  * **Near-field meetings:  
** This is ~53 hours, covering all 22 languages. Near field audio has speakers that are in close proximity to the microphone
  * **Far-field meetings:  
** This is ~27 hours. Here we have distant conference-style microphones so as to introduce reverberation, background noise, and overall more challenging acoustic conditions



**In-the-wild conversations:**

This is ~28 hours. This subset covers the 10 most-spoken Indian languages, with roughly two hours per language and around 750 unique speakers. This part of the dataset also captures the acoustic diversity and unpredictability of real-world recordings.

Four Indic DiarBench clips grouped by scenario, meeting calls, in-the-wild media, and high overlap. Pick a tab, press play, and follow speakers on the timeline and transcript.

### How the Data was Annotated

Every recording then went through a five stage annotation process:

  1. **Bootstrap transcription:** Multiple ASR models generated an initial transcript
  2. **Human correction:** Annotators verified every word, timestamp, and speaker label
  3. **Code-mixed transcription:** Each session was transcribed in two formats to account for code-mixing with English. One was entirely in the native Indic script and the other was using Roman script for English words and Arabic numerals. Both the formats were accepted while calculating WER
  4. **Quality control:** We had 2-3 checkers review consistency, speaker labels, timestamps, code mixing, numerals, and non speech events. Overlapping speech received additional review
  5. **Expert review:** An in-house expert then performed a final check and sent the files back for revision until they met our quality bar



The result is a dataset that links **what was said, when it was said, and who said it,** all on the same recordings.

## Evaluating Speaker-Attributed ASR

With Indic DiarBench dataset, systems can now be evaluated on realistic multi speaker Indic speech.

ASR providers can use the three established metrics below on our open-source dataset, each capturing a different part of the problem. Lower scores indicate better performance across all three.

  1. **DER (Diarization Error Rate):** Measures how well a system identifies who spoke when. It captures missed speech, false alarms, and speech assigned to the wrong speaker
  2. **cpWER (concatenated minimum-permutation Word Error Rate):** Measures transcription and speaker attribution together. A wrong word and a correctly transcribed word assigned to the wrong speaker both count as errors
  3. **WDER (Word Diarization Error Rate):** Isolates speaker attribution errors by measuring the percentage of aligned words assigned to the wrong speaker



Together, these metrics on the Indic DiarBench dataset show not just whether a system gets the words right, but whether it can correctly attribute those words to the people who said them.

### Try it

  1. Indic DiarBench dataset is fully open on Hugging Face: audio, annotations and evaluation protocol: [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)huggingface.co/datasets/sarvamai/indic-diarbench](https://huggingface.co/datasets/sarvamai/indic-diarbench)
  2. Indic DiarBench will be presented at Interspeech 2026. Read the paper on arXiv: [![](https://www.google.com/s2/favicons?domain=arxiv.org&sz=32)arxiv.org/abs/2607.23808](https://arxiv.org/abs/2607.23808)



Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
