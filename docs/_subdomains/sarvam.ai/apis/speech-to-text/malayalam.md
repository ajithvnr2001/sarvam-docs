---
url: https://sarvam.ai/apis/speech-to-text/malayalam/
title: Malayalam Speech to Text API | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:40.743066+00:00
---

# Malayalam Speech to Text API | Sarvam AI

> Source: https://sarvam.ai/apis/speech-to-text/malayalam/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

# Speech to Text,   
perfected for Malayalam

Every accent. Every dialect. Code-switching mid-sentence. Saaras hears Malayalam the way you actually speak it.

[Try Malayalam STT free](https://indus.sarvam.ai)[Contact Us](https://sarvam.ai/contact-us)

### Speak Malayalam to see live captions

Start speaking in Malayalam

Want to use this API?

Get 100 credits free

## Every Malayalam word,  
captured accurately

Code-mixing. Numbers. Proper nouns. Abbreviations.

PlayPlay Audio

0:00

അതെ,ഞാൻPROPER NOUNFlipkart-ൽനിന്ന്NUMBER12,499രൂപക്ക്ഒരുENTITYSamsungGalaxyCODE SWITCHphoneorderചെയ്ത്ഇരുന്നു.OrderIDABBREVIATIONFLK78234-XNആണ്.CODE SWITCHDeliveryaddress42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangaloreആണ്.എൻ്റെphonenumberPHONE NUMBER9840950950ആണ്.CODE SWITCHPlease,അത്വേഗംdeliverചെയ്യുക,എൻ്റെ

✱01

അതെ,ഞാൻPROPER NOUNFlipkart-ൽനിന്ന്NUMBER12,499രൂപക്ക്ഒരുENTITYSamsungGalaxyCODE SWITCHphoneorder

0:00

✱02

ചെയ്ത്ഇരുന്നു.

0:06

✱03

OrderIDABBREVIATIONFLK78234-XNആണ്.

0:07

✱04

CODE SWITCHDeliveryaddress42,PROPER NOUNKoramangala5thBlock,PROPER NOUNBangaloreആണ്.

0:12

✱05

എൻ്റെphonenumberPHONE NUMBER9840950950ആണ്.

0:17

✱06

CODE SWITCHPlease,അത്വേഗംdeliverചെയ്യുക,എൻ്റെ

0:22

## Flexible output. Same Malayalam audio,  
multiple formats

### Transcribe

With formatting and number normalization.

Output

എന്റെ ഫോൺ നമ്പർ 9840950950

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

എന്റെ ഫോൺ നമ്പർ 9840950950

## Saaras hears മലയാളം the  
way you speak it

Every feature shown with real Malayalam audio. Play each clip. Read the transcript. See the difference.

Speaker Diarization

### Know who said what

Automatically labels speakers in multi-party Malayalam conversations. Colors match the transcript.

Saaras v3

Play

Bank support callMalayalam · 2 speakers · 0:12 · 0:00

Click to play

Play

0:00Speaker 1

Hello, HDFC Bank-ൽ വിളിച്ചതിന്‌ നന്ദി. ഞാൻ Priya, ഞാൻ താങ്കളെ എങ്ങനെയാണ് help ചെയ്യേണ്ടത്?

0:02Speaker 2

എനിക്ക് എന്‌റെ savings account balance check ചെയ്യണം. Account number 2641-0078-3395 ആണ്.

0:13Speaker 1

Sure, verification-ന് വേണ്ടി ദയവായി താങ്കളുടെ registered mobile number confirm ചെയ്യുക.

Code-Mixing

### Seamless Manglish

Handles mid-sentence switching between Malayalam and English. No drops, no accent shifts.

Saaras v3

Play

Casual conversationManglish · 0:06 · 0:00

Click to play

Play

Today's Code-switchmeeting was super productive. After lunch, the coding session went smoothly. The team really did great work.

Telephony-Optimized

### Built for real calls

8kHz call center audio, compression, background noise. Maintains accuracy for Malayalam where others fail.

8kHzNoisy

Saaras v3

Play

Street interviewMalayalam · 8kHz · 0:10 · 0:00

Click to play

Play

അപ്പൊ, current government-ന്‌റെ പ്രവർത്തനങ്ങളെ കുറിച്ച് നിങ്ങൾക്ക് എന്ത് തോന്നുന്നു? നോക്കൂ, roads ഒക്കെ പണിതിട്ടുണ്ട്, പക്ഷെ inflation ഒരുപാട് കൂടിയിട്ടുണ്ട്. Petrol prices ₹108 ആയി. സാധാരണക്കാർക്ക് ഒരു relief വേണം. അതല്ലാതെ, metro work നന്നായി പോകുന്നുണ്ട്, Nagpur-ൽ ഒരുപാട് development നടക്കുന്നുണ്ട്.

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

### How accurate is Malayalam speech to text?

Saaras v3 achieves industry-leading word error rates for Malayalam, trained on diverse speech data covering regional accents and conversational patterns.

### Does it handle Malayalam-English code-mixing?

Yes. Saaras v3 handles natural Malayalam-English code-switching seamlessly without accent shifts or dropped words.

### Can I use Malayalam STT for real-time voice agents?

Yes. Our WebSocket streaming API delivers sub-250ms latency for Malayalam, ideal for real-time voice agents and conversational AI.

### What audio formats are supported?

10+ formats including MP3, WAV, AAC, OGG, Opus, FLAC, M4A, AMR, WMA, and WebM. Streaming API supports WAV and raw PCM at 16kHz.

Transcribe in 22 Indian languages Powered by Saaras v3 

Transcribe in 22 Indian languages

Powered by Saaras v3

[Sign Up](https://indus.sarvam.ai/speech-to-text)
