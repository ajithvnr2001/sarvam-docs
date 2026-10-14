#!/usr/bin/env python3
"""Mirchi-style Tamil AI podcast TTS: two RJs, natural conversation.
MADDY -> rohan (bulbul:v3), DIVYA -> ishita (bulbul:v3), ta-IN.
Each dialogue turn = one API call (natural turn-taking). Concat to half-hour mp3.
"""
import json, base64, os, re, time, urllib.request, urllib.error, subprocess

API_KEY = os.environ.get("SARVAM_API_KEY", "sk_mxoszip9_h5c89evYeP2WiiIAUBOOOJ5t")
BASE = "/data/opencode/sarvam"
SCRIPT = os.path.join(BASE, "ai_podcast_script.txt")
CHUNK_DIR = os.path.join(BASE, "podcast_chunks")
FINAL_MP3 = os.path.join(BASE, "ai_podcast_half_hour.mp3")
os.makedirs(CHUNK_DIR, exist_ok=True)

VOICES = {
    "MADDY": {"speaker": "rohan", "model": "bulbul:v3", "pace": 1.0, "temperature": 0.75},
    "DIVYA": {"speaker": "ishita", "model": "bulbul:v3", "pace": 1.02, "temperature": 0.75},
}

raw = open(SCRIPT, encoding="utf-8").read()
turns = []
for line in raw.strip().split("\n"):
    line = line.strip()
    if not line:
        continue
    m = re.match(r"^(MADDY|DIVYA)\s*:\s*(.+)$", line)
    if m:
        turns.append((m.group(1), m.group(2).strip()))
print(f"Turns: {len(turns)}, chars: {sum(len(t) for _, t in turns)}", flush=True)

def call_tts(text, voice, retries=4):
    payload = {"text": text, "target_language_code": "ta-IN",
               "speaker": voice["speaker"], "model": voice["model"],
               "pace": voice["pace"], "temperature": voice["temperature"],
               "speech_sample_rate": 22050, "output_audio_codec": "mp3"}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last = None
    for a in range(retries):
        try:
            req = urllib.request.Request("https://api.sarvam.ai/text-to-speech", data=data,
                headers={"api-subscription-key": API_KEY, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())["audios"][0]
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode()[:300]}"
            print(f"  retry {a+1}: {last}", flush=True)
            time.sleep(3 * (a + 1))
    raise RuntimeError(last)

files = []
for i, (who, text) in enumerate(turns):
    out = os.path.join(CHUNK_DIR, f"turn_{i+1:03d}_{who.lower()}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print(f"[{i+1}/{len(turns)}] {who} exists skip ({len(text)}ch)", flush=True)
        files.append(out)
        continue
    print(f"[{i+1}/{len(turns)}] {who}: {text[:60]}...", flush=True)
    b64 = call_tts(text, VOICES[who])
    open(out, "wb").write(base64.b64decode(b64))
    files.append(out)
    time.sleep(0.5)

lst = os.path.join(CHUNK_DIR, "list.txt")
with open(lst, "w") as f:
    for p in files:
        f.write(f"file '{p}'\n")
# concat + add short 0.35s silence between turns for natural FM pause
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", FINAL_MP3], check=True)
print("FINAL:", FINAL_MP3, os.path.getsize(FINAL_MP3), flush=True)
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", FINAL_MP3], capture_output=True, text=True)
dur = float(r.stdout.strip())
print(f"Duration: {dur:.1f}s = {dur/60:.1f} min", flush=True)
print("DONE", flush=True)
