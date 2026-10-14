---
url: https://sarvam.ai/apis/speech-to-text/telugu/
title: Telugu Speech to Text API | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:38.723070+00:00
---

# Telugu Speech to Text API | Sarvam AI

> Source: https://sarvam.ai/apis/speech-to-text/telugu/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

# Speech to Text,   
perfected for Telugu

Every accent. Every dialect. Code-switching mid-sentence. Saaras hears Telugu the way you actually speak it.

[Try Telugu STT free](https://indus.sarvam.ai)[Contact Us](https://sarvam.ai/contact-us)

### Speak Telugu to see live captions

Start speaking in Telugu

Want to use this API?

Get 100 credits free

## Every Telugu word,  
captured accurately

Code-mixing. Numbers. Proper nouns. Abbreviations.

PlayPlay Audio

0:00

అవునునేనుPROPER NOUNFlipkartనుండిNUMBER12,499రూపాయలకిENTITYSamsungGalaxyCODE SWITCHఫోన్ఆర్డర్చేశానునా ఆర్డర్ఐడిABBREVIATIONFLK-78234-XNCODE SWITCHడెలివరీఅడ్రస్వచ్చేసిForty42PROPER NOUNKoramangala5th Block, Bengaluruఫోన్నంబర్PHONE NUMBER9840950950CODE SWITCHప్లీజ్కొంచెండెలివరీ తొందరగా చేయండినా పాత ఫోన్ అస్సలు పని చేయటం లేదు

✱01

అవునునేనుPROPER NOUNFlipkartనుండిNUMBER12,499రూపాయలకిENTITYSamsungGalaxyCODE SWITCHఫోన్ఆర్డర్

0:00

✱02

చేశానునా ఆర్డర్ఐడిABBREVIATIONFLK-78234-XNCODE SWITCHడెలివరీఅడ్రస్వచ్చేసిForty42PROPER NOUNKoramangala5th Block, Bengaluruఫోన్

0:06

✱03

నంబర్PHONE NUMBER9840950950CODE SWITCHప్లీజ్కొంచెండెలివరీ తొందరగా చేయండినా పాత ఫోన్ అస్సలు పని చేయటం లేదు

0:18

## Flexible output. Same Telugu audio,  
multiple formats

### Transcribe

With formatting and number normalization.

Output

నా ఫోన్ నంబర్ 9840950950

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

నా ఫోన్ నంబర్ 9840950950

## Saaras hears తెలుగు the  
way you speak it

Every feature shown with real Telugu audio. Play each clip. Read the transcript. See the difference.

Speaker Diarization

### Know who said what

Automatically labels speakers in multi-party Telugu conversations. Colors match the transcript.

Saaras v3

Play

Bank support callTelugu · 2 speakers · 0:12 · 0:00

Click to play

Play

0:00Speaker 1

నమస్కారం, HDFC బ్యాంక్‌కి కాల్ చేసినందుకు ధన్యవాదాలు. నా పేరు ప్రియా, నేను మీకు ఏ విధంగా సహాయపడగలను?

0:00Speaker 2

హలో అండి, నేను నా savings account balance check చేయాలనుకుంటున్నాను. నా account number 2641-0078-3395.

0:00Speaker 1

తప్పకుండా అండి, verification కోసం మీ registered mobile number confirm చేయండి.

Code-Mixing

### Seamless Tenglish

Handles mid-sentence switching between Telugu and English. No drops, no accent shifts.

Saaras v3

Play

Casual conversationTenglish · 0:06 · 0:00

Click to play

Play

ఇరోజు మీటింగ్ చాల్ల ప్రడక్టివిగా జరిగింది లంచ్ తర్వాత కోడింగ్ సిష్ణ్ అంతా స్మూత్యా సాగిపేంది టిమ్ అంతా కలిసి చక్కగా పంచ మీటింగ్ చాల్ల ప్రడక్టివిగా ప్రడక్టివిగా పంచ

Telephony-Optimized

### Built for real calls

8kHz call center audio, compression, background noise. Maintains accuracy for Telugu where others fail.

8kHzNoisy

Saaras v3

Play

Street interviewTelugu · 8kHz · 0:10 · 0:00

Click to play

Play

అయితే, ప్రస్తుత ప్రభుత్వ పనితీరు గురించి మీకు ఏమనిపిస్తుంది? చూడండి, రోడ్లు బాగానే వేశారు, కానీ ధరలు చాలా పెరిగిపోయాయి. పెట్రోల్ ధర ₹108 అయిపోయింది. సామాన్య ప్రజలకు relief కావాలి. మిగతా metro పనులు బాగా జరుగుతున్నాయి, Nagpur లో చాలా development జరుగుతోంది.

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

### How accurate is Telugu speech to text?

Saaras v3 achieves industry-leading word error rates for Telugu, trained on diverse speech data covering regional accents and conversational patterns.

### Does it handle Telugu-English code-mixing?

Yes. Saaras v3 handles natural Telugu-English code-switching seamlessly without accent shifts or dropped words.

### Can I use Telugu STT for real-time voice agents?

Yes. Our WebSocket streaming API delivers sub-250ms latency for Telugu, ideal for real-time voice agents and conversational AI.

### What audio formats are supported?

10+ formats including MP3, WAV, AAC, OGG, Opus, FLAC, M4A, AMR, WMA, and WebM. Streaming API supports WAV and raw PCM at 16kHz.

Transcribe in 22 Indian languages Powered by Saaras v3 

Transcribe in 22 Indian languages

Powered by Saaras v3

[Sign Up](https://indus.sarvam.ai/speech-to-text)
