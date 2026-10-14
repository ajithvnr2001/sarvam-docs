#!/usr/bin/env python3
"""5-min cinematic Tamil thriller demo: multi-voice TTS + word-triggered SFX.
Voices: NARRATOR vijay_ta_narration (v4), VIVEK aravind_ta_suspense (v4),
        SUNDARI ishita (v3, only female Tamil voice). SFX synthesized, mixed via ffmpeg."""
import json, base64, os, re, time, urllib.request, urllib.error, subprocess
import numpy as np

API_KEY = os.environ.get("SARVAM_API_KEY", "sk_y3gx56hh_XELWhduPsxqfA7kZ2WZWVj35")
BASE = "/data/opencode/sarvam"
SCRIPT = os.path.join(BASE, "story_cinematic_script.txt")
WORK = os.path.join(BASE, "cinematic_chunks")
SFXD = os.path.join(BASE, "sfx")
FINAL = os.path.join(BASE, "story_5min_cinematic.mp3")
SR = 22050
os.makedirs(WORK, exist_ok=True)
os.makedirs(SFXD, exist_ok=True)

VOICES = {
    "NARRATOR": {"speaker": "vijay_ta_narration", "model": "bulbul:v4-flash"},
    "VIVEK": {"speaker": "aravind_ta_suspense", "model": "bulbul:v4-flash"},
    "GOPI": {"speaker": "aravind_ta_ads", "model": "bulbul:v4-flash"},
}

def wav(path, y):
    import wave
    y = np.clip(y, -1, 1)
    pcm = (y * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())

# ---- procedural SFX ----
rng = np.random.default_rng(7)
def noise(n): return rng.standard_normal(n)
def lowpass(x, k=64):
    k = np.ones(k) / k
    return np.convolve(x, k, mode="same")

rain = lowpass(noise(SR * 8)) * 0.5
rain = rain / np.abs(rain).max() * 0.35
wav(f"{SFXD}/rain.wav", rain)

t = np.arange(SR * 2.5) / SR  # thunder: low boom decay + rumble
th = np.exp(-3 * t) * np.sin(2 * np.pi * (55 - 20 * t) * t) + 0.4 * np.exp(-6 * t) * lowpass(noise(len(t)), 256)
th = th / np.abs(th).max() * 0.9
wav(f"{SFXD}/thunder.wav", th)

n = SR * 3  # wind: slow-modulated filtered noise
tt = np.arange(n) / SR
wind = lowpass(noise(n), 512) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * tt))
wind = wind / np.abs(wind).max() * 0.4
wav(f"{SFXD}/wind.wav", wind)

n = int(SR * 1.2)  # door creak: rising squeak (FM sweep) + thump
tt = np.arange(n) / SR
f = 300 + 500 * tt
creak = 0.3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-1.5 * tt)
wav(f"{SFXD}/door_creak.wav", creak)

n = int(SR * 0.7)  # door slam: low thump + click
tt = np.arange(n) / SR
slam = np.exp(-12 * tt) * np.sin(2 * np.pi * 90 * tt) + 0.5 * np.exp(-40 * tt) * noise(n)
slam = slam / np.abs(slam).max() * 0.9
wav(f"{SFXD}/door_slam.wav", slam)

n = SR * 2  # phone ring: dual-tone trill 440+480, on/off
tt = np.arange(n) / SR
gate = (tt % 1.0) < 0.5
ring = gate * 0.4 * (np.sin(2 * np.pi * 440 * tt) + np.sin(2 * np.pi * 480 * tt))
wav(f"{SFXD}/phone_ring.wav", ring * 0.5)

n = int(SR * 1.6)  # footsteps: 4 thuds
st = np.zeros(n)
for i in range(4):
    s = int(i * SR * 0.4)
    e = min(n, s + int(SR * 0.12))
    m = e - s
    st[s:e] += np.exp(-30 * np.arange(m) / SR) * np.sin(2 * np.pi * 70 * np.arange(m) / SR)
wav(f"{SFXD}/footsteps.wav", st / np.abs(st).max() * 0.7)
print("SFX ready", flush=True)

# ---- parse + TTS ----
turns = []
for line in open(SCRIPT, encoding="utf-8").read().strip().split("\n"):
    line = line.strip()
    if not line: continue
    who, rest = line.split("|", 1)
    pace_m = re.match(r"pace=([\d.]+)\|(.*)", rest, re.S)
    pace, text = float(pace_m.group(1)), pace_m.group(2)
    cues = re.findall(r"\[SFX:\s*([a-z_]+)\]", text)
    clean = re.sub(r"\[SFX:\s*[a-z_]+\]", "", text).strip()
    turns.append({"who": who, "pace": pace, "text": clean, "cues": [c for c in cues if c not in ("sob", "gasp")]})
print(f"Turns: {len(turns)}, chars: {sum(len(t['text']) for t in turns)}", flush=True)

def call_tts(text, who, pace, retries=4):
    v = VOICES[who]
    payload = {"text": text, "target_language_code": "ta-IN", "speaker": v["speaker"],
               "model": v["model"], "pace": pace, "speech_sample_rate": SR, "output_audio_codec": "mp3"}
    if "temperature" in v: payload["temperature"] = v["temperature"]
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

def dur_of(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", p], capture_output=True, text=True)
    return float(r.stdout.strip())

files, cue_events = [], []
cursor = 0.0
GAP = 0.6
for i, t in enumerate(turns):
    out = os.path.join(WORK, f"line_{i+1:02d}_{t['who'].lower()}.mp3")
    if not (os.path.exists(out) and os.path.getsize(out) > 5000):
        print(f"[{i+1}/{len(turns)}] {t['who']} p={t['pace']} cues={t['cues']}", flush=True)
        open(out, "wb").write(base64.b64decode(call_tts(t["text"], t["who"], t["pace"])))
        time.sleep(0.5)
    else:
        print(f"[{i+1}/{len(turns)}] {t['who']} skip", flush=True)
    d = dur_of(out)
    off = 0.0
    for c in t["cues"]:
        if c in ("rain_start", "rain_heavy"):
            continue
        cue_events.append((c, cursor + off))
        off += 0.3
    files.append(out)
    cursor += d + GAP

# concat dialogue
lst = os.path.join(WORK, "list.txt")
with open(lst, "w") as f:
    for p in files:
        f.write(f"file '{p}'\n")
dlg = os.path.join(WORK, "dialogue.mp3")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", dlg], check=True)
total = dur_of(dlg)
print(f"Dialogue: {total:.1f}s", flush=True)

# mix: dialogue + rain bed (vol 0.18, loop) + wind bed (0.12) + one-shot events
inp = ["-i", dlg, "-stream_loop", "-1", "-i", f"{SFXD}/rain.wav", "-stream_loop", "-1", "-i", f"{SFXD}/wind.wav"]
ev_inputs, ev_filters = [], []
for j, (c, ts) in enumerate(cue_events):
    fn = {"thunder": "thunder.wav", "door_creak": "door_creak.wav", "door_slam": "door_slam.wav",
          "phone_ring": "phone_ring.wav", "footsteps": "footsteps.wav", "wind": "wind.wav"}.get(c)
    if not fn: continue
    ev_inputs += ["-i", f"{SFXD}/{fn}"]
    ev_filters.append(f"[{3+j}:a]adelay={int(ts*1000)}|{int(ts*1000)},volume=0.9[ev{j}]")
base = "[0:a]volume=1.0[dlg];[1:a]volume=0.16[rain];[2:a]volume=0.10[wind];[dlg][rain]amix=inputs=2:duration=first:dropout_transition=0[m1];[m1][wind]amix=inputs=2:duration=first:dropout_transition=0[m2]"
if ev_filters:
    mix_ins = "[m2]" + "".join(f"[ev{j}]" for j in range(len(ev_filters)))
    filt = base + ";" + ";".join(ev_filters) + f";{mix_ins}amix=inputs={len(ev_filters)+1}:duration=first:dropout_transition=0,volume=1.1[out]"
else:
    filt = base + ";[m2]volume=1.1[out]"
cmd = ["ffmpeg", "-y"] + inp + ev_inputs + ["-filter_complex", filt, "-map", "[out]", "-t", f"{total:.2f}", FINAL]
print("MIX:", " ".join(cmd[:6]), "...", flush=True)
subprocess.run(cmd, check=True)
print("FINAL:", FINAL, os.path.getsize(FINAL), flush=True)
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", FINAL], capture_output=True, text=True)
d = float(r.stdout.strip())
print(f"Duration: {d:.1f}s = {d/60:.2f} min", flush=True)
print("DONE", flush=True)
