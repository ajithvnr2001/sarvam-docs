---
url: https://www.sarvam.ai/stories/supernova/
title: How Supernova Built a Voice-First English Tutor with Sarvam
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:03.424170+00:00
---

# How Supernova Built a Voice-First English Tutor with Sarvam

> Source: https://www.sarvam.ai/stories/supernova/

[Customer Stories](https://www.sarvam.ai/stories)

# How Supernova built a voice-first English tutor with Sarvam

* * *

August 3, 2026

Education

Download PDF

![](https://assets.sarvam.ai/tr:w-1600,h-865,q-70,f-auto,dpr-auto/images/03117ysv/production/190678dac8dffdf8615aee5eb4ad512fc9ca213e-3840x2160.png)

![supernova](https://assets.sarvam.ai/tr:w-480,q-90,f-png,dpr-auto/images/03117ysv/production/0f18b0c6096ee892d41c88598c8031edfe8f3e5d-985x98.png?fit=max)

> Building a spoken English learning app for India means your Speech to Text has to work for a Malayalam accent or a Hindi speaker attempting their first full sentence. The global providers we tried were not built for this. Latency was high and accuracy on Indian accents was unreliable. Sarvam changed that. Low latency across 11 Indian languages means users get near-instant feedback when they speak, which is core to how people learn. Production-quality support for Malayalam, Kannada, and Bengali opened up entirely new markets for us.

Anirudh Coontoor

CTO, Supernova

![](https://assets.sarvam.ai/assets/motifs/ui/testimonial-image.svg)

## Background

Across India, spoken English opens doors. It determines who gets the job, who gets heard in a meeting, who steps into opportunities that others cannot.

For most learners, the options to get there are expensive, inaccessible, or simply not built for how Indians actually learn. Supernova was built to change that.

Nova AI is their voice AI tutor. It listens to learners speak, gives instant feedback on grammar, and holds real conversations in the learner's own language so they can practice without hesitation. Available 24/7 on any phone at a price point designed for the people who need it most, Nova AI today serves over 1 crore learners across the country, from working professionals preparing for interviews to first-generation English speakers finding their footing in workplaces where English is the default.

## The Problem

For Supernova, the quality of the voice stack directly shaped how learners experienced the product. Every correction Nova AI gave, every response in a learner's own language, depended on the app accurately hearing what the user said. When it got that wrong, the experience broke down.

Supernova's earlier voice stack had three gaps, each with a direct consequence for learners.

  1. Accuracy on Indian accents and code-mixed speech was unreliable. India's learners speak with regional accents, mix languages mid-sentence, and switch between English and their mother tongue without thinking about it. The earlier stack could not keep up, and learners were being misheard mid-sentence.
  2. Latency was unpredictable, swinging between 1,000ms and 2,500ms and breaking the conversational rhythm that language practice depends on. Transcription costs were high enough that reaching the price-sensitive markets Supernova was built for was becoming unviable.
  3. For a product built for first-generation English speakers learning on a budget, none of this could be overlooked. The team needed a voice foundation that was accurate, consistently fast, and affordable.



## Why Sarvam

Supernova evaluated several providers before landing on Sarvam. The solution had to work accurately on Indian accents, respond fast enough to hold a conversation, and come in at a cost that made Supernova's target market viable. Most providers addressed one or two of these. Sarvam addressed all three.

The evaluation ran in two stages: internal benchmarks on curated samples, followed by A/B tests on live users measuring comprehension accuracy, response quality, and engagement. Sarvam cleared both stages, holding up on the accuracy, latency, and pricing that Supernova's core market depended on.

For a product where accuracy, speed, and cost each have a direct bearing on whether a learner comes back, finding a provider that delivered on all three was the deciding factor.

## The Solution

Supernova consolidated its entire voice layer on Sarvam. Every learner utterance routes through Sarvam's Speech-to-Text API in translate mode: English gets transcribed as-is, and questions asked in Tamil, Telugu, Hindi, Kannada, Malayalam, Marathi, Bengali, Punjabi, or Gujarati are translated into English in the same call. This meant Nova AI could respond to a learner who switched languages mid-session without treating it as an error, which for Supernova's users is not an edge case. It is how they naturally communicate.

The integration moved fast. Within seven days of first contact, Supernova's workloads had shifted to Sarvam's APIs. Within two weeks, translate mode was live and central to the product.

## Inside a session with Nova AI

A young professional from Kerala was using the app to prepare for workplace conversations: a job interview, a client call, the kind of English that actually matters. Mid-session, after working through a full answer, she paused and switched to Malayalam to ask whether her phrasing came across as confident. With an earlier stack, that switch would have registered as an error. With Sarvam's translate mode, Nova AI recognised it as a question about tone, handled it in the same API call, and responded with feedback on her phrasing. She got the answer she was looking for and kept going without breaking stride. For the first time, she said, the app felt like it was keeping up with her, not the other way around.

## The Impact

Switching to Sarvam moved the needle on every dimension that mattered to Supernova's learners and to the business.

Latency dropped from a range of 1,000 to 2,500ms to 550 to 650ms, a 2 to 4x improvement, with no supported language averaging above 660ms, restoring the conversational rhythm that language practice depends on

Accuracy improved significantly. Transcription error rates fell 50% versus the earlier stack, with Sarvam reaching roughly 19% Word Error Rate across all 11 supported Indian languages. Being heard correctly the first time kept learners in the session rather than dropping off in frustration.

Engagement followed. Scenario completion rates improved 5 to 8 percentage points. Among vernacular learners, practice sessions per user rose approximately 20%. Per-user engagement held or improved even as paid subscribers grew 3x.

Cost came down 30 to 35% compared to other providers evaluated, with a fallback rate under 1%, making the price point Supernova needed to reach its core market financially sustainable.

The scale that followed tells the rest of the story. In May 2025, Supernova was transcribing 236,107 minutes a month. By April 2026, that number had grown to 3.4 million, a 14x increase in under twelve months. Speech-to-Text call volume crossed 45 million in the second quarter, climbed past 53 million in the third, then surged 85% to nearly 99 million as a new wave of learners found Nova AI. What started as a careful pilot became one of the fastest-scaling voice workloads on Sarvam's platform.

## Looking Ahead

Supernova has shown that a voice AI tutor built for Indian learners can work at scale, reach the markets it was designed for, and earn the kind of repeat use that drives a learning product forward. As Nova AI continues to grow and Sarvam advances its multilingual voice capabilities, the two are building something that matters: accessible, accurate, affordable English fluency for the next hundred million learners in India.

## More Customer Stories

  * ### [How Sarvam's voice agents work across Mahindra Finance's businessMahindra Finance·Financial Services](https://www.sarvam.ai/stories/mahindra-finance-voice-agents)
  * ### [How IIM Udaipur is scaling its bilingual curriculum with SarvamIIM Udaipur·Education](https://www.sarvam.ai/stories/iim-udaipur)
  * ### [Equal scales its Call Screening Assistant to enterprise volume with SarvamEqual ·Technology](https://www.sarvam.ai/stories/equal)



[View all](https://www.sarvam.ai/stories)

![](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/motifs/blocks/motif-block-04.png)![](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/motifs/blocks/motif-block-01.png)![](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/motifs/blocks/motif-block-02.png)![](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/motifs/blocks/motif-block-03.png)

![Sarvam](https://assets.sarvam.ai/assets/brand/logos/sarvam-wordmark-black.svg)

Build the future of India's AI with Sarvam. 

Build the future of India's AI

with Sarvam.

[Sign Up](https://indus.sarvam.ai)
