---
url: https://sarvam.ai/apis/speech-to-text/hindi/
title: Hindi Speech to Text API | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:37.448853+00:00
---

# Hindi Speech to Text API | Sarvam AI

> Source: https://sarvam.ai/apis/speech-to-text/hindi/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

# Speech to Text,   
perfected for Hindi

Understands Hindi even with background noise, multiple accents, or   
mid-sentence language switches.

[Try Hindi STT free](https://indus.sarvam.ai)[Contact Us](https://sarvam.ai/contact-us)

### Speak Hindi to see live captions

Start speaking in Hindi

Want to use this API?

Get 100 credits free

## Every Hindi word,  
captured accurately

Code-mixing. Numbers. Proper nouns. Abbreviations.

PlayPlay Audio

0:00

हाँमैंनेPROPER NOUNFlipkartसेNUMBER₹12,499काENTITYSamsungGalaxyCODE SWITCHफ़ोनऑर्डरकियाथा।ऑर्डरIDहैABBREVIATIONFLK-78234-XN।CODE SWITCHडिलीवरीएड्रेसहै42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangalore।मेराफ़ोननंबरहैPHONE NUMBER9840950950।CODE SWITCHप्लीज़डिलीवरीजल्दीकरदीजिए,मेरापुरानाफ़ोनबिल्कुलकामनहींकररहा।

✱01

हाँमैंनेPROPER NOUNFlipkartसेNUMBER₹12,499काENTITYSamsungGalaxyCODE SWITCHफ़ोनऑर्डरकियाथा।

0:00

✱02

ऑर्डरIDहैABBREVIATIONFLK-78234-XN।

0:06

✱03

CODE SWITCHडिलीवरीएड्रेसहै42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangalore।

0:12

✱04

मेराफ़ोननंबरहैPHONE NUMBER9840950950।

0:17

✱05

CODE SWITCHप्लीज़डिलीवरीजल्दीकरदीजिए,मेरापुरानाफ़ोनबिल्कुलकामनहींकर

0:21

✱06

रहा।

0:24

## Flexible output. Same Hindi audio,  
multiple formats

### Transcribe

With formatting and number normalization.

Output

मेरा फोन नंबर है 9840950950

### Translate

From Indic languages to English.

Output

My phone number is 9840950950

### Transliteration

Indian languages written in English letters.

Output

mera phone number hai 9840950950

### Verbatim

Preserves fillers and spoken numbers.

Output

मेरा फोन नंबर है नौ आठ चार zero नौ पांच zero नौ पांच zero

## Saaras hears हिन्दी the  
way you speak it

Every feature shown with real Hindi audio. Play each clip. Read the transcript. See the difference.

Speaker Diarization

### Know who said what

Automatically labels speakers in multi-party Hindi conversations. Colors match the transcript.

Saaras v3

Play

Bank support callHindi · 2 speakers · 0:12 · 0:00

Click to play

Play

0:00Speaker 1

नमस्कार डब्ल्यूसी बैंक में संपर्क करने के लिए आपका धन्यवाद। मैं गीतिका आपकी किस प्रकार सहायता कर सकती हूँ?

0:09Speaker 2

नमस्कार मैं एक गिरवी लोन के आवेदन पूरा करना चाहती हूँ कृपया मुझे प्रक्रिया बताइए

0:17Speaker 1

ज़रूर कृपया अपना अकाउंट नंबर और पैन कार्ड नंबर बताइए

Code-Mixing

### Seamless Hinglish

Handles mid-sentence switching between Hindi and English. No drops, no accent shifts.

Saaras v3

Play

Casual conversationHinglish · 0:06 · 0:00

Click to play

Play

आज का Hinglishमीटिंग बहुत Code-switchप्रोडक्टिव रहा। लंच के बाद Englishकोडिंग सेशन में सब कुछ स्मूथ चला। टीम ने बहुत अच्छा काम किया।

Telephony-Optimized

### Built for real calls

8kHz call center audio, compression, background noise. Maintains accuracy for Hindi where others fail.

8kHzNoisy

Saaras v3

Play

Street interviewHindi · 8kHz · 0:10 · 0:00

Click to play

Play

अच्छा, मौजूदा सरकार का कामकाज आपको कैसा लगता है? मोदी सरकार बढ़िया है। विधायक का कामकाज कैसा रहा?

Streaming API

### Real-time transcription

WebSocket streaming with sub-250ms latency. Words appear as they're spoken in Hindi.

Saaras v3

Play

Live transcriptionHindi · Streaming · 0:06 · 0:00

Click to play

Play

~90ms

भारत की सुबह का नज़ारा ही कुछ और होता है। चाय की चुस्की के साथ अखबार पढ़ना, बच्चों की किलकारियां सुनना।

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

### How accurate is Hindi speech to text?

Saaras v3 achieves industry-leading word error rates for Hindi, including conversational speech, regional accents, and noisy environments. It handles Hinglish code-mixing natively without accuracy degradation.

### Does it understand Hindi dialects?

Yes. Saaras v3 is trained on diverse Hindi speech data covering major dialects and regional accents from across India, including Bhojpuri-influenced Hindi, Rajasthani Hindi, and more.

### Can I use Hindi STT for real-time voice agents?

Absolutely. Our WebSocket streaming API delivers sub-250ms latency for Hindi, making it ideal for real-time voice agents, IVR systems, and conversational AI.

### How well does it handle Hinglish?

Saaras v3 was trained on natural Hindi-English code-switching patterns. It transcribes mid-sentence language switches accurately without dropping words or misattributing languages.

### What audio formats are supported?

10+ formats including MP3, WAV, AAC, OGG, Opus, FLAC, M4A, AMR, WMA, and WebM. Streaming API supports WAV and raw PCM at 16kHz.

Transcribe in 22 Indian languages Powered by Saaras v3 

Transcribe in 22 Indian languages

Powered by Saaras v3

[Sign Up](https://indus.sarvam.ai/speech-to-text)
