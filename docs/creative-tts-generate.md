---
url: https://docs.sarvam.ai/creative-tts-generate/
title: Generating Speech | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:59.910708+00:00
---

# Generating Speech | Sarvam API Docs

> Source: https://docs.sarvam.ai/creative-tts-generate/

Skip to navigation

On this page

  * Interface Controls
  * Generate a Voice Clip



Scroll to top

[Content Studio](https://docs.sarvam.ai/creative-dubbing)[Text to Speech](https://docs.sarvam.ai/creative-text-to-speech)

# Generating Speech

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/creative-tts-generate.md "View this page as plain text")|More actions

This page is for Content Studio.

Generate a voice clip from written text, tuned for Indian accents and dialects. For an overview of what Text to Speech does and who it’s for, see the [Text to Speech overview](https://docs.sarvam.ai/creative-text-to-speech).

## Interface Controls

![Content Studio Text to Speech screen. Header row has the page title Text to Speech plus Feedback and History buttons in the top right. The main text input container comes pre-filled with sample text on first visit that you can overwrite. Along the bottom edge of the input box is a language dropdown and a live count reading 327 characters, approximately 0.98 credits. Below the input box, a Speed control shows a slider with a snail icon at the slow end and the current multiplier displayed on the right. The right side of the screen holds two tabs, Sarvam voices and Cloned voices, the Cloned voices tab, when empty, shows No cloned voices yet, the line Clone your own voice in 30 seconds and use it across Studio, and a black Clone a voice button.](https://docs.sarvam.ai/_fern-img/5245c95635c61c446075d4b093d096fd6594ca5be1fbadf89bba8ac5c67f0a32.webp)

Text input, Speed slider, and the Sarvam voices / Cloned voices tabs - everything needed to generate a clip lives on one screen.

  * **Text input box** \- central field, pre-filled with sample text you can try or overwrite; character count updates live to estimate credit cost.
  * **Feedback** and **History** \- header buttons for sending feedback and reviewing your past generations.
  * **Language dropdown** \- along the bottom edge of the input box.
  * **Speed** \- a slider showing the exact delivery-speed multiplier (e.g. “1.00x”).
  * **Sarvam voices / Cloned voices tabs** \- toggle between curated voices and your own clones. The Sarvam voices tab also has an **“All genres” filter** and a **Favorites** toggle, on top of each voice’s own favorite heart icon.



## Generate a Voice Clip

[1](https://docs.sarvam.ai/creative-tts-generate#enter-your-text)

### Enter Your Text

Paste or type your text into the text input box, replacing the sample text.

  * Punctuation matters more than you’d expect - commas and periods are what the model uses to place natural pauses. Under-punctuated text tends to sound rushed.



The gap between a rushed clip and a natural one is usually just punctuation:

  * **Weak:** _“welcome to sarvam ai we build voice technology for indian languages”_
  * **Better:** _“Welcome to Sarvam AI. We build voice technology for Indian languages.”_
  * **Best:** _“Welcome to Sarvam AI - we build voice technology for Indian languages, with support across more than 10 scripts.”_



The dash and comma in the last version give the model natural places to breathe, instead of reading the whole line in one flat rush.

[2](https://docs.sarvam.ai/creative-tts-generate#set-the-output-language)

### Set the Output Language

Choose the synthesis language from the dropdown along the bottom edge of the input box.

![Language dropdown open beneath the Text to Speech input box, showing a scrollable list of languages \(English checked, then Hindi, Bengali, Gujarati, Kannada, and more below\), with the live character-and-credit count visible underneath.](https://docs.sarvam.ai/_fern-img/9c6265d407e79f54bae61bb8d42d657b697356d623d1d09626ec94a6df3ee845.webp)

The language dropdown, expanded - scrollable list of Indian languages plus English, with the active selection checked.

  * This should match the language your text is actually written in - mismatches are one of the most common causes of mispronounced words.



[3](https://docs.sarvam.ai/creative-tts-generate#tune-the-delivery-speed)

### Tune the Delivery Speed

Drag the **Speed** slider to set the multiplier (e.g. “1.00x” is normal pace).

![Speed control showing a slider with a snail icon at the slow end, set to the default 1.00x multiplier.](https://docs.sarvam.ai/_fern-img/17e409b948ec09abc4d528ecf26d48d198af37a91e58cfacf7cee4039e47af30.webp)

  * Values below 1.00x read as more deliberate and authoritative - useful for narration or instructional content.
  * Values above 1.00x read as more energetic and casual - useful for ads or social content.



[4](https://docs.sarvam.ai/creative-tts-generate#pick-a-voice-persona)

### Pick a Voice Persona

Select a persona from the **Sarvam voices** or **Cloned voices** tab.

![Sarvam voices tab, active, showing the All genres filter, a Favorites toggle, and a list of voice rows \(e.g. Shubh, Ritu, Amit, Sumit, Pooja, Manan\) each with a gender tag, a one-line personality description, and a favorite heart icon.](https://docs.sarvam.ai/_fern-img/4c2675473730047c502ee56b40f1c042ff0b936d96917a2e9a22812fad9e40e8.webp)

![Cloned voices tab, active and empty, reading No cloned voices yet, Clone your own voice in 30 seconds and use it across Studio, with a black Clone a voice button.](https://docs.sarvam.ai/_fern-img/9462f58f83534e2ae69297094bcd18c6cf6c6e1a80a4354ef5892064a0ac00e1.webp)

  * No cloned voices yet? Click **Clone a voice** right there in the Cloned voices tab - it opens the cloning flow directly, and the new voice becomes available here once processing finishes.
  * Reusing the same persona across a project’s assets is what makes the output feel like one consistent “voice” rather than a series of one-off generations.



Need this in your own product instead of the dashboard? The same synthesis pipeline is available via the TTS API - see the API Reference.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/creative-text-to-speech)[Text to Speech Best PracticesNext](https://docs.sarvam.ai/creative-tts-best-practices)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Overview](https://docs.sarvam.ai/creative/studio-overview)
  * Content Studio

    * [Dubbing (Beta)](https://docs.sarvam.ai/creative-dubbing)

    * [Text to Speech](https://docs.sarvam.ai/creative-text-to-speech)
      * [Generating Speech](https://docs.sarvam.ai/creative-tts-generate)
      * [Text to Speech Best Practices](https://docs.sarvam.ai/creative-tts-best-practices)

    * [Voice Library](https://docs.sarvam.ai/creative-voice-library)

    * [Instant Voice CloningBeta](https://docs.sarvam.ai/creative-voice-cloning)

    * [Speech to Text](https://docs.sarvam.ai/creative-speech-to-text)

  * Resources

    * [Frequently Asked Questions](https://docs.sarvam.ai/creative/resources/faq)
    * [Data retention](https://docs.sarvam.ai/api/platform/data-retention "Data retention")



  * [Overview](https://docs.sarvam.ai/creative/studio-overview)
  * [Dubbing (Beta)](https://docs.sarvam.ai/creative-dubbing)
  * [Creating a Dub](https://docs.sarvam.ai/creative-dubbing-create)
  * [Editing a Dub](https://docs.sarvam.ai/creative-dubbing-edit)
  * [Dubbing Best Practices](https://docs.sarvam.ai/creative-dubbing-best-practices)
  * [Text to Speech](https://docs.sarvam.ai/creative-text-to-speech)
  * [Generating Speech](https://docs.sarvam.ai/creative-tts-generate)
  * [Text to Speech Best Practices](https://docs.sarvam.ai/creative-tts-best-practices)
  * [Voice Library](https://docs.sarvam.ai/creative-voice-library)
  * [Browsing and Selecting Voices](https://docs.sarvam.ai/creative-voice-library-browse)
  * [Managing Your Voice Library](https://docs.sarvam.ai/creative-voice-library-manage)
  * [Instant Voice Cloning](https://docs.sarvam.ai/creative-voice-cloning)
  * [Creating a Clone](https://docs.sarvam.ai/creative-cloning-create)
  * [Using a Cloned Voice](https://docs.sarvam.ai/creative-cloning-use)
  * [Cloning Best Practices](https://docs.sarvam.ai/creative-cloning-best-practices)
  * [Speech to Text](https://docs.sarvam.ai/creative-speech-to-text)
  * [Transcribing a File](https://docs.sarvam.ai/creative-stt-transcribe)
  * [Speech to Text Best Practices](https://docs.sarvam.ai/creative-stt-best-practices)
  * [Frequently Asked Questions](https://docs.sarvam.ai/creative/resources/faq)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


