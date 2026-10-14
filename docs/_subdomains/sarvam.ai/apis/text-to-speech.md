---
url: https://sarvam.ai/apis/text-to-speech/
title: Text to Speech API for Indian Languages | Sarvam
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:26.642681+00:00
---

# Text to Speech API for Indian Languages | Sarvam

> Source: https://sarvam.ai/apis/text-to-speech/

# Bulbul V4Flash

Expressive, accurate, fast.

[Get API key](https://indus.sarvam.ai/signin)Try the playground

V4

V4

V4

V4

## Don't take our word for it. Listen.

Voice agentCollectionsHealthcareTelephonyStorytelling

### Rail helpline

An agent checks a waiting list, offers another train and books it. The "एक सेकंड" pauses are where it waits on a tool call.

Hindi · hi-IN · 24 kHz · Pace 1.0

Bulbul V3Bulbul V4 Flash

0:00 / 1:19 · press M to switch

  1. Agentनमस्ते! रेल सहायता में आपका स्वागत है। बताइए, मैं आपकी क्या मदद कर सकती हूँ?
  2. Customerहाँ जी, मेरा एक ticket waiting में है... बस उसका status जानना था।
  3. Agentज़रूर। आप अपना PNR number बता दीजिए।



Aparna · FemaleShubh · Male

Edit this script and generate it live

## Built for the depth of Indian speech

Not just speaking India's languages, but speaking them the way India does.

V4

### Voices that sound native

Listen for the Bengali delivery of “ধুর বাবা”, the hesitation in “umm”, and English words such as “Auto-ওয়ালা” inside Bengali speech.

ধুর বাবা, এই জ্যামে আর পারা যায় না!

Listen

V4

### Indian English that sounds Indian

Listen for “ra”, “machaa” and “da”, the pronunciation of Tamizhselvi, and the Bengaluru cadence of “faster only, no?”

What ra Sudeep?

Listen

V4

### Names and numbers, read in context

Listen for the PNR, train number, coach and seat, and PAN and Aadhaar read the way people say them.

हाँ जी, umm… एक second, आपकी booking details check कर रही हूँ… हाँ, मिल गई.

Listen

V4

### Amounts and dates in a payment reminder

Listen for the rupee amount, due date and cut-off time in a firm but respectful call.

नमस्ते राहुल जी, मैं Vistaar Finance से बोल रही हूँ।

Listen

## Build with Bulbul V4 Flash

A third less than Bulbul V3, on the same API.

  * API, Playground and Content Studio 
  * Output from 8 kHz to 48 kHz 
  * Enterprise pricing available 



Standard price ₹20 per 10,000 characters

[View API pricing](https://sarvam.ai/api-pricing)[Contact us](https://sarvam.ai/contact-us)

## One model. Many experiences.

The same model becomes a voice agent, a teacher, a commentator and a narrator.

  * ### A voice agent

Eleven turns. Both voices were generated from a written script.

Listen
  * ### A support agent

Hesitation, clear next steps and calm delivery.

Listen
  * ### A teacher

Bose-Einstein condensation, in Bengali and English.

Listen
  * ### Live sports

Speed and energy, as the action unfolds.

Listen
  * ### A documentary

Measured pacing and a sense of wonder.

Listen
  * ### An ad

A Hinglish sale ad with energy that moves people.

Listen



## A voice for every experience

83 voices in 224 styles, purpose-built for customer care, sales, collections, banking and storytelling.

[ Explore all voices ](https://indus.sarvam.ai/text-to-speech)

  * SophiaConversational · Indian English
  * SanchitaAssistant · Hindi
  * AparnaCustomer care · Hinglish
  * ArnabConversational · Bengali
  * KalpitE-learning · Bengali
  * IshitaE-learning · Tamil
  * AshwinSports · Indian English
  * AnandDocumentary · Hindi



## Text to speech for every use case

From voice agents to content platforms. Real text-to-speech use cases, already in production.

###  [Dubbing and localization](https://sarvam.ai/products/content-studio)

Natural voiceovers for multilingual media and public communication.

  * Public announcements
  * Educational content
  * Marketing promos and ads
  * Podcast and informational videos



###  [Voice agents](https://sarvam.ai/products/voice-agents)

Real-time, human-like speech for customer-facing and internal agents.

  * Customer support
  * Sales and lead qualification
  * Edtech tutors
  * Social and companion agents



## Made for developers. Scales for enterprises.

  * Request First audio

HTTP streaming WebSocket Single response

### Real-time at scale

Under 250 ms to first audio in production, over HTTP streaming, WebSocket or a single response.

  * Pace

Pitch

Loudness

8 kHz to 48 kHz WAV MP3 FLAC AAC

### Configurable controls

Pace, pitch and loudness, sample rates from 8 kHz to 48 kHz, and WAV, MP3, FLAC or AAC output.

  * - "model": "bulbul:v3",+ "model": "bulbul:v4-flash",

Python SDK Node.js SDK

### Plug-and-play integrations

Same request shape as Bulbul V3, so existing integrations switch in one line. SDKs for Python and Node.js.




## Now write your own

Pick a voice, a language and a sample rate. Generation runs live on bulbul:v4-flash, and the code panel shows the exact request.

Text to generateनमस्ते! यह Bulbul V4 है। कोई भी line लिखिए, किसी भी भाषा में, और Generate दबाकर तुरंत सुनिए।

`Ctrl` `Enter` to generate

92 / 2,000

Your audio appears here, with a download and the exact API call beside it.

Voice

Shubh · ConversationalShubh · BankingShubh · E-commerceShalini · ConversationalAparna · Customer careAparna · E-learning, EnglishIshita · ConversationalRoopa · CompanionSanchita · Media, EnglishAnand · DocumentaryAshok · NewsRoopa · BengaliArnab · BengaliVijay · Tamil narrationRitu · MarathiChaitra · KannadaChetan · KannadaPooja · GujaratiBhavik · GujaratiGokul · NarrationAnand · Punjabi

Language

HindiEnglishBengaliTamilTeluguKannadaMalayalamMarathiGujaratiPunjabiOdia

Sample rate

8 kHz24 kHz48 kHz

Pace1.00×

Generate with Bulbul V4

cURLPython
    
    
    curl -X POST https://api.sarvam.ai/text-to-speech \
      -H "api-subscription-key: YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "text": "नमस्ते! यह Bulbul V4 है। कोई भी line लिखिए, किसी भी भाषा में, और Generate दबाकर तुरंत सुनिए।",
        "target_language_code": "hi-IN",
        "model": "bulbul:v4-flash",
        "speaker": "ishita_enhi_companion",
        "pace": 1,
        "speech_sample_rate": 24000
      }'

## Explore speech in your language

Open a language page to hear its voices and try your own text.

  * [ हिन्दी Hindi ](https://sarvam.ai/apis/text-to-speech/hindi)
  * [ தமிழ் Tamil ](https://sarvam.ai/apis/text-to-speech/tamil)
  * [ বাংলা Bengali ](https://sarvam.ai/apis/text-to-speech/bengali)
  * [ తెలుగు Telugu ](https://sarvam.ai/apis/text-to-speech/telugu)
  * [ ಕನ್ನಡ Kannada ](https://sarvam.ai/apis/text-to-speech/kannada)
  * [ മലയാളം Malayalam ](https://sarvam.ai/apis/text-to-speech/malayalam)
  * [ मराठी Marathi ](https://sarvam.ai/apis/text-to-speech/marathi)
  * [ ગુજરાતી Gujarati ](https://sarvam.ai/apis/text-to-speech/gujarati)
  * [ ਪੰਜਾਬੀ Punjabi ](https://sarvam.ai/apis/text-to-speech/punjabi)
  * [ ଓଡ଼ିଆ Odia ](https://sarvam.ai/apis/text-to-speech/odia)



## Your questions, answered

What is Bulbul V4 Flash?

Bulbul V4 Flash is Sarvam's text-to-speech model for real-time applications. It returns first audio in under 250 ms in production and costs ₹20 per 10,000 characters.

Which languages and voices are available?

Eleven languages: Hindi, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu and Indian English. There are 83 voices in 224 styles, and code-mixed text such as Hinglish works when each language is written in its own script.

How is it different from Bulbul V3?

It is more expressive, handles Indian names, numbers and abbreviations in context, and costs ₹20 per 10,000 characters against ₹30 for Bulbul V3. Play any sample in the studio on both models to hear the difference.

Do I need to change my integration?

No. Bulbul V4 Flash uses the same request shape as Bulbul V3, so switching is a one-line change to the model. It is available over HTTP streaming, WebSocket and a single-response endpoint.

Where can I use it?

Through the Sarvam API, the Playground and Content Studio.

How much does it cost?

₹20 per 10,000 characters.

Are the conversation samples live calls?

No. They are scripted demonstrations, and both speakers' audio is generated with Bulbul V4 Flash.

##  Your next million conversations can sound more human. 

[ Sign up ](https://indus.sarvam.ai/text-to-speech) Try the playground 
