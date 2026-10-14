---
url: https://sarvam.ai/blogs/sarvam-audio/
title: Sarvam Audio: speech beyond transcription | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:25.664670+00:00
---

# Sarvam Audio: speech beyond transcription | Sarvam AI

> Source: https://sarvam.ai/blogs/sarvam-audio/

  1. [ Home ](https://sarvam.ai/)
  2. /
  3. [ Blog ](https://sarvam.ai/blogs)



# Sarvam Audio: Speech Recognition beyond Transcription

Research

* * *

Feb 3, 2026·6 min readShare

![Sarvam Audio: Speech Recognition beyond Transcription](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/ca4060d763b96a07f3954323d7a2f31d98a67f9e-1512x945.png)

India is a voice-first country. The rigid structure of a keyboard struggles to capture the fluidity of Indian languages, and for most people, speaking is simply more natural than typing. From farmers checking crop prices, to gig workers receiving navigation instructions, to elderly users navigating WhatsApp and smart TVs, voice is the default mode of interaction.

This reality presents both opportunity and challenge. Traditional automatic speech recognition (ASR) systems perform well on clean, read-speech benchmarks, but they often break down in real-world Indian settings. In practice, accuracy alone is an insufficient lens. Speech recognition in India must go beyond transcription.

#### Three core challenges stand out:

**First, script control** Indian speakers freely mix English into their speech. In some applications, English words must be preserved in Roman script while in others they must be transliterated into the native script. A single fixed output format does not work.

**Second, multi-speaker separation** Real-world audio often involves multiple speakers talking simultaneously. Accurate recognition requires not just transcription, but reliable speaker identification and attribution.

**Third, contextual awareness** Speech recognition systems must improve using context derived from prior turns in a conversation or from accumulated context in long-form audio. Without this, short utterances, ambiguous phrases, and noisy segments are routinely misinterpreted.

**Sarvam Audio** addresses these challenges.

Sarvam Audio is an audio extension of **Sarvam 3B** , a 3-billion-parameter language model pre-trained from scratch on English and 22 Indian languages. Sarvam Audio moves beyond traditional ASR systems by producing multiple, user-controlled transcription formats and modeling speech as a contextual signal to support robust recognition across long durations, conversational settings, multi-speaker audio, and action-oriented voice interactions.

### Artifact

Assamese

Bank Balance Check · 0:10

Bengali

EPFO Passbook Request · 0:08

Bodo

Voter ID Verification · 0:12

Dogri

Bank Deposit Confirmation · 0:06

Gujarati

AICTE Diploma Search · 0:10

Hindi

COVID Vaccination Certificate · 0:12

Kannada

Vikram Movie Debut · 0:14

Kashmiri

CoWIN Registration · 0:10

Konkani

HP Gas Cylinder Booking · 0:08

Maithili

Consumer ID Information · 0:10

Malayalam

Birth Registration Update · 0:12

Manipuri

Bank Transfer Request · 0:10

Marathi

Film Awards Achievement · 0:14

Nepali

Passport Details · 0:06

Odia

International Cities · 0:10

Punjabi

National Planning Commission · 0:18

Sanskrit

Jio Money Wallet Transfer · 0:08

Santali

Bank Account Number · 0:08

Sindhi

Bank Balance Check · 0:12

Tamil

Online Dress Purchase · 0:12

Telugu

Rowing Competition History · 0:16

Urdu

Running Training Focus · 0:08

LanguageAuto DetectAssameseBengaliBodoDogriEnglishGujaratiHindiKannadaKashmiriKonkaniMaithiliMalayalamManipuriMarathiNepaliOdiaPunjabiSanskritSantaliSindhiTamilTeluguUrdu

Upload your audio

Literal TranscriptionNon Code-MixedCode MixedRomanizedSmart Translate

মোৰ বেংক একাউণ্টৰ বেলেন্স চেক কৰক আৰু মোক জনাওক যে মোৰ একাউণ্টত কিমান টকা আছে

### Finely Controlled Transcription Format

Real-world speech applications require control not just over _what_ is transcribed, but _how_ it is rendered. Indian speech is inherently multilingual and code-mixed, and different downstream use cases demand different transcription formats.

Sarvam Audio allows applications to explicitly specify the desired transcription style at inference time. Sarvam Audio supports five transcription modes:

## Audio LM Voice Features

### Literal Transcription

Recommended for Call Centers & QA

Word-for-word transcription exactly as spoken. Pure verbatim output for compliance and analysis.

Marathi

आज संध्याकाळी पुण्याला जाणार आहे

00:00

### Normalised Non-Code-Mixed

Recommended for Logistics & E-commerce

Formatted output with numbers as numerals and proper punctuation. Great for addresses and order IDs.

Hindi

भैया क्या मेरा सामान मकान नंबर के 45 गली नंबर 12 गणेश नगर वाले पते पर पहुँच गया है क्या?

00:00

### Normalized Code-Mixed

Recommended for Banking & Fintech

Best of both worlds: native script with English terms preserved in Roman. Ideal for transactions, app names, and technical conversations.

Sanskrit

मम Jio Money Wallet मध्ये Canara Bank account इत्यस्मात् 9000 धनं योजयितुं शक्नोषि वा

00:00

### Romanized Output

Recommended for Chat & Messaging

Full transcription in Roman script. Readable by anyone, searchable everywhere. Great for WhatsApp Business and chat support.

Tamil

Bro work stress thaanga mudilla Next weekend engeyaachum veliye pogalaama Idea nalladhaan irukkudhu Aanaal enge pogiradhu Ootyaa Ootyelaam semma bore namma Munnar pogalaam Ippo climate angay semma chillaga irukkum superaagavum irukkum Sari okay busil pogalaama Illai train book ticket pannava Rendumae venam Rendumae selavu namma pesamal carlaye poyiralaam Aa appo budget konjam yeriduvume Yaaya adhaan namma share pannikkalaam ondrum prachannai illai va Kamla

00:00

### Smart Translate

Recommended for YouTube & Instagram

Speak in any Indian language, get English output instantly. Built for creators who want to reach a global audience.

Kannada → English

Punjabi → English

Hello sir, this is a perfect spot for Bangalore weather. Boss, a ragi mudde and country chicken gravy. Bro, it's literally melting in my mouth. The spice level is crazy. Don't miss this spot, the taste is next level.

00:00

#### Evaluation

To quantify the impact of transcription format control, Sarvam Audio is evaluated against GPT-4o-Transcribe and Gemini-3-Flash using the Word Error Rate (WER) metric across three transcription styles unnormalised, normalised, and code-mixed.

  * **Dataset:**[![](https://www.google.com/s2/favicons?domain=arxiv.org&sz=32) IndicVoices ](https://arxiv.org/abs/2403.01926)benchmark [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)evaluation set](https://huggingface.co/datasets/ai4bharat/IndicVoices), a large-scale dataset covering diverse, real-world Indian speech conditions
  * **Metric: Word Error Rate (Lower is better)** WER measures the minimum number of insertions, deletions, and substitutions required to match the reference transcription, normalized by the total number of words.



Across all transcription styles, Sarvam Audio consistently outperforms baseline models, demonstrating that format control need not come at the cost of accuracy.

### State-of-the-Art Diarized Speech Recognition

Real-world audio is rarely single-speaker. Meetings, interviews, and conversations often involve multiple speakers, overlapping speech, and rapid turn-taking. Accurate speech recognition in these settings requires both high-quality transcription and reliable speaker attribution.

Sarvam Audio achieves **state-of-the-art performance on diarized speech recognition** for audio up to**60 minutes** , accurately transcribing speech while identifying who spoke what.

### Multi-Speaker Transcription

Every word transcribed. Every speaker identified.

0:003:34

0:00 – 0:14

Speaker 1

એ રીતે તમે આગળ વધો પોતાની ધર્મની માન્યતાઓને ને પોતાના અત્યાર સુધી તમે પ્રેક્ટિસ કરતા આવ્યા છો એને છોડીને તમે એક જ નિયમ પ્રમાણે ચાલો તો આ યોગ્ય નહીં હોય કારણ કે આપણે જ્યારે દેશ બન્યો ત્યારે દરેકને આશ્વાસન આપ્યું હતું

0:14 – 0:27

Speaker 1

કે એમને જેવી રીતે દેશમાં શાંતિથી રહેવું હશે તો એમને છૂટ આપીશું પોતાના ધર્મ પ્રમાણે પોતાની જાતિ પ્રમાણે કે જે તેમના નિયમો હોય કોઈ કુટુંબના હોય કે જે હોય ગામના એ પ્રમાણે એ પ્રેક્ટિસ કરી શકશે

0:28 – 0:38

Speaker 1

તો આ હાલ ડિસ્કશનમાં ચાલે છે ને એના ફાયદા ગેરફાયદાનો આપણે ડિસ્કસ કરવાનો છે કે શું આવું કરવું જોઈએ હાલ સમય આવી ગયો છે કે બધાને ફોર્સફુલી

0:35 – 0:36

Speaker 2

શું આવું કરવું જોઈએ

0:39 – 0:58

Speaker 1

આપણે એક જ નિયમ બનાવી દઈએ ને બધાને કહીએ કે તમે આ જ નિયમ ફોલો કરો ચાહે તમે હિન્દુ હોય તો પણ તમે આ જ નિયમ ફોલો કરો તમારા ધર્મ ને છોડી દો મુસલમાન હતા તો એમના ધર્મના જે નિયમો હોય એ છોડો અને આને જ ફોલો કરો શું આ સમય આવી ગયો છે કે આપણે આવો કાનૂન બનાવવો જોઈએ જેવી રીતે અમેરિકામાં યુરોપમાં છે ત્યાં કોઈ ધર્મ ધર્મ નથી જોવામાં આવતું જ્યારે એ લોકો કોર્ટમાં જાય છે

0:59 – 1:04

Speaker 1

ત્યાં કોર્ટના દેશના કાનૂન પ્રમાણે કેસ લો કરવામાં આવે તો શું આવું ઇન્ડિયામાં કરવું જોઈએ આ એના વિશે છે

1:06 – 1:07

Speaker 2

એક દેશ એક કાયદો

1:10 – 1:14

Speaker 2

આપણે કહી શકીએ કે એક દેશ અને એક કાયદો બધાએ આ જ કાયદો માનવું જોઈએ

1:13 – 1:32

Speaker 1

કાયદો માનવો જોઈએ હા માનવો જોઈએ પછી તમે તમારો ધર્મ ગમે તે કહેતું હોય તમે ગમે તે માન્યતામાં માનતા હોવ તમને યોગ્ય લાગતું હોય પણ ફોર્સ કરવામાં આવશે ગવર્મેન્ટ તરફથી કે હવે તમારે આ જ માનવું પડશે તો આ યોગ્ય છે દરેક સાથે આવી રીતે ફોર્સફુલી એમનું ઇમ્પ્લિમેન્ટ કરવું હાલ શું આ સમય યોગ્ય છે લોકો એટલા મેચ્યોર છે

1:32 – 1:34

Speaker 1

આ હાલ ડિસ્કશન ચાલે છે

1:34 – 1:51

Speaker 2

મારા હિસાબથી આમાં જોવા જાય તો બંનેના નુકસાન છે અને બંનેના જ ફાયદા છે આપણે અગર આને ઇમ્પ્લિમેન્ટ કરીએ એક દેશ એક કાયદો તો આપણા ધાર્મિક સ્વતંત્રતામાં બી આપણે હસ્તક્ષેપ થાય છે આપણા સંસ્કૃતિને બી આપણે નુકસાન થાય છે

1:51 – 2:06

Speaker 2

અને આને અમલ કરવું મુશ્કેલ છે કારણ કે લોકો ધર્મના પ્રતિ ભારતમાં વધારે પડતા છે બધાને પોતાનો ધર્મ પહેલો છે એટલે આને લાગુ કરવું તો મુશ્કેલ છે જ અને લોકો તો

2:04 – 2:11

Speaker 3

અને લોકશાહી શાસનથી ભી ડિફરન્ટ થશે ને કે લોકો માટે લોકોથી અને લોકો વડે ચાલતું શાસન

2:11 – 2:35

Speaker 3

તો એના અગેન્સ્ટના પ્રોટોકોલમાં આપણે જતા રહીશું કારણ કે આ લોકોથી તો નહીં જ ચાલતું હોય ને કારણ કે આમાં તો એક એક તમે રૂલ્સ બનાવી દીધું એન્ડ એ બધાના ઉપર તમે થોપી દેવામાં આવે કે તમે લોકો કરો જ બરાબર શાયદ એમ એ લોકો માટે બેનિફિશિયલ હોય પણ ખરા ના બી હોઈ શકે તો એમના ધાર્મિક રિચ્યુઅલ્સ પ્રમાણે એ કનેક્ટ થતું પણ હોય કે ના પી થતું હોય

2:15 – 2:16

Speaker 2

અ

2:35 – 2:43

Speaker 3

તો આ લોકો માટે તો નહીં ચાલતું રહે તો આ લોકશાહીનો ભી ભંગ થાય એવું લાગી રહ્યું છે આમ આ આનાથી તો

2:44 – 2:59

Speaker 2

પણ આમાં ફાયદો બી એ છે કે આમાં કાયદા આમ સરળ થઈ જાય છે અને આમાં લોકો આમાં ગવર્મેન્ટ એવું વિચારે કે ધર્મના ઉપર નાગરિક નાગરિક તરીકે ઓળખ વધારે થાય અને આમાં સ્ત્રી પુરુષની સમાનતા બી થાય

3:00 – 3:08

Speaker 2

આપણને જેન્ડર ઇક્વાલિટી બી મળે આમાં સ્ત્રી પુરુષને બરાબર બી આવી શકે છે એ એક પોઇન્ટ છે જે મને ગમ્યો આમાં

3:07 – 3:07

Speaker 1

પોઈન્ટ છે

3:08 – 3:22

Speaker 1

મારે એવું માનવું છે કે આની અંદર બધા જે વિષયો છે એક સાથે લઈ લેવા કેમ કે જમીનનો ઇસ્યુ હોય અથવા તો શાદીનો હોય બીજા બધા જે ઇસ્યુઝના હોય એના કરતાં ગવર્મેન્ટે અમુક જે કોમન વિષયો હોય

3:22 – 3:34

Speaker 1

કે જેમાં કોઈ પ્રોબ્લેમ દરેકને વધારે થાય એવું નથી ધર્મની રીતે જેમ કે મારે કઈ પ્રોપર્ટી ખરીદવી છે એના માટેના નિયમો હોય કોઈ બિઝનેસના રિલેટેડ હોય અથવા બીજા કોઈ હોય તો પહેલાં શરૂઆત એમણે આનાથી કરવી જોઈએ

#### Evaluation

  * **Word Diarization Error Rate (WDER) (lower is better)** Measures the percentage of aligned words (including matches and substitutions) that are attributed to the wrong speaker.
  * **Diarization Error Rate (DER) (lower is better)** Measures the sum of speaker confusion, false alarms, and missed speech, normalized by total speech time.



**Evaluation setup**

  * In-house benchmark built from real-world meeting recordings
  * Expert human annotations
  * Audio length: 1-60 minutes
  * Up to 8 speakers
  * Significant overlapping speech



### Contextual Speech Recognition

Context is essential for decoding real-world audio. LLM backbone allows Sarvam Audio to leverage context given via textual description or conversational history, to significantly improve transcription quality in tricky scenarios.

  * **Resolving linguistic ambiguity in short utterances** When a user responds with “नौ (Nau)” to a quantity prompt, Sarvam Audio uses conversational context to correctly interpret it as the Hindi number _nine_ , rather than the English word _no_.
  * **Recovering meaning from noisy audio** In degraded acoustic environments, if a user says “Bhaiya, loc son bhejo”, Sarvam Audio uses delivery-domain context to reconstruct the intended phrase “Bhaiya, location bhejo”.
  * **Domain-aware transcription** In a stock-market discussion, Sarvam Audio correctly transcribes “M&M” as _Mahindra & Mahindra_, rather than the literal phrase “M and M”.



Examples

Marathi

### Bot description

You are a helpful and polite female assistant built for debt collection by Aurora Financial for interacting with users who have taken a loan at the bank and has pending EMIs.

### Conversation history

Assistant: नमस्कार. मी निशा, Aurora Financial कडून बोलते आहे. मी Priya Sharma यांच्याशी बोलते आहे का?

User: हा, याच्याशी बोलते आहे का?

### Output

Gemini_w_ctx: "हो, मीच बोलतेय, सांगा काय काम होतं?"

Gemini_w_no_ctx: "हाय, कशा आहात? मजेत ना?"

Sarvam_audio_w_no_ctx: "हा येस कशाबद्दल आहे का"

Sarvam_audio_w_ctx: "हा, याच्याशी बोलते आहे का?"

Hindi

### Bot description

You are a friendly, chatty female virtual assistant for Alpine Lending, India’s leading NBFC, who explains the company when asked and continues conversations in a warm, natural, and engaging manner.

### Conversation history

Assistant: नमस्ते। मैं ज़ेनिथ फ़ाइनेंस से पूजा बोल रही हूँ। क्या मैं दास जी से बात कर रही हूँ?

User: हाँ।

Assistant: आपको ज़ेनिथ फ़ाइनेंस से सेवेंटी फाइव थाउज़ेंड रुपीज़ का प्री-अप्रूव्ड लोन मिल सकता है, अच्छे इंटरेस्ट रेट पर, बिना इनकम प्रूफ के। आप इस ऑफर के लिए एलिजिबल हैं क्योंकि आप हमारे वैल्यूड एग्ज़िस्टिंग कस्टमर हैं। क्या आप और जानना चाहेंगे?

User: मैडम, मुझे क्या चाहिए?

Assistant: ज़ेनिथ फ़ाइनेंस के प्री-अप्रूव्ड लोन ऑफर के बारे में कॉल किया है। आपको सेवेंटी फाइव थाउज़ेंड रुपीज़ का लोन अच्छे इंटरेस्ट रेट पर मिल सकता है, इनकम प्रूफ की ज़रूरत नहीं है। क्या आप इस ऑफर के बारे में और जानना चाहेंगे?

User: मैं कितना कर्ज़ दे सकता हूँ, मैडम?

Assistant: आप सेवेंटी फाइव थाउज़ेंड रुपीज़ के लोन के लिए एलिजिबल हैं। क्या आप इस ऑफर के बारे में और जानना चाहेंगे?

User: क्या मैडम?

### Output

Gemini_w_ctx: "हाँ मैडम"

Gemini_w_no_ctx: "हाँ मैडम"

Sarvam_audio_w_no_ctx: "हा मैडम"

Sarvam_audio_w_ctx: "क्या मैडम?"

#### Evaluation

On a benchmark that mirrors real-world conversational speech across Indian languages,**Sarvam Audio** outperforms **Gemini-3-Flash**.

Rather than relying solely on WER or CER because they capture only word-level similarity, an **LLM-based intent and entity preservation score** is used that better reflects real conversational and command-based use cases.

Evaluation measures:

  * **Intent preservation** -Whether the core action and intent of the utterance are correctly understood.
  * **Entity preservation** -Whether critical entities such as names, numbers, locations, and organizations are retained.



Sarvam Audio demonstrates a consistent performance advantage across languages. The evaluation framework is open-sourced [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)here](https://github.com/sarvamai/llm_intent_entity), and the **Synthetic Contextual ASR Benchmark (Indic)** is publicly released on [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)Hugging Face](https://huggingface.co/datasets/sarvamai/contextual_asr_benchmark).

**Benchmark overview.** This benchmark evaluates **context-aware ASR** for voice-bot interactions across the **top 10 Indian languages**. Each sample represents a single dialog turn and includes audio, ground-truth transcription, language, and rich conversational context (bot persona, history, and prompt). The dataset is synthetically generated across domains such as Banking, E-commerce, and Healthcare, and is designed to test contextual biasing, intent preservation, and end-to-end spoken language understanding.

**Speech to Command**

Voice agents are now everywhere. Most existing systems rely on a two-stage architecture: audio is first transcribed by an ASR model and then interpreted by a separate LLM. While effective, this approach introduces additional latency and often breaks contextual continuity particularly for short or noisy utterances.

Sarvam Audio demonstrates that **high-precision function calling and parameter extraction can be performed directly on the audio modality.**

By operating end-to-end on speech:

  * Intent and context are preserved
  * Latency is significantly reduced
  * System complexity is simplified



Production-grade understanding can be achieved with small, domain-specific fine-tuning datasets, enabling fast and reliable deployment of voice agents without large-model overhead.

Pay Bill

### Bot description

Handles bill payment requests for electricity, gas, water, and mobile bills by validating bill details and processing payments.

### Conversation history

Assistant: வணக்கம்! நான் உங்கள் பேமெண்ட் அசிஸ்டெண்ட். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?

User: நான் எனது மின்சாரக் கட்டணத்தைச் செலுத்த வேண்டும்.

Assistant: கண்டிப்பாக, நீங்கள் எந்த நிறுவனத்திற்குச் செலுத்த விரும்புகிறீர்கள்?

User: BESCOM-க்குச் செலுத்த வேண்டும்.

Assistant: தயவுசெய்து உங்கள் கணக்கு எண்ணைத் தெரிவிக்கவும்.

User: எனது கணக்கு எண் 401242532.

Assistant: நன்றி. BESCOM கணக்கு எண் 401242532-க்கு 850 ரூபாய் கட்டணம் நிலுவையில் உள்ளது. நான் பேமெண்ட்டை உறுதிப்படுத்தலாமா?

### Tool Definition

Add Biller: Assists users in adding a new biller for bill payments by collecting the bill type, biller name, and account information.

Mobile Recharge: Handles mobile recharge requests by validating the mobile number, auto-detecting operator/circle, selecting recharge plans, and processing the recharge.

Pay Bill: Handles bill payment requests for electricity, gas, water, and mobile bills by validating bill details and processing payments.

### Output
    
    
    {
    
        "transcription": "ஆம், உறுதிப்படுத்திப் பணம் செலுத்துங்கள்.",
    
        "tool_call": "payBill",
    
        "params": {
    
            "biller_name": "BESCOM",
    
            "account_number": "401242532",
    
            "amount": "850"
    
        }
    
    }

In the example above, Sarvam Audio infers the appropriate function name and its arguments directly from the speech input, conditioned on prior conversational context, enabling precise function invocation.

### Conclusion

Sarvam Audio rethinks speech recognition for India from the ground up. It delivers **state-of-the-art ASR across 22 Indian languages and Indian English** , while addressing the realities of code-mixing, script variation, long-form audio, overlapping speakers, and conversational context.

More importantly, it goes beyond traditional ASR. With built-in context awareness, diarization, format control, and direct speech-to-command capabilities, Sarvam Audio forms the foundation for a new generation of voice-first applications and agents built for real Indian users.

Sarvam Audio will be **available soon on the[![](https://www.google.com/s2/favicons?domain=dashboard.sarvam.ai&sz=32) Sarvam Dashboard](https://dashboard.sarvam.ai)**.

Voice is the interface. Sarvam Audio makes it work for India.

Building voice agents?

End-to-end pricing with the models included, as low as ₹3 a minute. 

[ Explore Voice Agents pricing ](https://sarvam.ai/products/voice-agents/pricing)

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
