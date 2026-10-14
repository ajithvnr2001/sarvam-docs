---
url: https://www.sarvam.ai/apis/speech-to-text/maithili/
title: Maithili Speech to Text API | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:53.701528+00:00
---

# Maithili Speech to Text API | Sarvam AI

> Source: https://www.sarvam.ai/apis/speech-to-text/maithili/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

# Speech to Text,   
perfected for Maithili

Every accent. Every dialect. Code-switching mid-sentence. Saaras hears Maithili the way you actually speak it.

[Try Maithili STT free](https://indus.sarvam.ai)[Contact Us](https://www.sarvam.ai/contact-us)

### Speak Maithili to see live captions

Start speaking in Maithili

Want to use this API?

Get 100 credits free

## Every Maithili word,  
captured accurately

Code-mixing. Numbers. Proper nouns. Abbreviations.

PlayPlay Audio

0:00

हाँहमPROPER NOUNFlipkartसँNUMBER₹12,499केरENTITYSamsungGalaxyCODE SWITCHफ़ोनऑर्डरकयनेछलहुँऑर्डरIDABBREVIATIONFLK-78234-XNCODE SWITCHडिलीवरीएड्रेसअछि42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangaloreहमरफ़ोननंबरअछिPHONE NUMBER9840950950CODE SWITCHप्लीज़डिलीवरीजल्दीकsदिअहमरपुरानफ़ोनबिल्कुलकाजनहिकsरहल अछि

✱01

हाँहमPROPER NOUNFlipkartसँNUMBER₹12,499केरENTITYSamsungGalaxyCODE SWITCHफ़ोनऑर्डर

0:00

✱02

कयनेछलहुँऑर्डरIDABBREVIATIONFLK-78234-XN

0:06

✱03

CODE SWITCHडिलीवरीएड्रेसअछि42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangaloreहमरफ़ोननंबरअछि

0:12

✱04

PHONE NUMBER9840950950CODE SWITCHप्लीज़डिलीवरीजल्दीकsदिअहमरपुरानफ़ोनबिल्कुल

0:21

✱05

काजनहिकsरहल अछि

0:30

## Flexible output. Same Maithili audio,  
multiple formats

### Transcribe

With formatting and number normalization.

Output

हमर फोन नंबर 9840950950

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

हमर फोन नंबर 9840950950

## Saaras hears मैथिली the  
way you speak it

Every feature shown with real Maithili audio. Play each clip. Read the transcript. See the difference.

Speaker Diarization

### Know who said what

Automatically labels speakers in multi-party Maithili conversations. Colors match the transcript.

Saaras v3

Play

Bank support callMaithili · 2 speakers · 0:12 · 0:00

Click to play

Play

0:00Speaker 1

नमस्कार, HDFC बैंकमे कॉल करबाक लेल धन्यवाद। हम प्रिया बात कs रहल छी, अहाँक कोना मदति कs सकैत छी?

0:09Speaker 2

हाँ, हम अपन savings account केर balance check करय चाहैत छी। Account number अछि 2641-0078-3395।

0:21Speaker 1

अवश्य, verification के लेल अपन registered mobile number confirm कs दिअ।

Code-Mixing

### Seamless Maithili-English

Handles mid-sentence switching between Maithili and English. No drops, no accent shifts.

Saaras v3

Play

Casual conversationMaithili-English · 0:06 · 0:00

Click to play

Play

आजुक मीटिंग बट प्रोडक्टिव रहल लंच के रबाद कोडिंग सेशन में सब किच स्मूध चलल टीम बट नीक काज के लग

Telephony-Optimized

### Built for real calls

8kHz call center audio, compression, background noise. Maintains accuracy for Maithili where others fail.

8kHzNoisy

Saaras v3

Play

Street interviewMaithili · 8kHz · 0:10 · 0:00

Click to play

Play

नीक, मौजूदा सरकार केर कामकाज अहाँकेँ केहन लगैत अछि? देखू, सड़क तs बनल अछग, मुदा महंगाई बड्ड बढ़ि गेल अछि। पेट्रोलक दाम ₹108 भs गेल अछि। आम आदमीकेँ relief चाही। बाकी metro केर काज नीक चलि रहल अछि, Nagpur मे बड्ड development भs रहल अछि।

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

### How accurate is Maithili speech to text?

Saaras v3 achieves industry-leading word error rates for Maithili, trained on diverse speech data covering regional accents and conversational patterns.

### Does it handle Maithili-English code-mixing?

Yes. Saaras v3 handles natural Maithili-English code-switching seamlessly without accent shifts or dropped words.

### Can I use Maithili STT for real-time voice agents?

Yes. Our WebSocket streaming API delivers sub-250ms latency for Maithili, ideal for real-time voice agents and conversational AI.

### What audio formats are supported?

10+ formats including MP3, WAV, AAC, OGG, Opus, FLAC, M4A, AMR, WMA, and WebM. Streaming API supports WAV and raw PCM at 16kHz.

Transcribe in 22 Indian languages Powered by Saaras v3 

Transcribe in 22 Indian languages

Powered by Saaras v3

[Sign Up](https://indus.sarvam.ai/speech-to-text)
