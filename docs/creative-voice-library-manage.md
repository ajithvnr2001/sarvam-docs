---
url: https://docs.sarvam.ai/creative-voice-library-manage/
title: Managing Your Voice Library | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:00.606183+00:00
---

# Managing Your Voice Library | Sarvam API Docs

> Source: https://docs.sarvam.ai/creative-voice-library-manage/

Skip to navigation

On this page

  * Naming and Organizing Cloned Voices
  * Voice ID for the API
  * Keeping Projects Consistent



Scroll to top

[Content Studio](https://docs.sarvam.ai/creative-dubbing)[Voice Library](https://docs.sarvam.ai/creative-voice-library)

# Managing Your Voice Library

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/creative-voice-library-manage.md "View this page as plain text")|More actions

This page is for Content Studio.

As your roster of cloned voices grows, a little organization up front keeps the library usable instead of cluttered.

## Naming and Organizing Cloned Voices

  * Give cloned voices specific, descriptive names at creation time - “Course Narrator v2” is far easier to find later than a default label once your library has a dozen entries.
  * Rename or delete a cloned voice directly from the **My voices** tab.
  * Use the heart icon on any voice row to favorite it, so your most-used personas surface quickly without re-filtering the table every time.
  * If you maintain multiple versions of the same clone (e.g. after a re-recording), version the name explicitly (`v1`, `v2`) rather than overwriting - this keeps older projects that already selected `v1` unaffected.



## Voice ID for the API

Each cloned voice has a **Voice ID** (`svc-…`) on its card under **My voices** (also on Instant Voice Cloning home). Use the copy control, then pass that value as `voice_id` on `POST /voices/clone`.

`GET /voices` and `GET /voices/{voice_id}` return the same IDs for the same org — list/get response field `id` is the value you send as `voice_id` when synthesizing. Voices created in Studio and via `POST /voices/create` share this library. See [Using a Cloned Voice](https://docs.sarvam.ai/creative-cloning-use#use-the-same-voice-in-the-api) and [Manage saved voices](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview#manage-saved-voices).

## Keeping Projects Consistent

A voice you select in the Voice Library carries over into Text to Speech and Dubbing automatically. Changing it here changes it everywhere it’s referenced.

  * Settle on a persona per project before generating multiple assets - retroactively swapping a voice mid-project means re-generating everything that used the old one.
  * Periodically review unused cloned voices and remove ones you no longer need, especially if they were created for a one-off project.



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/creative-voice-library-browse)[Instant Voice CloningNext](https://docs.sarvam.ai/creative-voice-cloning)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Overview](https://docs.sarvam.ai/creative/studio-overview)
  * Content Studio

    * [Dubbing (Beta)](https://docs.sarvam.ai/creative-dubbing)

    * [Text to Speech](https://docs.sarvam.ai/creative-text-to-speech)

    * [Voice Library](https://docs.sarvam.ai/creative-voice-library)
      * [Browsing and Selecting Voices](https://docs.sarvam.ai/creative-voice-library-browse)
      * [Managing Your Voice Library](https://docs.sarvam.ai/creative-voice-library-manage)

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


