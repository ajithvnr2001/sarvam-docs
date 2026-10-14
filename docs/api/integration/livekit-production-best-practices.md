---
url: https://docs.sarvam.ai/api/integration/livekit-production-best-practices/
title: LiveKit in Production | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:42.438894+00:00
---

# LiveKit in Production | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/livekit-production-best-practices/

Skip to navigation

On this page

  * LiveKit in Production
  * Which STT class to use
  * Contents
  * 1\. Reference config
  * 2\. Where latency hides
  * 3\. Skip LiveKit’s Silero VAD
  * 4\. STT configuration
  * 5\. Tuning Sarvam’s VAD
  * 6\. Turn handling and endpointing
  * 7\. Barge-in and interruptions
  * 8\. TTS configuration
  * 9\. Measuring latency
  * 10\. Capturing request IDs
  * 11\. The legacy class and migration
  * 12\. Reliability and failure modes
  * 13\. Tuning playbook
  * 14\. Copy-paste configs
  * WebRTC or app: lowest latency, clean audio
  * Telephony or SIP: noisy, echo handled by the carrier
  * Quick reference



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)[Best Practices](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)

# LiveKit in Production

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/livekit-production-best-practices.md "View this page as plain text")|More actions

This page is for Model APIs.

## LiveKit in Production

A tuning and operations guide for teams shipping cascading voice agents (Sarvam STT, then an LLM, then Sarvam TTS) on the LiveKit Agents SDK.

Everything here is derived from the current `livekit-plugins-sarvam` plugin source and the `livekit-agents` runtime. New to LiveKit and Sarvam? Start with [Build Your First Voice Agent using LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit) first; come back here before you ship.

The LiveKit defaults are tuned for English, LiveKit Cloud hosted, Silero VAD driven pipelines. A Sarvam pipeline is none of those three. At minimum, change `vad`, `turn_detection`, `stream_type`, and the endpointing delays. Shipping on defaults is the single most common cause of “the agent feels slow” or “it cuts me off.”

### Which STT class to use

Class| Model| Recommendation| Use for  
---|---|---|---  
`sarvam.STTStreaming`| `saaras:v3-realtime`| **Use this**|  All new voice agents  
`sarvam.STT`| `saaras:v3`| Legacy| Batch `recognize()`, existing deployments  
  
`saaras:v3-realtime` gives you true partial transcripts (barge-in no longer waits for a final), a simpler VAD (three millisecond-valued parameters instead of ten frame counters), live reconfiguration without a reconnect, and a structured event and close-code protocol. This guide documents `STTStreaming` throughout; the legacy class is covered only in [Section 11](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#11-the-legacy-class-and-migration).

`sarvam.STT`’s default model is not `saaras:v3`. If you use the legacy class, pass `model="saaras:v3"` explicitly.

* * *

## Contents

  1. [Reference config](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#1-reference-config)
  2. [Where latency hides](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#2-where-latency-hides)
  3. [Skip LiveKit’s Silero VAD](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#3-skip-livekits-silero-vad)
  4. [STT configuration](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#4-stt-configuration)
  5. [Tuning Sarvam’s VAD](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#5-tuning-sarvams-vad)
  6. [Turn handling and endpointing](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#6-turn-handling-and-endpointing)
  7. [Barge-in and interruptions](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#7-barge-in-and-interruptions)
  8. [TTS configuration](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#8-tts-configuration)
  9. [Measuring latency](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#9-measuring-latency)
  10. [Capturing request IDs](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#10-capturing-request-ids)
  11. [The legacy class and migration](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#11-the-legacy-class-and-migration)
  12. [Reliability and failure modes](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#12-reliability-and-failure-modes)
  13. [Tuning playbook](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#13-tuning-playbook)
  14. [Copy-paste configs](https://docs.sarvam.ai/api/integration/livekit-production-best-practices#14-copy-paste-configs)



* * *

## 1\. Reference config
    
    
    from livekit.agents import AgentSession
    
    from livekit.plugins import sarvam
    
    session = AgentSession(
    
        # STT: Sarvam's own server-side VAD drives turn-taking
    
        stt=sarvam.STTStreaming(
    
            language="hi-IN",
    
            stream_type="fast",         # was "balanced": 500 ms chunks instead of 1000 ms
    
            mode="transcribe",
    
            endpointing="vad",
    
            sample_rate=16000,
    
            vad_min_silence_ms=400,     # Sarvam's end-of-turn silence window
    
        ),
    
        llm=sarvam.LLM(model="sarvam-105b"),   # or any other LLM plugin
    
        tts=sarvam.TTS(
    
            model="bulbul:v4-flash",
    
            speaker="priya",
    
            language_code="hi-IN",
    
            min_buffer_size=30,         # was 50, lowers TTFB
    
            max_chunk_length=150,
    
            output_audio_codec="linear16",   # skip the mp3 decode hop
    
            speech_sample_rate=24000,
    
        ),
    
        # Critical: no LiveKit VAD. Sarvam STT already has one.
    
        vad=None,
    
        turn_handling={
    
            "turn_detection": "stt",             # trust Sarvam's vad.speech_end
    
            "endpointing": {
    
                "mode": "fixed",
    
                "min_delay": 0.25,               # was 0.5 (or 0.3 streaming default)
    
                "max_delay": 2.0,
    
            },
    
            "interruption": {
    
                "enabled": True,
    
                "mode": "vad",                   # the adaptive detector can't work here, see Section 7
    
                "min_words": 1,                  # the real noise filter when vad=None
    
                "false_interruption_timeout": 1.5,
    
                "resume_false_interruption": True,
    
            },
    
            "preemptive_generation": {"enabled": True},
    
        },
    
        # other defaults worth revisiting
    
        aec_warmup_duration=None,        # None for telephony/SIP, keep 3.0 for WebRTC + mic
    
        user_away_timeout=None,          # or a value that matches your product
    
        min_consecutive_speech_delay=0.0,
    
    )

Every override above is explained below. If you change nothing else, change `vad`, `turn_detection`, `stream_type`, and `endpointing.min_delay`.

* * *

## 2\. Where latency hides

The user-perceived latency is the sum of the whole chain, not any one model:

Three things worth knowing:

  * **The first hop is a hard floor most people never look at.** The plugin buffers audio into fixed-size chunks before sending: 1000 ms on the default `stream_type="balanced"`, 500 ms on `"fast"`. Sarvam’s VAD can’t detect end-of-speech until the chunk containing that silence arrives, so `balanced` adds up to a full second in front of every turn. Set `stream_type="fast"`.
  * **`vad_min_silence_ms` and `min_delay` stack. They don’t overlap.** 500 ms of Sarvam silence plus a 0.5 s `min_delay` is a full second of dead air. Tune both together.
  * **TTS time-to-first-byte is dominated by connection state, not model speed.** A cold Sarvam TTS websocket costs a full TLS handshake on the critical path. Call `prewarm()` (Section 8).



Measure this instrumented, don’t guess: Section 9.

* * *

## 3\. Skip LiveKit’s Silero VAD

Pass `vad=None` and let Sarvam’s server-side VAD drive turn-taking.

`STTStreaming` runs with `endpointing="vad"` by default, so the server emits `vad.speech_start` and `vad.speech_end` on every session, and the plugin maps those onto the framework’s start/end-of-speech events. That VAD already runs server-side on the exact audio the recognizer sees, is tunable through three explicit parameters trained on Indic speech (Section 5), and adds no local inference cost. Running Silero alongside it means two VADs disagreeing about turn boundaries: double-triggered interruptions, warnings in your logs, and endpointing metrics anchored on the wrong timestamp.

If you omit `vad`, `AgentSession` silently installs a LiveKit Inference-hosted Silero VAD, which needs LiveKit Cloud credentials and adds a network hop. Pass `vad=None` explicitly to opt out.

Passing `vad=None` does disable four framework features gated on a VAD instance. Be deliberate about the trade:

Feature| Why it breaks with `vad=None`| Do this instead  
---|---|---  
Semantic end-of-turn model (`inference.TurnDetector`)| Needs a VAD `INFERENCE_DONE` event; never fires without one| Set `turn_detection="stt"`, tune `vad_min_silence_ms` and `min_delay`  
`endpointing.max_delay`| Only applies when the EOT model returns a low probability; no VAD means no prediction| Treat `min_delay` as your only endpointing knob  
`interruption.min_duration`| Evaluated against VAD speech duration, which never fires| Use `interruption.min_words` instead (Section 7)  
Adaptive interruption detection| Needs a VAD and an STT with aligned transcripts; `STTStreaming` doesn’t have the latter| Set `interruption.mode="vad"` explicitly  
  
The trade is a good one on `saaras:v3-realtime` specifically: because it emits real partial transcripts and signals end-of-speech before the final transcript, barge-in fires on partials (Section 7) and preemptive generation actually engages (Section 6), neither of which worked without a VAD on the legacy plugin.

The semantic turn detector is a weak fit for Sarvam regardless: outside LiveKit Cloud it resolves to a local model whose per-language thresholds cover 14 languages (Hindi included), falling back to an English-calibrated threshold for everything else. Sarvam’s own VAD plus a tuned `min_delay` is the more predictable choice for Indic languages.

If you do keep a VAD (for example, on LiveKit Cloud, to get the EOT model for Hindi), its `min_silence_duration` must be at least 0.25 s, or `AgentSession` raises a `ValueError`.

* * *

## 4\. STT configuration
    
    
    sarvam.STTStreaming(
    
        language="hi-IN",            # default: "en-IN"
    
        stream_type="fast",          # default: "balanced"
    
        mode="transcribe",           # default: "transcribe"
    
        endpointing="vad",           # default: "vad"
    
        encoding="linear16",         # only value accepted
    
        sample_rate=16000,           # default: 16000 (8000 or 16000 only)
    
        prompt=None,
    
        return_timestamps=False,
    
        api_key=None,                # falls back to SARVAM_API_KEY
    
        # server-side VAD tuning, see Section 5
    
        vad_sot_threshold=None,
    
        vad_min_speech_ms=None,
    
        vad_min_silence_ms=None,
    
    )

Endpoint: `wss://api.sarvam.ai/speech-to-text-realtime/ws`. Model is fixed at `saaras:v3-realtime`; any invalid parameter raises `ValueError` at construction.

**`stream_type`** is the single biggest latency knob. `fast` buffers audio in 500 ms chunks before sending; `balanced` (the default) and `simulated` use 1000 ms. Set `"fast"` for any interactive agent; the default is the single most impactful bad setting for voice.

**`endpointing`** : `vad` (default) has the server emit speech-start and speech-end events, and pairs with `turn_detection="stt"`. `manual` has the plugin send events itself on the first audio frame and on flush; pair with the framework’s `turn_detection="manual"` for push-to-talk or IVR flows. In `manual` mode the VAD tuning parameters aren’t sent at all.

**`mode`** :

Mode| Output| Use when  
---|---|---  
`transcribe`| Verbatim, spoken language/script| Default; your LLM handles Indic input  
`codemix`| Preserves Hindi-English code-mixing| Urban Indian call flows; usually the most faithful for real conversations  
`translate`| English| Your LLM or downstream logic is English-only  
`verbatim`| Literal, minimal normalization| Compliance and audit transcripts  
`translit`| Romanized Indic| Your LLM is stronger on Latin script  
  
`codemix` is worth A/B-testing against `transcribe` for consumer-facing Indian deployments.

**`prompt`** carries domain vocabulary: product names, city names, SKUs, agent names. It’s the cheapest accuracy win available and frequently left empty. Unlike the legacy class, the realtime plugin sends it as a URL query parameter on the websocket handshake, so keep it short (a compact term list) or a long prompt risks a rejected handshake; use a TTS pronunciation dictionary (`dict_id`) for output-side fixes instead.
    
    
    stt = sarvam.STTStreaming(
    
        language="hi-IN",
    
        stream_type="fast",
    
        prompt="Insurance policy renewal. Terms: premium, NCB, IDV, Bajaj Allianz, endorsement.",
    
    )

**Live reconfiguration.** `STTStreaming.update_options(...)` sends a config update over the live websocket, no reconnect, no dropped audio, and the plugin defers any endpointing switch until the current utterance completes. Updatable in place: `language`, `stream_type`, `mode`, `prompt`, `endpointing`, and all three VAD parameters. `sample_rate` and `return_timestamps` are connection-only: changing them on a live stream is logged and ignored, so set them at construction.
    
    
    # e.g. the caller switched to Tamil: no reconnect, no dropped audio
    
    session.stt.update_options(language="ta-IN")

**`sample_rate` and `encoding`**: 8000 or 16000 only, and `linear16` only. Use 16000 for WebRTC; 8000 matches PSTN, but upsampling to 16 kHz is usually cheaper than degrading the recognizer’s input.

**Event mapping:**

Sarvam event| Framework event| Notes  
---|---|---  
`session.begin`| (none)| `request_id` and `session_id` captured  
`vad.speech_start`| `START_OF_SPEECH`| Carries `utterance_idx`  
`transcript.partial`| `INTERIM_TRANSCRIPT`| Real partials: drives fast barge-in and live UI  
`vad.speech_end`| `END_OF_SPEECH`| Emitted immediately, before the final  
`transcript.final`| `FINAL_TRANSCRIPT`| Committed after end-of-speech  
`session.end`| `RECOGNITION_USAGE`| Carries authoritative `audio_duration_s`  
`config.updated`| (none)| Acknowledges a live config update  
`error`| warning or `APIStatusError`| Depends on `is_fatal`, see Section 12  
  
`END_OF_SPEECH` precedes `FINAL_TRANSCRIPT`, the opposite of the legacy plugin, and it’s why preemptive generation works here (Section 6): the framework marks the turn committed at end-of-speech, then the arriving final triggers speculative LLM work and starts the endpointing hold. If the final never arrives, the plugin emits `END_OF_SPEECH` anyway after a 2.0 s fallback.

* * *

## 5\. Tuning Sarvam’s VAD

Three parameters, sent only when `endpointing="vad"`. All default to `None` (Sarvam’s server-side default applies); set them explicitly whenever you need reproducible behavior across environments.

Parameter| Wire name| Controls  
---|---|---  
`vad_sot_threshold`| `threshold`| Speech-onset probability required to start an utterance (0.0 to 1.0)  
`vad_min_speech_ms`| `min_speech_duration_ms`| Minimum speech length before `vad.speech_start` fires  
`vad_min_silence_ms`| `silence_duration_ms`| Silence required to fire `vad.speech_end`; your primary end-of-turn knob  
  
Lowering `vad_min_silence_ms` ends turns faster (snappier, more mid-sentence cutoffs); raising it holds through natural pauses (no cutoffs, more dead air). It stacks with `endpointing.min_delay` (Section 6): budget them together, since tuning one down while leaving the other conservative won’t move the needle.

Raise `vad_sot_threshold` first on noisy telephony, before touching anything else; it’s the cleanest defense against a VAD that keeps triggering on ambient audio. Raise `vad_min_speech_ms` to ignore clicks, coughs, keyboard noise, and DTMF beeps; lower it to catch very short words.

Recommended starting points by channel:

Channel| `vad_min_silence_ms`| `vad_min_speech_ms`| `vad_sot_threshold`  
---|---|---|---  
WebRTC / headset (clean audio, latency first)| 300| 80| 0.5  
Telephony (PSTN/SIP, noisy, connect-time noise)| 500| 200| 0.7  
Open-ended conversation (protect mid-sentence pauses)| 800| 120| 0.6  
Short transactional (OTP, yes/no, menu)| 200| 60| 0.5  
  
Tune the VAD before you tune `min_delay`. They compensate for each other, so changing both at once means you can’t attribute a regression.

* * *

## 6\. Turn handling and endpointing

`min_endpointing_delay`, `allow_interruptions`, `turn_detection`, `preemptive_generation`, and similar flat `AgentSession` kwargs are deprecated in favor of a nested `turn_handling` dict:
    
    
    AgentSession(
    
        turn_handling={
    
            "turn_detection": "stt",
    
            "endpointing":           {"mode": ..., "min_delay": ..., "max_delay": ..., "alpha": ...},
    
            "interruption":          {"enabled": ..., "mode": ..., "min_duration": ..., "min_words": ...,
    
                                      "false_interruption_timeout": ..., "resume_false_interruption": ...},
    
            "preemptive_generation": {"enabled": ..., "preemptive_tts": ..., "max_speech_duration": ..., "max_retries": ...},
    
            "user_turn_limit":       {"max_words": ..., "max_duration": ...},
    
        },
    
    )

**`turn_detection`** : set it to `"stt"`. Omitting it defaults to a semantic EOT model that needs a VAD and is English-calibrated outside 14 languages; `"vad"` needs a LiveKit VAD; `"stt"` trusts Sarvam’s own `vad.speech_end` and is the right choice here.

**Endpointing defaults, and why to change them:**

Key| Default| Recommended for Sarvam  
---|---|---  
`mode`| `"fixed"`| `"fixed"` to start  
`min_delay`| 0.3 to 0.5 s| 0.2 to 0.3 s  
`max_delay`| 2.5 to 3.0 s| 2.0 s (largely inert, see below)  
`alpha`| 0.9| 0.9 (`dynamic` mode only)  
  
`min_delay` is a hard sleep after the turn is detected and before it’s committed: `sleep(min_delay - time_since_last_speech)`. It’s a grace period, not pure waste; a new `vad.speech_start` during the hold cancels the pending commit. Because Sarvam’s VAD already confirmed silence server-side, the default 0.5 s is redundant margin stacked on margin. Dropping it to 0.25 s typically removes about 250 ms of dead air per turn with no increase in cutoffs, provided `vad_min_silence_ms` isn’t itself set aggressively low.

`max_delay` only applies when a semantic EOT model returns a low probability. With `turn_detection="stt"` or `vad=None`, no prediction is ever made, so the hold is always exactly `min_delay`. Keep `max_delay` as a documented ceiling, but don’t tune it expecting an effect.

**Preemptive generation** should stay enabled. Because `saaras:v3-realtime` emits end-of-speech before the final transcript, the framework has already marked the turn committed by the time the final arrives, which is the condition it needs to start speculative LLM work: a genuine improvement over the legacy plugin, where the reverse event order kept speculation inert in `"stt"` mode.

Key| Default| Guidance  
---|---|---  
`enabled`| `True`| Keep on  
`preemptive_tts`| `False`| Set `True` only if you can absorb wasted TTS spend on discarded speculative turns; it removes TTS TTFB from the critical path  
`max_speech_duration`| 10.0 s| Speculation is skipped past this; raise for long-form dictation  
`max_retries`| 3| Speculative attempts per user turn  
  
Interim transcripts don’t trigger speculation; the framework only speculates on finals. Interims buy you barge-in and live UI, not an earlier LLM start.

`mode: "dynamic"` learns `min_delay` per session from the user’s own pausing rhythm, clamped so your configured value is a floor. Worth trying for long consultative calls with a stable speaker; skip for short transactional calls, which never accumulate enough samples to learn anything. With `turn_detection="stt"` and `vad=None` there are fewer observations available, so expect it to stay near the floor; `"fixed"` is the honest default.

**Other defaults worth revisiting:**

Parameter| Default| Guidance  
---|---|---  
`aec_warmup_duration`| 3.0 s| Interruptions are ignored for the first 3 s of every agent turn. Right for WebRTC with a speaker and mic; set `None` for telephony/SIP, where the carrier handles echo  
`user_away_timeout`| 15.0 s| Flips `user_state` to `"away"` after mutual silence; set `None` if you don’t act on it  
`min_consecutive_speech_delay`| 0.0 s| Raise to about 0.2 s if back-to-back agent utterances sound rushed  
`session_close_transcript_timeout`| 2.0 s| Grace period for the last transcript at session close; raise if you lose final turns in your logs  
`max_tool_steps`| 3| Each step is a full LLM round trip; keep low for voice  
`user_turn_limit`| disabled| Set `max_words` or `max_duration` to catch a runaway monologue or stuck agent  
  
* * *

## 7\. Barge-in and interruptions

Key| Default| With `vad=None`  
---|---|---  
`enabled`| `True`| Works  
`mode`| auto| Set to `"vad"` explicitly  
`min_duration`| 0.5 s| Inert (VAD-derived)  
`min_words`| 0| Your main noise filter  
`false_interruption_timeout`| 2.0 s| Works  
`resume_false_interruption`| `True`| Works, needs a pause-capable audio output  
`discard_audio_if_uninterruptible`| `True`| Works  
`backchannel_boundary`| `(1.0, 1.0)`| Inert (adaptive mode only)  
  
Interruption is triggered from three places in the runtime; only two are reachable with `vad=None`: an interim-transcript hook, since Sarvam’s `transcript.partial` lands there, and a final-transcript hook as backstop. VAD-driven interruption never fires. So barge-in latency equals the time for Sarvam to return the first partial of the interrupting speech, a single 500 ms chunk plus model and network time on `stream_type="fast"`, not a completed utterance or local VAD energy detection. It’s also more robust than local-VAD barge-in: a cough, a door slam, or TV audio can’t interrupt the agent, because none of those produce a transcript.

Since `min_duration` is inert, `min_words` is your noise filter:
    
    
    "interruption": {"enabled": True, "mode": "vad", "min_words": 1}

`0` (default) lets any transcript interrupt; occasionally over-eager on ASR artifacts. `1` is a good default, filtering empty or whitespace-only artifacts. `2` suits noisy channels, but while the agent is speaking, a user turn shorter than `min_words` is dropped entirely rather than merely failing to interrupt, so single-word acknowledgements get discarded mid-agent-speech. Don’t exceed 2, and don’t go above 1 at all if single-word confirmations matter in your flow. Word counting is whitespace-delimited, so Devanagari, Tamil, Telugu, Bengali, and similar scripts are counted correctly with no adjustment needed.

**False-interruption recovery.** When something interrupts the agent and no real user turn materializes, the agent’s speech is paused, not cancelled; after `false_interruption_timeout` seconds of silence it resumes and fires an `agent_false_interruption` event. Lower the timeout to 1.2 to 1.5 s (the 2.0 s default is a long, awkward silence on a call). Instrument the event; a high false-interruption rate means the VAD is too eager, and the fix is at the VAD (raise `vad_sot_threshold` or `vad_min_speech_ms`), not here.
    
    
    @session.on("agent_false_interruption")
    
    def _on_false_interruption(ev):
    
        logger.warning("false interruption", extra={"resumed": ev.resumed})

For confirmations, legal disclaimers, or OTP readback, disable interruptions per turn rather than for the whole session (which makes the agent feel like an IVR):
    
    
    handle = session.say("Your OTP is 4 7 2 9.", allow_interruptions=False)
    
    await handle

* * *

## 8\. TTS configuration
    
    
    sarvam.TTS(
    
        model="bulbul:v4-flash",                 # default: "bulbul:v3"
    
        speaker="priya",                   # default: "shubh"
    
        language_code="hi-IN",      # default: "en-IN"
    
        speech_sample_rate=24000,          # default: 22050
    
        pace=1.0,
    
        temperature=0.6,                   # v3 only
    
        output_audio_codec="linear16",     # default: "mp3"
    
        output_audio_bitrate="128k",
    
        min_buffer_size=30,                # default: 50
    
        max_chunk_length=150,              # default: 150
    
        dict_id=None,                      # v3 only
    
        send_completion_event=True,        # leave True
    
    )

Use `bulbul:v4-flash` (latest) or `bulbul:v3`; `temperature` and `dict_id` are supported on both (not on `bulbul:v2`).

**Validation ranges** (enforced client-side, `ValueError` unless noted): `pace` 0.3 to 3.0, `loudness` 0.5 to 2.0, `temperature` 0.01 to 2.0, `min_buffer_size` 30 to 200, `max_chunk_length` 50 to 500, `output_audio_bitrate` one of 32k/64k/96k/128k/192k, `speech_sample_rate` one of 8000/16000/22050/24000/32000/44100/48000, `output_audio_codec` one of mp3/opus/flac/aac/wav/linear16/mulaw/alaw. `pitch` (-0.75 to 0.75) is the one exception: out-of-range values are clamped with a warning instead of raising. Speaker and model compatibility is validated at construction, so an unsupported voice fails at startup rather than mid-call.

**Latency levers, in order of impact:**

Lever| Default| Recommendation| Effect  
---|---|---|---  
`min_buffer_size`| 50| 30 (the minimum)| Characters buffered before synthesis starts; lower means audio starts sooner, at a small cost to opening-word prosody  
`output_audio_codec`| `mp3`| `linear16` (or `mulaw` at 8 kHz telephony)| `linear16` is raw passthrough, no decode hop; `mp3` needs a decoder pass per chunk  
`max_chunk_length`| 150| 150| Affects chunk cadence, not first-byte latency; lower means smoother interruption granularity but more websocket traffic  
`prewarm()`| not called| call it in `setup_fnc`| Removes the first utterance’s TLS handshake from the critical path  
  
`prewarm()` in practice:
    
    
    from livekit.agents import AgentServer, JobProcess
    
    def setup(proc: JobProcess) -> None:
    
        proc.userdata["tts"] = sarvam.TTS(model="bulbul:v4-flash", speaker="priya",
    
                                          language_code="hi-IN")
    
        proc.userdata["tts"].prewarm()
    
    server = AgentServer(setup_fnc=setup)

Verify it worked: `TTSMetrics.connection_reused` should read `True` and `acquire_time` near zero from the second turn on. If it’s `False` every turn, you’re likely constructing a new `sarvam.TTS()` per session instead of reusing one.

Leave `send_completion_event=True`; setting it `False` means the receive loop never sees a completion signal and blocks until it times out as `APITimeoutError`.

**Voice quality.** `pace` at 1.0 often reads slightly fast for support flows; 0.9 to 0.95 measurably helps comprehension, and intelligibility degrades above 1.15. `temperature` at 0.3 to 0.5 gives consistent delivery for regulated content (disclaimers, amounts, OTPs); 0.8 and up is more expressive, at the cost of occasional mispronunciation. `dict_id` (v3 only) is worth setting for brand names and place names that generic TTS mangles. `AgentSession` filters markdown and emoji from TTS input by default; keep both on, and instruct your LLM to produce properly punctuated sentences, since the plugin tokenizes on sentence boundaries.

* * *

## 9\. Measuring latency

Track end-to-end latency first, then decompose. `ChatMessage.metrics` is the primary surface; every committed turn carries these fields:

Field| Meaning  
---|---  
`e2e_latency`| User stopped speaking to agent started responding; the number your SLO lives on  
`transcription_delay`| End of user speech to transcript available  
`end_of_turn_delay`| End of speech to the decision to end the turn (your `endpointing.min_delay`)  
`llm_node_ttft`| LLM time to first token  
`tts_node_ttfb`| First text token to first audio chunk  
`on_user_turn_completed_delay`| Your callback’s duration; blocking I/O here adds directly to `e2e_latency`  
      
    
    @session.on("conversation_item_added")
    
    def _on_item(ev):
    
        m = getattr(ev.item, "metrics", None)
    
        if m:
    
            logger.info("turn_latency", extra={"e2e_latency": m.get("e2e_latency"),
    
                                                "llm_ttft": m.get("llm_node_ttft"),
    
                                                "tts_ttfb": m.get("tts_node_ttfb")})

Report the p50 and p95, not just the average. (p50 is the median: half your turns are faster than this. p95 is the value 95% of turns beat, so it captures the slow tail that an average hides.) A p50 of 800 ms with a p95 of 4 s feels broken to users even though the average looks fine.

`metrics_collected` remains the per-request latency and request-ID feed (usage and cost tracking has moved to `session_usage_updated`). `TTSMetrics.cancelled=True` counts barge-ins that killed a synthesis in flight, a good proxy for interruption health. For realtime STT, billed audio duration comes from the server’s `session.end` when available, falling back to a local estimate if the session dies first; reconcile against Sarvam’s dashboard rather than assuming either source is complete.

The SDK also emits OpenTelemetry spans (`user_turn`, `eou_detection`, `stt_node`, `llm_node`, `tts_node`, `tts_request_run`). Wire up an OTel exporter in production; it’s the only view that shows where a slow turn was actually slow, and it’s where Sarvam’s TTS request IDs land (Section 10).

**Suggested SLOs for a cascading Sarvam pipeline:**

Metric| Good| Acceptable| Investigate  
---|---|---|---  
`e2e_latency` p50| under 900 ms| under 1.4 s| over 2 s  
`e2e_latency` p95| under 1.8 s| under 2.5 s| over 3.5 s  
`transcription_delay` p95| under 400 ms| under 700 ms| over 1 s: check `stream_type`  
`tts_node_ttfb` p95| under 350 ms| under 600 ms| over 800 ms: check `prewarm`/`connection_reused`  
False-interruption rate| under 2%| under 5%| over 8%: raise `vad_sot_threshold`  
  
* * *

## 10\. Capturing request IDs

Sarvam’s server-side `request_id` is what their support team needs to investigate a bad transcript or mispronunciation. Coverage differs by surface:

Surface| Realtime STT| Sarvam TTS (streaming)| Sarvam TTS (batch)  
---|---|---|---  
`STTMetrics.request_id`| Sarvam’s real ID| not applicable| not applicable  
`TTSMetrics.request_id`| not applicable| client-side ID, not Sarvam’s| Sarvam’s real ID  
OTel span `lk.provider_request_ids`| yes, on `user_turn`| yes, on `tts_request_run`| not applicable  
`ChatMessage.metrics["provider_request_ids"]`| empty| empty| empty  
  
`STTMetrics.request_id` is the real Sarvam ID; log it and you’re done for STT. On the streaming TTS path, `TTSMetrics.request_id` is a locally generated ID assigned before Sarvam replies, so Sarvam’s actual ID only reaches the OTel span attribute `lk.provider_request_ids`; enable tracing if you need it there. `ChatMessage.metrics["provider_request_ids"]` is populated only for realtime (speech-to-speech) models, so it stays empty in any cascading STT-LLM-TTS pipeline.

Events emitted before Sarvam’s first message with an ID (a `START_OF_SPEECH` at session start, for instance) can carry an empty `request_id`. Treat `""` as “not yet known,” not as an error.

A minimal production log line should carry `session_id`, `turn_id`, `speech_id`, the Sarvam STT request ID, the Sarvam TTS request IDs, and `e2e_latency`. With those six fields you can escalate any complaint to Sarvam support with evidence. `speech_id` ties one utterance’s LLM and TTS calls together; `segment_id` identifies an individual synthesis segment within an utterance. Keep the IDs logged for as long as your support SLA requires, and don’t store transcript text alongside them unless that store meets your PII policy: Indian consumer call transcripts routinely contain names, addresses, and financial details.

* * *

## 11\. The legacy class and migration

`sarvam.STT` with `model="saaras:v3"` is the only path that supports batch `recognize()` (`STTStreaming` raises `NotImplementedError` for it). If you’re maintaining an existing deployment on it, the differences that matter:

| `STTStreaming` (realtime)| `STT` (legacy)  
---|---|---  
Interim transcripts| Real `INTERIM_TRANSCRIPT`| Never emitted  
Event order| End-of-speech, then final| Final, then end-of-speech  
Preemptive generation| Engages| Effectively inert in `"stt"` mode  
VAD tuning| 3 parameters| 10 frame-counter parameters  
Live reconfiguration| `config.update`, no reconnect| Forces a reconnect  
Retries| Framework default (3)| Forced to 0  
Chunking| `stream_type` (500/1000 ms)| Fixed 50 ms  
End-of-speech fallback| 2.0 s| 1.0 s  
`confidence` fallback| `0.0`| `1.0`  
Batch `recognize()`| Not supported| Supported  
Odia code| `or-IN`| `od-IN`  
  
New builds should use `STTStreaming`. Migrating is mostly a constructor swap plus replacing the VAD parameters per Section 5, but re-tune `min_delay` afterward, since the event ordering and chunking both change your latency profile.

* * *

## 12\. Reliability and failure modes

**Retries.** `STTStreaming` uses the framework default: 3 retries, 2.0 s interval, 10.0 s timeout. That timeout is too long for voice; a caller will have hung up. Tighten it:
    
    
    from livekit.agents import APIConnectOptions
    
    from livekit.agents.voice.agent_session import SessionConnectOptions
    
    conn_options = SessionConnectOptions(
    
        stt_conn_options=APIConnectOptions(max_retry=2, timeout=5.0),
    
        tts_conn_options=APIConnectOptions(max_retry=1, timeout=5.0),
    
        llm_conn_options=APIConnectOptions(max_retry=1, timeout=8.0),
    
        max_unrecoverable_errors=3,
    
    )

For calls you can’t afford to drop, wrap STT and TTS in a `FallbackAdapter`; a failed TTS is a silent agent, which is worse than a wrong one.

**Websocket close codes** are the most useful operational signal available:

Code| Meaning| Retryable| Action  
---|---|---|---  
1000 / 1001| Normal close| n/a| Expected  
1003| Auth, quota, or rate-limit error| No| Check the API key and concurrency limits; alert on this  
1008| Session timed out or exceeded max duration| No| Plan a reconnect strategy for long calls  
1013| Backend temporarily unavailable| Yes| Transient; alert only on sustained rates  
4000| Session rejected (bad parameters)| No| A config error; should have failed at construction  
  
Non-fatal `error` events (`is_fatal: false`) log a warning and let the session continue; watch their rate as an early degradation signal, since it’s otherwise invisible. Fatal errors raise `APIStatusError`. `ValueError` on any parameter fires at construction time, so instantiate `sarvam.STTStreaming` and `sarvam.TTS` in `setup_fnc`, not the entrypoint, so config errors fail the worker at startup rather than the caller’s session.

Sarvam closes idle TTS websockets after 60 s. The plugin defends on two layers, a transport-level ping every 20 s and an application-level ping every 30 s, so stale pooled connections are detected and replaced transparently. Size your key’s rate limits against peak concurrent calls times two (one STT socket plus one TTS socket per call), not average volume, and alert on close code 1003.

* * *

## 13\. Tuning playbook

Change one thing at a time and measure between steps.

  1. **Instrument first.** Wire up Section 9 and Section 10 before touching any parameter, and collect a baseline over at least 30 real calls.
  2. **Get the architecture right.** `stream_type="fast"`, `vad=None`, `turn_detection="stt"`, `model="bulbul:v4-flash"`. Confirm there’s no `TurnDetector requires a VAD model` warning at startup; if you see it, `vad=None` didn’t take effect.
  3. **Tune Sarvam’s VAD.** Raise `vad_min_silence_ms` if users get cut off mid-sentence; lower it if there’s dead air after they finish. Raise `vad_sot_threshold`, then `vad_min_speech_ms`, if noise or crosstalk is triggering turns.
  4. **Trim`endpointing.min_delay`.** Step down from 0.5 in 0.1 s increments (0.4, 0.3, 0.25, 0.2), stopping one step before cutoffs reappear. Most Sarvam pipelines land at 0.2 to 0.3 s.
  5. **Fix barge-in.** Raise `interruption.min_words` (0, then 1, then 2) until noise-triggered interruptions stop, watching that real single-word replies survive. Lower `false_interruption_timeout` to 1.2 to 1.5 s. For telephony, set `aec_warmup_duration=None`.
  6. **Cut TTS time-to-first-byte.** `min_buffer_size=30`, `output_audio_codec="linear16"` (or `mulaw` for 8 kHz), and `prewarm()`.
  7. **Cut LLM time-to-first-token.** Shrink the system prompt, scope the tool list to the current conversation phase, cap conversation history, and keep `max_tool_steps` low.
  8. **Polish the voice.** `pace` 0.9 to 0.95 for support flows, lower `temperature` for regulated content, and a `dict_id` dictionary for brand and place names.
  9. **Re-baseline.** Re-measure over 30-plus calls and set alerts on p95 `e2e_latency`, false-interruption rate, close code 1003, and non-fatal STT error rate.



* * *

## 14\. Copy-paste configs

### WebRTC or app: lowest latency, clean audio
    
    
    import logging
    
    from livekit.agents import (
    
        Agent, AgentServer, AgentSession, JobContext, JobProcess,
    
        TurnHandlingOptions, cli, metrics,
    
    )
    
    from livekit.plugins import sarvam
    
    logger = logging.getLogger("sarvam-agent")
    
    def setup(proc: JobProcess) -> None:
    
        # Construct here so config errors fail the worker, not the caller's session.
    
        proc.userdata["stt"] = sarvam.STTStreaming(
    
            language="hi-IN",
    
            stream_type="fast",
    
            mode="codemix",
    
            endpointing="vad",
    
            sample_rate=16000,
    
            vad_min_silence_ms=300,
    
            vad_min_speech_ms=80,
    
            vad_sot_threshold=0.5,
    
            prompt="Customer support for a fintech app. Terms: UPI, KYC, NEFT, IMPS, mandate.",
    
        )
    
        proc.userdata["tts"] = sarvam.TTS(
    
            model="bulbul:v4-flash",
    
            speaker="priya",
    
            language_code="hi-IN",
    
            speech_sample_rate=24000,
    
            output_audio_codec="linear16",
    
            min_buffer_size=30,
    
            max_chunk_length=150,
    
            pace=0.95,
    
            temperature=0.5,
    
        )
    
        proc.userdata["tts"].prewarm()
    
    server = AgentServer(setup_fnc=setup)
    
    @server.rtc_session()
    
    async def entrypoint(ctx: JobContext) -> None:
    
        ctx.log_context_fields = {"room": ctx.room.name}
    
        session = AgentSession(
    
            stt=ctx.proc.userdata["stt"],
    
            llm=sarvam.LLM(model="sarvam-105b"),
    
            tts=ctx.proc.userdata["tts"],
    
            vad=None,
    
            turn_handling=TurnHandlingOptions(
    
                turn_detection="stt",
    
                endpointing={"mode": "fixed", "min_delay": 0.22, "max_delay": 2.0},
    
                interruption={
    
                    "enabled": True,
    
                    "mode": "vad",
    
                    "min_words": 1,
    
                    "false_interruption_timeout": 1.3,
    
                    "resume_false_interruption": True,
    
                },
    
                preemptive_generation={"enabled": True},
    
            ),
    
            aec_warmup_duration=3.0,     # keep for open mic + speaker
    
            user_away_timeout=None,
    
            max_tool_steps=2,
    
        )
    
        @session.on("metrics_collected")
    
        def _on_metrics(ev):
    
            metrics.log_metrics(ev.metrics)
    
        @session.on("agent_false_interruption")
    
        def _on_false(ev):
    
            logger.warning("false_interruption", extra={"resumed": ev.resumed})
    
        await session.start(
    
            agent=Agent(instructions="You are a concise Hindi-speaking support agent. "
    
                                     "Reply in one or two short sentences. Use proper punctuation."),
    
            room=ctx.room,
    
        )
    
    if __name__ == "__main__":
    
        cli.run_app(server)

### Telephony or SIP: noisy, echo handled by the carrier
    
    
    stt = sarvam.STTStreaming(
    
        language="hi-IN",
    
        stream_type="fast",
    
        mode="transcribe",
    
        endpointing="vad",
    
        sample_rate=16000,             # upsample; usually cheaper than degrading the recognizer
    
        vad_min_silence_ms=500,
    
        vad_min_speech_ms=200,         # ignore line clicks, ringback, DTMF
    
        vad_sot_threshold=0.7,         # reject TV / crosstalk / ambient speech
    
    )
    
    tts = sarvam.TTS(
    
        model="bulbul:v4-flash",
    
        speaker="simran_en_customer",
    
        language_code="hi-IN",
    
        speech_sample_rate=8000,       # match the carrier
    
        output_audio_codec="mulaw",    # decoded in-process, no resample
    
        output_audio_bitrate="64k",
    
        min_buffer_size=30,
    
        pace=0.92,                     # slower reads better on narrowband
    
        temperature=0.5,
    
    )
    
    session = AgentSession(
    
        stt=stt, llm=sarvam.LLM(model="sarvam-105b"), tts=tts,
    
        vad=None,
    
        turn_handling={
    
            "turn_detection": "stt",
    
            "endpointing": {"mode": "fixed", "min_delay": 0.3, "max_delay": 2.5},
    
            "interruption": {
    
                "enabled": True,
    
                "mode": "vad",
    
                "min_words": 2,        # noisy line: stricter filter
    
                "false_interruption_timeout": 1.5,
    
                "resume_false_interruption": True,
    
            },
    
            "preemptive_generation": {"enabled": True},
    
            "user_turn_limit": {"max_duration": 45.0},   # catch a stuck call
    
        },
    
        aec_warmup_duration=None,      # important for telephony
    
        user_away_timeout=20.0,
    
    )

For compliance and audit flows, use `mode="verbatim"`, `return_timestamps=True`, a higher `vad_min_silence_ms` (around 900), a lower `temperature` (around 0.3), and disable `preemptive_generation` to avoid speculative spend; disable interruptions per-turn for disclosures. For push-to-talk or IVR, set `endpointing="manual"` on the STT and `turn_detection="manual"` on the session, then call `session.commit_user_turn()` yourself on a DTMF key or button release.

* * *

## Quick reference

Setting| Plugin default| Sarvam recommendation| Why  
---|---|---|---  
STT class| n/a| `sarvam.STTStreaming`| `saaras:v3` is legacy; realtime adds interims, live reconfig, a simpler VAD  
`stt.stream_type`| `"balanced"` (1000 ms)| `"fast"` (500 ms)| Hard floor under every downstream latency number  
`vad`| hosted Silero VAD| `None`| Sarvam STT has its own server-side VAD  
`turn_handling["turn_detection"]`| semantic EOT model| `"stt"`| Trust Sarvam’s `vad.speech_end`  
`stt.vad_min_silence_ms`| server default| set explicitly (200 to 900 by channel)| Your primary end-of-turn knob  
`endpointing.min_delay`| 0.3 to 0.5 s| 0.2 to 0.3 s| Sarvam’s VAD already confirmed silence  
`interruption.min_words`| 0| 1 (2 on noisy lines)| `min_duration` is inert without a VAD  
`interruption.false_interruption_timeout`| 2.0 s| 1.2 to 1.5 s| 2 s of silence is a long time on a call  
`interruption.mode`| auto| `"vad"`| Adaptive is unavailable with Sarvam STT  
`aec_warmup_duration`| 3.0 s| `None` for telephony| Otherwise 3 s of uninterruptible speech  
`tts.min_buffer_size`| 50| 30| Directly lowers TTS TTFB  
`tts.output_audio_codec`| `mp3`| `linear16` (`mulaw` at 8 kHz)| Skips a decode hop  
`tts.prewarm()`| not called| call it| Removes TLS setup from the first utterance  
`stt_conn_options.timeout`| 10.0 s| about 5 s| A 10 s stall means the caller has already hung up  
  
Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/langchain)[Pipecat Production GuideNext](https://docs.sarvam.ai/api/integration/pipecat-production-guide)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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
      * [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)
      * [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)
      * [Twilio](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio)
      * [Exotel](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)
      * [Vobiz](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)
      * [Vapi](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)
      * [n8n](https://docs.sarvam.ai/api/integration/n8n)
      * [Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)
      * [LangChain](https://docs.sarvam.ai/api/integration/langchain)
      * Best Practices
        * [LiveKit in Production](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)
        * [Pipecat in Production](https://docs.sarvam.ai/api/integration/pipecat-production-guide)

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


