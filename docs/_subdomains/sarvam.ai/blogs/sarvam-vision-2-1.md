---
url: https://sarvam.ai/blogs/sarvam-vision-2-1/
title: Sarvam Vision 2.1 document intelligence | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:19.993853+00:00
---

# Sarvam Vision 2.1 document intelligence | Sarvam AI

> Source: https://sarvam.ai/blogs/sarvam-vision-2-1/

  1. [ Home ](https://sarvam.ai/)
  2. /
  3. [ Blog ](https://sarvam.ai/blogs)



# Sarvam Vision 2.1: Pushing the Pareto frontier of document intelligence

Achieves state-of-the-art on global and Indic benchmarks with new capabilities for structured extraction and Indic handwritten recognition

Research

[Try in Playground](https://dashboard.sarvam.ai/document-intelligence)

* * *

Sep 24, 2026·7 min readShare

![Sarvam Vision 2.1: Pushing the Pareto frontier of document intelligence](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/1a855fb8970a94f498b89ab0a4d6a86d8bf5b503-2160x1440.png)

## Introduction

Sarvam Vision, launched as part of our sovereign models line up in February 2026, delivered frontier performance on document intelligence. While being a general vision-language model (VLM), the model focused on optical character recognition (OCR) capabilities for Indic, table parsing, multilingual visual reasoning, and structured outputs from visual data. Since launch the model adoption has grown widely and we received important feedback on the areas of improvement. These signals were primarily along two axes: (a) certain capabilities (or lack thereof) and (b) practical concerns around usability.

For the usability concerns, we focused on making optimizations to the inference stack. This enabled serving the model at a cheaper price point than we had announced at launch. Furthermore, the model API is now optimized for production workloads as a result. On the axis of capabilities, several workflows in document intelligence require strong performance on complex table parsing (e.g., structured extraction from multi-page tables); key-value (KV) extraction from forms; Indic handwritten recognition to solve last-mile intelligence. Alongside these new capabilities, some of the model weaknesses - mainly around hallucinations and inconsistencies - have been addressed.

Sarvam Vision 2.1 is a step change in terms of its new and improved capabilities: it achieves frontier performance on benchmarks, and is built for production workflows.

## Data and Model Architecture

In line with the previous release, our architecture follows the harness-with-VLM paradigm. The semantic layout parser and a pointer reading order network make for the primary harnesses. While our VLM is capable of working directly at page- or document-level, the accuracy trade-off necessitates harnessing the model for superior results.

On the data curation front, we carefully crafted high-quality and large-scale datasets for KV extraction and Indic handwritten. These comprised data of both types - synthetic and real-world. For instance, we built handwritten and printed synthetic forms in large quantities in various languages. To balance synthetic with real-world distribution, we further obtained forms from the web and filled them in synthetically to achieve high variance. Similarly, for Indic handwritten, we leveraged videos and other sources which contain a rich variety of handwritten content. These novel sources of data, along with refinements to our existing training corpus, allowed for training new capabilities and overcoming weaknesses.

Leveraging the data improvements, we performed large-scale post-training: supervised fine-tuning followed by RLVR.

## Global Benchmarks

In the previous version of Sarvam Vision, we reported on two primary benchmarks: olmOCR-Bench and OmniDocBench. These evaluations provide a general yardstick for measuring model performance across various types of documents and problems encountered in document intelligence workflows. We continue to report on these benchmarks, though, arguably they are saturated. The main reason to leverage these benchmarks is to signal model capabilities measured by an acceptable standard set by the community. Of course, there is a question of the generality of such evaluations: the correlation between a strong result on a benchmark vs. real-world usefulness. The model has undergone rigorous testing internally on various types of real-world workflows to deem generally useful.

### olmOCR-Bench

The benchmark tests document-level performance using pass-fail checks. These checks span a diverse range of document variations: arXiv math, old-scan math, tables, degraded old scans, multi-column pages, and long runs of tiny text. Instead of finding subtle digressions, the benchmark tests for presence and absence of facts.

(Note: This benchmark is officially English-only. However, it contains some contaminant samples in Chinese and others. Since our 1.0 model was trained on Indic and English languages, we previously reported on a filtered English-only set; this iteration reports on the official set for parity with competitor models.)

Model| Math| Base| Hdr/Ftr| TinyTxt| MultCol| OldScan| OldMath| Tables| Overall  
---|---|---|---|---|---|---|---|---|---  
Sarvam Vision 2.1| 90.5| 99.8| 96.3| 92.5| 82.1| 55.3| 89.7| 91.9| 87.3  
Infinity-Parser2 Pro| 87.4| 100.0| 95.1| 92.5| 83.3| 58.0| 83.6| 88.9| 86.1  
Opus 5| 90.0| 100.0| 83.9| 93.5| 85.8| 54.0| 84.3| 89.5| 85.1  
Chandra-OCR2| 86.5| 99.9| 91.5| 93.4| 82.4| 49.2| 85.8| 87.5| 84.5  
Mistral OCR4| 83.7| 99.7| 91.6| 91.6| 85.7| 48.9| 75.1| 88.6| 83.1  
Gemini 3.6 Flash| 86.5| 99.9| 87.5| 92.5| 78.6| 48.1| 79.9| 85.9| 82.4  
GPT 6 Astra| 82.6| 99.9| 95.7| 74.9| 77.8| 47.0| 85.8| 90.9| 81.8  
PaddleOCR-VL 1.6| 86.9| 98.9| 95.8| 92.8| 82.7| 37.5| 70.5| 83.7| 81.1  
Gemma 4| 84.1| 99.6| 76.2| 85.1| 79.2| 47.3| 83.8| 91.8| 80.9  
GLM-OCR| 84.0| 99.0| 96.1| 90.3| 78.5| 40.3| 68.1| 74.8| 78.9  
Bodhan Indic-OCR| 82.0| 99.1| 81.1| 82.8| 74.5| 45.8| 75.5| 89.1| 78.8  
DeepSeek-OCR2| 81.6| 99.9| 95.9| 89.1| 82.0| 34.2| 70.5| 76.5| 78.7  
Google Cloud Vision| 0.0| 98.4| 19.6| 89.6| 79.9| 29.0| 0.0| 0.3| 39.6  
AWS Textract| 0.0| 100.0| 24.4| 40.0| 12.3| 26.7| 0.0| 0.2| 25.5  
Azure Vision 4.0| 0.0| 98.4| 20.1| 39.6| 13.3| 24.7| 0.0| 0.2| 24.5  
  
Scroll

Scroll

olmOCR-Bench (Category-wise Performance Comparison)

### OmniDocBench v1.6

The benchmark is a composite measure of three continuous similarity measures - text edit distance, table structure using TEDS, and formula recognition using CDM. The evaluation samples include newspapers, textbooks, magazines, financial reports and the like. The focus of this benchmark is to measure structural fidelity.

Model| Text edit-dist ↓| Formula CDM ↑| Table TEDS ↑| Table TEDS-struct ↑| Reading order ↓| Overall  
---|---|---|---|---|---|---  
PaddleOCR-VL 1.6| 0.0356| 0.985| 0.931| 0.961| 0.100| 96.01  
Sarvam Vision 2.1| 0.0289| 0.988| 0.890| 0.935| 0.099| 94.97  
GLM-OCR| 0.0374| 0.984| 0.895| 0.933| 0.099| 94.71  
GPT 6 Astra| 0.0460| 0.967| 0.891| 0.942| 0.098| 93.74  
Gemini 3.6 Flash| 0.0371| 0.976| 0.869| 0.925| 0.136| 93.58  
Infinity-Parser2 Pro| 0.0325| 0.963| 0.865| 0.911| 0.092| 93.18  
Opus 5| 0.0471| 0.967| 0.856| 0.905| 0.113| 92.51  
Bodhan Indic-OCR| 0.0471| 0.973| 0.839| 0.891| 0.119| 92.17  
Chandra-OCR2| 0.0403| 0.963| 0.842| 0.909| 0.101| 92.14  
Mistral OCR4| 0.0414| 0.967| 0.826| 0.874| 0.101| 91.72  
Gemma 4| 0.0644| 0.958| 0.834| 0.883| 0.179| 90.94  
DeepSeek-OCR2| 0.0445| 0.927| 0.755| 0.817| 0.114| 87.91  
Azure Vision 4.0| 0.0499| 0.398| 0.000| 0.000| 0.181| 44.95  
Google Cloud Vision| 0.0876| 0.351| 0.000| 0.000| 0.244| 42.10  
AWS Textract| 0.3863| 0.209| 0.000| 0.000| 0.436| 27.42  
  
Scroll

Scroll

OmniDocBench v1.6 (Detailed Performance Comparison)

## Sarvam Indic OCR Bench

Global, English-centric benchmarks already evaluate the structural and technical aspects of document processing - layout fidelity, tables, math, scan quality, and the like - sufficiently well. The gap that remains is a high-quality benchmark that rigorously evaluates model accuracy on the 22 official Indian languages. Today, we release our Indic OCR bench to enable benchmarking by the community. The set comprises 6,909 samples (6,609 spanning 22 Indian languages; 300 in English). Its sole focus is language accuracy: each sample is curated to robustly measure character and word accuracy.

Most Indian languages have undergone a tremendous transformation in language and in script. In order to best measure OCR accuracy, the samples are derived from a wide variety of sources (newspapers, brochures, textbooks, historical writings, and the like) and curated from across time periods ranging from 1800 to present day.

The benchmark is hosted at our huggingface: [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)https://huggingface.co/datasets/sarvamai/indic-ocr-bench](https://huggingface.co/datasets/sarvamai/indic-ocr-bench)

Language| Sarvam Vision 2.1| Bodhan Indic-OCR| Gemini 3.6 Flash| Google Cloud Vision| Surya OCR 2| Mistral OCR4| Opus 5| Gemma 4| Chandra-OCR2| GPT 6 Astra| Infinity-Parser2 Pro| Azure Vision 4.0| AWS Textract  
---|---|---|---|---|---|---|---|---|---|---|---|---|---  
Overall accuracy ↑| 87.39| 84.94| 79.35| 71.76| 69.96| 69.16| 68.81| 65.53| 64.56| 63.69| 49.83| 41.29| 4.64  
Bengali| 93.47| 90.87| 90.36| 85.24| 81.79| 85.06| 88.75| 81.45| 80.64| 83.99| 81.12| 8.24| 7.56  
Gujarati| 88.87| 83.26| 83.68| 64.40| 65.80| 68.19| 70.92| 70.68| 59.14| 70.71| 48.09| 11.79| 10.01  
Hindi| 93.52| 90.99| 92.11| 84.29| 86.12| 85.87| 89.38| 85.03| 83.18| 85.52| 84.15| 85.72| 9.67  
Kannada| 90.54| 86.51| 82.70| 75.40| 79.60| 77.84| 78.87| 59.36| 71.93| 73.43| 20.94| 9.32| 10.17  
Malayalam| 90.24| 86.38| 84.41| 76.06| 76.61| 71.50| 82.44| 63.57| 69.36| 80.10| 22.82| 10.16| 9.03  
Marathi| 95.06| 90.76| 93.14| 86.50| 86.58| 84.17| 86.55| 82.91| 83.66| 84.74| 78.35| 87.86| 16.80  
Odia| 80.01| 75.45| 81.01| 68.32| 69.34| 57.04| 65.99| 43.37| 68.09| 69.74| 9.63| 4.16| 1.79  
Punjabi| 89.16| 86.51| 87.06| 81.65| 83.06| 81.65| 84.22| 72.53| 80.17| 81.84| 66.67| 7.76| 6.72  
Tamil| 87.70| 84.21| 84.58| 78.14| 79.07| 79.73| 80.46| 74.20| 76.35| 80.07| 60.12| 80.96| 10.47  
Telugu| 91.55| 86.92| 85.22| 75.71| 72.55| 78.06| 77.54| 71.08| 70.88| 75.82| 43.69| 17.09| 17.58  
Urdu| 91.21| 90.62| 89.52| 84.77| 86.01| 78.11| 88.22| 79.31| 82.62| 85.29| 63.85| 11.61| 0.15  
Sindhi| 91.44| 88.89| 85.78| 84.76| 83.02| 81.65| 81.66| 79.32| 75.23| 73.42| 74.15| 84.69| 0.35  
Santhali| 53.91| 68.30| 51.84| 32.10| 21.53| 29.95| 26.26| 20.68| 10.16| 26.37| 24.61| 0.07| 0.03  
Sanskrit| 84.05| 78.11| 81.07| 71.35| 60.25| 71.35| 46.30| 62.86| 60.23| 34.49| 45.01| 57.32| 0.13  
Nepali| 97.00| 94.70| 95.03| 94.88| 89.54| 91.53| 88.92| 91.57| 84.02| 88.65| 79.01| 91.91| 0.01  
Manipuri| 85.12| 82.85| 0.55| 0.00| 0.00| 0.00| 0.00| 0.00| 0.00| 0.19| 0.00| 0.00| 0.00  
Maithili| 96.70| 93.64| 93.71| 84.48| 78.00| 78.01| 57.29| 85.01| 75.86| 36.89| 66.03| 83.47| 0.07  
Konkani| 97.41| 95.99| 93.93| 93.72| 90.81| 87.35| 84.55| 80.95| 83.76| 77.77| 65.98| 92.29| 0.25  
Kashmiri| 54.82| 48.04| 36.04| 24.22| 26.27| 22.63| 32.20| 23.02| 24.33| 26.84| 15.18| 11.95| 0.22  
Dogri| 89.46| 85.51| 80.03| 69.23| 65.87| 55.91| 53.82| 66.65| 52.34| 38.12| 56.05| 75.14| 0.39  
Bodo| 90.48| 90.69| 86.37| 76.88| 69.96| 70.03| 62.78| 70.26| 52.48| 43.09| 46.61| 76.57| 0.71  
Assamese| 90.88| 89.41| 87.55| 86.58| 87.25| 85.97| 86.62| 77.85| 75.79| 84.08| 44.26| 0.22| 0.02  
  
Scroll

Scroll

Sarvam Indic OCR Bench (Language-wise accuracy)

## The Pareto frontier of document intelligence

Document intelligence is a multi-objective problem. A strong system is judged on several axes, many of which do not necessarily correlate: transcribing a 1950s scan without hallucinating (fscan); correctly reproducing a table's structure (ftable); or transcribing Tamil accurately (ftamil). Hence, what matters in such a setting is not the best score on any one axis but whether there exists another system that is better on every axis at once. This property of the Sarvam Vision 2.1 model can be studied by Pareto analysis.

The document-intelligence community already applies this idea to accuracy v. cost frontiers. We leverage the idea for accuracy v. accuracy frontiers over capabilities that do not necessarily move together.

Let's score each system on said capabilities (higher is better): fscan​, ftable​, ftamil​. System _A_ dominates System _B_ if fi​(A) ≥ fi​(B) on every axis i and fj​(A) > fj​(B) on at least one axis j. That is, _A_ is at least as good everywhere, and strictly better somewhere. The Pareto frontier is the set of systems that no evaluated system dominates.

In the figures below, each axis is a benchmark overall score, itself a weighted aggregate of such capabilities, so a system is a point (x, y) such as (olmOCR-Bench, OmniDocBench). It sits on the frontier if no other point lies to its upper-right.

We report two frontiers: (a) olmOCR-Bench against OmniDocBench (global benchmarks that measure different things); and (b) English against Indic. In both plots every point is a system evaluated by us on both axes under one harness.

### Sarvam Vision 2.1 pushes the Pareto frontier of olmOCR x OmniDocBench

The model is pareto-optimal across the two global benchmarks. A new region at the frontier has been unlocked (see shaded region).

The olmOCR-Bench x OmniDocBench frontier before and after Sarvam Vision 2.1. The animation loops continuously; hover any point for exact scores.

### Pareto-dominant on the English and Indic frontier

Generally, the best model on English benchmarks performs poorly on Indic languages. Sarvam Vision 2.1 achieves state-of-the-art in olmOCR-Bench and on our Indic benchmark.

The English and Indic frontier before and after Sarvam Vision 2.1. The animation loops continuously; hover any point for exact scores.

## Illustrations of New Capabilities

### 1\. Key-Value Extraction from Tables

0:00

-0:00

1×

### 2\. Key-Value Extraction from Forms

0:00

-0:00

1×

### 3\. Indic Handwritten Recognition

0:00

-0:00

1×

### 4\. Indic Handwritten Extraction

0:00

-0:00

1×

## Try out now!

  * **Digitize API:** convert complex multi-page documents, tables, and handwritten content across English and 22 Indic languages into clean, structured digital text with high layout fidelity - [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)https://docs.sarvam.ai/api-reference/doc-ai/job/digitise](https://docs.sarvam.ai/api-reference/doc-ai/job/digitise)
  * **Extract API:** perform extraction of key-value pairs, tables, and form field, enabling automated end-to-end document workflows - [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)https://docs.sarvam.ai/api-reference/doc-ai/job/extract](https://docs.sarvam.ai/api-reference/doc-ai/job/extract)
  * **Akshar Document Agents:** human-in-the-loop system for building end-to-end document intelligence workflows - [![](https://www.google.com/s2/favicons?domain=indus.sarvam.ai&sz=32)https://indus.sarvam.ai/akshar/dashboard](https://indus.sarvam.ai/akshar/dashboard)



Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
