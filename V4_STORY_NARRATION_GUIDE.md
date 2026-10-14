# bulbul:v4-flash — Capabilities In-Depth + Perfect Story Narration End-to-End

Source: `docs/api/api-guides-tutorials/text-to-speech/best-practices.md` (v4 Flash guide) + `docs/api-reference/text-to-speech/convert.md`, every claim below live-verified against the API unless marked.

## PART 1 — Every v4-flash capability

**What it is:** Sarvam's low-latency TTS tier for interactive workloads (voice agents, IVR) that also serves offline file generation. Same model on **three transports**:

| Transport | Path | Returns | Max rate | Use when |
|---|---|---|---|---|
| REST (single response) | `POST /text-to-speech` | JSON, base64 in `audios[]` | **48 kHz** | Offline files, broadcast-grade audio (our story files) |
| HTTP streaming | `POST /text-to-speech/stream` | Chunked audio bytes, playable before completion | 24 kHz | Someone is waiting for the first word (agents, IVR, LLM read-aloud) |
| WebSocket | `wss://api.sarvam.ai/text-to-speech/ws` | `{"type":"audio"}` base64 chunks, one connection, many utterances | 24 kHz | High-volume sequential synthesis (`config` → `text` → `flush`, `ping` keep-alive) |

**Languages (11):** `hi-IN en-IN bn-IN gu-IN kn-IN ml-IN mr-IN od-IN pa-IN ta-IN te-IN`. (`en-US` rejected — use `en-IN`.) Strong on Indian names/places/cultural terms. Code-mixing (Tanglish etc.) works when each language is written in **its own script** (Tamil in Tamil script, English in Latin). Romanised Tamil degrades quality.

**Voice roster:** 83 personas, **224 speaker IDs live**. ID format = `voice_language_style` (e.g. `aravind_ta_suspense`); same voice under multiple styles = different energy, so switching *style* beats switching voice. Tamil coverage is narrow: **4 IDs, all male** (`gokul_ta_narration`, `aravind_ta_ads`, `aravind_ta_suspense`, `vijay_ta_narration`) — verified live; docs pages showing `vetri_*` are stale and return 400. Omit `speaker` and you get default `shubh_enhi_ads`.

**Prosody (all live-verified on v4-flash):**

| Param | Range | Default | Notes |
|---|---|---|---|
| `pace` | 0.5–2.0 | 1.0 | 0.8–0.9 narration/EdTech; 1.0 conversation; 1.1–1.2 news/IVR |
| `pitch` | −0.5–0.5 | 0.0 | Deeper/sharper, identity preserved. ±0.1–0.2 for brand-tone tweaks |
| `loudness` | 0.1–2.5 | 1.0 | Gain at source — prefer over downstream amplification |
| `enable_preprocessing` | bool | — | Normalises numbers/dates/currency/mixed-script; with it ON, do NOT hand-expand numbers — model rules beat yours. Large numbers need locale grouping (`10,000`) |

⚠️ The API-reference page claims pitch/loudness are v2-only — **stale**. Live test (this repo, 2026-10-14): `pitch:-0.1 + loudness:1.1 + enable_preprocessing:true + 44100Hz` → HTTP 200. Trust the v4 best-practices guide + live test, not the reference page.

**Codecs/rates:** `wav mp3 flac aac` (wav+mp3 on WebSocket). Rates 8k (telephony) / 16k (agents) / 22.05k (general) / 24k (streaming max) / **32k·44.1k·48k REST-only** (broadcast/podcast/studio). Don't request 48 kHz for an 8 kHz gateway — pure transfer cost.

**Limits:** 2500 chars/request — **chunk on sentence boundaries** (mid-sentence splits strand intonation = audible seams). No SSML on v4. `request_id` in every response — log it for support. Errors: 400 bad speaker/param (often lists valid speakers), 403 bad key (note: 403, not 401), 429 throttle → exponential backoff. Unknown speaker returns 400 with the live list — that's how we discovered the real Tamil roster.

## PART 2 — Using v4 for story narration (why our 36.9-min file works)

1. **One persona for the whole story** (`aravind_ta_suspense`): consistency across 30+ min is what makes it feel like one narrator, not 15 clips. Never switch personas mid-story.
2. **Spoken Tamil, not book Tamil:** the model reads what you write — `கொட்டிட்டு இருக்கு` sounds native, `கொட்டிக் கொண்டிருந்தது` sounds like a newsreader. Write dialogue the way actors speak it.
3. **Punctuation is direction:** `,` short pause · `.`/`।` sentence end (use `।` for Indic-script sentence ends) · `!` emphasis · `…` sparing hesitation · line break = paragraph pause. Under-punctuated text rushes.
4. **Pace as emotion:** narration 0.85–0.9 (weight), dialogue 0.95–1.05 (life), climax 1.05–1.1. Automate it: dialogue-marker regex (`? ! என்றார் என்றாள் கேட்டார்…`) → faster chunk, else slow.
5. **Pitch −0.1 for the thriller narrator:** deeper without changing identity. Small moves (±0.1–0.2); audition bigger ones.
6. **Preprocessing ON** for dates/money/phone-numbers in the plot; locale-grouped digits (`10,000`).
7. **REST @ 44.1/48 kHz mp3/flac** for the master (broadcast-grade); 22.05 kHz is fine for drafts.
8. **Test line first:** one sentence through the full chain before 15 chunks — catches mispronunciation at 1/15th the cost.
9. **Resume-safe chunking:** skip existing chunk files; concat with `ffmpeg -f concat -safe 0 -c copy`; verify with `ffprobe` duration.
10. **SFX are not Sarvam's job:** `[SFX: thunder]` cues in script → synthesize/collect wavs → `adelay` to cue timestamps → `amix` under dialogue (see `generate_cinematic.py`).

## PART 3 — The perfected half-hour (this repo)

`generate_tts_perfect.py` → `tamil_thriller_half_hour_perfect.mp3`. Same beloved story, upgraded chain:

- 44100 Hz mp3 (was 22050), `enable_preprocessing: true` (was off)
- `pitch: -0.1` deeper narrator (was 0.0), `loudness: 1.0`
- Per-chunk pace: 0.88 narration / 1.0 dialogue-detected (was flat 0.92)
- Same sentence-boundary 15 chunks, retries + resume, ffmpeg concat + ffprobe verify

Compare with the original `tamil_thriller_half_hour.mp3` and keep whichever your ears prefer — both are committed.
