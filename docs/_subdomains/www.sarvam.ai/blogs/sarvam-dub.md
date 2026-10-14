---
url: https://www.sarvam.ai/blogs/sarvam-dub/
title: Sarvam Dub: SOTA Indian language dubbing | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:22.509137+00:00
---

# Sarvam Dub: SOTA Indian language dubbing | Sarvam AI

> Source: https://www.sarvam.ai/blogs/sarvam-dub/

  1. [ Home ](https://www.sarvam.ai/)
  2. /
  3. [ Blog ](https://www.sarvam.ai/blogs)



# Sarvam Dub: State-of-the-Art Dubbing for Indian Languages

AnnouncementCompany

* * *

Feb 1, 2026·8 min readShare

![Sarvam Dub: State-of-the-Art Dubbing for Indian Languages](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/ae5abe6ab7c5c58111bd62d53e5c18e2897e1b12-1047x666.png)

AI has changed the way content moves. For creators and content teams, this shift raises the bar. They are expected to move faster, publish more frequently, and ship content in many languages at once. They need a way to take a piece of content, move it across formats and languages, preserve meaning and quality, and keep the process fast enough for modern release cycles.

Today, we’re introducing Sarvam Dub, a state-of-the-art AI dubbing model that helps creators extend the life and reach of a single piece of content, quickly.

Dubbing can be tricky. Languages differ in word length, rhythm, and prosody, so even small timing mismatches feel unnatural to viewers. A sentence that takes two seconds in English may take three in Hindi. A phrase that lands with emphasis in one language may fall flat in another. The traditional solution required voice artists, translators, editors, and multiple recording sessions. A process that worked, but couldn't scale.

Sarvam Dub addresses this. What used to take weeks of scripting, recording, studio time, and publishing effort can now be dubbed in minutes. With zero-shot voice cloning, tight control over timing, and cross-lingual speech models, we deliver dubbing that sounds natural, and like the original speaker. An education course recorded once can serve learners across regions. A show produced in one language can be watched and heard in many. A podcast can travel beyond the language in which it was first produced.

In this blog, we explain what makes dubbing technically hard, how Sarvam Dub addresses those challenges, and what early deployments tell us about where this is heading. We walk through the experience layer using both real-time and pre-recorded examples, and explain why preserving speaker identity and timing is critical for production use. We share the evaluations and benchmarks we use to measure voice similarity and timing control, followed by real-world examples from public communication, education, and news.

## **Things Dubbing Must Get Right**

At the core of dubbing is speaker identity. In the Indian context, preserving that identity is especially difficult. Voice cannot simply flow from one dominant language into others. It must survive movement in every direction, across a network of Indian languages where any language can be the source and any other the destination. The speaker must sound unmistakably like the same person regardless of the language, accent, emotion, or speaking style. When this continuity breaks, the illusion fails immediately.

Timing is equally critical. When content moves between Indian languages, sentences naturally expand or contract. The video timeline, however, remains fixed. Many systems attempt to correct this after generation by speeding up or slowing down audio. This approach distorts natural rhythm and quickly degrades the listening experience. High quality dubbing requires duration control that is intrinsic to speech generation, where timing is shaped as the voice is produced rather than adjusted afterward.

There is also the realism of everyday Indian speech. Speakers routinely mix languages within a sentence, switch scripts, and use expressions that reflect how people actually talk. They expect accurate pronunciation of names, places, and brands, along with support for Indian English and a wide range of regional accents. These patterns are not edge cases. They are the norm.

Dubbing for India therefore demands systems built to preserve identity, control timing, and handle true Indian multilingual complexity by design, from the outset.

## **Preserving Speaker Identity**

A person’s identity lives in their voice. When you hear it, you recognize the person. Voice conveys personality, credibility, emotion, and trust in ways words alone never can. A speech, a lecture, a video, or a film can be made available in many languages. But if the voice changes, something essential is lost. People do not just want the message. They want the messenger. They want to hear the person, not a replacement. Sarvam Dub preserves this very connection. It ensures that when a voice crosses into another language, it remains undeniably and recognizably the same.

To measure how well speaker identity is preserved, we use speaker similarity scores between the original and generated audio samples. Both samples pass through a speech representation model that captures the characteristics of a speaker’s voice ([![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)ECAPA-TDNN speaker embeddings](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb)). We calculate similarity as a cosine score between these embeddings. Higher scores indicate stronger preservation of the speaker’s unique voice.

Sarvam Dub consistently achieves state-of-the-art speaker similarity in both same-language reproduction and cross-lingual translation, outperforming leading alternatives. The gap is most pronounced when voices move across languages, where maintaining identity is hardest. Even as the language changes, the speaker’s voice remains consistent, distinctive, and clearly attributable to the original speaker. The results are summarized in the chart below.

Our evaluation uses a standardized [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)benchmarking set ](https://huggingface.co/datasets/sarvam/sarvam-dub-benchmark-set)that we created for this purpose. It spans 64 distinct speakers across 10 Indian languages and English, covering both same-language and cross-lingual scenarios. We evaluated over 700 audio samples per system, with all models tested under identical conditions. All models evaluated under identical conditions: same encoder, same test set, same scoring.

## **Precise Control on Duration**

Voice preservation alone doesn't solve dubbing. The generated speech must also fit the video timeline exactly.

When content moves between languages, sentence length changes. A two-second phrase in English might take three seconds in Hindi, or one and a half in Tamil. The viewer sees the mismatch immediately.

Most commercial offerings handle this by generating audio first, then stretching or compressing it to fit. This works on paper. In practice, it destroys natural rhythm. Speech that's been time-stretched sounds mechanical. Compressed speech feels rushed and unnatural. Either way, the result doesn't feel human.

Sarvam Dub integrates duration control directly into the speech generation process. The model doesn't produce audio and then adjust it. It literally shapes the audio waveform to the timing constraint. You specify the target duration upfront. The model produces speech that hits that duration naturally, without post-processing.

See the effect of this in the following famous six-sixes video. Across languages, the commentary is aligned to the action in the shot - right when Yuvraj hoists the next six the commentator bursts into a frenzy. Crisp.

Original (English)Hindi

Timing also matters for editing in real workflows. Video content evolves. A creator needs to update a name, correct a word, or produce regional variations of the same video. With precise duration control, they can swap audio directly without re-editing the video. The new audio drops in cleanly.

## **What We Have Been Building**

The true test of dubbing isn't whether it works once. It's whether it works reliably, at scale, in production. The following examples show dubbing used consistently for content that matters.

### Public Outreach

Mann Ki Baat is the Prime Minister's monthly address to the nation. Each episode is dubbed into 11 Indian languages. The same message reaches audiences across regions in the languages they speak. It's a production workflow that runs every month, consistently. Clearly in this case the connect that the Prime Minister has with citizens needs to remain authentic with a voice that sounds like him, but in the language of the listeners. Check out the following snippet or the videos on the official channels for other months.

Original (Hindi)MalayalamTeluguGujarati

### Education

We worked with IIT Madras to demonstrate dubbing for educational content. The video shows a technical lecture dubbed across multiple Indian languages while preserving the speaker's voice and instructional clarity. Educational content presents specific challenges. Technical terminology must remain precise. The speaker's authority and credibility need to carry across languages. We believe this can create opportunity for content to be made relevant for much larger audiences.

OriginalTamilPunjabiOdia

### **Live Streams**

India's Union Budget 2026 was the first national budget to be dubbed live using AI. Finance Minister Nirmala Sitharaman's address was made available in real-time in Kannada and Hindi, powered by Sarvam on Republic TV. This is a particularly hard case as the budget speech is not available earlier and needs a dubbing flow that is fast and reliable. Check out some samples here.

A critical challenge in getting dubbing work on live streams is to optimise the model for latency. Our systems engineering team pulled off a massive 6.6x reduction in latency over a base Torch implementation of our model. This came from various techniques such as cleaner ONNX tracing, selective quantisation on the ONNX graph, post-training quantisation (PTQ) on calibration data that matches the content distribution, and intelligent caching. The result not only brings the cost of dubbing lower, but also creates a model that can fit into most media organisation’s streaming workflows.

## **We are Excited to See What You Will Build**

For creators, educationalists, news and media organisations, Sarvam Dub provides a lot of opportunities. We are particularly stoked by expanding reach for content creators to wider audiences. We will have more to share and say in this regard very soon.

For us as a nation, understanding should never be a problem. In India, we celebrate our differences. And for India as a nation, language should be a bridge, not a barrier.

The goal isn’t to make everyone speak the same language. It’s to make language differences irrelevant to understanding. To preserve the beauty and specificity of how people express themselves, while ensuring those expressions can be understood by anyone who seeks to understand them.

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
