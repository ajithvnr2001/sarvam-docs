---
url: https://sarvam.ai/blogs/asr/
title: Introducing Saaras V3 speech recognition | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:23.926903+00:00
---

# Introducing Saaras V3 speech recognition | Sarvam AI

> Source: https://sarvam.ai/blogs/asr/

  1. [ Home ](https://sarvam.ai/)
  2. /
  3. [ Blog ](https://sarvam.ai/blogs)



# Introducing Saaras V3

Built for the Way India Speaks

Research

[Try in Playground](https://dashboard.sarvam.ai/speech-to-text)

* * *

Feb 11, 2026·8 min readShare

![Introducing Saaras V3](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/9169939a6657e90c740ae4e658261315366d8987-1800x1350.png)

India runs on voice. Billions of them. Today, we’re introducing Saaras V3, built to understand all of them.

In June 2025, Saaras V2.5 marked an important step forward. It introduced multilingual speech recognition across 11 Indian languages and achieved ~22% Word Error Rate (WER) on the IndicVoices benchmark, consistently outperforming competing frontier models. It set a new baseline for speech recognition performance in Indian languages.

Powered by a new architecture, the Saaras V3 now natively supports streaming for low latency decoding. This upgrade also brings enhanced recognition accuracy, particularly for code-mixed and noisy speech to 22 official Indian languages and English. When evaluated on the same IndicVoices benchmark, Saaras V3 achieves ~19% WER.

Speech systems are judged in motion. Responsiveness matters. Stability under mixed inputs matters. The difference between a usable system and a frustrating one often comes down to how quickly and reliably the first tokens appear.

Saaras V3 now supports real time transcription in addition to a standard batch-oriented approach. Instead of waiting for speech to finish, the model decodes incrementally, producing partial transcripts while audio is still ongoing. This reduces time to first token and allows the text to build naturally in real time.

## The New Standard for Indian ASR

ASR systems deployed in India must work on speech as it is actually spoken. Conversations are spontaneous. Languages are mixed mid-sentence. Accents vary widely. Numbers are expressed in multiple forms. Background noise is common. Clean, read-speech benchmarks do not fully capture this variability.

Saaras V3 is designed with this reality as a starting point.

The model is trained on 1 million+ hours of curated multilingual audio data spanning Indian languages, accents, and acoustic conditions with a special focus on low resource languages. Adaptive data sampling during the training ensured good performance across languages. Training happened in multiple stages, beginning with large-scale pre-training and followed by supervised fine-tuning and reinforcement learning. Post-training targeted fixing long-tail errors, improving cross-language consistency, and ensuring stable, well-structured outputs suitable for downstream systems.

These choices are reflected in how the system performs on inputs that typically challenge multilingual ASR models. A few illustrative examples are outlined below.

##### Example 1: Code-Mixed Conversational Speech

Bengali Hindi Codemix00:00

0msLatency

Saaras V3 handles code-mixed speech without distorting it. It preserves correct word boundaries and formatting, and avoids hallucinated insertions or dropped words, which are common failure modes in multilingual ASR systems.

##### Example 2: Named Entities, Numerics & Noise

Numerical Entities00:00

0msLatency

Saaras V3 maintains numeric precision and preserves entity fidelity, even in compressed or acoustically noisy settings. Numbers, dates, names, and structured expressions are transcribed accurately and consistently.

### Evaluation Framework and Results

Saaras V3 was evaluated on multilingual benchmarks as well as real-world conversational datasets.

The primary evaluation uses the [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)IndicVoices dataset](https://huggingface.co/datasets/ai4bharat/IndicVoices), a large-scale, open multilingual speech corpus that spans Indian languages, accents, and recording conditions. Unlike controlled read-speech benchmarks, IndicVoices captures realistic variation in speaking style, pace, and channel quality. It provides a closer approximation to how ASR systems are used in practice.

Within this framework, Saaras V3 is compared against leading speech models, including GPT-4o Transcribe, Gemini 3 Pro, Deepgram Nova3, and Scribe v2.

On the 10 most popular languages subset of IndicVoices, Saaras V3 achieves a word error rate of 19.31 percent. This represents a clear improvement over Saaras V2.5 and maintains a consistent margin over competing models evaluated under the same setup.

Crucially, this performance gap widens on the remaining 12 languages on IndicVoices benchmark. Saaras V3 demonstrates consistent accuracy across these low-resourced languages, whereas competing models either completely lack coverage or yield heavily degraded transcriptions.

The gains are not limited to offline evaluation. The same level of accuracy is preserved in streaming configurations, ensuring that performance holds under real-time deployment conditions.

#### English Benchmark: Svarah

Indian-accented English is underrepresented in widely used ASR benchmarks such as LibriSpeech and Switchboard, despite India having an estimated 130 million English speakers. As a result, performance on these standard datasets does not fully reflect how systems handle English as spoken in India.

To address this gap, Saaras V3 was evaluated on Svarah, a 9.6-hour benchmark comprising 117 speakers across 65 districts in 19 Indian states. The dataset captures substantial accent variation and includes both read and spontaneous conversational speech across real-world domains, providing a more representative assessment of Indian English ASR performance.

This performance reflects the model’s strong ability to handle accent variation and phonetic shifts more reliably than systems primarily optimized on Western English benchmarks.

## Perfected for Live Speech

Accuracy alone is not sufficient for live systems. Voice agents, live captions, gaming interactions, and call-center assist tools operate in real time. They cannot wait for a speaker to finish before responding. Transcription must begin immediately and update continuously as speech unfolds.

Saaras V3 is designed for this streaming-first deployment model. It delivers ultra-low time to first token and maintains stable incremental decoding, allowing transcripts to build progressively without disruptive rewrites or lag.

Saaras V3 realtime is developed by training the encoder from scratch with causal attention to enable streaming capability. Instead of maintaining separate models for each latency setting, a unified multilingual model was trained on audios of varying chunk sizes and diverse conditions. This diversity pushes the model to learn representations that remain reliable even with very short, low-context, high tempo audios - a common reality in real-world streaming. As a result, a single Saaras realtime model can operate across different latency requirements with minimal drop in accuracy.

### Operating Modes: Latency v/s Accuracy Trade-Offs

Saaras V3 exposes configurable decoding modes aligned with the architecture described earlier:

  * **Simulated Streaming →** Powered by Voice Activity Detection (VAD) model and Saaras V3. Available today via WebSocket API
  * **Realtime Accurate→** Lowest WER, optimized for transcription fidelity
  * **Realtime Balanced→** Strong accuracy with reduced latency
  * **Realtime Fast→** Ultra-low TTFT, designed for sub-150ms response initiation



> **Coming Soon:** Accurate, Balanced, and Fast modes will soon be available through a dedicated Realtime endpoint. In Fast mode, the endpoint guarantees less than 150 milliseconds time to first token. It also supports structured streaming outputs, including word-level timestamps.

These configurations make latency and accuracy trade-offs explicit. Teams can choose the operating point that matches their use case, whether the priority is compliance-grade transcription, responsive conversation, or live interactive voice interfaces.

### Beyond Words

Saaras V3 is built as more than a speech-to-text model. In production systems, raw transcripts are rarely enough. Developers need structure, speaker attribution, and predictable output formats that integrate cleanly into downstream workflows.

For that reason, Saaras V3 supports structured audio understanding features alongside transcription.

#### Panel Discussion

Every word transcribed. Every speaker identified.

0:00

0:00

0:00 - 0:14

Speaker 1

એ રીતે તમે આગળ વધો પોતાની ધર્મની માન્યતાઓને ને પોતાના અત્યાર સુધી તમે પ્રેક્ટિસ કરતા આવ્યા છો એને છોડીને તમે એક જ નિયમ પ્રમાણે ચાલો તો આ યોગ્ય નહીં હોય કારણ કે આપણે જ્યારે દેશ બન્યો ત્યારે દરેકને આશ્વાસન આપ્યું હતું

0:14 - 0:27

Speaker 1

કે એમને જેવી રીતે દેશમાં શાંતિથી રહેવું હશે તો એમને છૂટ આપીશું પોતાના ધર્મ પ્રમાણે પોતાની જાતિ પ્રમાણે કે જે તેમના નિયમો હોય કોઈ કુટુંબના હોય કે જે હોય ગામના એ પ્રમાણે એ પ્રેક્ટિસ કરી શકશે

0:28 - 0:38

Speaker 1

તો આ હાલ ડિસ્કશનમાં ચાલે છે ને એના ફાયદા ગેરફાયદાનો આપણે ડિસ્કસ કરવાનો છે કે શું આવું કરવું જોઈએ હાલ સમય આવી ગયો છે કે બધાને ફોર્સફુલી

0:35 - 0:36

Speaker 2

શું આવું કરવું જોઈએ

0:39 - 0:58

Speaker 1

આપણે એક જ નિયમ બનાવી દઈએ ને બધાને કહીએ કે તમે આ જ નિયમ ફોલો કરો ચાહે તમે હિન્દુ હોય તો પણ તમે આ જ નિયમ ફોલો કરો તમારા ધર્મ ને છોડી દો મુસલમાન હતા તો એમના ધર્મના જે નિયમો હોય એ છોડો અને આને જ ફોલો કરો શું આ સમય આવી ગયો છે કે આપણે આવો કાનૂન બનાવવો જોઈએ જેવી રીતે અમેરિકામાં યુરોપમાં છે ત્યાં કોઈ ધર્મ ધર્મ નથી જોવામાં આવતું જ્યારે એ લોકો કોર્ટમાં જાય છે

0:59 - 1:04

Speaker 1

ત્યાં કોર્ટના દેશના કાનૂન પ્રમાણે કેસ લો કરવામાં આવે તો શું આવું ઇન્ડિયામાં કરવું જોઈએ આ એના વિશે છે

1:06 - 1:07

Speaker 2

એક દેશ એક કાયદો

1:10 - 1:14

Speaker 2

આપણે કહી શકીએ કે એક દેશ અને એક કાયદો બધાએ આ જ કાયદો માનવું જોઈએ

1:13 - 1:32

Speaker 1

કાયદો માનવો જોઈએ હા માનવો જોઈએ પછી તમે તમારો ધર્મ ગમે તે કહેતું હોય તમે ગમે તે માન્યતામાં માનતા હોવ તમને યોગ્ય લાગતું હોય પણ ફોર્સ કરવામાં આવશે ગવર્મેન્ટ તરફથી કે હવે તમારે આ જ માનવું પડશે તો આ યોગ્ય છે દરેક સાથે આવી રીતે ફોર્સફુલી એમનું ઇમ્પ્લિમેન્ટ કરવું હાલ શું આ સમય યોગ્ય છે લોકો એટલા મેચ્યોર છે

1:32 - 1:34

Speaker 1

આ હાલ ડિસ્કશન ચાલે છે

1:34 - 1:51

Speaker 2

મારા હિસાબથી આમાં જોવા જાય તો બંનેના નુકસાન છે અને બંનેના જ ફાયદા છે આપણે અગર આને ઇમ્પ્લિમેન્ટ કરીએ એક દેશ એક કાયદો તો આપણા ધાર્મિક સ્વતંત્રતામાં બી આપણે હસ્તક્ષેપ થાય છે આપણા સંસ્કૃતિને બી આપણે નુકસાન થાય છે

1:51 - 2:06

Speaker 2

અને આને અમલ કરવું મુશ્કેલ છે કારણ કે લોકો ધર્મના પ્રતિ ભારતમાં વધારે પડતા છે બધાને પોતાનો ધર્મ પહેલો છે એટલે આને લાગુ કરવું તો મુશ્કેલ છે જ અને લોકો તો

2:04 - 2:11

Speaker 3

અને લોકશાહી શાસનથી ભી ડિફરન્ટ થશે ને કે લોકો માટે લોકોથી અને લોકો વડે ચાલતું શાસન

2:11 - 2:35

Speaker 3

તો એના અગેન્સ્ટના પ્રોટોકોલમાં આપણે જતા રહીશું કારણ કે આ લોકોથી તો નહીં જ ચાલતું હોય ને કારણ કે આમાં તો એક એક તમે રૂલ્સ બનાવી દીધું એન્ડ એ બધાના ઉપર તમે થોપી દેવામાં આવે કે તમે લોકો કરો જ બરાબર શાયદ એમ એ લોકો માટે બેનિફિશિયલ હોય પણ ખરા ના બી હોઈ શકે તો એમના ધાર્મિક રિચ્યુઅલ્સ પ્રમાણે એ કનેક્ટ થતું પણ હોય કે ના પી થતું હોય

2:15 - 2:16

Speaker 2

અ

2:35 - 2:43

Speaker 3

તો આ લોકો માટે તો નહીં ચાલતું રહે તો આ લોકશાહીનો ભી ભંગ થાય એવું લાગી રહ્યું છે આમ આ આનાથી તો

2:44 - 2:59

Speaker 2

પણ આમાં ફાયદો બી એ છે કે આમાં કાયદા આમ સરળ થઈ જાય છે અને આમાં લોકો આમાં ગવર્મેન્ટ એવું વિચારે કે ધર્મના ઉપર નાગરિક નાગરિક તરીકે ઓળખ વધારે થાય અને આમાં સ્ત્રી પુરુષની સમાનતા બી થાય

3:00 - 3:08

Speaker 2

આપણને જેન્ડર ઇક્વાલિટી બી મળે આમાં સ્ત્રી પુરુષને બરાબર બી આવી શકે છે એ એક પોઇન્ટ છે જે મને ગમ્યો આમાં

3:07 - 3:07

Speaker 1

પોઈન્ટ છે

3:08 - 3:22

Speaker 1

મારે એવું માનવું છે કે આની અંદર બધા જે વિષયો છે એક સાથે લઈ લેવા કેમ કે જમીનનો ઇસ્યુ હોય અથવા તો શાદીનો હોય બીજા બધા જે ઇસ્યુઝના હોય એના કરતાં ગવર્મેન્ટે અમુક જે કોમન વિષયો હોય

3:22 - 3:34

Speaker 1

કે જેમાં કોઈ પ્રોબ્લેમ દરેકને વધારે થાય એવું નથી ધર્મની રીતે જેમ કે મારે કઈ પ્રોપર્ટી ખરીદવી છે એના માટેના નિયમો હોય કોઈ બિઝનેસના રિલેટેડ હોય અથવા બીજા કોઈ હોય તો પહેલાં શરૂઆત એમણે આનાથી કરવી જોઈએ

This structured output allows downstream systems to distinguish who said what, not just what was said. Speaker attribution becomes part of the transcript itself, rather than an external post-processing step.

This capability is essential for applications such as call analytics, meeting assistants, customer support quality assurance, and conversational AI orchestration, where identity and turn-taking are as important as the words spoken.

### Core Capabilities

  * **Automatic Language Detection:** High-accuracy detection of the spoken language, paired with transcripts generated in the native script.
  * **Output Format Control:** Fine-grained control over text and numeral formatting, tailored to your downstream use case and localization needs.
  * **Speaker Diarization:** Real-time and batch speaker separation with stable attribution across conversational turns.
  * **Multilingual Coverage:** 23 languages supported within a unified multilingual model.



Available today via the [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)Saaras V3 API!](https://docs.sarvam.ai/api-reference-docs/api-guides-tutorials/speech-to-text/overview)

## Powering Real-World Audio Experiences

Model quality is best evaluated not in isolation, but in deployment.

Saaras V3 is designed to operate across diverse production environments, from live conversational agents and call-center assist systems to multilingual media workflows and analytics pipelines.

The component below illustrates five real-world use cases, each accompanied by practical examples that demonstrate how Saaras V3 adapts to varying latency, formatting, and multilingual requirements. Rather than optimizing for a single benchmark scenario, the system is built to perform reliably across heterogeneous audio conditions and application demands.

Categories

Call Centers / Voice Bots3News & Announcements3Interviews & YouTube3Healthcare4Multilingual2

Interview Agent

English / Hinglish

Gram Panchayat Assistant

Hindi

Medical Appointment Booking

Hinglish

Transcript

Start Transcription

These examples highlight how unified multilingual modeling, streaming-first design, and structured audio intelligence combine to enable deployable, production-grade audio experiences, not just accurate transcripts.

## Experience Saaras V3 on APIs Today

For teams that want to dive straight into trying Saaras V3 and test the model’s limits, we have built an interactive no-code experience within the Sarvam Dashboard.

Get started instantly with our no-code, interactive experience on the Sarvam API Platform:[![](https://www.google.com/s2/favicons?domain=dashboard.sarvam.ai&sz=32)Sarvam Platform](https://dashboard.sarvam.ai/speech-to-text)

Looking to integrate the **Saaras V3 API** within your Products/Applications? Check out our API Dev docs! We have ready to go SDKs & code snippets to help you get **setup in minutes:**

**Want to enable Saaras V3 within your Voice Agents on Pipecat / Livekit?**

Building voice agents?

End-to-end pricing with the models included, as low as ₹3 a minute. 

[ Explore Voice Agents pricing ](https://sarvam.ai/products/voice-agents/pricing)

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
