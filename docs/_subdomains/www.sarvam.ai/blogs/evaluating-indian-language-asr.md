---
url: https://www.sarvam.ai/blogs/evaluating-indian-language-asr/
title: Indic ASR evaluation: beyond WER to LLM & semantic metrics | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:19.244712+00:00
---

# Indic ASR evaluation: beyond WER to LLM & semantic metrics | Sarvam AI

> Source: https://www.sarvam.ai/blogs/evaluating-indian-language-asr/

  1. [ Home ](https://www.sarvam.ai/)
  2. /
  3. [ Blog ](https://www.sarvam.ai/blogs)



# Evaluating Indian Language ASR

A practical guide to layered Indic ASR evaluation: LLM-WER and LLM-CER, Intent and Entity scores, COMET, and open-source evaluation frameworks.

Research

* * *

Apr 2, 2026·14 min readShare

![Evaluating Indian Language ASR](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/f9eda141eb063a92ed8c01a81b9b7dae871e7451-2016x1260.png)

## Introduction

Measuring how well a speech recognition system performs in Indian languages is harder than it looks. The standard metrics weren't built for them, and that mismatch quietly distorts how Indic ASR systems get evaluated.

Word Error Rate(WER), Character Error Rate(CER), and BLEU were developed primarily for English. They work well when every word has a single accepted spelling, when languages don't mix mid-sentence, and when the gap between formal and colloquial usage is narrow. Indian languages don't fit that description. Colloquial and formal registers coexist and are equally understood by speakers. English loanwords appear in both Indic and Latin script, sometimes within the same utterance. Numbers have multiple valid written forms. Applying these metrics without adjustment can make an Indic ASR system look significantly worse or better than it actually performs in practice.

This is a harder problem than it first appears. It isn't just that the metrics are imperfect. The deeper issue is that WER and CER penalize surface-level differences in character sequences without any understanding of whether two transcriptions mean the same thing. When a model correctly transcribes a spoken word but renders it in a different but equally valid script or spelling, the metric counts that as an error. The transcript is right. The score is wrong.

This blog describes a layered evaluation approach that addresses these gaps directly. It explains what WER and CER measure and where they break down, then introduces four LLM-based metrics - LLM-WER, LLM-CER, Intent Score, and Entity Preservation Score. Together, they give a more accurate and complete picture of how an Indic ASR system is actually performing. The blog also introduces two open-source evaluation frameworks you can drop into an existing pipeline.

Throughout, we draw on examples from Saaras V3, Sarvam's speech recognition API for 22 Indian languages. Saaras V3 supports five output modes - transcription, translation, verbatim output, transliteration, and code-mix - which makes it a useful concrete anchor for the broader evaluation principles discussed. The open-source frameworks below can be adapted to evaluate any Indic ASR system.

[![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_wer**](https://github.com/sarvamai/llm_wer)

[![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_intent_entity**](https://github.com/sarvamai/llm_intent_entity)

We don't think this approach is the final word on Indic ASR evaluation. The field is still developing, and the right set of metrics will likely evolve as the systems themselves do. But we believe this layered framework is meaningfully closer to what evaluation for Indian languages actually requires, and the tools exist today to start using it.

## Working Example: Saaras V3 by Sarvam

This section below covers Saaras V3's output modes and delivery options. The metric discussions that follow reference these modes directly, so it helps to have them in view before diving in. If you're evaluating a different ASR system, the same principles apply. Substitute your system's equivalent modes and endpoints where relevant.

### Output Modes

To make the differences between modes concrete, all five examples below are drawn from the same spoken Hindi sentence:

**Input sentence (spoken Hindi)** मुझे कल सुबह नौ बजे doctor के पास जाना है

**Note** the code-mixed English word 'doctor' and the spoken number 'नौ'

Mode| What it returns| Example output from the sentence above| Primary evaluation metric  
---|---|---|---  
Transcribe| Normalised transcript with numbers, punctuation, and formatting| मुझे कल सुबह 9 बजे डॉक्टर के पास जाना है।  
  
**Note:**  


  1. 'नौ' → '9' - spoken number normalised to digit  

  2. 'doctor' → 'डॉक्टर' - loanword transliterated to Devanagari  

  3. Full stop added.

| LLM-WER / LLM-CER  
Translate| English translation of the spoken input| I need to go to the doctor tomorrow morning at 9.| Intent Score + Entity Score + COMET  
Verbatim| Exact word-for-word output, no normalisation| मुझे कल सुबह नौ बजे डॉक्टर के पास जाना है| Standard WER (strict)  
Translit| Indic script converted to the Latin alphabet| Mujhe kal subah nau baje doctor ke paas jaana hai.| LLM-CER  
Codemix| Mixed output preserving Indic and English tokens| मुझे कल सुबह 9 बजे doctor के पास जाना है।  
  
**Note:**  


  1. 'नौ' → '9' - number normalised  

  2. 'doctor' stays in Latin script rather than being transliterated  
  
The code-mixed nature of the speech is preserved.

| LLM-WER + Entity Score  
  
Scroll

Scroll

### API Delivery Options

Saaras V3 is available through three delivery methods. The right choice depends on your file length, latency requirements, and integration architecture.

API| Best for| Limits| Response type| Latency  
---|---|---|---|---  
REST API| Single short files, webhook integrations, synchronous pipelines| Up to 30 seconds per file| Synchronous result returned in the same HTTP response| 2-5 seconds  
Batch API| Long recordings, bulk jobs, overnight pipelines, call centre archives| Up to 60 minutes per file; up to 20 files per request| Asynchronousreturns a job ID; poll for results| Minutes to hours depending on queue  
WebSocket Streaming| Real-time voice assistants, live captions, interactive conversational bots| Continuous audio stream; no fixed file size limit| Real-time partial results as audio arrives| Sub-second to first word  
  
Scroll

Scroll

## Metrics Overview

An overview of all five metrics covered in this blog, organised by category.

  * **Traditional Metrics:** String-matching and n-gram overlap, designed primarily for English.
    * WER / CER (Section 3): Word/Character Error Rate. Edit-distance metric; fast, well-understood, and the standard benchmark baseline.
      * COMET (Section 6): Neural translation metric trained on human judgements. Better than BLEU for measuring translation fluency.
    * BLEU (Section 7.2): N-gram overlap for translation quality. Included as context; superseded by COMET for modern use.
  * **Gen-AI Metrics:** LLM-based metrics that measure meaning, not just character distance.
    * LLM-WER / LLM-CER (Section 5): WER/CER rescored by an LLM judge. Segments that are semantically or phonetically equivalent are no longer counted as errors.
    * Intent Score (Section 7): Binary score (0 or 1). An LLM judges whether the core meaning of the utterance is preserved.
    * Entity Preservation Score (Section 8): Float between 0 and 1. The fraction of named entities (names, places, numbers, dates) that appear correctly in the transcription.



Indian languages have multiple valid forms for the same spoken word, colloquial and formal registers, code-mixed English loanwords, numbers written in digits or spelled out. Traditional metrics treat all of these as errors. Section 4 shows six concrete failure classes in detail, and the Gen-AI metrics in Sections 5 - 8 are designed to handle each of them.

### Metric 1: Standard WER and CER

WER and CER are the traditional baselines for ASR evaluation. They are well-understood, fast to compute and genuinely useful in specific circumstances.

#### Definitions

Word Error Rate (WER) measures the edit distance between the ASR output and a reference transcript at the word level counting substitutions (S), deletions (D) and insertions (I) divided by the total reference word count (N):

Copy
    
    
    WER = (Substitutions + Deletions + Insertions) / Total Reference Words

Word Error Rate (conceptual formula)

Character Error Rate (CER) applies the same formula at the character level. It is preferred over WER for agglutinative languages (Malayalam, Kannada, Telugu) where a single word token can be very long, making word-level edit distance disproportionately punishing.

#### When WER and CER Are Still Useful

  * mode="verbatim": exact transcription is the requirement WER is the correct strict measure
  * Benchmarking against published numbers on datasets like Vistaar or IndicVoices, which report raw WER
  * As a complementary baseline alongside LLM-based metrics, always report both



A note on evaluation strategy: For Indian languages, WER and CER work best as one layer in a multi-metric strategy, not as a standalone quality gate. Section 4 walks through the specific scenarios where LLM-based metrics give a more accurate picture.

### Understanding the limits of Standard Metrics for Indian Languages

WER and CER were designed for English, which has a near one-to-one relationship between spoken words and written tokens, fixed spelling conventions, and no code-mixing in standard speech. Indian languages have more flexibility built in. That flexibility is a feature, not a problem. The six scenarios below illustrate where standard metrics misread a correct transcription as an error, and why LLM-based metrics give a fairer read.

#### Colloquial Variants: When 'Wrong' Is Right

Every Indian language has a formal written register and a colloquial spoken register. Native speakers use both interchangeably and understand both perfectly. WER treats any deviation from the reference form as an error, regardless of whether meaning is preserved.

Here is a concrete walkthrough for **Tamil** : how the reference, ASR output, metric verdicts, and real-world impact line up.  
  
---  
**What the speaker said** \- A casual, colloquial Tamil sentence spoken naturally  
**Reference (formal)** \- அவர்கள் ஒன்றாக வேலை செய்கிறார்கள் (avargal: "they work together")  
**Example ASR output** \- அவுங்க ஒண்ணா வேலை செய்றாங்க (avunga: colloquial form, identical meaning)  
**Standard WER verdict** \- ❌ 4 out of 5 words flagged as errors. WER = 80%.  
**Reality** \- ✅ A native Tamil speaker hears this as a perfect transcription.  
**Business impact** \- If you set a WER threshold of 20% for your Tamil voice bot, you will reject a high-quality ASR output and may never ship.  
  
#### Code-Mixing: The Script Mismatch Trap

Hundreds of millions of Indians code-mix naturally, switching between their native language and English mid-sentence. When the ASR and the reference annotator make different but equally valid choices about how to write an English word, WER registers it as an error.

Here is a concrete walkthrough for **Hindi (code-mixed with English)** : how the reference, ASR output, metric verdicts, and real-world impact line up.  
  
---  
**Reference** \- वह doctor के पास गया (English word kept in Latin script)  
**Example ASR output** \- वह डॉक्टर के पास गया (same word transliterated to Devanagari)  
**Standard WER verdict** \- ❌ Flags 'doctor' as a substitution. WER = 20% on this sentence.  
**Reality** \- ✅ Identical meaning. Both spellings are correct.  
**Business impact** \- A customer service bot for a bank handles code-mixed Hindi all day. Every loanword ('account', 'balance', 'transfer', 'nominee') is a potential false WER error. The model looks 15% worse than it is.  
  
#### Short Helper Words: Exponential Penalties

Hindi, Bengali, and Marathi rely on short helper words, typically 2 to 3 characters. WER's division-by-word-count formula produces skewed scores when these words have minor deviations.

Here is a concrete walkthrough for **Hindi** : how the reference, ASR output, metric verdicts, and real-world impact line up.  
  
---  
**Reference** \- नहीं ("no": 2 characters)  
**Example ASR output (echo repeat)** \- नहीं नहीं (word echoed once due to audio processing)  
**Standard WER verdict** \- ❌ WER = 300%. The model appears catastrophically wrong.  
**Second reference** \- है ("is": a 2-character helper word)  
**Example ASR output (diacritic drift)** \- हई (phonetically near-identical, minor diacritic shift)  
**Standard WER verdict** \- ❌ WER = 100% on this word; a complete failure for a single diacritic.  
**Reality** \- ✅ A Hindi speaker hears no meaningful difference in either case.  
  
#### Agglutinative Languages: Suffix Substitutions

Malayalam, Kannada, and Telugu build long compound words by chaining morphemes. A minor suffix substitution, grammatically trivial, creates a large CER penalty because the entire token is affected.

Here is a concrete walkthrough for **Malayalam** : how the reference, ASR output, metric verdicts, and real-world impact line up.  
  
---  
**Reference** \- വിദ്യാർത്ഥികളുമായി സംസാരിച്ചു ("spoke with the students"; suffix: ഉമായി)  
**Example ASR output** \- വിദ്യാർത്ഥികളൊടു സംസാരിച്ചു (same meaning, grammatically valid alternate suffix ഒടു)  
**Standard CER verdict** \- ❌ Multi-character penalty on a long token. CER = ~30% despite no meaningful difference.  
**Reality** \- ✅ Both forms are grammatically valid. Native speakers consider them equivalent.  
  
#### Numeric Format Variability

The same number can appear in at least three valid written forms in an Indic language. WER treats all three as completely unrelated tokens.

Here is a concrete walkthrough for **Hindi (numbers)** : how the reference, ASR output, metric verdicts, and real-world impact line up.  
  
---  
**All three mean exactly "500"** \- पांच सौ (spoken) | 500 (Arabic numerals) | ५०० (Devanagari numerals)  
**Standard WER verdict** \- ❌ Treats all three as unrelated. If reference has '500' and output has 'पांच सौ', WER = 100% on this segment.  
**Dates follow the same pattern** \- '२५ जनवरी २०२८' vs '25-01-2024' vs '25 Jan 2024' are all correct, all penalised by WER when mixed.  
**LLM-WER verdict** \- ✅ Normalises numeric forms before scoring; All three treated as correct.  
  
#### Semantic Drift Blindness: The Danger in Translate Mode

WER is also blind to single-word changes that completely reverse meaning. This is the most dangerous failure mode for Saaras in translate mode.

The following walkthrough uses a **spoken Hindi **utterance and shows how ASR output,**WER** , and **Intent Score **can disagree when intent flips.  
  
---  
**Example ASR output** \- मैं कल स्कूल नहीं जाना चाहता हूं (one word insertion; intent completely reversed)  
**Standard WER verdict** \- ❌ Minor penalty (~14%). The translation appears almost correct.  
**Intent Score verdict** \- ✅ Score: 0 (FAIL). Correctly identifies this as a fundamental failure.  
  
**Key insight** \- WER and CER measure the distance between two strings. The LLM-based metrics in Sections 5-8 measure the distance between two meanings. For Indian languages, those two distances can be very different. Combining both perspectives gives the most accurate picture of ASR quality.

### Metric 2: LLM-Based WER and CER

LLM-WER and LLM-CER address the six failure classes from Section 4 by replacing rigid string-matching with a semantic and phonetic judgement made by an LLM. Segments that are meaning-equivalent or phonetically similar are treated as correct. Only genuinely wrong segments count as errors.

[![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_wer**](https://github.com/sarvamai/llm_wer)

#### Three-Step Methodology

  * Identify differences: Run standard WER/CER alignment to find the exact segments where the ASR output and reference do not match.
  * Consult the LLM: For each mismatched segment, the LLM is asked two questions:


  1. Are these phrases semantically equivalent? (Do they carry the same meaning?)
  2. Are they phonetically similar? (Would they sound the same when spoken?)



The LLM defaults to non-equivalence in any ambiguous case, confirming a match only with high certainty.

  * Score intelligently: Segments the LLM judges as equivalent are treated as correct. The final LLM-WER/CER is computed only over genuinely erroneous segments.



**Hallucination capping** \- When Saaras echoes a word (नहीं नहीं where the reference has नहीं), raw WER = 300%. LLM-WER caps each token's contribution at a maximum of 1.0, preventing a single hallucination from dominating your aggregate score.

#### Standard WER vs. LLM-WER: Side-by-Side

Failure class| ASR output vs reference| Standard WER| LLM-WER  
---|---|---|---  
Colloquial Tamil| avunga vs avargal| ❌ Error| ✅ Equivalent  
Code-mixed Hindi| डॉक्टर vs doctor| ❌ Script mismatch| ✅ Same word  
Diacritic drift| हई vs है| ❌ 100% on word| ⚠️ Soft penalty  
Number format| पांच सौ vs 500| ❌ Mismatch| ✅ Normalised as equal  
Hallucination repeat| नहीं नहीं vs नहीं| ❌ 300%| ✅ Capped at 1.0  
Malayalam suffix| ഉമായി vs ഒടു same meaning| ❌ High CER on long token| ✅ Semantic equivalence confirmed  
  
Scroll

Scroll

#### Installation and Usage

[![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_wer**](https://github.com/sarvamai/llm_wer)

  * Input: a CSV/JSONL file with columns ground_truth, asr_output, language, and optionally context.
  * The framework uses Gemini via Vertex AI as the LLM judge.



_See the repository README for full configuration and output format details._

### Metric 3: COMET Score

COMET is a neural translation quality metric trained on human translation judgements. Unlike BLEU, which counts n-gram overlaps, COMET encodes the source sentence, the reference translation, and the hypothesis using a multilingual transformer, producing a learned similarity score that correlates far better with human judgement.

Use COMET as a secondary metric alongside Intent Score when evaluating ASR outputs in translate mode. It is particularly useful for ranking model versions continuously: higher COMET means better quality. Intent Score is better at catching catastrophic semantic failures.

The following compares a **reference** (Can you come tomorrow? (reference English translation)) with model output and metric scores.  
  
---  
**Saaras V3 output** \- Are you available to come tomorrow? (Different phrasing, same meaning)  
**Standard BLEU** \- ❌ Low score: n-gram mismatch on 'are you available' vs 'can you'. Penalises a perfectly valid rephrasing.  
**COMET (wmt22-comet-da)** \- ✅ ~0.91: recognises semantic equivalence. Correct verdict.  
  
#### Usage Guidelines

  * Recommended model: Unbabel/wmt22-comet-da (reference-based) or cometkiwi (reference-free, no ground truth needed).
  * Always record the exact COMET model version. Scores are not cross-model comparable.
  * For lower-resource Indic languages not well-represented in COMET training data, weight Intent Score more heavily than COMET.



### Metric 4: Intent Score

Intent Score is the primary metric for evaluating Saaras V3 in translate mode. It answers the single most important question: did Saaras correctly capture what the speaker was trying to say?

[![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_intent_entity**](https://github.com/sarvamai/llm_intent_entity)

#### Scoring: Binary (0 or 1)

Intent Score is a binary judgment made by an LLM judge.

Score| Meaning| The LLM judge's criterion  
---|---|---  
1 ✅ PASS| The core message is intact| Minor spelling variations, equivalent phrasing, and synonym use are all acceptable  
0 ❌ FAIL| The meaning has changed| Subject or object altered, action reversed, statement converted to a question, or key information added or removed  
  
Scroll

Scroll

### Why BLEU Fails for translate mode: Four Concrete Failures

### Failure 1: Valid paraphrasing is penalised

The following compares a **reference** (Can you come tomorrow?) with model output and metric scores.

  * **Example ASR output** \- Are you available to come tomorrow?
  * **Standard BLEU** \- ❌ Low score; different n-grams, different word choice. Yet meaning is perfectly preserved.
  * **Intent Score** \- ✅ Score: 1 (PASS). Core message intact.



### Failure 2: Code-mixed input has no clean reference

**Code-mixed Hindi** input with no single canonical translation - how BLEU variance contrasts with **Intent Score**.

  * **Example ASR output** \- I won't go to the office tomorrow
  * **BLEU verdict** \- ❌ Highly sensitive to reference wording. Score varies wildly depending on the reference annotator's phrasing.
  * **Intent Score verdict** \- ✅ Score: 1 (PASS); captures the meaning accurately.



### Failure 3: Semantic drift is invisible to BLEU

The following compares a **reference** (I want to go to school) with model output and metric scores.

  * **Example ASR output** \- I do not want to go to school (one word inserted, intent completely reversed)
  * **Standard BLEU** \- ❌ Minor penalty (~14%). The output appears almost correct.
  * **Intent Score** \- ✅ Score: 0 (FAIL). Correctly identifies this as a fundamental failure.



### Failure 4: Many valid translations exist for a single utterance

**Translate-mode** phrasing variance: reference vs ASR output, **BLEU** , and **Intent Score**.

  * **Reference** \- I'm hungry, is there anything to eat?
  * **Example ASR output** \- I'm feeling hungry, do you have any food?
  * **BLEU verdict** \- ❌ Low score - 'anything to eat' ≠ 'any food' as n-grams.
  * **Intent Score verdict** \- ✅ Score: 1 (PASS) - same meaning, correct evaluation.



**Recommended Threshold** Flag any utterance with Intent Score = 0 for manual review. For aggregate reporting, track the percentage of utterances scoring 1 across your evaluation set. This is your Intent Pass Rate.

### Metric 5: Entity Preservation Score

Intent Score tells you whether the general meaning is preserved. Entity Preservation Score tells you whether specific named entities are transcribed correctly. These are the pieces of information that carry the most weight in domain applications. A single wrong entity can be a catastrophic failure regardless of overall intent.

[![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_intent_entity**](https://github.com/sarvamai/llm_intent_entity)

**Source note:** The scoring methodology below is based on the [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)sarvamai/llm_intent_entity](https://github.com/sarvamai/llm_intent_entity) GitHub README. The LLM judges entity preservation using `prompt_template.txt` in that repository.

#### Why Entity Score Matters: Three Production Failures

**Banking voice bot**

  * **Spoken:** 'Transfer ₹5,000 to account 9876543210'
  * **ASR output:** 'Transfer ₹5,000 to account 9876543220'
  * **Intent Score** = 1 (PASS - intent preserved). **Entity Score** = 0.5 (FAIL - account number wrong). Transaction fails.



**Navigation app**

  * **Spoken:** 'वसंत विहार जाना है'
  * **ASR output:** 'I need to go to Vasant Kunj'
  * **Intent Score** = 1 (PASS - intent of navigation preserved). **Entity Score** = 0.0 (FAIL - wrong destination). User arrives at the wrong place.



**Medical transcription**

  * **Spoken:** 'Give 500mg of Metformin twice daily'
  * **ASR output:** 'Give 250mg of Metformin twice daily'
  * **Intent Score** = 1 (PASS). **Entity Score** = 0.5 (FAIL - dosage halved). Patient safety issue.



#### How the score is computed

Entity Preservation Score is a float between 0 and 1. It represents the fraction of key entities in the ground truth that were correctly preserved in the ASR output.

  * The LLM identifies key entities from the ground truth: person names, place names, organisation names, dates, times, numeric quantities, and object names.
  * It then checks each entity against the ASR output, penalising for missing entities (present in reference, absent in output) and substituted entities (present but wrong).
  * If the ground truth contains no entities, for example "hello, how are you?", the score is automatically 1.0.



Reference| Saaras V3 Output| Entity Score| What failed  
---|---|---|---  
Call John at 3pm| Call John at 3pm| 1.0 ✅| Nothing  
Call John at 3pm| Call at 3pm| 0.5 ⚠️| 'John' missing  
Transfer ₹5,000 to acc 9876543210| Transfer ₹5,000 to acc 9876543220| 0.5 ⚠️| Account number wrong  
Hello, how are you?| Hello, how are you doing?| 1.0 ✅| No entities; auto 1.0  
  
Scroll

Scroll

#### Intent Score + Entity Score Together

Neither metric alone gives the full picture. Use both.

Scenario| Intent Score| Entity Score| Diagnosis  
---|---|---|---  
Fluent output, entity dropped| 1 (PASS)| 0.5 ❌| Entity-level failure hidden behind passing intent  
Negation flipped, entity present| 0 (FAIL)| 1.0 ✅| Semantic failure - entity preserved but meaning reversed  
Both correct| 1 (PASS)| 1.0 ✅| Pass  
Both failed| 0 (FAIL)| 0.0 ❌| Critical failure: escalate for model review  
  
Scroll

Scroll

**Recommended threshold** \- Entity Score ≥ 0.9 for general use cases. Entity Score ≥ 0.95 for banking, medical, or navigation applications where a wrong entity has direct downstream consequences.

### Open-Source Evaluation Frameworks

Sarvam has open-sourced two repositories that implement the full evaluation stack described in this blog. Both are freely available on GitHub and work with any Indic ASR system, not only Saaras V3. Both use Gemini via Google Vertex AI as the LLM judge. The methodology is compatible with other capable multilingual LLMs.

#### llm_wer: LLM-Based WER and CER

[![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_wer**](https://github.com/sarvamai/llm_wer)

  * Implements the three-step LLM-WER/CER methodology
  * Handles all six Indic language failure classes described in Section 4
  * Outputs per-utterance LLM-WER/CER scores with LLM explanation logs



Installation:

bash

Copy
    
    
    git clone https://github.com/sarvamai/llm_wercd llm_weruv venv --python 3.12 && source .venv/bin/activateuv pip sync uv.lock && uv pip install -e .

Install and set up the llm_wer environment

#### llm_intent_entity - Intent Score and Entity Score

[![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_intent_entity**](https://github.com/sarvamai/llm_intent_entity)

  * Implements binary Intent Score (0 or 1) per utterance
  * Implements Entity Preservation Score (0.0 to 1.0 float) per utterance
  * Outputs CSV with scores and LLM explanation text for every row
  * Hash-based caching layer to avoid re-evaluating identical inputs
  * Optional Google Sheets export for team-level reporting



Installation:

bash

Copy
    
    
    git clone https://github.com/sarvamai/llm_intent_entitycd llm_intent_entityuv venv --python 3.12 && source .venv/bin/activateuv pip sync uv.lock && uv pip install -e .

Install llm_intent_entity

Input columns required: ground_truth, asr_output, language, audio_file, context (optional). Supported languages: Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, English, and other Indic languages.

Running an evaluation:

python

Copy
    
    
    from llm_intent_entity import evaluateresults = evaluate(    dataset_path="eval_set.csv",    reference_col_name="ground_truth",    predicted_col_name="asr_output",    language_col_name="language",    context_col_name="context",    ignore_cache=False,    gemini_location="us-central1")

Run evaluation with llm_intent_entity

#### Ensuring Reproducible Results

LLM-based evaluation is only useful if results are consistent across runs. The most common cause of variability is forgetting to control the LLM's randomness. Here is the complete checklist.

**Set temperature = 0**

The single most important reproducibility setting: temperature = 0Setting temperature=0 switches the LLM to greedy decoding - the highest-probability token is always selected, making output deterministic for the same input. This one setting eliminates the large majority of run-to-run variability in LLM-based evaluation.

**Pin the model version**

  * Specify the exact model version: e.g., gemini-1.5-pro-002, not gemini-1.5-pro-latest
  * Even with temperature=0, provider-side model weight updates can shift scores. Pinning ensures a stable comparison baseline.
  * Run a fixed 50-sample calibration set any time you change the judge model or version. If scores shift more than 1 percentage point, treat the new run as a new benchmark series.



**Use seed parameters where available**

  * OpenAI (GPT-4o): pass seed=42 alongside temperature=0
  * Gemini (Vertex AI): pass seed in generation_config when available
  * Anthropic (Claude): temperature=0 is sufficient



**Version-control prompts and use structured output**

  * Store all evaluation prompts in the same repository as your evaluation code
  * Record a hash of (prompt + model version) alongside every result set
  * Require structured JSON output from the LLM judge (e.g., {"pass": true/false, "reason": "..."}) to constrain the output format and reduce parsing variability
  * Include 2-3 labelled few-shot examples per language in the system prompt to anchor the model's judgment scale



**Normalise text before evaluation**

  * Strip leading and trailing whitespace
  * Apply Unicode NFC normalisation to handle diacritic encoding variants
  * Pick one canonical numeric form (Arabic digits or Indic numerals) and apply it consistently to both reference and hypothesis before scoring



**Reproducibility checklist**

  * Set `temperature=0` on all LLM judge calls
  * Pin the LLM model version (not `latest`)
  * Set seed parameter where supported (e.g., `seed=42` for OpenAI)
  * Version-control all evaluation prompts; log prompt hash with every result
  * Apply Unicode NFC normalisation to all text before evaluation
  * Use structured `JSON` output in judge prompts
  * Include few-shot examples (2-3 per language) in the system prompt
  * Run 50-sample calibration set when changing judge model or version



### End-to-End Evaluation Workflow

The workflow below applies to any Indic ASR system. The table maps each output type to the right metric stack. The pipeline that follows walks through the full sequence, from data preparation to final reporting.

#### Metric Selection by ASR Output Type

ASR output type / use case| Primary metric| Secondary metrics  
---|---|---  
Normalised transcription| LLM-WER| Standard WER (baseline), Entity Score  
Verbatim / exact transcription| Standard WER (strict)| CER for Dravidian languages  
Translation to English| Intent Score| COMET, Entity Score  
Transliteration| LLM-CER| Standard CER (baseline)  
Code-mixed output| LLM-WER| Entity Score  
Domain-critical (banking, medical, navigation)| Entity Score| Intent Score, LLM-WER  
Model regression testing| WER/CER delta| LLM-WER delta on adversarial set  
  
Scroll

Scroll

#### Step-by-Step Pipeline

  * Prepare evaluation data: collect audio with human-verified reference transcriptions or translations. Apply Unicode NFC normalisation to all text.
  * Run ASR inference: capture raw model output for the output type you are evaluating. Avoid post-processing before scoring.
  * Compute baseline WER/CER: apply text normalisation, then compute standard WER/CER as your regression baseline.



Run LLM-WER/CER: use the llm_wer framework with temperature=0 and a pinned model version. [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_wer**](https://github.com/sarvamai/llm_wer)

Run Intent Score and Entity Score: use the llm_intent_entity framework with the same LLM configuration. [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_intent_entity**](https://github.com/sarvamai/llm_intent_entity)

  * Run COMET (translation output only): use Unbabel/wmt22-comet-da.
  * Aggregate and report: compute mean and median scores per language and per domain. Flag utterances with Intent Score = 0 or Entity Score below 0.8 for manual review.
  * Run calibration check: re-score a fixed 50-sample calibration set. If any score deviates more than one percentage point from the baseline, investigate the model or prompt drift before publishing results.



### Quick Reference: Metric Summary

Metric| Best for| Key limitation| Threshold| LLM needed?  
---|---|---|---|---  
WER / CER| Verbatim mode; regression deltas| Penalises valid Indic variants| Track as delta| No  
LLM-WER / LLM-CER| transcribe, translit, codemix| Adds cost and latency| < 15% general| Yes  
COMET| translate - continuous ranking| Weaker for low-resource languages| 

> 0.80

| No (neural)  
Intent Score| translate - meaning capture| Doesn't catch entity errors| 100% pass rate| Yes  
Entity Score| Banking, medical, navigation| Needs context column for domain entities| ≥ 0.90| Yes  
  
Scroll

Scroll

### Packages and Repositories

All packages and source repositories referenced in this blog, in one place.

Metric| Category| Install| GitHub Repository  
---|---|---|---  
LLM-WER / LLM-CER| Gen-AI| pip install openai| [llm_wer on GitHub](https://github.com/sarvamai/llm_wer)  
Intent Score| Gen-AI| pip install openai| [llm_intent_entity on GitHub](https://github.com/sarvamai/llm_intent_entity)  
Entity Score| Gen-AI| pip install openai| [llm_intent_entity on GitHub](https://github.com/sarvamai/llm_intent_entity)  
  
Scroll

Scroll

## Conclusion

Languages like Hindi and Tamil allow for a high degree of morphological variation. This flexibility makes them expressive, but it also introduces challenges for evaluation. Standard string matching approaches often fail to capture correctness in these settings. A transcription can be accurate in meaning and still produce a high WER. A translation can diverge semantically while continuing to score well on BLEU. In both cases, the issue is not that the metric is incorrect, but that it is measuring a different property than intended.

For this reason, no single metric is sufficient. WER and CER remain important because they are reproducible, interpretable, and comparable across systems. However, they primarily capture surface level similarity. LLM based evaluation methods are better suited to assessing semantic preservation, but they require careful grounding. Without a reference signal, these systems can drift over time. In practice, both types of evaluation are necessary, and each should be interpreted in the context of what it is designed to measure.

The choice of additional metrics should depend on the application. Intent Score is useful in settings where preserving meaning is critical, such as conversational systems and voice interfaces. Entity Score becomes more important when outputs are consumed by downstream systems, including databases, medical workflows, or financial processes. COMET is appropriate for evaluating translation quality specifically. These metrics are not interchangeable. Each captures a distinct class of failure.

There are also practical considerations in implementation. Running LLM based evaluators at temperature 0 improves consistency. Version pinning the evaluation model is equally important. Without these controls, results may shift in ways that are difficult to detect and reproduce.

All five frameworks described here are open source, and the align judge rescore approach can be applied across Indic ASR systems. The objective is to establish a shared baseline. When a team reports a given WER on Hindi, that number should be interpretable in a consistent way across organizations. While this level of standardization is not yet common, the necessary tools are already available.

**The five-metric checklist**

  * WER / CER: always report as your baseline
  * LLM-WER / LLM-CER: the semantically-aware complement to standard WER
  * COMET: for translate mode evaluation
  * Intent Score: when meaning preservation is the quality gate
  * Entity Score: when names, numbers, and places must be exact



### Further Resources

  * [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_wer**](https://github.com/sarvamai/llm_wer)
  * [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)**llm_intent_entity**](https://github.com/sarvamai/llm_intent_entity)
  * [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)**Sarvam docs**](https://docs.sarvam.ai)



[a]Recommended Title: Evaluating Speech Recognition for Indian Languages.

[b]Evaluating ASR for Indian Languages.

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
