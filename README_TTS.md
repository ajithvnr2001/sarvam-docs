# Tamil Sarvam TTS — End-to-End (Private)

Everything in this repo section was built end-to-end from `/data/opencode/sarvam/docs/` (Sarvam API docs crawl) using the Sarvam Text-to-Speech REST API. Audio + scripts + builders all live in this same folder.

## Outputs (the actual deliverables)

| File | What | Duration | Model / Voice |
|---|---|---|---|
| `tamil_thriller_half_hour.mp3` | Crime thriller `நள்ளிரவில் ஒலித்த கடைசி அழைப்பு` (Rajesh Kumar style, DSP Vivek) | 36.9 min | `bulbul:v4-flash` / `aravind_ta_suspense` |
| `tamil_thriller_story.txt` | Full thriller script (~28,199 chars) | — | — |
| `ai_podcast_half_hour_v4.mp3` | Mirchi-FM style AI fun podcast, RJs Maddy + Surya | 24.5 min | `bulbul:v4-flash` / `vijay_ta_narration` + `aravind_ta_ads` |
| `ai_podcast_script_v4.txt` | Podcast script (107 turns) | — | — |
| `ai_podcast_half_hour.mp3` | Same podcast, male+female version (older) | 24.5 min | `bulbul:v3` / `rohan` + `ishita` |
| `story_5min_cinematic.mp3` | Cinematic thriller demo, spoken-Tamil + SFX (rain, thunder, wind, door, phone, footsteps) | ~3 min | 3× `bulbul:v4-flash` |
| `story_cinematic_script.txt` | Cinematic script with `[SFX: …]` cues | — | — |

See `RANKING_HALF_HOUR.md` for which half-hour is ranked best and why. See `TAMIL_API_GUIDE.md` (தமிழில்) for API usage across use cases.

## 1. Prerequisites

```bash
python3 --version   # 3.8+
ffmpeg -version     # for concat + SFX mix
pip install numpy   # only for cinematic SFX synthesis
```

No Sarvam SDK needed — everything below uses plain HTTPS (`urllib` / `curl`).

## 2. API key setup (never hardcode)

```bash
export SARVAM_API_KEY="YOUR_KEY"
```

Every request sends the header:

```
api-subscription-key: YOUR_KEY
```

(Auth failures return HTTP **403**, not 401, per `docs/api-reference/authentication.md`.)

## 3. Core API contract (from `docs/api-reference/text-to-speech/convert.md`)

```
POST https://api.sarvam.ai/text-to-speech
Content-Type: application/json
api-subscription-key: KEY
```

Minimal Tamil request:

```bash
curl -X POST https://api.sarvam.ai/text-to-speech \
  -H "api-subscription-key: $SARVAM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "வணக்கம்! இது ஒரு சோதனை.",
    "target_language_code": "ta-IN",
    "speaker": "aravind_ta_suspense",
    "model": "bulbul:v4-flash",
    "pace": 0.95,
    "speech_sample_rate": 22050,
    "output_audio_codec": "mp3"
  }' | python3 -c "import json,base64,sys; open('/tmp/t.mp3','wb').write(base64.b64decode(json.load(sys.stdin)['audios'][0]))"
```

Response is JSON: `{ "request_id": "…", "audios": ["<base64 mp3/wav>"] }` — **decode base64 before use**.

### Hard limits / verified findings

- Max **2500 chars** per request (v3/v4-flash). Chunk long scripts at ~1900 chars on sentence boundaries.
- `target_language_code: "ta-IN"` for Tamil (field is `target_language_code`, not `language_code`, on this endpoint).
- **v4-flash has only 4 Tamil voices, all male** (verified live against the API; docs still show old `vetri_*` names which the API rejects):
  `gokul_ta_narration`, `aravind_ta_ads`, `aravind_ta_suspense`, `vijay_ta_narration` (224 total v4 voices).
- Female Tamil voice exists only on v3 (`ishita`, `ritu`). So: all-v4 = male voices only; male+female = v3 (or mixed models).
- Emotion knobs on v3/v4: **speaker persona + `pace` (0.5–2.0) + `temperature` (0.01–1)**. `pitch`/`loudness` work **only on legacy v2** (`docs/.../how-to/adjust-the-tone.md`). Sarvam does **not** generate SFX/music — mix those in post (see §6).
- Measured Tamil rate: ~770 chars/min at pace ~0.95 → **~23,000 chars ≈ 30 min**.

## 4. Recipe A — single-voice long-form (the 36.9-min thriller)

```bash
python3 generate_tts.py
```

What `generate_tts.py` does: splits `tamil_thriller_story.txt` into ~1900-char sentence-safe chunks → `POST` each (`aravind_ta_suspense`, pace 0.92) with retries → base64-decodes to `tts_chunks/chunk_*.mp3` (skips existing, so re-runs resume) → `ffmpeg concat` → `tamil_thriller_half_hour.mp3` → `ffprobe` duration check. Write your own story in **spoken Tamil** (பேச்சுத் தமிழ்: `இருக்கு`, `யாருடா`, `பாக்க`) for native accent — formal written Tamil sounds bookish.

## 5. Recipe B — two-voice podcast (the 24.5-min FM show)

Script format (one turn per line):

```
MADDY: வணக்கம் மக்களே! …
SURYA: ஹாய்! …
```

```bash
python3 generate_podcast_v4.py   # v4, two male RJs
python3 generate_podcast.py      # v3, male+female (older)
```

Each turn = one API call (turn-taking = natural). Chunks in `podcast_v4_chunks/` resume on re-run. Concat with ffmpeg.

## 6. Recipe C — cinematic multi-voice + word-triggered SFX (the ~3-min demo)

Script format with cues:

```
NARRATOR|pace=0.88|[SFX: thunder] வானத்தையே கிழிக்கிற மாதிரி …
VIVEK|pace=1.0|கோபி! யாரும் உள்ள வராதீங்க! …
```

```bash
python3 generate_cinematic.py
```

Pipeline: parse turns + `[SFX: name]` cues → per-turn TTS (own voice/pace) → synthesize SFX procedurally (`sfx/*.wav`: rain bed, thunder, wind, door creak/slam, phone ring, footsteps) → `ffmpeg`: concat dialogue, loop rain/wind beds low, `adelay` one-shots to cue timestamps, `amix` → `story_5min_cinematic.mp3`. Add new SFX by adding a generator + cue name.

## 7. Verify anything

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <file>.mp3
ls -lh *.mp3
```

## 8. File map

```
tamil_thriller_story.txt  thriller script          generate_tts.py         Recipe A
tts_chunks/               thriller chunk mp3s      ai_podcast_script*.txt  podcast scripts
ai_podcast_half_hour*.mp3 podcast outputs          generate_podcast*.py    Recipe B
story_cinematic_script.txt cinematic script        generate_cinematic.py   Recipe C
cinematic_chunks/ sfx/    demo turns + SFX         *_run.log tts_log.json  run logs
RANKING_HALF_HOUR.md      half-hour ranking        TAMIL_API_GUIDE.md      தமிழ் API வழிகாட்டி
docs/                     Sarvam docs crawl (source of all API facts above)
```
