---
url: https://docs.sarvam.ai/api/integration/pipecat-production-guide/
title: Pipecat Production Guide | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:14:42.913790+00:00
---

# Pipecat Production Guide | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/integration/pipecat-production-guide/

Skip to navigation

On this page

  * Pipecat Production Guide
  * Contents
  * 1\. The defaults that cost you
  * 2\. Pipeline architecture
  * Recommended setup
  * Use the current API
  * 3\. STT reference: SarvamRealtimeSTTService
  * Constructor arguments
  * Settings fields
  * 4\. VAD and barge-in: do not add Silero
  * Barge-in
  * 5\. Turn management
  * The default is an ML model, not a timeout
  * 6\. TTS reference: bulbul:v4-flash and v3
  * 7\. Latency: budget and measurement
  * 8\. Capturing STT and TTS request IDs
  * STT: on every frame (SarvamRealtimeSTTService)
  * TTS: only in a trace log
  * 9\. Reliability and error handling
  * 10\. Sarvam LLM
  * 11\. Legacy: SarvamSTTService and saaras:v3
  * 12\. Production tuning playbook



Scroll to top

[Integration](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)[Best Practices](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)

# Pipecat Production Guide

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/integration/pipecat-production-guide.md "View this page as plain text")|More actions

This page is for Model APIs.

## Pipecat Production Guide

A reference and tuning playbook for the Sarvam STT, TTS, and LLM plugins in Pipecat.

This page assumes you are writing Pipecat code. Every parameter, default, and code snippet was verified against source. Where a default is likely to hurt you in production, it is called out explicitly. New to Pipecat and Sarvam? Start with [Build Your First Voice Agent using Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat) first.
    
    
    pip install "pipecat-ai[sarvam]"

**Scope.** This guide covers `saaras:v3-realtime` via `SarvamRealtimeSTTService` for STT and `bulbul:v4-flash` (latest) / `bulbul:v3` for TTS. Both ship in `pipecat-ai[sarvam]` (realtime STT since Pipecat 1.8.0). The older `SarvamSTTService` (`saaras:v3` / `saaras:v4`) is documented in [Section 11](https://docs.sarvam.ai/api/integration/pipecat-production-guide#11-legacy-sarvamsttservice-and-saarasv3) for existing deployments.

* * *

## Contents

  1. [The defaults that cost you](https://docs.sarvam.ai/api/integration/pipecat-production-guide#1-the-defaults-that-cost-you)
  2. [Pipeline architecture](https://docs.sarvam.ai/api/integration/pipecat-production-guide#2-pipeline-architecture)
  3. [STT reference: SarvamRealtimeSTTService](https://docs.sarvam.ai/api/integration/pipecat-production-guide#3-stt-reference-sarvamrealtimesttservice)
  4. [VAD and barge-in: do not add Silero](https://docs.sarvam.ai/api/integration/pipecat-production-guide#4-vad-and-barge-in-do-not-add-silero)
  5. [Turn management](https://docs.sarvam.ai/api/integration/pipecat-production-guide#5-turn-management)
  6. [TTS reference: bulbul:v4-flash and v3](https://docs.sarvam.ai/api/integration/pipecat-production-guide#6-tts-reference-bulbulv4-flash-and-v3)
  7. [Latency: budget and measurement](https://docs.sarvam.ai/api/integration/pipecat-production-guide#7-latency-budget-and-measurement)
  8. [Capturing request IDs (SarvamRealtimeSTTService + TTS)](https://docs.sarvam.ai/api/integration/pipecat-production-guide#8-capturing-stt-and-tts-request-ids)
  9. [Reliability and error handling](https://docs.sarvam.ai/api/integration/pipecat-production-guide#9-reliability-and-error-handling)
  10. [Sarvam LLM](https://docs.sarvam.ai/api/integration/pipecat-production-guide#10-sarvam-llm)
  11. [Legacy: SarvamSTTService and saaras:v3](https://docs.sarvam.ai/api/integration/pipecat-production-guide#11-legacy-sarvamsttservice-and-saarasv3)
  12. [Production tuning playbook](https://docs.sarvam.ai/api/integration/pipecat-production-guide#12-production-tuning-playbook)



* * *

## 1\. The defaults that cost you

Ranked by impact. Each is explained in full later.

#| Parameter| Owner| Default| Why it hurts  
---|---|---|---|---  
1| `user_turn_strategies`| `LLMUserAggregatorParams`| `None`: a local ML smart-turn model| Not a simple timeout. You get `TurnAnalyzerUserTurnStopStrategy(LocalSmartTurnAnalyzerV3())`, an ML model running inference locally every turn, keyed to Pipecat VAD frames the Sarvam service never emits  
2| `model`| `SarvamTTSService.Settings`| not `bulbul:v4-flash`| Set `bulbul:v4-flash` (latest) or `bulbul:v3` explicitly. The Pipecat service default may be an older model and you lose v4 persona voices and `temperature` unless you set it  
3| `min_buffer_size`| `SarvamTTSService.Settings`| `50`| Sarvam buffers 50 characters server-side _after_ Pipecat already aggregated a sentence: double buffering before the first audio byte  
4| `stream_type`| `SarvamRealtimeSTTService.Settings`| `"fast"`| Even the fastest setting holds 500 ms of audio client-side before sending. `balanced` and `simulated` double it to 1000 ms  
5| `user_idle_timeout`| `LLMUserAggregatorParams`| `0` (disabled)| No dead-air recovery. A silent caller is never re-engaged  
6| `user_turn_stop_timeout`| `LLMUserAggregatorParams`| `5.0`| If no stop strategy fires, the turn hangs a full 5 s  
7| `sample_rate`| `SarvamTTSService(...)`| Pipecat/plugin default (often 24000)| Mismatch forces per-chunk resampling. `PipelineParams.audio_out_sample_rate` does not fix this, see Section 6  
8| `keepalive_timeout`| inherited constructor arg| `None` (disabled)| Idle sockets get dropped during long silences, and enabling it with `mulaw`/`alaw` sends the wrong format (Section 9)  
9| `ttfs_p99_latency`| `SarvamRealtimeSTTService(...)` constructor| `1.17` (`SARVAM_TTFS_P99`)| Mostly inert on the recommended setup, but costs `1.17` minus `stop_secs` per turn the moment you add a Pipecat VAD. There is no separately measured realtime constant; this value is carried over from the legacy model  
  
Two things that look like configuration but are not:

  * **Settings passed as constructor kwargs are silently ignored, not rejected.** `SarvamRealtimeSTTService(api_key=..., stream_type="balanced")` constructs fine and runs with `stream_type="fast"` anyway; `**kwargs` swallows it. Everything in the `Settings` table must go through `settings=`.
  * **`ttfs_p99_latency` is the reverse:** a constructor argument, not a `Settings` field. Spelled `ttfs_p99_latency` (time to final segment), not `p99_ttfs_latency`.



* * *

## 2\. Pipeline architecture

Frames flow through a chain of processors:

### Recommended setup

Sarvam’s realtime STT detects speech server-side and emits the speaking frames itself, so there is no Pipecat VAD in this pipeline. The External turn strategies are the correct pairing: they trigger on the plain `UserStartedSpeakingFrame` and `UserStoppedSpeakingFrame` that the service broadcasts.
    
    
    import os
    
    from pipecat.pipeline.pipeline import Pipeline
    
    from pipecat.pipeline.worker import PipelineParams, PipelineWorker
    
    from pipecat.processors.aggregators.llm_context import LLMContext
    
    from pipecat.processors.aggregators.llm_response_universal import (
    
        LLMContextAggregatorPair,
    
        LLMUserAggregatorParams,
    
    )
    
    from pipecat.services.sarvam.stt import SarvamRealtimeSTTService
    
    from pipecat.services.sarvam.tts import SarvamTTSService
    
    from pipecat.turns.user_start import ExternalUserTurnStartStrategy
    
    from pipecat.turns.user_stop import ExternalUserTurnStopStrategy
    
    from pipecat.turns.user_turn_strategies import UserTurnStrategies
    
    from pipecat.workers.runner import WorkerRunner
    
    stt = SarvamRealtimeSTTService(
    
        api_key=os.environ["SARVAM_API_KEY"],
    
        settings=SarvamRealtimeSTTService.Settings(
    
            language_code="hi-IN",     # or "auto"
    
            mode="transcribe",
    
            stream_type="fast",        # 500 ms client-side chunks, the lowest available
    
            endpointing="vad",         # Sarvam's server-side VAD drives turns
    
            encoding="linear16",
    
            sample_rate=16000,
    
        ),
    
        should_interrupt=True,         # set False to gate barge-in in Pipecat instead, see Section 4
    
    )
    
    tts = SarvamTTSService(
    
        api_key=os.environ["SARVAM_API_KEY"],
    
        settings=SarvamTTSService.Settings(
    
            model="bulbul:v4-flash",         # must be set explicitly
    
            voice="ishita_hi_devotional",  # v4 persona; use v3 short names only with model="bulbul:v3"
    
            language="hi-IN",
    
            pace=1.0,
    
            temperature=0.6,
    
            min_buffer_size=20,        # default 50, lower for faster first audio
    
        ),
    
    )
    
    context = LLMContext(messages)
    
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
    
        context,
    
        user_params=LLMUserAggregatorParams(
    
            user_turn_strategies=UserTurnStrategies(
    
                start=[ExternalUserTurnStartStrategy()],
    
                stop=[ExternalUserTurnStopStrategy(timeout=0.2, wait_for_transcript=True)],
    
            ),
    
            user_idle_timeout=12.0,    # default 0, disabled
    
            user_turn_stop_timeout=3.0,
    
            # no vad_analyzer, see Section 4
    
        ),
    
    )
    
    pipeline = Pipeline([
    
        transport.input(), stt, user_aggregator, llm, tts,
    
        transport.output(), assistant_aggregator,
    
    ])
    
    worker = PipelineWorker(
    
        pipeline,
    
        params=PipelineParams(enable_metrics=True, enable_usage_metrics=True),
    
        observers=[MetricsLogObserver()],
    
    )
    
    runner = WorkerRunner()
    
    await runner.add_workers(worker)
    
    await runner.run()

### Use the current API

Pipecat 1.3.0 renamed the top-level runnable unit from “pipeline task” to worker:

Deprecated (since 1.3.0)| Use instead  
---|---  
`from pipecat.pipeline.task import ...`| `from pipecat.pipeline.worker import ...`  
`PipelineTask(...)`| `PipelineWorker(...)`  
`PipelineRunner(...)`| `WorkerRunner(...)`  
  
`PipelineParams` itself is not deprecated, only its old import path and `PipelineTask`.

`allow_interruptions` is not a `PipelineParams` field in this version. It appears nowhere in the source, and `PipelineParams` is a Pydantic model that rejects unknown fields. Interruption behavior comes from `should_interrupt` and your turn strategies.

* * *

## 3\. STT reference: SarvamRealtimeSTTService

Streams raw audio to `wss://api.sarvam.ai/speech-to-text-realtime/ws` and maps Sarvam’s server-side VAD and transcript events into Pipecat frames. The model is hard-locked to `saaras:v3-realtime`; any other value raises `ValueError`.

### Constructor arguments

All keyword-only.

Argument| Default| Notes  
---|---|---  
`api_key`| required| Sent as the `API-SUBSCRIPTION-KEY` header  
`base_url`| `wss://api.sarvam.ai/speech-to-text-realtime/ws`| Must not already carry a query string  
`sample_rate`| `16000`| 8000 or 16000 only  
`settings`| `None`| Canonical config surface  
`should_interrupt`| `True`| Whether provider speech-start broadcasts an interruption (Section 4)  
`session_end_timeout`| `0.5`| Grace period waiting for `session.end` on clean shutdown  
`ttfs_p99_latency`| `1.17` (`SARVAM_TTFS_P99`)| Section 7  
  
Inherited via `**kwargs`: `reconnect_on_error` (default `True`, but see Section 9: this does not translate into automatic recovery from an STT connection failure), `audio_passthrough` (default `True`), `stt_ttfb_timeout` (default `2.0`), `keepalive_timeout` (default `None`), `keepalive_interval`.

`sample_rate` precedence is inverted from what you’d expect. `settings=Settings(sample_rate=8000)` is applied _after_ the constructor argument, so the `Settings` value wins.

### Settings fields

Field| Default| Allowed values| Live-updatable  
---|---|---|---  
`language_code`| `"hi-IN"`| 24 values incl. `"auto"`| Yes  
`stream_type`| `"fast"`| `fast`, `balanced`, `simulated`| Yes  
`endpointing`| `"vad"`| `vad`, `manual`| Yes  
`mode`| `"transcribe"`| `transcribe`, `translate`, `verbatim`, `translit`, `codemix`| Yes  
`prompt`| `None`| decoding prompt| Yes  
`threshold`| `None`| VAD sensitivity| Yes  
`silence_duration_ms`| `None`| end-of-speech silence| Yes  
`min_speech_duration_ms`| `None`| minimum speech to count| Yes  
`lid_gate_seconds`| `None`| auto language ID gate| Yes  
`lid_confidence_threshold`| `None`| auto language ID confidence| Yes  
`encoding`| `"linear16"`| `linear16`, `linear32`, `mulaw`, `alaw`| No  
`sample_rate`| ctor value| 8000, 16000| No  
`prefix_padding_ms`| `None`| audio kept before onset| No  
`return_timestamps`| `False`| segment offsets on finals| No  
  
Ten of the fourteen fields update live. `_update_settings` sends a Sarvam `config.update` message over the open socket: no reconnect, no dropped audio. This is a real operational advantage over the legacy service, where changing the language tears down the WebSocket. Notably `mode` is in this set, so you can switch between `transcribe` and `codemix` mid-call.

The four non-updatable fields log an unhandled-setting warning if you change them. There is also a public `update_config(**fields)` method if you want to push a config change directly. Optional parameters are sent on the connect query string only when not `None`; leaving one unset means the Sarvam server default applies.

**Modes:**

Mode| Output  
---|---  
`transcribe`| Transcription in the spoken language (default)  
`translate`| Translated to English  
`verbatim`| Includes fillers and disfluencies  
`translit`| Roman-script output  
`codemix`| Optimized for code-mixed / Hinglish speech  
  
**Language.** `language_code` takes the Sarvam code directly and is the recommended field: 24 values including `"auto"` for detection. The inherited `language` enum field also works, but with two sharp edges: it only converts `language_code` while that field is still at its default (`"hi-IN"`), and it accepts only Indian-locale members, so `Language.EN_US` raises `ValueError` at construction. Prefer setting `language_code` alone. With `language_code="auto"`, the transcript frame’s `language` is `None` and Sarvam reports the detected language per message; `lid_gate_seconds` and `lid_confidence_threshold` tune that detection.

**Frames it emits:**

Sarvam event| Pipecat result  
---|---  
`session.begin`| captures `request_id` (logged at INFO)  
`vad.speech_start`| `UserStartedSpeakingFrame` broadcast, plus `broadcast_interruption()` if `should_interrupt`  
`vad.speech_end`| `UserStoppedSpeakingFrame` broadcast, TTFB timer starts  
`transcript.partial`| `InterimTranscriptionFrame`  
`transcript.final`| `TranscriptionFrame(finalized=True)`  
`session.end`| `SarvamRealtimeSTTUsageMetricsData` (server-authoritative audio seconds)  
`error` with `is_fatal`| fatal `ErrorFrame`, then raises (Section 9)  
  
Two of these matter most for turn-taking, and both improve on the legacy service: interim transcripts exist, so `use_interim` on turn strategies genuinely works, and finals carry `finalized=True`, which short-circuits Pipecat’s STT safety-net timer. The frame names are the plain `UserStartedSpeakingFrame` and `UserStoppedSpeakingFrame`, not the `VADUser*` variants; strategies keyed to VAD-prefixed frames will never see these events, which is why Section 2 uses the External strategies.

`encoding` accepts `mulaw` and `alaw` at `sample_rate=8000`, so 8 kHz telephony audio can be sent without transcoding; chunk sizing accounts for the codec’s bytes-per-sample automatically.

* * *

## 4\. VAD and barge-in: do not add Silero

Do not add `SileroVADAnalyzer` to a pipeline using Sarvam STT. Sarvam runs its own VAD server-side, exposed through `endpointing` and four tuning parameters. Running Silero as well means two independent VADs disagreeing about the same audio, and Silero is not tuned for Indian acoustic conditions: background fans, traffic, and short acknowledgements like “haan” or “achha”. Keep `endpointing="vad"` (the default) and tune the server-side parameters instead.

**What you gain by not adding one:**

| Sarvam VAD (`endpointing="vad"`)| Adding a Pipecat VAD  
---|---|---  
Speech detection| Sarvam, tuned for Indian audio| Silero, general-purpose  
Frames from STT| `UserStartedSpeakingFrame`, `UserStoppedSpeakingFrame`| plus duplicate `VADUser*` frames  
Turn strategies| `External*`| `MinWords` plus `SpeechTimeout`  
`ttfs_p99_latency`| inert| adds `ttfs_p99_latency` minus `stop_secs` per turn  
Barge-in control| `should_interrupt` plus server parameters| Pipecat min-words gating  
  
`endpointing="manual"` means your application must signal turn ends itself; do not choose it unless you are driving turns externally.

### Barge-in

Unlike the legacy service, barge-in here is genuinely controllable. With `should_interrupt=True` (the default), every `vad.speech_start` immediately calls `broadcast_interruption()` and cuts the bot’s audio: lowest-latency barge-in, with sensitivity governed entirely by the server-side parameters below. With `should_interrupt=False`, Sarvam still emits the speaking frames but broadcasts no interruption; your Pipecat turn-start strategy decides instead, so you can require several words before the bot yields:
    
    
    stt = SarvamRealtimeSTTService(api_key=..., should_interrupt=False)
    
    user_params = LLMUserAggregatorParams(
    
        user_turn_strategies=UserTurnStrategies(
    
            start=[MinWordsUserTurnStartStrategy(min_words=3, use_interim=True)],
    
            stop=[ExternalUserTurnStopStrategy(timeout=0.2)],
    
        ),
    
    )

Because the realtime service emits interim transcripts, `use_interim=True` lets that decision land early rather than waiting for the final transcript. This is the configuration to reach for when false interruptions from “haan” or “achha” are the main complaint. `should_interrupt` is a constructor argument and cannot be changed at runtime.

**Server-side VAD parameters.** All default to `None` (use the Sarvam server default) and are sent only when set.

Parameter| Controls| Tuning for noisy Indian environments| Live-updatable  
---|---|---|---  
`threshold`| VAD sensitivity: probability above which audio counts as speech| Raise to reject fans, traffic, TV| Yes  
`silence_duration_ms`| Silence needed to declare end of speech| Lower for snappier turns, raise for speakers who pause mid-sentence| Yes  
`min_speech_duration_ms`| Minimum speech duration to count as a turn| Raise to reject clicks, coughs, door slams: the main dial against false barge-in| Yes  
`prefix_padding_ms`| Audio retained before detected onset| Raise if first syllables are clipped| No  
  
Because `threshold`, `silence_duration_ms`, and `min_speech_duration_ms` all update live, you can tune them mid-call without dropping the connection.

* * *

## 5\. Turn management

### The default is an ML model, not a timeout

If you pass no `user_turn_strategies`, you get:
    
    
    start = [VADUserTurnStartStrategy(), TranscriptionUserTurnStartStrategy()]
    
    stop  = [TurnAnalyzerUserTurnStopStrategy(turn_analyzer=LocalSmartTurnAnalyzerV3())]

That is a local ML smart-turn model running inference on every turn, and both defaults key off `VADUser*` frames that Sarvam never emits. Always pass strategies explicitly.

**Start strategies** (`pipecat.turns.user_start`): `MinWordsUserTurnStartStrategy`, `TranscriptionUserTurnStartStrategy`, `VADUserTurnStartStrategy`, `WakePhraseUserTurnStartStrategy`, `ExternalUserTurnStartStrategy`, `KrispVivaIpUserTurnStartStrategy`.

**Stop strategies** (`pipecat.turns.user_stop`): `SpeechTimeoutUserTurnStopStrategy`, `TurnAnalyzerUserTurnStopStrategy`, `LLMTurnCompletionUserTurnStopStrategy`, `DeferredUserTurnStopStrategy`, `ExternalUserTurnStopStrategy`, `ExternalUserTurnCompletionStopStrategy`.

There is no `VADUserTurnStopStrategy`. If an older guide mentions one, it does not exist. There is `FilterIncompleteUserTurnStrategies`, a third container that makes the LLM the end-of-turn gate, worth considering for users who pause mid-sentence a lot.

`ExternalUserTurnStopStrategy`, the recommended stop strategy, takes `timeout` (default `0.5`, a short delay to coalesce consecutive speech segments) and `wait_for_transcript` (default `True`, require a transcript before ending the turn). Drop `timeout` to 0.2 to 0.3 for snappier turns, since Sarvam’s server-side endpointing has already decided speech ended.

**Strategy order matters: first match wins.** The controller iterates start strategies and stops at the first one that claims the turn; once a turn is open, later strategies are no-ops.
    
    
    # WRONG: min_words is dead code. External claims the turn on speech-start,
    
    # before any transcript exists.
    
    start=[ExternalUserTurnStartStrategy(), MinWordsUserTurnStartStrategy(min_words=3)]
    
    # RIGHT: pick one. External for lowest latency, or MinWords alone to gate on words.
    
    start=[MinWordsUserTurnStartStrategy(min_words=3, use_interim=True)]

This is a silent failure: the pipeline looks configured for backchannel suppression and provides none.

**`MinWordsUserTurnStartStrategy`.** `min_words` is required with no default; `use_interim` defaults `True` and works here because the realtime service emits interim transcripts; `enable_user_speaking_frames` defaults `True` (base class). The threshold is asymmetric, and that is the point:
    
    
    min_words = self._min_words if self._bot_speaking else 1

While the bot is speaking, the user needs `min_words` words to take the turn (“haan”, “okay”, “achha” do not); while the bot is silent, a single word takes the turn immediately, so the agent stays responsive. Transcripts below the threshold call `trigger_reset_aggregation()`, discarding accumulated text. Pair this with `should_interrupt=False` (Section 4), otherwise Sarvam has already cut the bot’s audio before the word count is evaluated.

**Idle and safety timeouts:**

Parameter| Default| Recommendation  
---|---|---  
`user_idle_timeout`| `0` (disabled)| 8 to 15 s  
`user_turn_stop_timeout`| `5.0`| 2.5 to 3.0, fires `on_user_turn_stop_timeout`  
`audio_idle_timeout`| `1.0`| Forces speech-stop when audio stops arriving mid-speech; leave as is  
  
`user_idle_timeout` is narrower than the name suggests: the timer is anchored to `BotStoppedSpeakingFrame`, fires once per bot turn, is cancelled by function calls in progress, and only emits an `on_user_turn_idle` event. It does not re-prompt the LLM; your handler must. Adjustable at runtime with `UserIdleTimeoutUpdateFrame(timeout=...)`; `0` cancels.

Do not set `audio_passthrough=False` on the STT service. Anything downstream that needs raw audio, a smart-turn analyzer or an aggregator VAD, only receives it because the STT passes it through.

* * *

## 6\. TTS reference: bulbul:v4-flash and v3

Two services: `SarvamTTSService` streams over WebSocket, so audio flows before the sentence finishes synthesizing; use this for conversational agents. `SarvamHttpTTSService` does one HTTP round trip per utterance with the whole audio at once, so time to first audio is the full synthesis time; fine for batch or fixed IVR prompts, too slow for live conversation.

**`bulbul:v4-flash` (latest) and `bulbul:v3` properties:** omitted `speech_sample_rate` → 22050 Hz output; `pace` 0.5 to 2.0; `temperature` 0.01 to 1.0 (default 0.6). v4 defaults to persona **`shubh_enhi_ads`** when `voice`/`speaker` is omitted (or set any ID from the [v4 catalog](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices#bulbul-v4-flash-voices)); v3 defaults to `shubh`. `pitch` and `loudness` are not supported on v3/v4 and are dropped with a warning; preprocessing is always enabled and cannot be disabled.

**bulbul:v4-flash:** 200+ persona IDs such as `simran_en_customer`, `ishita_hi_devotional`, `gokul_ta_narration` — full list in the [Voices guide](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices#bulbul-v4-flash-voices).

**bulbul:v3:** short names such as `shubh`, `priya`, `anand` (30+ speakers).

Set `model="bulbul:v4-flash"` explicitly for new agents. The Pipecat service default may still target an older Bulbul generation, which changes sample rate, voice set, and supported parameters.

Voices are not validated against the model in Pipecat. A v3 short name with `bulbul:v4-flash` (or the reverse) is often accepted locally and fails on the Sarvam API. Use `get_speakers_for_model("bulbul:v4-flash")` or `get_speakers_for_model("bulbul:v3")` when available, or pick IDs from the docs catalog.

`pace` outside 0.5 to 2.0 is clamped, with a warning.

**Latency-relevant settings:**

Field| Default| Effect  
---|---|---  
`min_buffer_size`| `50`| Characters Sarvam buffers server-side before emitting audio. Stacks on Pipecat’s own sentence aggregation. Lower to 15 to 25  
`max_chunk_length`| `150`| Max characters per synthesis chunk  
`pace`| `1.0`| Speaking rate  
`temperature`| `0.6`| Voice variation; lower is more consistent  
  
Because Pipecat aggregates a sentence and then Sarvam waits for `min_buffer_size` characters, the default double-buffers before the first audio byte; on short replies (“Ji, bilkul”) the server-side buffer dominates. The service requests `send_completion_event=true`, so `TTSStoppedFrame` fires as soon as synthesis finishes rather than waiting on an idle timer. A keepalive ping is sent every 20 s.
    
    
    from pipecat.frames.frames import TTSUpdateSettingsFrame
    
    await worker.queue_frame(
    
        TTSUpdateSettingsFrame(delta=SarvamTTSService.Settings(voice="simran_en_customer"))
    
    )

Always use `delta=` with a typed `Settings` object. The dict form is deprecated since 0.0.104, and on the WebSocket service it is actively dangerous: `SarvamTTSSettings` redefines its alias map for `language_code`, which overrides the inherited `voice_id` to `voice` alias. So `TTSUpdateSettingsFrame(settings={"voice_id": "simran_en_customer"})` is a silent no-op, the value lands in `extra` and the voice never changes. `{"speaker": ...}` silently no-ops too.

Any settings change resends the config message to Sarvam.

`PipelineParams.audio_out_sample_rate` does not affect Sarvam TTS. The service always passes a concrete sample rate from the constructor (or its plugin default), so the pipeline value is never consulted. To change output rate, pass `sample_rate=` on `SarvamTTSService(...)`. Align it with your transport (8000 for telephony, 16000/24000 for WebRTC).

Set it to match your transport, or every chunk is resampled in-process (CPU and jitter cost). Telephony is typically 8000 Hz.

The WebSocket TTS service cannot emit mu-law. `output_audio_codec` and `output_audio_bitrate` are hardcoded to `"linear16"` and `"128k"` in `__init__`, neither is a constructor argument nor a `Settings` field, and both are reachable only through the deprecated `params=InputParams(...)` path. You can request `sample_rate=8000`, but mu-law conversion for telephony must happen in your serializer or transport. Note the asymmetry: realtime STT accepts mu-law input natively, see Section 3.

* * *

## 7\. Latency: budget and measurement

**Where the time goes:**

**`stream_type` is a latency floor.** Audio is held client-side until a full chunk accumulates: `fast` is 500 ms (16000 bytes at 16 kHz linear16), `balanced` and `simulated` are 1000 ms (32000 bytes). This buffering is additive to network and model time. Even on `fast` there is a 500 ms client-side floor before the first byte leaves your process, usually the single largest fixed cost in the STT leg, and it is not tunable below 500 ms. Use `fast` for conversational agents.

**Enabling metrics:**
    
    
    PipelineParams(enable_metrics=True, enable_usage_metrics=True)

Metrics arrive as `MetricsFrame` carrying typed objects: `TTFBMetricsData` (`value`, seconds), `TTFAMetricsData` (`ttfa`, `leading_silence`, time to first audio), `ProcessingMetricsData` (`value`), `LLMUsageMetricsData` (`value: LLMTokenUsage`, prompt/completion/total/cache/reasoning), `SarvamRealtimeSTTUsageMetricsData` (`value`, audio seconds, server-authoritative), `TTSUsageMetricsData` (`value`, characters), and `TurnMetricsData` (`is_complete`, `probability`, `e2e_processing_time_ms`).
    
    
    from pipecat.observers.loggers.metrics_log_observer import MetricsLogObserver
    
    from pipecat.observers.loggers.transcription_log_observer import TranscriptionLogObserver
    
    observers=[MetricsLogObserver(), TranscriptionLogObserver(level="DEBUG")]

Narrow it with `MetricsLogObserver(include_metrics={TTFBMetricsData, LLMUsageMetricsData})`. Realtime STT usage comes from Sarvam’s own `session.end` message, so billed audio seconds are authoritative rather than locally estimated, provided the socket closes cleanly within `session_end_timeout` (0.5 s). On timeout the service falls back to its locally counted total; raise the timeout if you reconcile usage against Sarvam’s billing.

**`ttfs_p99_latency`.** This value tells turn-stop strategies how long to wait after speech end for a final transcript. It matters only when a strategy is armed by `VADUserStoppedSpeakingFrame`, which the Sarvam service does not emit, so on the recommended setup in Section 2 it is inert. It becomes live the moment you add a Pipecat VAD, where it costs `max(0, ttfs_p99_latency - stop_secs)` per turn.

The default is `SARVAM_TTFS_P99 = 1.17`, measured for the legacy model with VAD `stop_secs=0.2`; there is no separately measured realtime constant. Pipecat maintains distinct values elsewhere where a realtime path was actually measured (`ELEVENLABS_TTFS_P99 = 2.01` alongside `ELEVENLABS_REALTIME_TTFS_P99 = 0.41`, `OPENAI_TTFS_P99 = 2.01` alongside `OPENAI_REALTIME_TTFS_P99 = 1.66`), so `1.17` is plausibly an unmeasured carry-over here.

If you do add a Pipecat VAD, don’t trust the shipped default as-is: measure your own value against your traffic with [the stt-benchmark tool](https://github.com/pipecat-ai/stt-benchmark), and treat Sarvam’s mode choice (`transcribe`, `codemix`, `verbatim`, and so on) as one of the variables worth benchmarking, since they are not equally fast. Pass whatever you measure at construction:
    
    
    SarvamRealtimeSTTService(api_key=..., ttfs_p99_latency=...)

Do not pass `ttfs_p99_latency=None` to “disable” it; that selects `DEFAULT_TTFS_P99 = 1.0`.

`stt_ttfb_timeout` (default `2.0`) is easy to confuse with this. It only affects what gets _reported_ as STT TTFB, not how long turn-taking waits.

* * *

## 8\. Capturing STT and TTS request IDs

Every Sarvam session has a `request_id`. Capture it alongside your own turn identifier for debugging and for raising issues with Sarvam support.

The STT observer in this section is for `SarvamRealtimeSTTService` only. On `SarvamSTTService`, it will log `request_id=None`. Use [Section 11](https://docs.sarvam.ai/api/integration/pipecat-production-guide#11-legacy-sarvamsttservice-and-saarasv3), or migrate.

### STT: on every frame (`SarvamRealtimeSTTService`)

`SarvamRealtimeSTTService` captures `request_id` from Sarvam’s `session.begin` event and attaches it to every interim and final transcript frame’s `result` (the shape is flat: `frame.result["request_id"]`), and logs it once per session at INFO. If you are on `SarvamSTTService`, this observer will log `request_id=None`. Use [Section 11](https://docs.sarvam.ai/api/integration/pipecat-production-guide#11-legacy-sarvamsttservice-and-saarasv3) (or migrate).

Because the ID comes from `session.begin`, it identifies the WebSocket session, not an individual utterance; after a reconnect you get a new one, which makes it a useful correlation key for diagnosing mid-call reconnections.

On realtime frames only, `result.get("language")` is the language Sarvam reported, and final transcripts additionally carry `speech_end_audio_position_s` for aligning against a recording. Neither field exists on legacy `SarvamSTTService` frames; language there is `frame.language` (Section 11). Filter `isinstance(data.source, SarvamRealtimeSTTService)` so you do not scrape Daily/DTMF `TranscriptionFrame`s from other processors.
    
    
    from pipecat.services.sarvam.stt import SarvamRealtimeSTTService
    
    class SarvamRequestIdObserver(BaseObserver):
    
        async def on_push_frame(self, data: FramePushed):
    
            if not isinstance(data.source, SarvamRealtimeSTTService):
    
                return
    
            frame = data.frame
    
            if not isinstance(frame, TranscriptionFrame):
    
                return
    
            result = frame.result or {}
    
            logger.info("sarvam.stt request_id={} lang={} text={!r}",
    
                        result.get("request_id"), result.get("language"), frame.text)

Add it to `observers=[...]` on your worker and ship those lines to your log store.

### TTS: only in a trace log

`SarvamTTSService` reads a per-request `request_id` off each audio message but only writes it to a `TRACE`-level log line (`TTS request_id=<id>, context_id=<id>`); it is not attached to any frame, so an observer cannot see it. To capture it, add a loguru sink scoped to that module, since a process-wide `TRACE` level would be unusably verbose:
    
    
    _TTS_ID = re.compile(r"TTS request_id=(?P<request_id>\S+?), context_id=(?P<context_id>\S+)")
    
    def capture_tts_request_id(message):
    
        match = _TTS_ID.search(message.record["message"])
    
        if match:
    
            logger.bind(sarvam_tts=True).info("sarvam.tts {}", match.groupdict())
    
    logger.add(capture_tts_request_id, level="TRACE", filter="pipecat.services.sarvam.tts")

`context_id` is Pipecat’s per-utterance audio-context id, also carried on `TTSAudioRawFrame.context_id`. That gives you a join key: observe `TTSAudioRawFrame` to map a `context_id` to a conversation turn, then use the sink to map the same `context_id` to Sarvam’s `request_id`.

* * *

## 9\. Reliability and error handling

The realtime service is materially more robust than the legacy one, but two behaviors need handling.

**Reconnection.** Despite inheriting `WebsocketService`’s `reconnect_on_error=True` default, the realtime STT service does not automatically recover from a dropped or failed connection: there is no retry/backoff loop that re-establishes the socket for you. Treat an STT connection error as terminal for that session, handle `on_connection_error`, and rebuild the service (or fail the call over) yourself rather than assuming the framework will reconnect it.

If you build your own reconnect logic, in-flight audio is not replayed: `STTService` implements a VAD-aware buffered replay, but the realtime service never requests it, so audio sent up to the point of failure is lost rather than replayed on the new connection. Expect a gap in the transcript, not a silent hang.

A new `request_id` is issued on a rebuilt connection (Section 8), which is how you detect this happened in your logs.

**Fatal errors do raise.** When Sarvam sends an `error` event with `is_fatal`, the service pushes a fatal `ErrorFrame`, stops metrics, and raises `SarvamRealtimeSTTError`. This is deliberate and different from the legacy service, which reports everything non-fatally; non-fatal errors are logged as warnings and otherwise ignored.
    
    
    @stt.event_handler("on_connection_error")
    
    async def on_stt_connection_error(service, error):
    
        logger.error("Sarvam realtime STT error: {}", error)
    
        # Escalate: end the call, fail over, or hand off to a human.

An invalid API key surfaces as a WebSocket close with code `1003` on the first receive, not at connect time, so authentication failures appear slightly later than you might expect.

**Keepalive.** `keepalive_timeout` is `None` (disabled) by default; enabling it prevents idle sockets being dropped during long silences.

Keepalive sends 16-bit PCM silence regardless of your `encoding`. The base class generates `b"\x00" * (num_samples * 2)`. If you configured `mulaw`, `alaw`, or `linear32`, those bytes are the wrong format. Leave keepalive off when using a non-`linear16` encoding.

* * *

## 10\. Sarvam LLM

`SarvamLLMService` is OpenAI-compatible. Because Sarvam’s API does not accept some OpenAI fields, the service removes `stream_options`, `max_completion_tokens`, and `service_tier` from the request.

`extra` is not a workaround for those three fields. `extra` is merged _before_ the removal step, so anything you inject under those names is stripped anyway. Only fields Sarvam’s schema does not declare survive via `extra`.

For voice, the system prompt is a latency parameter as much as a quality one: long replies delay first audio and give users more to interrupt.
    
    
    system_instruction=(
    
        "Respond in natural spoken language. Never use markdown, bullet points, or emoji. "
    
        "Keep replies to one or two sentences. "
    
        "Reply in the same language the user speaks, including Hinglish."
    
    )

Three things this buys you: markdown and emoji sound terrible read aloud, language matching makes code-mixed conversation feel natural, and short replies cut perceived latency directly.

* * *

## 11\. Legacy: SarvamSTTService and saaras:v3

`SarvamSTTService` (`saaras:v3` / `saaras:v4`) is the previous generation. It remains in `pipecat-ai[sarvam]` for existing deployments. New work should target `SarvamRealtimeSTTService` / `saaras:v3-realtime` (Section 3).

**Why migrate:**

| `saaras:v3` (legacy)| `saaras:v3-realtime`  
---|---|---  
Reconnect on error| None, see below (silent failure)| None automatically either, but raises a fatal error immediately instead of silently discarding audio (Section 9)  
Interim transcripts| Never| Yes  
`finalized=True` on finals| Never| Yes  
Barge-in control| None, always interrupts| `should_interrupt`  
Runtime config changes| Reconnect required| Live `config.update`, 10 fields  
`mode` changes| Init-only| Runtime-updatable  
Input encodings| `wav`| `linear16`, `linear32`, `mulaw`, `alaw`  
Fatal errors| Reported non-fatally| Raise  
  
**The failure mode that ends calls silently.** `SarvamSTTService` has no automatic recovery from a WebSocket failure. `_connect()` catches connection errors, reports them non-fatally, and leaves the socket `None`; `run_stt()` then begins with `if not self._socket_client: return`, so every audio frame is discarded from that point on. Nothing retries: `STTService`’s `_do_reconnect()` hook is a no-op by default and this service does not override it. The result: the call stays up, the user keeps talking, and the agent never hears another word, with no further errors emitted. Handle `on_connection_error` and rebuild or end the call, and set `keepalive_timeout` so idle sockets are not dropped in the first place.

**Configuration.** `vad_signals` is a `Settings` field, not a constructor argument; passing it to the constructor is silently ignored. Set `vad_signals=True` to use Sarvam’s server-side VAD, and add no Pipecat VAD.

Never leave `vad_signals` unset while also omitting a VAD analyzer. Pipecat then sends `flush_signal=true` at connect, but `flush()` is only called in response to a `VADUserStoppedSpeakingFrame`, produced only by a Pipecat VAD. With no VAD anywhere the flush never fires and nothing is transcribed.

With `vad_signals=True` the service calls `broadcast_interruption()` unconditionally on every speech-start. There is no `should_interrupt` here, so Pipecat’s min-words gating cannot prevent a barge-in; sensitivity is controlled only by ten fine-grained server-side VAD parameters (`positive_speech_threshold`, `negative_speech_threshold`, `min_speech_frames`, `first_turn_min_speech_frames`, `negative_frames_count`, `negative_frames_window`, `start_speech_volume_threshold`, `interrupt_min_speech_frames`, `pre_speech_pad_frames`, `num_initial_ignored_frames`). Of these, `interrupt_min_speech_frames` is the barge-in dial. All are `None` by default, sent only when set, and changing any one reconnects the socket.

`mode` is a constructor argument and init-only. `SarvamSTTService` does not accept `should_interrupt`.

**The turn-end wait.** Because `SarvamSTTService` never sets `finalized=True`, the STT safety net in `SpeechTimeoutUserTurnStopStrategy` never short-circuits. With a Pipecat VAD and default settings that costs `1.17 - 0.2 = 0.97 s` on every turn, and the turn requires _both_ timers, so lowering `user_speech_timeout` below 0.97 changes nothing. With `vad_signals=True` and the External strategies, the wait does not arise; this is the main latency reason to migrate.

**Language.** Auto-detect is the literal string `"unknown"`, not an omitted parameter. When Sarvam returns no `language_code` and none is configured, the transcript is stamped `Language.HI_IN` unconditionally, and unrecognized codes also fall back to `HI_IN`, so English-first deployments see transcripts labelled Hindi. Pin `language` if you branch on `TranscriptionFrame.language`. Language on the frame is `frame.language`, not `result.get("language")`.

**Request IDs.** `request_id` is not on transcript frames for `SarvamSTTService`. Today the service sets `result=message.dict()`, and that dict is empty (`{}`) even when `message.data.transcript` is still present (for example `"yes"`). Language on the frame is `frame.language` (it falls back to `hi-IN` if unset). The raw SDK object is the `DEBUG Received response: {message}` log line; if `request_id` is only there, it never reaches an observer. Copying the Section 8 observer, even with nested fallbacks, will not invent the id.

Do not mix the two shapes in one snippet. Realtime (`SarvamRealtimeSTTService`, Section 8) is flat `result["request_id"]` (the session id from `session.begin`). Legacy, if Pipecat dumps the SDK object properly (`model_dump(exclude_unset=False)` or copying `message.data.request_id` onto `result`), is nested `result["data"]["request_id"]`. Until that dump is fixed, there is no `frame.result` path for the id. Server-side metrics (`processing_latency`, `audio_duration`) and `language_probability` live on that SDK object too, not on `frame.result`.

* * *

## 12\. Production tuning playbook

Work in this order. Fixing them out of order produces misleading measurements.

  1. **Turn on metrics.** `PipelineParams(enable_metrics=True, enable_usage_metrics=True)` plus `MetricsLogObserver()`. The biggest wins here are inaudible until you measure them.
  2. **Pass explicit turn strategies.** The defaults are a local ML model keyed to VAD frames Sarvam never emits. Use `External*` (Section 2).
  3. **Confirm no Pipecat VAD.** Keep `endpointing="vad"` and add no `SileroVADAnalyzer`. This also keeps `ttfs_p99_latency` inert.
  4. **Decide the barge-in model.** `should_interrupt=True` for lowest-latency barge-in, or `should_interrupt=False` plus `MinWordsUserTurnStartStrategy(min_words=2..3, use_interim=True)` when false interruptions from acknowledgements are the complaint.
  5. **Tune endpointing.** Lower `ExternalUserTurnStopStrategy.timeout` toward 0.2. Raise `min_speech_duration_ms` until coughs and clicks stop triggering turns, and `threshold` against background noise. All of these update live, so you can iterate mid-call.
  6. **Cut time-to-first-audio.** Set TTS `model="bulbul:v4-flash"` (or v3) explicitly, lower `min_buffer_size` to 15–25, and align TTS `sample_rate` with the transport on the constructor. Keep STT `stream_type="fast"`.
  7. **Set the safety nets.** `user_idle_timeout` 8 to 15 s with a re-prompt handler, `user_turn_stop_timeout` 2.5 to 3.0, and `keepalive_timeout` 30 to 45 s if your encoding is `linear16`.
  8. **Handle fatal STT errors** (Section 9) before launch, not after the first mid-call outage.
  9. **Prompt for speech** (Section 10).



Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)[MCP ServerNext](https://docs.sarvam.ai/api/developer-tools/mcp)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


