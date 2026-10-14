# How Everything Was Achieved End-to-End (Build Log)

This file records exactly how the Tamil TTS deliverables in this repo were built — every step, command, and decision. Reproduce it top to bottom and you get the same outputs.

## Phase 0 — Read the docs (source of truth)

Base: `/data/opencode/sarvam/` — a full crawl of `https://docs.sarvam.ai/` (1090 pages, `docs/`).

1. `docs/README` + `guide_code/README.md` → understood crawl layout.
2. `docs/creative-text-to-speech.md`, `creative-tts-generate.md`, `creative-tts-best-practices.md` → Content-Studio UI docs (dashboard, not API — noted and set aside).
3. `docs/api-reference/text-to-speech/convert.md` → the real contract: `POST https://api.sarvam.ai/text-to-speech`, header `api-subscription-key`, body `{text (≤2500), language_code/speaker/pace/pitch/loudness/speech_sample_rate/enable_preprocessing/model/output_audio_codec/temperature/dict_id}`, response `{request_id, audios:[base64]}`.
4. `docs/api-reference/authentication.md` → auth header; failures are **403**, not 401.
5. `docs/api/api-guides-tutorials/text-to-speech/voices.md` → Tamil shortlist; `best-practices.md` (v4 Flash guide) → punctuation table, preprocessing, chunking, 48 kHz REST, pitch/loudness on v4.
6. Grep for `ta-IN` across `docs/` → confirmed language code + Tamil-capable speakers.

## Phase 1 — Live-verify every claim (trust, then verify)

Docs contradicted each other (reference page: pitch/loudness v2-only; v4 guide: supported on v4; `vetri_*` vs `aravind_*` Tamil names). Each was settled with a tiny live call before building on it:

```bash
# 1. Tamil voices that actually work
python3 -c "… POST … speaker=vetri_ta_suspense …"   # → 400, live list has aravind_ta_*
python3 -c "… speaker=aravind_ta_suspense, model=bulbul:v4-flash …"  # → 200 OK
python3 -c "… speaker=rohan / ishita, model=bulbul:v3 …"             # → 200 OK
# 2. Full v4 roster: sent speaker=xxx, parsed 400 error → 224 IDs, 4 Tamil, all male
# 3. Speech rate: 180 Tamil chars → 13.95 s ⇒ ~770 chars/min ⇒ ~23,000 chars ≈ 30 min
# 4. v4 extras: pitch −0.1 + loudness 1.1 + enable_preprocessing + 44100 Hz → 200 OK (reference page was stale)
```

Findings locked in: `target_language_code: ta-IN`; v4 Tamil = 4 male IDs; v3 needed for female; ~770 chars/min; pitch/loudness/preprocessing/44.1 kHz all live on v4.

## Phase 2 — Half-hour thriller (single voice, v4)

1. Authored `tamil_thriller_story.txt` (~28,199 chars, 10 chapters, Rajesh Kumar style: DSP Vivek, locked room, 2nd murder, twist + open ending) in 3 appended parts.
2. `generate_tts.py`: sentence-boundary chunks (~1900 chars, 15 chunks) → per-chunk POST (`aravind_ta_suspense`, pace 0.92, 22050 Hz mp3) with retries + skip-existing resume → base64-decode → `ffmpeg -f concat -safe 0 -c copy` → `ffprobe` verify.
3. Result: `tamil_thriller_half_hour.mp3`, 2214 s = **36.9 min**. Ran as background job (~15 chunks).

## Phase 3 — Half-hour FM podcast (two voices)

1. Authored `ai_podcast_script.txt` (~20k chars, `MADDY:`/`DIVYA:` turns, Mirchi-style AI banter).
2. First cut `generate_podcast.py`: v3 `rohan` + `ishita` (only way to get male+female) → 24.5 min. User judged v3 quality poor → verified v4 has no female Tamil voice → user chose v4 two-male.
3. Adapted script (`DIVYA→SURYA`, gender refs fixed, dup lines dropped) → `generate_podcast_v4.py` (`vijay_ta_narration` + `aravind_ta_ads`, 107 turns, one API call per turn) → `ai_podcast_half_hour_v4.mp3`, 24.5 min.

## Phase 4 — Cinematic demo (multi-voice + word-triggered SFX)

Sarvam makes voices, not SFX — so SFX are post-production:
1. `story_cinematic_script.txt`: `SPEAKER|pace=X|[SFX: name] text…` (Narrator/Vivek/Gopi — Gopi rewritten male so all-v4; spoken Tamil for native accent).
2. `generate_cinematic.py`: per-turn TTS (own voice/pace) → procedural SFX via numpy (`sfx/`: rain bed, thunder, wind, door creak/slam, phone ring, footsteps) → ffmpeg: concat dialogue, looped low beds, `adelay` one-shots to cue timestamps, `amix` → `story_5min_cinematic.mp3` (~3 min).

## Phase 5 — Rank + guides

- `RANKING_HALF_HOUR.md`: thriller 🥇 BEST (only true 30 min+, consistent v4 suspense voice), podcast-v4 🥈, podcast-v3 🥉.
- `README_TTS.md`: setup, contract, 3 recipes, file map. `TAMIL_API_GUIDE.md`: Tamil guide, 7 use cases. `V4_STORY_NARRATION_GUIDE.md`: v4 capabilities + perfecting recipe.

## Phase 6 — Perfect + push to private GitHub

1. `generate_tts_perfect.py` (44.1 kHz, preprocessing, pitch −0.1, dialogue-regex auto-pace) → `tamil_thriller_half_hour_perfect.mp3` (34.5 min).
2. Git + push (private repo), exact commands:

```bash
cd /data/opencode/sarvam
git add <guides, scripts, mp3s, chunks, logs>   # mp3s <100 MB each, no LFS needed
git commit -m "…"
# create private repo (once) — token from user, never printed:
curl -X POST -H "Authorization: Bearer $GH_TOK" https://api.github.com/user/repos \
  -d '{"name":"tamil-sarvam-tts","private":true}'
git remote add delivery "https://USER:TOKEN@github.com/ajithvnr2001/tamil-sarvam-tts.git"
git push -u delivery HEAD:main
# verify: GET /repos/ajithvnr2001/tamil-sarvam-tts/contents/ lists all files
# hygiene: git remote remove delivery  (removes stored token; code stays on GitHub)
```

Repo: **`ajithvnr2001/tamil-sarvam-tts`** (private), branch `main`. Total ~250 MB (docs crawl + audio). Pushed in 3 commits; every push verified via the contents API.

## Reproduce from zero (cheat sheet)

```bash
export SARVAM_API_KEY="KEY"
cd /data/opencode/sarvam
python3 generate_tts.py          # 36.9-min thriller
python3 generate_podcast_v4.py   # 24.5-min podcast
python3 generate_cinematic.py    # ~3-min cinematic + SFX
python3 generate_tts_perfect.py  # 34.5-min perfected thriller
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <file>.mp3
```
