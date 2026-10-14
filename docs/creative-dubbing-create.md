---
url: https://docs.sarvam.ai/creative-dubbing-create/
title: Creating a Dub | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:58.482273+00:00
---

# Creating a Dub | Sarvam API Docs

> Source: https://docs.sarvam.ai/creative-dubbing-create/

Skip to navigation

On this page

  * Step 1: Upload Your Source File
  * Step 2: Add Dubbing Details
  * Track Progress



Scroll to top

[Content Studio](https://docs.sarvam.ai/creative-dubbing)[Dubbing (Beta)](https://docs.sarvam.ai/creative-dubbing)

# Creating a Dub

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/creative-dubbing-create.md "View this page as plain text")|More actions

This page is for Content Studio.

Create a new dub in two steps - upload your source file, then add your dubbing details - and track it through processing. For an overview of what Dubbing does and who it’s for, see the [Dubbing overview](https://docs.sarvam.ai/creative-dubbing).

## Step 1: Upload Your Source File

![Dubbing landing screen. Header reads Dubbing, with a green pill showing remaining free time \(e.g. 54min 44sec left\), a Feedback button, and a black plus New dub button. Below, a GET STARTED label leads into the headline Dub any video into 12 Indian languages, with the subtitle Upload a video, pick target languages, and keep your speaker's voice. Below that, four gradient category cards, each with an icon, a title, three bullet points, and its own call-to-action button: Dub educational content \(lotus icon\) with button Dub a lecture; Dub drama and fiction \(globe icon\) with button Dub a scene; Dub spiritual content \(shield icon\) with button Dub a discourse; Dub Reels and Shorts \(play icon\) with button Dub a reel.](https://docs.sarvam.ai/_fern-img/c47b0501485a5cfb8fdd4fff92087ca9e0945640149f7c1d46523f9e581927a0.webp)

The Dubbing landing page, with a category card and matching call-to-action for each common use case.

[1](https://docs.sarvam.ai/creative-dubbing-create#start-a-new-dub)

### Start a New Dub

Click **\+ New dub** in the top-right corner, or click one of the category card buttons on the landing page (**Dub a lecture** , **Dub a scene** , **Dub a discourse** , **Dub a reel**) to open the “Create a dub” modal.

![Create a dub modal, Step 1 of 2, titled Add your video, shown over a blurred background list of past dub projects. A bordered dropzone reads Drag and Drop or click to upload, with the caption Video \(MP4, MOV\) or Audio \(MP3, WAV\) and an Upload button on the right. Below the dropzone, a text link reads or record a video. The modal footer has Cancel and Next buttons.](https://docs.sarvam.ai/_fern-img/c27e5151d9af62d5f09fec4b81429cdf17baff5b267e4745c48608c2d094a4bc.webp)

Create a dub, Step 1 of 2: a drag-and-drop dropzone for your video or audio file, with a direct-record option alongside it.

  * The dropzone accepts **video (MP4, MOV) or audio (MP3, WAV)** \- or click **or record a video** to capture footage directly instead of uploading a file.



[2](https://docs.sarvam.ai/creative-dubbing-create#provide-your-source-file)

### Provide Your Source File

Upload a video or audio file, or attach an accessible social URL.

  * Uploads are capped at **2 GB per file**.
  * A URL link skips the local download-then-upload round trip for content you’ve already published (e.g. a YouTube or social link).
  * The modal displays your uploaded file’s name, size, and duration once attached (e.g. “165.2 MB · 5:16”) before you move to the next step.



## Step 2: Add Dubbing Details

![Create a dub modal, Step 2 of 2, titled Add dubbing details, with an attached file Demo Video.mp4 at 132.6 MB and 13:30 duration. An editable Project name text field is pre-filled from the source filename. Below that, a two-column row holds Source language \(a dropdown with a colored icon, set to Hindi\) and Number of speakers \(a dropdown, set to 1 speaker\). Below that, Target languages is shown as removable tag chips \(e.g. Gujarati, Malayalam, each with an x to remove\) with a dropdown to add more. A Voice dropdown is set to Clone speaker voice. A Translation style dropdown is set to Auto. At the bottom, a credit summary reads 1,024 divided by 1,00,090.25 credits, with the note 1 minute of dubbed output equals 80 credits. The modal footer has Back and Create dub buttons.](https://docs.sarvam.ai/_fern-img/58546084035ed99e7529fb352a5774e09527a03863596ca783ee2df40b3882b6.webp)

The full dubbing setup form - project name, source language, speaker count, target languages, voice strategy, and translation style, all in one step.

[1](https://docs.sarvam.ai/creative-dubbing-create#name-your-project)

### Name Your Project

The **Project name** field is pre-filled from your source filename - edit it to something you’ll recognize later, especially if you’re running several dubs at once.

[2](https://docs.sarvam.ai/creative-dubbing-create#set-the-source-language)

### Set the Source Language

Search or scroll the **Source language** dropdown and select the language actually spoken in your file.

  * Each language shows a colored icon alongside its name, making the list easy to scan visually as well as by search.
  * This tells the model which phonemes and speech patterns to expect, which affects transcription and speaker-separation accuracy before translation even starts.



[3](https://docs.sarvam.ai/creative-dubbing-create#select-the-number-of-speakers)

### Select the Number of Speakers

Choose a count from the **Number of speakers** dropdown (1, 4, 5, 6, 7, 8, and more on scroll).

  * Round upward for multi-speaker conversations - undercounting is worse than overcounting.
  * Merging two distinct speakers into one slot blends their voices in the output, which is much harder to fix in the editor than simply merging an unused extra slot.



[4](https://docs.sarvam.ai/creative-dubbing-create#select-your-target-languages)

### Select Your Target Languages

Add as many languages as you need to the **Target languages** field. Each one appears as a removable tag (with an x), and the dropdown stays open to add more.

  * Real-world usage skews heavily toward Hindi and Telugu, with the full set covering most major Indian languages plus English.
  * Adding multiple targets in one pass produces several localized versions from a single upload - no need to re-process the source per language.



[5](https://docs.sarvam.ai/creative-dubbing-create#match-speaker-strategy-to-your-use-case)

### Match Speaker Strategy to Your Use Case

Choose how the dubbed voice should be generated from the **Voice** dropdown:

  * **Clone speaker voice** \- zero-shot vocal trait tracking. Use this when audience recognition of the original speaker matters (a host, a founder, a recurring instructor). This is the default.
  * **Use Sarvam voices** \- native artist personas. Faster to review since the persona is already familiar and consistent across projects.



[6](https://docs.sarvam.ai/creative-dubbing-create#set-the-translation-register)

### Set the Translation Register

Choose a style from the dropdown, or leave it on **Auto** :

  * **Auto** \- automatically picks the best style for the content. Default.
  * **Formal** \- polished, professional language for official content.
  * **Urban colloquial** \- modern, trend-aware localization with urban phrasing and idioms.
  * **Standard colloquial** \- everyday spoken language that feels natural without being overly trendy.
  * **Traditional colloquial** \- conventional spoken language that preserves local linguistic and cultural nuance.
  * Style changes register and word choice, not just vocabulary - a serious lecture translated in `Urban colloquial` style will read as too casual, even if every fact is correct.



[7](https://docs.sarvam.ai/creative-dubbing-create#submit-for-processing)

### Submit for Processing

Click **Create dub** to dispatch the file to the localization pipeline.

  * If the banner reads “The video is fully free,” this dub won’t draw against your free minutes or credits.
  * Setup fields lock once submitted - double-check source language and speaker count first, since fixing them afterward means starting a new dub rather than editing this one.



## Track Progress

![Processing video dialog showing a 50 percent circular progress indicator, a linear progress bar, and a Status History timeline listing pipeline stages: Translating \(Running, started 23 seconds ago\), Transcribing \(Done, with start and end times and duration\), and Processing video \(Done, with start and end times and duration\). A Go to Projects button sits at the bottom.](https://docs.sarvam.ai/_fern-img/c2fa5f1c8360d262c10bcd3c7e96db96275174deaa23ae7ea3b646d34c558819.webp)

A live progress card shows each pipeline stage - processing, transcribing, translating - with timestamps and durations as it moves through them.

After you click **Create dub** , a processing dialog opens automatically so you can track progress at every stage instead of waiting on a blank screen.

  * The **Status History** timeline shows each pipeline stage in order (processing video, transcribing, translating, and so on) as it runs, with a `Running` or `Done` tag and how long each stage took.
  * You don’t have to wait on this screen. Click **Go to Projects** to navigate away - the dub keeps processing in the background, and the project will show as “Review Ready” once it’s done.



Once your dub reaches “Review Ready” status, head to [Editing a Dub](https://docs.sarvam.ai/creative-dubbing-edit) to refine it.

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/creative-dubbing)[Editing a DubNext](https://docs.sarvam.ai/creative-dubbing-edit)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Overview](https://docs.sarvam.ai/creative/studio-overview)
  * Content Studio

    * [Dubbing (Beta)](https://docs.sarvam.ai/creative-dubbing)
      * [Creating a Dub](https://docs.sarvam.ai/creative-dubbing-create)
      * [Editing a Dub](https://docs.sarvam.ai/creative-dubbing-edit)
      * [Dubbing Best Practices](https://docs.sarvam.ai/creative-dubbing-best-practices)

    * [Text to Speech](https://docs.sarvam.ai/creative-text-to-speech)

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


