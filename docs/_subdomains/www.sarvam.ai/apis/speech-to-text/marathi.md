---
url: https://www.sarvam.ai/apis/speech-to-text/marathi/
title: Marathi Speech to Text API | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:48.397809+00:00
---

# Marathi Speech to Text API | Sarvam AI

> Source: https://www.sarvam.ai/apis/speech-to-text/marathi/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

# Speech to Text,   
perfected for Marathi

Every accent. Every dialect. Code-switching mid-sentence. Saaras hears Marathi the way you actually speak it.

[Try Marathi STT free](https://indus.sarvam.ai)[Contact Us](https://www.sarvam.ai/contact-us)

### Speak Marathi to see live captions

Start speaking in Marathi

Want to use this API?

Get 100 credits free

## Every Marathi word,  
captured accurately

Code-mixing. Numbers. Proper nouns. Abbreviations.

PlayPlay Audio

0:00

होमीPROPER NOUNFlipkartवरुनNUMBER₹12,499चाENTITYSamsungGalaxyCODE SWITCHफोनऑर्डरकेलाहोताऑर्डरIDआहेABBREVIATIONFLK78234-XNआणिCODE SWITCHडिलीवरीॲड्रेसआहे42,PROPER NOUNKoraMangala5thBlockPROPER NOUNBangaloreमाझाफोननंबरआहेPHONE NUMBER9840950950CODE SWITCHप्लीजडिलीव्हरीलवकरकरूशकालकामाझाजुनाफोनअगदीचकामकरतनाहीये

✱01

होमीPROPER NOUNFlipkartवरुनNUMBER₹12,499चाENTITYSamsungGalaxyCODE SWITCHफोनऑर्डरकेलाहोता

0:00

✱02

ऑर्डरIDआहेABBREVIATIONFLK78234-XNआणिCODE SWITCHडिलीवरीॲड्रेसआहे42,PROPER NOUNKoraMangala5thBlock

0:06

✱03

PROPER NOUNBangaloreमाझाफोननंबरआहेPHONE NUMBER9840950950CODE SWITCHप्लीजडिलीव्हरीलवकरकरू

0:16

✱04

शकालकामाझाजुनाफोनअगदीचकामकरतनाहीये

0:25

## Flexible output. Same Marathi audio,  
multiple formats

### Transcribe

With formatting and number normalization.

Output

माझा फोन नंबर 9840950950

### Translate

From Indic languages to English.

Output

My phone number is 9840950950

### Transliteration

Indian languages written in English letters.

Output

phone number 9840950950

### Verbatim

Preserves fillers and spoken numbers.

Output

माझा फोन नंबर 9840950950

## Saaras hears मराठी the  
way you speak it

Every feature shown with real Marathi audio. Play each clip. Read the transcript. See the difference.

Speaker Diarization

### Know who said what

Automatically labels speakers in multi-party Marathi conversations. Colors match the transcript.

Saaras v3

Play

Bank support callMarathi · 2 speakers · 0:12 · 0:00

Click to play

Play

0:01Speaker 1

नमस्कार, HDFC बँकेमध्ये कॉल केल्याबद्दल धन्यवाद. मी प्रिया बोलतीये. मी तुमची काय मदत करू शकते?

0:10Speaker 2

हो, मला माझ्या savings account चा balance check करायचा आहे. Account number आहे 2641-0078-3395.

0:20Speaker 1

ओके, verification साठी तुमचा registered mobile number confirm करा

Code-Mixing

### Seamless Minglish

Handles mid-sentence switching between Marathi and English. No drops, no accent shifts.

Saaras v3

Play

Casual conversationMinglish · 0:06 · 0:00

Click to play

Play

अच्छी मीटिंग सूपर प्रड़क्टिव जाली, लंच नंतर चा कोडिंग सेशन मदे तर सगला इक्तम स्मूथली जाला, टीम ने फारच चान काम केला

Telephony-Optimized

### Built for real calls

8kHz call center audio, compression, background noise. Maintains accuracy for Marathi where others fail.

8kHzNoisy

Saaras v3

Play

Street interviewMarathi · 8kHz · 0:10 · 0:00

Click to play

Play

अच्छा, तुम्हाला सध्याच्या सरकारच्या कामाबद्दल काय वाटतं? हे बघा, रस्ते तर बनले आहेत, पण महागाई प्रचंड वाढली आहे. पेट्रोलचा दर ₹108 झाला आहे. समान्य जनतेला जरा relief पाहिजे. बाकी metro चं काम चांगलं चालू आहे, Nagpur मध्ये खूप development होतीये.

## Developer-first platform

OpenAI-compatible APIs. Drop-in SDKs for Python and Node.js. Go from zero to first transcription in under 5 minutes.

REST & WebSocket APIs 

Standard REST for batch, WebSocket for real-time streaming with sub-250ms first byte. 

SDKs & libraries 

Official Python and Node.js SDKs with TypeScript support. pip install sarvam-ai. 

Complete documentation 

Interactive API reference, code samples, and integration guides for every endpoint. 

Free tier included 

Start building immediately. No credit card, no sales call, no minimum commitment. 

PythonJavaScriptcURL

Copy
    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    # Transcribe audio
    response = client.speech_to_text.transcribe(
        file_path="call_recording.wav",
        language_code="hi-IN",
        model="saaras:v3",
        with_diarization=True
    )
    
    print(response.transcript)
    for turn in response.turns:
        print(f"[{turn.speaker}] {turn.text}")

## Enterprise-ready. Responsible AI.

Built with safety, compliance, and data sovereignty at the core.

![SOC 2 Type II & ISO 27001](https://assets.sarvam.ai/assets/products/voice-agents/built-for/built-for-03.png)

###  SOC 2 Type II & ISO 27001 

Enterprise-grade security certifications. Annual audits, documented controls, continuous monitoring. 

![No training on your data](https://assets.sarvam.ai/assets/products/voice-agents/built-for/built-for-02.png)

###  No training on your data 

Your API inputs are never used for model training. Zero data retention after processing unless explicitly requested. 

![Data sovereignty](https://assets.sarvam.ai/assets/products/voice-agents/built-for/built-for-01.png)

###  Data sovereignty 

All data processed and stored in India. No cross-border transfers. Full compliance with Indian data regulations. 

![Audio data privacy](https://assets.sarvam.ai/assets/products/voice-agents/built-for/built-for-02.png)

###  Audio data privacy 

Audio data is processed in real-time and never stored unless explicitly requested. Complete privacy by default. 

![Content safety filters](https://assets.sarvam.ai/assets/products/voice-agents/built-for/built-for-01.png)

###  Content safety filters 

Automated detection and filtering of harmful, abusive, or misleading content in transcriptions. 

![Audit-ready logging](https://assets.sarvam.ai/assets/products/voice-agents/built-for/built-for-03.png)

###  Audit-ready logging 

Comprehensive API usage logs, access controls, and RBAC for enterprise governance and compliance reporting. 

##  Simple, transparent  
pricing 

Start free. Scale as you grow. No hidden costs. 

[ Sign up](https://indus.sarvam.ai)

Base plan 

₹1.25 per minute

Free trial included 

No credit card required. Get API keys instantly. 

Volume discounts available 

Enterprise pricing available 

Speaker diarization included 

Usage analytics 

All 22 languages 

Best for startups 

## Your questions, answered

### How accurate is Marathi speech to text?

Saaras v3 achieves industry-leading word error rates for Marathi, trained on diverse speech data covering regional accents and conversational patterns.

### Does it handle Marathi-English code-mixing?

Yes. Saaras v3 handles natural Marathi-English code-switching seamlessly without accent shifts or dropped words.

### Can I use Marathi STT for real-time voice agents?

Yes. Our WebSocket streaming API delivers sub-250ms latency for Marathi, ideal for real-time voice agents and conversational AI.

### What audio formats are supported?

10+ formats including MP3, WAV, AAC, OGG, Opus, FLAC, M4A, AMR, WMA, and WebM. Streaming API supports WAV and raw PCM at 16kHz.

Transcribe in 22 Indian languages Powered by Saaras v3 

Transcribe in 22 Indian languages

Powered by Saaras v3

[Sign Up](https://indus.sarvam.ai/speech-to-text)
