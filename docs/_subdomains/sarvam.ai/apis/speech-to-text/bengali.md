---
url: https://sarvam.ai/apis/speech-to-text/bengali/
title: Bengali Speech to Text API | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:37.065226+00:00
---

# Bengali Speech to Text API | Sarvam AI

> Source: https://sarvam.ai/apis/speech-to-text/bengali/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

# Speech to Text,   
perfected for Bengali

Every accent. Conjunct consonants. Benglish switching. Saaras hears Bengali the way Bengalis actually speak it.

[Try Bengali STT free](https://indus.sarvam.ai)[Contact Us](https://sarvam.ai/contact-us)

### Speak Bengali to see live captions

Start speaking in Bengali

Want to use this API?

Get 100 credits free

## Every Bengali word,  
captured accurately

Code-mixing. Numbers. Proper nouns. Abbreviations.

PlayPlay Audio

0:00

হ্যাঁআমিPROPER NOUNFlipkartথেকেNUMBER₹12,499এরএকটাENTITYSamsungGalaxyCODE SWITCHphoneorderকরেছিলাম।OrderIDহলোABBREVIATIONFLK-78234-XN।CODE SWITCHDeliveryaddressহলো42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangalore।আমারphonenumberহলোPHONE NUMBER9840950950।CODE SWITCHPleasedeliveryটাএকটুতাড়াতাড়িকরেদিন,আমারপুরোনোফোনটাএকদমকাজকরছেনা।

✱01

হ্যাঁআমিPROPER NOUNFlipkartথেকেNUMBER₹12,499এরএকটাENTITYSamsungGalaxyCODE SWITCHphoneorderকরেছিলাম।

0:00

✱02

OrderIDহলোABBREVIATIONFLK-78234-XN।

0:06

✱03

CODE SWITCHDeliveryaddressহলো42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangalore।

0:11

✱04

আমারphonenumberহলোPHONE NUMBER9840950950।

0:15

✱05

CODE SWITCHPleasedeliveryটাএকটুতাড়াতাড়িকরেদিন,আমারপুরোনোফোনটাএকদমকাজকরছে

0:19

✱06

না।

0:24

## Flexible output. Same Bengali audio,  
multiple formats

### Transcribe

With formatting and number normalization.

Output

আমার ফোন নম্বর হলো 9840950950

### Translate

From Indic languages to English.

Output

My phone number is 9840950950

### Transliteration

Indian languages written in English letters.

Output

amar phone number holo 9840950950

### Verbatim

Preserves fillers and spoken numbers.

Output

আমার ফোন নম্বর হলো নয় আট চার zero নয় পাঁচ zero নয় পাঁচ zero

## Saaras hears বাংলা the  
way you speak it

Every feature shown with real Bengali audio. Play each clip. Read the transcript. See the difference.

Speaker Diarization

### Know who said what

Automatically labels speakers in multi-party Bengali conversations. Colors match the transcript.

Saaras v3

Play

Bank support callBengali · 2 speakers · 0:12 · 0:00

Click to play

Play

0:04Speaker 1

নমস্কার, HDFC bank-এ call করার জন্য ধন্যবাদ। আমি প্রিয়া বলছি, আপনাকে কীভাবে help করতে পারি?

0:09Speaker 2

হ্যাঁ, আমি আমার savings account-এর balance check করতে চাই। Account number হলো 2641-0078-3395।

0:18Speaker 1

অবশ্যই, verification-এর জন্য আপনার registered mobile numberটা confirm করুন।

Code-Mixing

### Seamless Benglish

Handles mid-sentence switching between Bengali and English. No drops, no accent shifts.

Saaras v3

Play

Casual conversationBenglish · 0:06 · 0:00

Click to play

Play

আজকের Code-switchmeetingটা খুব productive ছিল। Lunch-এর পর Englishcoding session-টা একদম smooth গেছে। Team দারুণ কাজ করেছে।

Telephony-Optimized

### Built for real calls

8kHz call center audio, compression, background noise. Maintains accuracy for Bengali where others fail.

8kHzNoisy

Saaras v3

Play

Street interviewBengali · 8kHz · 0:10 · 0:00

Click to play

Play

আচ্ছা, বর্তমান সরকার-এর কাজকর্ম আপনার কেমন লাগছে? দেখুন, রাস্তাঘাট তো হয়েছে, কিন্তু জিনিসপত্রের দাম অনেক বেড়ে গেছে। পেট্রোলের দাম ₹108 হয়ে গেছে। সাধারণ মানুষ একটু relief চায়। তবে metro-র কাজ ভালো চলছে, Nagpur-এ অনেক development হচ্ছে।

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

### How accurate is Bengali speech to text?

Saaras v3 achieves industry-leading accuracy for Bengali, correctly processing complex conjunct consonant forms across literary and colloquial speech.

### Does it handle Benglish code-mixing?

Yes. Saaras v3 handles natural Bengali-English code-switching seamlessly without accent shifts or dropped words.

### Can I use Bengali STT for real-time voice agents?

Yes. Our WebSocket streaming API delivers sub-250ms latency for Bengali, ideal for real-time voice agents and conversational AI.

### Does it understand Bengali dialects?

Saaras v3 is trained on diverse Bengali speech data including Kolkata Bengali, Bangladeshi Bengali influences, and regional variations across West Bengal.

### What audio formats are supported?

10+ formats including MP3, WAV, AAC, OGG, Opus, FLAC, M4A, AMR, WMA, and WebM. Streaming API supports WAV and raw PCM at 16kHz.

Transcribe in 22 Indian languages Powered by Saaras v3 

Transcribe in 22 Indian languages

Powered by Saaras v3

[Sign Up](https://indus.sarvam.ai/speech-to-text)
