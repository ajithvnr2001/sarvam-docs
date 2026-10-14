---
url: https://docs.sarvam.ai/creative-stt-transcribe/
title: Transcribing a File | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:59.342928+00:00
---

# Transcribing a File | Sarvam API Docs

> Source: https://docs.sarvam.ai/creative-stt-transcribe/

Skip to navigation

On this page

  * Upload and Transcribe
  * Reviewing and Exporting



Scroll to top

[Content Studio](https://docs.sarvam.ai/creative-dubbing)[Speech to Text](https://docs.sarvam.ai/creative-speech-to-text)

# Transcribing a File

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/creative-stt-transcribe.md "View this page as plain text")|More actions

This page is for Content Studio.

Upload or record audio and get back a speaker-labeled transcript. For an overview of Speech to Text, supported formats, and limits, see the [Speech to Text overview](https://docs.sarvam.ai/creative-speech-to-text).

## Upload and Transcribe

![Speech to Text screen. Header has Feedback and History buttons. The main panel is a dashed-border drop zone with a microphone icon reading Drop audio here, or browse files, with the caption listing supported formats and a 500 MB size limit. Below it, a second option reads or record audio with its own microphone icon. Below that, Try an example offers three colored example chips: Gujarati finance news, Marathi cricket commentary, and Tamil healthcare conversation.](https://docs.sarvam.ai/_fern-img/77448ece879c97deccf65102a90697facca80fef39b1cc712a233106e6d76c29.webp)

Upload, record, or try a real example clip - three ways to get audio into Speech to Text without friction.

[1](https://docs.sarvam.ai/creative-stt-transcribe#provide-your-audio)

### Provide Your Audio

Drop a file, click **browse files** , or click **or record audio** to capture audio directly in the browser.

  * Video files work directly - you don’t need to extract the audio track yourself first.
  * No file of your own handy? Click one of the **Try an example** chips to see a full transcription on a real sample clip.



[2](https://docs.sarvam.ai/creative-stt-transcribe#set-the-spoken-language-and-speaker-count)

### Set the Spoken Language and Speaker Count

Once you’ve provided a file, its name and size are confirmed (e.g. “Demo Video.mp4 · 35.0 MB”), and two dropdowns plus a toggle appear.

![Speech to Text screen with a file attached, showing Demo Video.mp4 at 35.0 MB with a remove button. Below it, a Language dropdown set to Auto Detect and a Mode dropdown set to Transcribe, alongside a Diarization toggle labeled Detect and label speakers. A black Transcribe button sits below, with an estimated cost of approximately 7.00 credits and an account balance reading 1,00,090 of 1,00,100 remaining.](https://docs.sarvam.ai/_fern-img/aab8dc526c6ec1ace4a6b7a62f21d5f9eb19d83888f5d6d4f8c50bc114454ade.webp)

Post-upload configuration: Language, Mode, and a Diarization toggle, with a live credit-cost estimate and account balance.

  * **Language** \- leave on **Auto Detect** , or pick the spoken language explicitly. Getting this right matters more for regional Indian languages and dialects than it might seem - an incorrect setting doesn’t just mistranslate a few words, it can distort the model’s expectations for the entire recording’s phonetics.
  * **Mode** \- defaults to **Transcribe**.
  * **Diarization** \- toggle this on to detect and label individual speakers in the transcript. For a roundtable or panel recording, accurate diarization is often the single biggest factor in whether the transcript correctly separates who said what.
  * The estimated credit cost (e.g. “~7.00 credits”) and your remaining account balance are both shown live before you commit.



[3](https://docs.sarvam.ai/creative-stt-transcribe#transcribe)

### Transcribe

Start transcription and wait for processing to complete.

## Reviewing and Exporting

  * Once processing completes, the transcript opens in a slide-over **Transcript** panel.
  * A playback bar at the bottom shows the source filename, a waveform, and elapsed/total duration.
  * Icons beside the playback bar let you copy, download, or share the transcript.



Need this as a live API integration instead of a one-off upload? The same diarization pipeline is available via the Speech-to-Text API.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/creative-speech-to-text)[Speech to Text Best PracticesNext](https://docs.sarvam.ai/creative-stt-best-practices)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Overview](https://docs.sarvam.ai/creative/studio-overview)
  * Content Studio

    * [Dubbing (Beta)](https://docs.sarvam.ai/creative-dubbing)

    * [Text to Speech](https://docs.sarvam.ai/creative-text-to-speech)

    * [Voice Library](https://docs.sarvam.ai/creative-voice-library)

    * [Instant Voice CloningBeta](https://docs.sarvam.ai/creative-voice-cloning)

    * [Speech to Text](https://docs.sarvam.ai/creative-speech-to-text)
      * [Transcribing a File](https://docs.sarvam.ai/creative-stt-transcribe)
      * [Speech to Text Best Practices](https://docs.sarvam.ai/creative-stt-best-practices)

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


