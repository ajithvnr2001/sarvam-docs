#!/usr/bin/env python3
"""Perfected half-hour thriller: v4-flash best practices.
44100Hz broadcast mp3, enable_preprocessing, pitch -0.1 (deeper narrator),
per-chunk pace (narration 0.88 / dialogue 1.0), sentence-boundary chunks."""
import json, base64, os, re, time, urllib.request, urllib.error, subprocess

API_KEY = os.environ.get("SARVAM_API_KEY", "sk_y3gx56hh_XELWhduPsxqfA7kZ2WZWVj35")
BASE = "/data/opencode/sarvam"
STORY = os.path.join(BASE, "tamil_thriller_story.txt")
WORK = os.path.join(BASE, "tts_perfect_chunks")
FINAL = os.path.join(BASE, "tamil_thriller_half_hour_perfect.mp3")
os.makedirs(WORK, exist_ok=True)

DIALOG_RE = re.compile(r"[?!]|என்றார்|என்றாள்|கேட்டார்|கேட்டாள்|சொன்னார்|சொன்னாள்|கத்தின|சிரித்த")

text = open(STORY, encoding="utf-8").read()
sents = re.split(r"(?<=[\.!?।\n])\s+", text)
chunks, cur = [], ""
for s in sents:
    s = s.strip()
    if not s: continue
    if len(cur) + len(s) + 1 <= 1900:
        cur = (cur + " " + s).strip()
    else:
        chunks.append(cur)
        cur = s
if cur: chunks.append(cur)
print(f"Chars: {len(text)}, chunks: {len(chunks)}", flush=True)

def pace_for(c):
    return 1.0 if DIALOG_RE.search(c) else 0.88

def call_tts(t, pace, retries=4):
    payload = {"text": t, "target_language_code": "ta-IN", "speaker": "aravind_ta_suspense",
               "model": "bulbul:v4-flash", "pace": pace, "pitch": -0.1, "loudness": 1.0,
               "enable_preprocessing": True, "speech_sample_rate": 44100,
               "output_audio_codec": "mp3"}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last = None
    for a in range(retries):
        try:
            req = urllib.request.Request("https://api.sarvam.ai/text-to-speech", data=data,
                headers={"api-subscription-key": API_KEY, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read())["audios"][0]
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode()[:300]}"
            print(f"  retry {a+1}: {last}", flush=True)
            time.sleep(4 * (a + 1))
    raise RuntimeError(last)

files = []
for i, ch in enumerate(chunks):
    out = os.path.join(WORK, f"pchunk_{i+1:02d}.mp3")
    p = pace_for(ch)
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print(f"[{i+1}/{len(chunks)}] skip pace={p}", flush=True)
        files.append(out); continue
    print(f"[{i+1}/{len(chunks)}] pace={p} chars={len(ch)}", flush=True)
    open(out, "wb").write(base64.b64decode(call_tts(ch, p)))
    files.append(out)
    time.sleep(1)

lst = os.path.join(WORK, "list.txt")
with open(lst, "w") as f:
    for pth in files: f.write(f"file '{pth}'\n")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", FINAL], check=True)
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
    "-of", "default=noprint_wrappers=1", FINAL], capture_output=True, text=True)
print(r.stdout.strip(), flush=True)
print("FINAL:", FINAL, os.path.getsize(FINAL), flush=True)
print("DONE", flush=True)
