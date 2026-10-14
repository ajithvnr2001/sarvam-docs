---
url: https://sarvam.ai/blogs/bulbul-v4-flash/
title: Introducing Bulbul V4 Flash text-to-speech for India | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:23.818449+00:00
---

# Introducing Bulbul V4 Flash text-to-speech for India | Sarvam AI

> Source: https://sarvam.ai/blogs/bulbul-v4-flash/

# Introducing  
Bulbul V4 Flash

PlayPause

PlayPause

PlayPause

The launch announcement, in one voice.

0:00 / 0:00

Persona
    Main hero

aparna_en_edtech

Introducing Bulbul V4 Flash.

Voice that sounds naturally Indian. Expressive, fluid, and blazing fast.

With a much bigger voice library, there are more voices to choose from, and more ways to bring every conversation to life.

Built for real-time conversations, it delivers natural-sounding speech at the speed you need.

Bulbul V4 Flash. Our best yet.

Bulbul V4 Flash

The launch announcement, in one voice.

Persona
    Main hero

aparna_en_edtech

Introducing Bulbul V4 Flash.

Voice that sounds naturally Indian. Expressive, fluid, and blazing fast.

With a much bigger voice library, there are more voices to choose from, and more ways to bring every conversation to life.

Built for real-time conversations, it delivers natural-sounding speech at the speed you need.

Bulbul V4 Flash. Our best yet.

[Try Bulbul V4 Flash](https://indus.sarvam.ai/api-playground/text-to-speech)

HISBLCE

0:00 / 0:00

Read the blog

Today, we're introducing **Bulbul V4 Flash** , our latest text to speech model that brings more natural and expressive speech across Indian languages, with the speed and efficiency needed for real-time applications.

With V4 Flash, our research focused on capturing the richness and nuances of Indian languages, while making high-quality speech generation faster and more affordable.

We've made substantial improvements in how expressive speech is generated across Indian languages. The model is better at capturing emotion, adjusting emphasis, pacing sentences and responding to the context of what is being said. We've focused on bringing greater depth and expressiveness across the breadth of Indian languages, preserving the distinct character of each language and the subtleties that make speech sound natural to its speakers.

Alongside improvements in speech quality, we've developed a smaller, more efficient model and optimised the inference stack around it. In real-time voice applications, every delay affects the flow of a conversation. Fast, predictable responses allow conversations to flow naturally, even when thousands of calls are happening at once.

Flash delivers under 250 ms time-to-first-audio in production and costs ₹20 per 10,000 characters.

## **Frontier quality in a smaller model**

Flash is an outcome of our V4 research. We set aside the latency and cost limits of a production model to see how far speech quality could go. We trained larger language backbones, explored richer audio representations, tested different generative approaches and scaled training data to more than 400 billion audio tokens.

Quality had not plateaued. Even at that scale, more data and more capable models kept improving the model’s use of context, along with its prosody, expressiveness and robustness.

To build Flash, we looked across several experimental iterations, identified what drove the gains, and distilled it into a much smaller, more efficient model. Flash keeps the qualities listeners notice most while meeting the speed and cost requirements of production.

Bulbul V3 was priced at ₹30 per 10,000 characters. Flash costs ₹20, a third less, and it sounds better, with richer prosody, stronger contextual delivery and higher speech quality. At production volume, expressive speech no longer has to give way to cost.

Bulbul V3Bulbul V4

AparnaShubh

### Rail helpline

1:19

An agent checks a waiting list, offers another train and books it. The "एक सेकंड" pauses are where it waits on a tool call.

नमस्ते! रेल सहायता में आपका स्वागत है। बताइए, मैं आपकी क्या मदद कर सकती हूँ?

हाँ जी, मेरा एक ticket waiting में है... बस उसका status जानना था।

ज़रूर। आप अपना PNR number बता दीजिए।

हाँ, लिख लीजिए... 8 4 2 7 1 5 9 3 6 0।

एक सेकंड, मैं check कर रही हूँ... हाँ, मिल गया। आपका ticket अभी waiting list में 14 नंबर पर है, ट्रेन 1 2 9 5 2, मुंबई राजधानी, 18 October, शाम 4 बजकर 55 मिनट। Chart बनने में अभी दो दिन बाकी हैं, तो confirm होने के chances अच्छे हैं।

अच्छा... और अगर confirm नहीं हुई तो? उसी दिन कोई और ट्रेन मिल जाएगी?

मैं देख लेती हूँ... हाँ, उसी शाम 1 2 9 5 4 अगस्त क्रांति राजधानी में 3rd AC की छह seats खाली हैं, किराया 3,290 रुपये। आप कहें तो मैं अभी book कर देती हूँ। Waiting वाली ticket अपने आप cancel हो जाएगी, और उसका refund तीन-चार दिन में आपके account में आ जाएगा।

हाँ हाँ, वही कर दीजिए।

एक सेकंड... हो गया! Coach B2, berth 41, lower berth। Ticket की details आपके mobile पर SMS कर दी हैं। और कुछ मदद कर सकती हूँ?

नहीं, बस इतना ही था। Thank you!

धन्यवाद! आपकी यात्रा शुभ हो।

## **Built for the breadth and depth of Indian Languages**

Speech data across Indian languages varies widely in volume, speaker diversity and expressive range. We expanded our proprietary speech datasets nearly seven times relative to V3, increasing coverage across languages, regional accents, speakers, emotional registers and conversational styles.

Scale solved one problem and exposed another. A compact model trained on many languages tends to average them, blurring the features that make each one distinct. So we pretrained V4 from scratch with Indian language representation as a primary objective. We then trained it with a continuous, language-balanced curriculum designed to reinforce native pronunciation, speaker identity and expressive delivery throughout training.

As a result, regional voices sound native, Indian English sounds Indian, and names, numbers and everyday expressions come out the way people say them.

### Native, down to the detail

A voice sounds native when it gets the small things right. A Bengali speaker’s "ধুর বাবা". The respect in a Telugu “garu”. Their meaning comes through pauses, emphasis and intonation, and through the ease with which speakers move between languages.

V4 learns these patterns across its multilingual curriculum, where every language is reinforced throughout training rather than added at the end. A final voice-specialization phase then tunes each voice to its native accent, conversational rhythm and expressive delivery, so that a Bengali voice carries Bengali parlance in every sentence it reads.

Bengali: A frustrating commute through Kolkata

0:00

ধুর বাবা, এই জ্যামে আর পারা যায় না! Ultadanga থেকে Salt Lake আসতে, umm, কত, দেড় ঘণ্টা লাগলো, ভাবা যায়? Auto-ওয়ালা আবার বলে, 'দাদা, দশ টাকা extra লাগবে, ঘুরে যেতে হবে।' আমি বললাম, যা খুশি কর ভাই, শুধু পৌঁছে দে, please। 

### **Indian English, as it’s spoken**

For many conversations in India, English is the working language. It should sound like the English India speaks.

Indian English has its own pronunciation, stress and intonation, shaped by the regional accents that run through it. For V4, we kept Indian-English speech in balance through pretraining and every stage after it.

Indian English: A very Bengaluru conversation

0:00

What ra Sudeep? So ... Tamizhselvi said she'll reach in ten minutes. That was, like, forty-five minutes ago, machaa. Apparently she's still near Silk Board. Full psych scenes, da. I mean... should we just go meet her there? It'll be faster only, no? 

### Context-aware by design

Much of what voice agents say is names, amounts, dates and reference numbers. The correct spoken form depends on context. ISRO is said as a word, “is-row”, while EMI is spoken letter by letter. PAN is pronounced as a word, and Aadhaar has its own familiar pronunciation.

To address this, we built a real-time contextual text normalization layer. It interprets text in context, identifies what each element represents, and determines how it should be spoken. Expressive alignment during training then ties that accuracy to the model’s delivery, so the details come through correctly without interrupting the flow of the conversation.

Listen for the PNR, train number, coach and seat, each read the way it should be, alongside PAN, Aadhaar, dates and times, all within a fluid Hindi-English conversation. When a customer’s name, a payment amount or a booking reference is spoken correctly, the conversation keeps moving. That is what language depth means in Bulbul V4 Flash. Every detail sounds right to the person on the other end of the call.

Hindi: Railway booking assistant

0:00

हाँ जी, umm… एक second, आपकी booking details check कर रही हूँ… हाँ, मिल गई. आपका PNR 4827319560 है, train number 12951 Mumbai Rajdhani, coach B4, seat 27 lower berth. Departure 18 October को 5:10 PM है, platform 3 से. और हाँ, ticket पर ID proof के लिए PAN या Aadhaar में से कोई एक valid रहेगा — बस OTP या CVV किसी को share मत कीजिएगा। 

_Listen for context-aware pronunciation of the PNR, train number, coach and seat, alongside natural handling of PAN, Aadhaar, dates and time, all within a fluid Hindi-English conversation._

For voice agents, this distinction matters. An incorrectly spoken customer name, payment amount or booking reference isn't just unnatural; it can make an otherwise helpful interaction confusing.

V4 brings together native pronunciation, contextual understanding and expressive speech, so that real-world information can be delivered both accurately and naturally.

**That's language depth in Bulbul V4 Flash: not just speaking India's languages, but speaking them the way India does.**

### **Low latency at scale**

Bulbul V4 Flash delivers under 250 ms time-to-first-audio in production.

Flash runs on a streaming-first inference stack. Receptive-field-aware streaming skips any work that cannot affect the next stretch of audio. Real-time pacing keeps compute on what active conversations need now, instead of generating far ahead of them.

We also tuned the serving path for many simultaneous conversations. We cut unnecessary synchronization and copying, grouped compatible streaming work, and balanced requests by live load. Every optimization was gated on output correctness, so speed never came at the cost of speech quality.

Together with V4’s architectural improvements, these changes make Flash upto 40% faster than V3 under comparable load, with substantially more headroom for concurrent conversations.

## One model. Many experiences.

The most exciting part of V4 Flash is seeing the same underlying model become completely different products.

Collections(Hinglish)

AparnaShubh

### EMI overdue reminder

0:32

Amount, due date, a cut-off time, a payment link and a way out if the customer is struggling.

नमस्ते राहुल जी, मैं Vistaar Finance से बोल रही हूँ। बस एक छोटा-सा reminder देना था, आपके personal loan की इस महीने की EMI, 12,450 रुपये, 5 October को due थी, और वो अभी तक pending दिख रही है। अगर आज शाम 6 बजे तक payment हो जाए, तो कोई late fee नहीं लगेगी, और आपके credit score पर भी असर नहीं पड़ेगा। मैं आपको अभी WhatsApp पर payment link भेज देती हूँ, UPI, debit card या net banking, जो भी आपको आसान लगे। और अगर इस महीने थोड़ी दिक़्क़त चल रही है, तो बेझिझक बताइए, हम मिलकर कोई रास्ता निकाल लेंगे।

And this is only the beginning.

V4 Flash launches with **83 voices across 11 languages and 224 voice-and-style combinations** , spanning customer care, sales, collections, banking, ecommerce, education, conversational experiences, narration and more.

A voice for every experience.

## And we are not done

Flash answers one part of the V4 question:

How much frontier speech capability can we bring into a model that is fast, reliable and economical enough to serve everywhere?

We are pushing the other side too.

There is a growing model in the V4 family that can laugh.

Pause.

Sigh.

Get excited.

Sound nervous.

Emphasize exactly the part of a sentence that matters.

And express the same words in ways that feel completely different.

We call it

Bulbul V4 Pro.

Here's a glimpse of what's coming up next.

Bulbul V4 Pro

0:00

अरे वाह! आप यहाँ तक पहुँच गए? LAUGH Impressive. इतना patience दिखाया है, reward तो बनता है ना?लेकिन जाने से पहले... एक छोटा-सा सवाल.happy अगर आवाज़ हँस सकती है... sad तो क्या वो उदास भी हो सकती है? fear घबरा सकती है? angry अचानक गुस्सा कर सकती है? whisper या बिना आवाज़ ऊँची किए... सिर्फ़ एक शब्द पर ज़ोर देकर पूरी बात बदल सकती है? SIGH हाँ.शायद आवाज़ के बारे में सबसे दिलचस्प बात यही है…हम सिर्फ़ ये नहीं सुनते कि कोई क्या कह रहा है.हम ये भी सुनते हैं कि…वो emphasis कैसे कह रहा है.कभी आवाज़ में खुशी होती है…कभी थोड़ा-सा डर.कभी नाराज़गी.और कभी…whisper बस एक शब्द ही काफ़ी होता है. क्योंकि असली बात केवल शब्दों में नहीं होती.तो, ये थी बुलबुल V4 Pro की एक झलक।

## Try Bulbul V4 Flash

Bulbul V4 Flash is available today through the **Sarvam API, Playground and Content Studio**.

  * **< 250 ms** time-to-first-audio
  * **₹20** per 10,000 characters
  * **11** languages
  * **83** voices
  * **224** voice and style combinations



Existing Bulbul users can move to V4 Flash using the familiar Bulbul API.

Research

Share

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
