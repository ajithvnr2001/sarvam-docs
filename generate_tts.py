#!/usr/bin/env python3
"""Tamil thriller TTS via Sarvam API end-to-end (docs: docs/api-reference/text-to-speech/convert.md).
POST https://api.sarvam.ai/text-to-speech, header api-subscription-key.
Chunks story <2000 chars (limit 2500), decodes base64 audios, concats with ffmpeg.
"""
import json, base64, os, re, sys, time, urllib.request, urllib.error, subprocess

API_KEY = os.environ.get("SARVAM_API_KEY", "sk_mxoszip9_h5c89evYeP2WiiIAUBOOOJ5t")
BASE = "/data/opencode/sarvam"
STORY = os.path.join(BASE, "tamil_thriller_story.txt")
CHUNK_DIR = os.path.join(BASE, "tts_chunks")
FINAL_MP3 = os.path.join(BASE, "tamil_thriller_half_hour.mp3")
FINAL_WAV = os.path.join(BASE, "tamil_thriller_half_hour.wav")
LOG = os.path.join(BASE, "tts_log.json")

MODEL = "bulbul:v4-flash"
SPEAKER = "aravind_ta_suspense"  # Tamil suspense voice (v4-flash Tamil: gokul_ta_narration, aravind_ta_ads, aravind_ta_suspense, vijay_ta_narration)
LANG = "ta-IN"
PACE = 0.92
MAX_CHARS = 1900

os.makedirs(CHUNK_DIR, exist_ok=True)

text = open(STORY, encoding="utf-8").read()
# Split into sentences (Tamil uses . ? ! । + newline). Keep delimiters.
sentences = re.split(r'(?<=[\.!?।\n])\s+', text)
chunks, cur = [], ""
for s in sentences:
    s = s.strip()
    if not s:
        continue
    if len(cur) + len(s) + 1 <= MAX_CHARS:
        cur = (cur + " " + s).strip()
    else:
        if cur:
            chunks.append(cur)
        # very long sentence fallback: hard split
        while len(s) > MAX_CHARS:
            chunks.append(s[:MAX_CHARS])
            s = s[MAX_CHARS:]
        cur = s
if cur:
    chunks.append(cur)

print(f"Total chars: {len(text)}, chunks: {len(chunks)}", flush=True)
for i, c in enumerate(chunks):
    print(f"  chunk {i+1}: {len(c)} chars", flush=True)

def call_tts(t, retries=4):
    payload = {
        "text": t,
        "target_language_code": LANG,
        "speaker": SPEAKER,
        "model": MODEL,
        "pace": PACE,
        "speech_sample_rate": 22050,
        "output_audio_codec": "mp3",
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_err = None
    for a in range(retries):
        try:
            req = urllib.request.Request(
                "https://api.sarvam.ai/text-to-speech", data=data,
                headers={"api-subscription-key": API_KEY, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read())
                return d["audios"][0]
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:500]
            last_err = f"HTTP {e.code}: {body}"
            print(f"    retry {a+1}: {last_err}", flush=True)
            time.sleep(3 * (a + 1))
    raise RuntimeError(last_err)

results = []
for i, ch in enumerate(chunks):
    out = os.path.join(CHUNK_DIR, f"chunk_{i+1:02d}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print(f"[{i+1}/{len(chunks)}] exists, skip", flush=True)
        results.append(out)
        continue
    print(f"[{i+1}/{len(chunks)}] synthesizing {len(ch)} chars...", flush=True)
    b64 = call_tts(ch)
    open(out, "wb").write(base64.b64decode(b64))
    print(f"[{i+1}/{len(chunks)}] saved {out} ({os.path.getsize(out)} bytes)", flush=True)
    results.append(out)
    time.sleep(1)

# Concat with ffmpeg
lst = os.path.join(CHUNK_DIR, "list.txt")
with open(lst, "w", encoding="utf-8") as f:
    for p in results:
        f.write(f"file '{p}'\n")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", FINAL_MP3], check=True)
print("FINAL MP3:", FINAL_MP3, os.path.getsize(FINAL_MP3), flush=True)
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", FINAL_MP3],
                   capture_output=True, text=True)
dur = float(r.stdout.strip())
print(f"Duration: {dur:.1f}s = {dur/60:.1f} min", flush=True)
json.dump({"chunks": len(chunks), "duration_s": dur, "files": results}, open(LOG, "w"), indent=2)
print("DONE", flush=True)
