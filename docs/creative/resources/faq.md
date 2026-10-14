---
url: https://docs.sarvam.ai/creative/resources/faq/
title: Frequently Asked Questions | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:01.307401+00:00
---

# Frequently Asked Questions | Sarvam API Docs

> Source: https://docs.sarvam.ai/creative/resources/faq/

Skip to navigation

On this page

  * Dubbing
  * Text to Speech
  * Voice Library & Instant Voice Cloning
  * Speech to Text
  * Licensing & commercial use
  * Data & Security
  * Need More Help?



Scroll to top

[Resources](https://docs.sarvam.ai/creative/resources/faq)

# Frequently Asked Questions

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/creative/resources/faq.md "View this page as plain text")|More actions

This page is for Content Studio.

Short answers to the most common questions about Content Studio. Questions already covered in the how-to pages aren’t repeated here - follow the links inline for the full walkthrough.

## Dubbing

###### Is there a file size limit for Dubbing?

Yes - uploads are capped at **2 GB per file**. Separately, dubs are also metered by **video duration** : new accounts get **60 minutes of free dubbing time** , shown as a live countdown badge in the header, and some videos are marked **“fully free”** and don’t draw against your allowance or credits at all.

Very large files may still hit browser upload timeouts even under 2 GB. For those, or for anything programmatic, use the Dubbing API instead of the dashboard.

###### What's the difference between Clone speaker voice and Use Sarvam voices?

  * **Clone speaker voice** \- zero-shot vocal trait tracking from the original speaker. Use this when audience recognition of that specific speaker matters (a host, a founder, a recurring instructor).
  * **Use Sarvam voices** \- native artist personas. Faster to review since the persona is already familiar and consistent across projects, but doesn’t carry the original speaker’s identity.



See [Creating a Dub](https://docs.sarvam.ai/creative-dubbing-create) for where this is set.

###### Which translation style should I use?

Five options, chosen per dub: **Auto** (default, picks automatically), **Formal** (official/institutional content), **Urban colloquial** (trend-aware, casual), **Standard colloquial** (everyday spoken language), and **Traditional colloquial** (preserves local linguistic and cultural nuance).

Style changes register and word choice, not just vocabulary - a serious lecture translated in `Urban colloquial` style will read as too casual, even if every fact is correct. Leave it on `Auto` unless you have a specific reason not to.

###### How does Sarvam handle multi-speaker tracking?

Diarization isolates overlapping audio waveforms. For clean results, manually specify the exact speaker count during project setup - if you’re unsure, round your estimate upward rather than down. Undercounting merges two real speakers into one voice, which is much harder to fix afterward than simply merging an unused extra slot.

###### Can I fix one line without re-rendering the whole file?

Yes. The Dubbing editor supports per-block correction: edit the text in that specific block, then click **Regenerate audio** \- only that block re-renders, not the full timeline. See [Editing a Dub](https://docs.sarvam.ai/creative-dubbing-edit).

###### Can I control how much of the original audio comes through in the dub?

Yes. The Dubbing editor has three independent volume sliders - **Dubbed** , **Original** , and **Background** \- so you can blend the new voice track against the source instead of fully replacing it. Useful when you want ambient sound or background music from the source to carry through.

###### What happens while my dub is processing?

A live progress card opens automatically after you click **Create dub** , showing each pipeline stage (processing, transcribing, translating) with timestamps and durations. You don’t have to wait on this screen - click **Go to Projects** to navigate away; the dub keeps processing in the background and shows as “Review Ready” once it’s done.

###### I dubbed into multiple languages at once - how do I manage them?

Use the language pill in the editor header to switch between target languages. Each language keeps its own independent transcript and edits, and you can export each one separately once it’s ready - no need to wait for every language to finish review before exporting any of them.

###### A name or term came out mistranslated - how do I fix it without redoing the whole dub?

A few things to try, in order:

  1. **If the same term is wrong in multiple places,** use **Find & Replace** in the editor instead of fixing each occurrence by hand.
  2. **If it’s a one-off line,** edit the translated text directly in that block, then click **Regenerate audio** \- only that block re-renders.
  3. **If the whole dub reads as too casual or too formal,** the issue is likely the translation style, not a specific word. Revisit the style dropdown on a fresh dub - see [Which translation style should I use?](https://docs.sarvam.ai/creative/resources/faq#dubbing) above.



###### The dubbed voice doesn't really sound like the original speaker - what went wrong?

Check the speaker strategy first: this only happens with **Clone speaker voice** , not **Use Sarvam voices** (which intentionally uses a native artist persona instead). If Clone speaker voice was selected and it still doesn’t land, the likely cause is source audio quality for that speaker’s segments - background noise or overlapping speech in the original carries through into the clone.

## Text to Speech

###### How is Text to Speech cost calculated?

Credit cost is based on character count, estimated live as you type - for example, the interface shows “327 characters · ~0.98 credits” for a sample paragraph.

###### Can I use a cloned voice in Text to Speech?

Yes. The **Cloned voices** tab sits right next to **Sarvam voices** in the persona picker. If you don’t have a clone yet, that tab shows a **Clone a voice** button that takes you straight into the cloning flow without leaving Text to Speech. See [Generating Speech](https://docs.sarvam.ai/creative-tts-generate).

###### What does the Speed slider actually change?

It’s a delivery-pace multiplier (shown as e.g. “1.00x”), and it changes more than playback speed - it changes perceived tone. Values below 1.00x read as more deliberate and authoritative (good for narration); values above 1.00x read as more energetic and casual (good for ads and social content).

###### A word came out mispronounced - what should I check?

In order:

  1. **Language mismatch is the most common cause.** Confirm the output language dropdown matches the language your text is actually written in.
  2. **Check punctuation around the word.** Missing commas or periods can merge it awkwardly with neighboring words.
  3. **Spell out ambiguous numbers or abbreviations** if you notice mispronunciation - some readings have more than one valid pronunciation.
  4. **Try a different voice.** Personas can differ slightly in how they handle uncommon names or loanwords.



## Voice Library & Instant Voice Cloning

###### What's the difference between Sarvam voices and cloned voices?

Sarvam voices are curated, ready-to-use personas. Cloned voices are ones you’ve created yourself via Instant Voice Cloning, and require your explicit consent that you hold rights to the voice being cloned.

###### What's the difference between My voices and Explore voices?

**My voices** is your personal set - favorited and cloned voices. **Explore voices** is the full browsable catalog. Both live under the same filters (use case, gender) and search box in the Voice Library. See [Browsing and Selecting Voices](https://docs.sarvam.ai/creative-voice-library-browse).

###### Do I need to upload a file to clone a voice?

No - cloning is a **live in-browser recording** , not a file upload. You pick a language, read a short provided passage aloud (Shuffle for a different one), and record directly for about 10 seconds. See [Creating a Clone](https://docs.sarvam.ai/creative-cloning-create).

###### What's the Style setting when creating a clone?

A separate setting from the personality tags shown in the Voice Library - think of it as a hint for how the clone should be used, not a fixed label. Options are **General** (default), **Conversational** , **Professional** , **Warm** , and **Energetic**.

###### Can I preview a cloned voice before saving it?

Yes. The final step plays back your recording and lets you hear the clone on three sample lines in different registers - casual, news-anchor, and storytelling - before you confirm consent and save. If you’re not happy, **Re-record** is available right up to that last step.

###### Do I have to give consent to clone a voice?

Yes, and it’s mandatory, not a formality - you can’t save a clone without checking the consent box confirming you have the rights to record, process, and use that voice for generating new content.

###### My cloned voice doesn't sound quite like me - how do I improve it?

A cleaner recording almost always beats tweaking anything after the fact:

  1. **Re-record in a quiet room with no music playing** \- this is the product’s own stated requirement, not just a suggestion.
  2. **Read at your normal pace.** Rushing a short recording tends to distort natural speech patterns.
  3. **Use Re-record before finalizing,** on either Step 1 or the final Preview step - don’t settle for a take you’re unsure about.
  4. **If a passage feels awkward to read aloud, click Shuffle** for an easier one. A clean read of an easy passage beats a shaky read of a hard one.



###### How do I use a Studio-cloned voice in the API?

Open **Voice Library → My voices** (or Instant Voice Cloning home), copy **Voice ID** (`svc-…`) from the clone card, and pass it as `voice_id` on `POST /voices/clone`. Your API key must be bound to the same organization. See [Using a Cloned Voice](https://docs.sarvam.ai/creative-cloning-use#use-the-same-voice-in-the-api) and the [Instant Voice Cloning API overview](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview).

###### Will an API-created voice show up in Studio?

Yes. Voices created with `POST /voices/create` appear under **My voices** for the same account/org, and you can use them in Text to Speech and Dubbing like any Studio clone. The reverse works too: Studio clones are listed by `GET /voices` and usable via `voice_id`. See [Using a Cloned Voice](https://docs.sarvam.ai/creative-cloning-use#use-the-same-voice-in-the-api).

## Speech to Text

###### What file types and size limits does Speech to Text support?

**MP3, WAV, M4A, FLAC, OGG, and AAC** , up to **500 MB** per file. Video files work directly too - no need to extract the audio track yourself first.

###### Can I record audio instead of uploading a file?

Yes - click **or record audio** on the upload screen to capture audio directly in the browser. There are also three built-in example clips (“Gujarati finance news,” “Marathi cricket commentary,” “Tamil healthcare conversation”) if you want to see a real transcription before committing your own recording.

###### Does it handle code-mixed speech (e.g. a regional language with English terms)?

Yes, and it transcribes as-is - a real example output includes Gujarati text with embedded English financial terms like “IDBI bank,” “share,” and “disinvestment.” This is normal, expected behavior, not an error.

###### How do I get accurate speaker separation?

Provide an accurate speaker count if you know it - for a roundtable or panel recording, this is often the single biggest factor in whether the transcript correctly separates who said what. If unsure, round upward: merging an unused extra slot is a smaller error than splitting an undercounted one. Cross-talk and overlapping speech are a known hard case for diarization generally.

###### My transcript has errors or missed words - what should I check?

In order:

  1. **Confirm the language setting matches what’s actually spoken.** This affects the model’s phonetic expectations for the whole recording, not just word choice.
  2. **Check the speaker count** , especially for multi-speaker recordings - an inaccurate count is the most common cause of garbled or merged segments.
  3. **If the errors cluster around overlapping speech,** that’s expected - cross-talk is a known hard case for diarization generally, not specific to your recording.
  4. **If English terms appear inside regional-language text,** that’s correct behavior, not an error - code-mixed speech transcribes as heard.



## Licensing & commercial use

###### Can I use Bulbul v3 or cloned-voice audio in a commercial product (game, app, paid media)?

Yes. Output you generate on your account — including Text to Speech exports, Dubbing exports, and API audio from **Bulbul v3** — may be used in shipped, sold products when generation runs while credits are consumed on your account. That includes your **₹100 signup credits** ; there is no separate production tier or minimum top-up beyond normal credit usage.

Cloned voices require the mandatory dashboard consent confirming you hold rights to the voice. No additional commercial registration is needed.

See [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing) for the full policy, including retained rights after you stop using Sarvam.

###### Do I keep rights to audio I already exported if I stop using Sarvam?

Yes. Under our EULA, Sarvam assigns Output rights to you. Audio you already exported and incorporated into a product remains licensed for that use, even if you later stop topping up or close your account — as long as it was generated while you were in compliance with our terms.

See [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing).

## Data & Security

###### Are my uploaded files secure?

Sarvam’s infrastructure follows standard institutional data-security practices. For specifics on data residency or retention relevant to your use case, check with your Sarvam account contact - commitments here can vary by plan and deployment.

## Need More Help?

[Email supportReach out directly at support@sarvam.ai.](mailto:support@sarvam.ai)[Join our DiscordEarly access to new releases, biweekly challenges, office hours with the team, and India’s AI builder community.](https://discord.com/invite/5rAsykttcs)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/creative-stt-best-practices)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Overview](https://docs.sarvam.ai/creative/studio-overview)
  * Content Studio

    * [Dubbing (Beta)](https://docs.sarvam.ai/creative-dubbing)

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


