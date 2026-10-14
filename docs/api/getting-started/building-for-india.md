---
url: https://docs.sarvam.ai/api/getting-started/building-for-india/
title: Building for Indian Languages | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:32.709506+00:00
---

# Building for Indian Languages | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/getting-started/building-for-india/

Skip to navigation

On this page

  * Language coverage at a glance
  * Speech-to-Text: transcribe real Indian audio
  * Telephony and 8kHz audio
  * Text-to-Speech: natural Indian voices
  * Pronunciation control
  * Document AI: Indic OCR with Sarvam Vision
  * Document translation
  * Text translation and transliteration
  * Where to go next



Scroll to top

[Getting Started](https://docs.sarvam.ai/api/getting-started/welcome)

# Building for Indian Languages

The concepts that make Indian-language speech and document apps work in production: code-mixing, scripts, telephony audio, voices, and Indic OCR.

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/getting-started/building-for-india.md "View this page as plain text")|More actions

This page is for Model APIs.

Indian-language products have to handle realities that English-first stacks ignore: people mix English into every sentence, the same language is written in multiple scripts, a lot of audio arrives over 8kHz phone lines, and documents come as scans in regional scripts. This page maps those realities to the exact Sarvam speech, voice, and vision APIs, with code that’s been run against the live API.

## Language coverage at a glance

Coverage differs by capability, so pick the model that matches your language set.

Capability| Model| Languages  
---|---|---  
Speech-to-Text| Saaras v3| 23 (22 Indian + English)  
Speech-to-Text-Translate| Saaras v3| 23 (22 Indian + English) → English  
Text-to-Speech| Bulbul v3| 11 (10 Indian + English)  
Document Digitization| Sarvam Vision| 23 (22 Indian + English)  
Document Translation| Document Translation API| 23 (22 Indian + English); PDF, Office, and web formats  
Text translation| Mayura v1 / Sarvam-Translate v1| 11 (10 Indian + English) / 23 (22 Indian + English)  
Chat / reasoning| Sarvam-105B| 11 (10 Indian + English)  
  
## Speech-to-Text: transcribe real Indian audio

`saaras:v3` exposes a `mode` parameter that controls _how_ speech is written down. This is where most Indic-specific decisions happen:

`mode`| What you get  
---|---  
`transcribe`| Transcription in the native script  
`translate`| English translation of the speech  
`verbatim`| Word-for-word, including fillers and repetitions  
`translit`| Romanized (Latin-script) output  
`codemix`| Natural code-mixed text, English words stay in English  
  
The difference is easiest to see on one clip. For audio of _“मुझे flight book करनी है”_ (a typical Hinglish sentence), the **same audio** produces:

`mode`| Transcript (live output)  
---|---  
`transcribe`| मुझे फ्लाइट बुक करनी है।  
`codemix`| मुझे flight बुक करनी है।  
`translit`| Mujhe flight book karni hai.  
      
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    with open("audio.wav", "rb") as f:
    
        response = client.speech_to_text.transcribe(
    
            file=f,
    
            model="saaras:v4",
    
            mode="codemix",          # keep English words in English
    
            language_code="hi-IN",
    
        )
    
    print(response.transcript)       # मुझे flight बुक करनी है।

Use `codemix` for chat/agent transcripts that feel natural, `transcribe` for clean native-script records, and `translit` when a downstream system only handles Latin script. The REST endpoint handles clips up to 30 seconds, for longer audio use the [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api).

### Telephony and 8kHz audio

A large share of Indian voice traffic is phone audio: 8kHz, mono, often µ-law/A-law encoded. Two rules keep transcription quality high:

  1. **Match the sample rate everywhere.** For 8kHz audio, set `sample_rate=8000` **both** when opening the streaming connection **and** when sending each audio chunk. Mismatched rates cause garbled output.
  2. **Use a supported streaming codec.** Streaming STT accepts WAV and raw PCM (`pcm_s16le`, `pcm_l16`, `pcm_raw`) only.
  3. **Signal end-of-audio.** Call `ws.flush()` after the last chunk so the server knows to emit a transcript instead of waiting indefinitely for more audio.



`saaras:v3` is tuned for telephony, so prefer it for call audio.
    
    
    import asyncio
    
    import base64
    
    from sarvamai import AsyncSarvamAI
    
    # Load 8kHz call audio and base64-encode it
    
    with open("call_recording_8khz.wav", "rb") as f:
    
        audio_chunk = base64.b64encode(f.read()).decode("utf-8")
    
    async def transcribe_call_audio():
    
        client = AsyncSarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
        async with client.speech_to_text_streaming.connect(
    
            model="saaras:v4",
    
            mode="transcribe",
    
            language_code="hi-IN",
    
            sample_rate=8000,              # match the phone line
    
            input_audio_codec="pcm_s16le",
    
            flush_signal=True,             # required to enable ws.flush()
    
        ) as ws:
    
            await ws.transcribe(audio=audio_chunk, encoding="audio/wav", sample_rate=8000)
    
            await ws.flush()        # signal end-of-audio so the server emits a transcript
    
            print(await ws.recv())
    
    asyncio.run(transcribe_call_audio())

See the [Streaming STT guide](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api) for the full WebSocket lifecycle, VAD, reconnection, and voice-agent barge-in.

## Text-to-Speech: natural Indian voices

`bulbul:v3` speaks 11 languages (10 Indian + English) with 30+ voices, and it’s built for the way Indians actually write, so you usually don’t pre-process anything.

  * **Pass code-mixed text directly.** Mixed Hindi-English (“आपका OTP 4321 है। Please use it…”) is spoken naturally; no need to romanize or split it.
  * **Normalize English words and numbers** with `enable_preprocessing=true` when your text has lots of abbreviations or digits.
  * **Pick a voice** with `speaker` (e.g. `shubh`, `priya`, `kavya`). See the [voice list](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api).
  * **Output to a phone line** by requesting a telephony codec, `output_audio_codec` supports `mulaw` and `alaw` alongside `mp3`, `wav`, `opus`, etc.


    
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key="YOUR_SARVAM_API_KEY")
    
    with open("otp.mp3", "wb") as f:
    
        for chunk in client.text_to_speech.convert_stream(
    
            text="आपका OTP 4321 है। Please use it within 5 minutes.",
    
            language_code="hi-IN",
    
            speaker="shubh",
    
            model="bulbul:v4-flash",
    
            output_audio_codec="mp3",
    
        ):
    
            f.write(chunk)

### Pronunciation control

Brand names, abbreviations, and regional terms (“NEFT”, “KYC”, a company name) don’t always come out right by default. Create a [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary) with Bulbul v3 to pin how specific words are spoken, then pass its `dict_id` to any TTS call (REST, HTTP stream, or WebSocket):
    
    
    for chunk in client.text_to_speech.convert_stream(
    
        text="NEFT transfer karein aur KYC complete karein",
    
        language_code="hi-IN",
    
        speaker="shubh",
    
        model="bulbul:v4-flash",
    
        dict_id="p_5cb7faa6",        # your pronunciation dictionary
    
        output_audio_codec="mp3",
    
    ):
    
        ...  # write/play chunk

## Document AI: Indic OCR with Sarvam Vision

Indian documents arrive as scans, photos, and PDFs in regional scripts, often with tables and mixed languages. **Sarvam Vision** extracts text and structure across **23 languages (22 Indian + English)** , preserving the original script. **Digitise** returns the whole document as `html` or `md`; **Extract** pulls just the fields you define.

It’s an asynchronous job API: create the job in one call, poll status, then fetch the output.
    
    
    import os, time
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    with open("document.pdf", "rb") as f:
    
        job = client.doc_ai.digitise(
    
            file=[("document.pdf", f, "application/pdf")],
    
            language="hi-IN",     # primary document language (BCP-47)
    
            output_format="md",   # "html" (default) or "md"
    
        )
    
    TERMINAL = {"completed", "partially_completed", "failed", "rejected"}
    
    while True:
    
        st = client.doc_ai.get_status(job_id=job.job_id)
    
        if st.status.lower() in TERMINAL:
    
            break
    
        time.sleep(5)
    
    # ZIP containing the .md output plus page-level JSON
    
    dl = client.doc_ai.get_download_url(job_id=job.job_id)
    
    print("download:", dl.method, dl.url)

See the [Document AI guide](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview) for schema-based Extract and the full job lifecycle. The older `document_intelligence` job API (create → upload → start → poll → download) still works for existing integrations, but new work should use `doc_ai`.

## Document translation

When the deliverable is a **translated file** (not plain text), use the [Document Translation API](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview). Upload once, pick up to 12 target languages per job, and export each language in the **same format** as the source (PDF stays PDF, DOCX stays DOCX). The pipeline runs OCR or structural extraction, then translation — layout and formatting are preserved.

The flow matches other async document APIs: create job → `PUT` file to signed `upload_url` → `start` → poll `live-status` → `export` per language.
    
    
    import os, time
    
    from pathlib import Path
    
    import httpx
    
    from sarvamai import SarvamAI
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    document = Path("handbook.pdf")
    
    job = client.document_translation.create(
    
        job_name="handbook",
    
        source_language_code="en-IN",
    
        target_language_codes=["hi-IN", "ta-IN"],
    
        original_filename=document.name,
    
    )
    
    with document.open("rb") as f:
    
        httpx.put(
    
            job.upload_url,
    
            content=f.read(),
    
            headers={
    
                "Content-Type": "application/pdf",
    
                "x-ms-blob-type": "BlockBlob",
    
            },
    
            timeout=120.0,
    
        ).raise_for_status()
    
    client.document_translation.start(job_id=job.job_id)
    
    TERMINAL = {"Completed", "PartiallyCompleted", "Failed"}
    
    while True:
    
        status = client.document_translation.get_live_status(job_id=job.job_id)
    
        if status.job_state in TERMINAL:
    
            break
    
        time.sleep(12)
    
    # Export each completed language — see Poll and export for the download loop
    
    print("job_id:", job.job_id, "state:", status.job_state)

See [Poll and export](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/poll-and-export) for per-language `export` and download URLs.

Use [Document AI](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview) when you only need digitised text or structured fields. Use Document Translation when stakeholders need an editable or printable file in another language.

## Text translation and transliteration

For **short text** (not whole files), `mayura:v1` (11 languages, 10 Indian + English, colloquial modes, output-script and native-numeral control) and `sarvam-translate:v1` (23 languages, 22 Indian + English, formal) handle translation, and the [Transliteration API](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/transliteration) converts between scripts. See the [Text translation guide](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/translation) for `output_script` and `numerals_format` options.

## Where to go next

  * [Speech-to-Text overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview) · [Streaming STT](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api) · [Batch STT](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
  * [Text-to-Speech overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview) · [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
  * [Document AI](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview) · [Document Translation](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)
  * [Libraries & SDKs](https://docs.sarvam.ai/api/getting-started/sdks) · [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/getting-started/sdks)[ModelsNext](https://docs.sarvam.ai/api/getting-started/models)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
    * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
    * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
    * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
    * [Models](https://docs.sarvam.ai/api/getting-started/models)

    * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
    * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
    * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
    * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
    * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
    * Account & Billing

  * API Guides & Tutorials

    * Large Language Models

    * Speech to Text

    * Text to Speech

    * Text Processing

    * Document Intelligence

    * Document Translation

    * Dubbing

    * Instant Voice CloningBeta

  *     * Integration

    * Developer Tools

  * Cookbook

    * Guides

    * Example Voice Agents

  * Self-Hosted Deployments

    * Overview

    * AWS SageMaker

  *     * Migrations




  * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
  * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
  * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
  * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
  * [Models](https://docs.sarvam.ai/api/getting-started/models)
  * [Saaras](https://docs.sarvam.ai/api/getting-started/models/saaras)
  * [Bulbul](https://docs.sarvam.ai/api/getting-started/models/bulbul)
  * [Sarvam 105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)
  * [Open-Weight Models](https://docs.sarvam.ai/api/getting-started/models/openweight)
  * [GLM-5.3](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)
  * [Gemma 4 31B](https://docs.sarvam.ai/api/getting-started/models/openweight/gemma-4-31b)
  * [DeepSeek V4.1 Flash](https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash)
  * [Mayura](https://docs.sarvam.ai/api/getting-started/models/mayura)
  * [Sarvam Translate](https://docs.sarvam.ai/api/getting-started/models/sarvam-translate)
  * [Sarvam Vision](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)
  * [Sarvam 30B (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/sarvam-30b)
  * [Sarvam M (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/sarvam-m)
  * [Saarika (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/saarika)
  * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
  * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
  * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
  * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
  * [Organisations & workspaces](https://docs.sarvam.ai/api/platform/organisations-and-workspaces)
  * [Create an organisation](https://docs.sarvam.ai/api/platform/create-an-organisation)
  * [Create a workspace](https://docs.sarvam.ai/api/platform/create-a-workspace)
  * [Invite your team](https://docs.sarvam.ai/api/platform/invite-your-team)
  * [Billing & payments](https://docs.sarvam.ai/api/platform/billing)
  * [Platform FAQ](https://docs.sarvam.ai/api/platform/faq)
  * [Chat Completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * [Responses API](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/responses-api)
  * [List your chat messages](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/list-your-chat-messages)
  * [Control response randomness](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-response-randomness)
  * [Control response diversity](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-response-diversity)
  * [Adjust the model's thinking level](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/adjust-the-models-thinking-level)
  * [Encourage new topics in response](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/encourage-new-topics-in-response)
  * [Reduce repetition words or phrases in response](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/reduce-repetition-words-or-phrases-in-response)
  * [Get repeatable results](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/get-repeatable-results)
  * [Control the response length](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-the-response-length)
  * [Control where the model stops](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-where-the-model-stops)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)
  * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
  * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)
  * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
  * [Realtime Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming)
  * [Best Practices](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/best-practices)
  * [FAQs](https://docs.sarvam.ai/api/speech-to-text/faq)
  * [Select Output Mode](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/select-output-mode)
  * [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/specify-language-codes)
  * [Enable Speaker Diarization](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/enable-speaker-diarization)
  * [Keyterm Prompting](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/keyterms)
  * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/ivr-contact-center)
  * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/bfsi-voice-bots)
  * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
  * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services)
  * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/agri-rural)
  * [Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)
  * [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)
  * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/which-api-to-use)
  * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)
  * [HTTP Stream](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream)
  * [WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket)
  * [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
  * [Best Practice Guide for Bulbul v4 Flash](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices)
  * [Best Practices (Bulbul v3)](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices)
  * [Set the Language](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-the-language)
  * [Change the Speaker Voice](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/change-the-speaker-voice)
  * [Adjust the Tone](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-tone)
  * [Adjust the Speed](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-speed)
  * [Adjust the Loudness](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-loudness)
  * [Set the Sample rate](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-the-sample-rate)
  * [Enable Text Preprocessing](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/enable-text-preprocessing)
  * [Set audio format for output](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-audio-format-for-output)
  * [Set bitrate for output](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-bitrate-for-output)
  * [Set maximum length for sentence splitting](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-maximum-length-for-sentence-splitting)
  * [Set buffer size to start processing](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-buffer-size-to-start-processing)
  * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/ivr-contact-center)
  * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/bfsi-voice-bots)
  * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
  * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/government-services)
  * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview)
  * [Text Translation](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/translation)
  * [Transliteration](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/transliteration)
  * [Language Detection](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/language-detection)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview)
  * [Get your config_id](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/how-to/get-your-config-id)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)
  * [Set Style Guidelines](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/style-guidelines)
  * [Pick a Genre](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/genre-and-model-tier)
  * [Use Native Numerals](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/native-numerals)
  * [Poll Status and Export Results](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/poll-and-export)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/faq)
  * [Use Cases](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/use-cases)
  * [Translate a PDF](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/guides/translate-a-pdf)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)
  * [Job Lifecycle](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle)
  * [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/specify-language-codes)
  * [Control Translation Tone](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/control-translation-tone)
  * [Choose a Voice](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice)
  * [Choose Export Formats](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/faq)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview)
  * [Prepare Reference Audio](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/prepare-reference-audio)
  * [Clone Across Languages](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/clone-across-languages)
  * [Choose Audio Formats](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/choose-audio-formats)
  * [Use Quality Control](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/use-quality-control)
  * [HTTP Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/http-streaming)
  * [WebSocket Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/websocket-streaming)
  * [Supported Languages](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/supported-languages)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/faq)
  * [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)
  * [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)
  * [Twilio](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio)
  * [Exotel](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)
  * [Vobiz](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)
  * [Vapi](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)
  * [n8n](https://docs.sarvam.ai/api/integration/n8n)
  * [Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)
  * [LangChain](https://docs.sarvam.ai/api/integration/langchain)
  * [LiveKit in Production](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)
  * [Pipecat in Production](https://docs.sarvam.ai/api/integration/pipecat-production-guide)
  * [MCP Server](https://docs.sarvam.ai/api/developer-tools/mcp)
  * [Markdown & llms.txt](https://docs.sarvam.ai/api/developer-tools/llms-txt)
  * [Context7](https://docs.sarvam.ai/api/developer-tools/context7)
  * [Agent Skills](https://docs.sarvam.ai/api/developer-tools/agent-skills)
  * [Call Analytics Pipeline](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)
  * [Live Video Transcription](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)
  * [Podcast Generator](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator)
  * [WhatsApp Bot](https://docs.sarvam.ai/api/cookbook/guides/whats-app-bot)
  * [Collection Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/collection-agent)
  * [Government Scheme Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent)
  * [Tutor Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/tutor-agent)
  * [Loan Advisory Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/loan-advisory-agent)
  * [Introduction](https://docs.sarvam.ai/api/self-hosted/introduction)
  * [Managed vs Self-Hosted](https://docs.sarvam.ai/api/self-hosted/hosted-vs-self-hosted)
  * [How it works](https://docs.sarvam.ai/api/self-hosted/architecture)
  * [Get started](https://docs.sarvam.ai/api/self-hosted/sagemaker/get-started)
  * [Speech-to-Text (Saaras v3)](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-saaras)
  * [Sarvam Vision](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-vision)
  * [Text-to-Speech (Bulbul v3)](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-bulbul)
  * [Deploy with Terraform](https://docs.sarvam.ai/api/self-hosted/sagemaker/terraform)
  * [Speech-to-Text](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-saaras)
  * [Sarvam Vision](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-vision)
  * [Text-to-Speech](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-bulbul)
  * [Error handling](https://docs.sarvam.ai/api/self-hosted/sagemaker/errors)
  * [Configure & tune](https://docs.sarvam.ai/api/self-hosted/sagemaker/configure)
  * [Operations](https://docs.sarvam.ai/api/self-hosted/sagemaker/operations)
  * [Limitations](https://docs.sarvam.ai/api/self-hosted/sagemaker/limitations)
  * [Troubleshooting](https://docs.sarvam.ai/api/self-hosted/sagemaker/troubleshooting)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text)
  * [Instant Voice Cloning](https://docs.sarvam.ai/api/migrations/from-elevenlabs/voice-cloning)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-cartesia/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-cartesia/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-cartesia/speech-to-text)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-deepgram/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-deepgram/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-deepgram/speech-to-text)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-gemini/overview)
  * [Chat Completion](https://docs.sarvam.ai/api/migrations/from-gemini/chat-completion)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-gemini/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-gemini/speech-to-text)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


