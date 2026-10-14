---
url: https://www.sarvam.ai/apis/speech-to-text/nepali/
title: Nepali Speech to Text API | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:52.038297+00:00
---

# Nepali Speech to Text API | Sarvam AI

> Source: https://www.sarvam.ai/apis/speech-to-text/nepali/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

# Speech to Text,   
perfected for Nepali

Every accent. Every dialect. Code-switching mid-sentence. Saaras hears Nepali the way you actually speak it.

[Try Nepali STT free](https://indus.sarvam.ai)[Contact Us](https://www.sarvam.ai/contact-us)

### Speak Nepali to see live captions

Start speaking in Nepali

Want to use this API?

Get 100 credits free

## Every Nepali word,  
captured accurately

Code-mixing. Numbers. Proper nouns. Abbreviations.

PlayPlay Audio

0:00

PROPER NOUNफ्लिपकार्डबाटNUMBER12,499रुपियाँकोENTITYSamsungGalaxyCODE SWITCHफोनअर्डरगरेकोथिएँ।त्यसकोअर्डरIDABBREVIATIONFLK-78234-XNहो,अनिCODE SWITCHडेलिभरीएड्रेस42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangaloreहो,मेरोफोननम्बरPHONE NUMBER9840950950हो,CODE SWITCHप्लिजडेलिभरीछिटोगरिदिनुहोला,मेरोपुरानो फोनले काम नै गरिरहेको छैन।

✱01

PROPER NOUNफ्लिपकार्डबाटNUMBER12,499रुपियाँकोENTITYSamsungGalaxyCODE SWITCHफोनअर्डरगरेकोथिएँ।

0:00

✱02

त्यसकोअर्डरIDABBREVIATIONFLK-78234-XNहो,अनिCODE SWITCHडेलिभरीएड्रेस42,PROPER NOUNKoramangala5thBlock,

0:05

✱03

PROPER NOUNBangaloreहो,मेरोफोननम्बरPHONE NUMBER9840950950हो,CODE SWITCHप्लिजडेलिभरीछिटोगरिदिनु

0:14

✱04

होला,मेरोपुरानो फोनले काम नै गरिरहेको छैन।

0:22

## Flexible output. Same Nepali audio,  
multiple formats

### Transcribe

With formatting and number normalization.

Output

मेरो फोन नम्बर 9840950950

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

मेरो फोन नम्बर 9840950950

## Saaras hears नेपाली the  
way you speak it

Every feature shown with real Nepali audio. Play each clip. Read the transcript. See the difference.

Speaker Diarization

### Know who said what

Automatically labels speakers in multi-party Nepali conversations. Colors match the transcript.

Saaras v3

Play

Bank support callNepali · 2 speakers · 0:12 · 0:00

Click to play

Play

0:00Speaker 1

नमस्कार, HDFC ब्याङ्कमा कल गर्नु भएकोमा धन्यवाद। म प्रिया हुँ, तपाईँलाई कसरी सहयोग गर्न सक्छु?

0:00Speaker 2

हजुर, म आफ्नो savings account को balance check गर्न चाहन्छु। मेरो Account number 2641-0078-3395 हो।

0:00Speaker 1

अवश्य, verification को लागि आफ्नो registered mobile number confirm गरिदिनुहोस् न।

Code-Mixing

### Seamless Nepali-English

Handles mid-sentence switching between Nepali and English. No drops, no accent shifts.

Saaras v3

Play

Casual conversationNepali-English · 0:06 · 0:00

Click to play

Play

को मिटिंग धेरै प्रोडक्टिव भायो, लंच पछे को कोडिंग सेशन मा सवै कुराई स्मूध भायो, तिमले धेरै राम्र काम गर्यो.

Telephony-Optimized

### Built for real calls

8kHz call center audio, compression, background noise. Maintains accuracy for Nepali where others fail.

8kHzNoisy

Saaras v3

Play

Street interviewNepali · 8kHz · 0:10 · 0:00

Click to play

Play

भन्नुहोस् त! वर्तमान सरकारको कामकाज तपाईँलाई कस्तो लागिरहेको छ? हेर्नुहोस्, सडक त बनिएको छ तर महँगी धेरै बढेर गयो। पेट्रोलकै दाम पनि 108 रुपियाँ भइसक्यो। आम मानिसहरूलाई relief चाहिन्छ। अरू हेर्दा metro को काम राम्रै चल्दैछ, Nagpur मा पनि धेरै development हुँदैछ।

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

### How accurate is Nepali speech to text?

Saaras v3 achieves industry-leading word error rates for Nepali, trained on diverse speech data covering regional accents and conversational patterns.

### Does it handle Nepali-English code-mixing?

Yes. Saaras v3 handles natural Nepali-English code-switching seamlessly without accent shifts or dropped words.

### Can I use Nepali STT for real-time voice agents?

Yes. Our WebSocket streaming API delivers sub-250ms latency for Nepali, ideal for real-time voice agents and conversational AI.

### What audio formats are supported?

10+ formats including MP3, WAV, AAC, OGG, Opus, FLAC, M4A, AMR, WMA, and WebM. Streaming API supports WAV and raw PCM at 16kHz.

Transcribe in 22 Indian languages Powered by Saaras v3 

Transcribe in 22 Indian languages

Powered by Saaras v3

[Sign Up](https://indus.sarvam.ai/speech-to-text)
