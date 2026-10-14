# Sarvam TTS API — தமிழில் முழு வழிகாட்டி (End-to-End, பல பயன்பாடுகள்)

இந்த வழிகாட்டி `docs/` கிராலில் இருந்து எடுத்த உண்மைகளின் அடிப்படையில் எழுதப்பட்டது. எல்லா உதாரணமும் தமிழ் (`ta-IN`) மையம்.

## 1. அடிப்படை: ஒரு கோரிக்கை (curl)

```bash
export SARVAM_API_KEY="உங்கள்_கீ"
curl -X POST https://api.sarvam.ai/text-to-speech \
  -H "api-subscription-key: $SARVAM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "வணக்கம்! இன்று நாம் ஏஐ பற்றிப் பேசுவோம்.",
    "target_language_code": "ta-IN",
    "speaker": "vijay_ta_narration",
    "model": "bulbul:v4-flash",
    "pace": 1.0,
    "speech_sample_rate": 22050,
    "output_audio_codec": "mp3"
  }' -o பதில்.json
# பதில்: {"request_id":"…","audios":["<base64>"]} → base64-ஐ டிகோட் செய்து mp3 ஆக்கவும்
```

Python-இல்:

```python
import json, base64, urllib.request
def tts(text, speaker="vijay_ta_narration", model="bulbul:v4-flash", pace=1.0, key="YOUR_KEY"):
    payload = {"text": text, "target_language_code": "ta-IN", "speaker": speaker,
               "model": model, "pace": pace, "speech_sample_rate": 22050,
               "output_audio_codec": "mp3"}
    req = urllib.request.Request("https://api.sarvam.ai/text-to-speech",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"api-subscription-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return base64.b64decode(json.loads(r.read())["audios"][0])
open("/tmp/வணக்கம்.mp3", "wb").write(tts("வணக்கம் மக்களே!"))
```

## 2. குரல் தேர்வு (v4-flash தமிழ் — 4 குரல், நாலும் ஆண்)

| குரல் | பாணி | எதற்கு |
|---|---|---|
| `aravind_ta_suspense` | சஸ்பென்ஸ் | திரில்லர், கிரைம் கதை |
| `vijay_ta_narration` | விவரிப்பு | ஆடியோபுக், செய்தி, கல்வி |
| `aravind_ta_ads` | விளம்பரம் | விளம்பரம், பாட்காஸ்ட் இணை தொகுப்பாளர் |
| `gokul_ta_narration` | விவரிப்பு | ஆவணப்படம், மாற்று கதைசொல்லி |

பெண் குரல் வேண்டுமானால் v3 (`ishita`, `ritu`) — ஆனால் தரம் v4-ஐ விட குறைவு. ஒரு கோரிக்கை 2500 எழுத்துக்கு மிகாமல் பார்த்துக்கொள்ளவும்; நீண்டதை ~1900 எழுத்துத் துண்டுகளாக்கி `ffmpeg concat` செய்யவும்.

## 3. பல பயன்பாடுகள் (Use Cases)

### அ) ஆடியோபுக் / கதை (இந்த ரெபோவில் செய்தது)
- குரல்: `aravind_ta_suspense`, pace 0.88–0.95. பேச்சுத் தமிழில் எழுதவும் (`இருக்கு`, `யாருடா`) — அச்சுத் தமிழ் புத்தக வாசிப்பு போல ஒலிக்கும்.
- உதாரணம்: `tamil_thriller_story.txt` + `generate_tts.py` (36.9 நிமிடம்).

### ஆ) பாட்காஸ்ட் / FM ஷோ (இந்த ரெபோவில் செய்தது)
- இரண்டு குரல், ஒவ்வொரு டயலாக் turn-உம் தனி API call. pace 1.0–1.05, உற்சாகமான சொற்கள் (`செம`, `அடடே`).
- உதாரணம்: `ai_podcast_script_v4.txt` + `generate_podcast_v4.py` (24.5 நிமிடம்).

### இ) சினிமா டப்பிங் உதவி
- கதாபாத்திரத்துக்கு ஒரு குரல்; உணர்ச்சிக் காட்சிக்கு pace குறைவு (0.85), சண்டை/வேகக் காட்சிக்கு pace அதிகம் (1.1). SFX/பின்னணி இசையை `ffmpeg amix`-இல் கலக்கவும் (உதாரணம்: `generate_cinematic.py`).

### ஈ) IVR / வாடிக்கையாளர் சேவை
- குரல்: `aravind_ta_ads` (தெளிவு), pace 1.0. குட்டி வாக்கியம், நிறுத்தற்குறி சரியாக: `"வணக்கம்! உங்கள் கணக்கு எண்ணை அழுத்தவும்."` ஒவ்வொரு மெனுவும் தனி mp3.

### உ) கல்வி (பாடம், டுட்டோரியல்)
- குரல்: `vijay_ta_narration`, pace 0.9. கடின சொல்லை எழுத்து வடிவில் (`இ எம் ஐ` போல) எழுதினால் உச்சரிப்பு சரியாகும். Pronunciation Dictionary API-யில் நிரந்தரமாகச் சேமிக்கலாம்.

### ஊ) செய்தி வாசிப்பு
- குரல்: `gokul_ta_narration`, pace 1.0. எண்களைத் தமிழில் எழுதவும் (`பத்து கோடி` — `10,00,00,000` என எழுத வேண்டாம்; 4 இலக்கத்துக்கு மேல் கமா அவசியம்: `10,000`).

### எ) விளம்பரம்
- குரல்: `aravind_ta_ads`, pace 1.05–1.1, குட்டி வரி (30–60 சொல்), முடிவில் கடை பெயர் + தொலைபேசி.

## 4. இயல்பாக ஒலிக்க 5 விதி

1. **பேச்சுத் தமிழில் எழுதுக** — ஏடுதான் உச்சரிப்பு. 2. **நிறுத்தற்குறி = மூச்சு** — கமா, முற்றுப்புள்ளி தாராளமாக. 3. **ஒரு கதாபாத்திரம் = ஒரு குரல்**, மாற்றாதே. 4. **pace**: கதை 0.88, உரையாடல் 1.0, விளம்பரம் 1.05. 5. **சோதனை வரி**: நீண்ட ஸ்கிரிப்டுக்கு முன் ஒரு வரி சோதித்துப் பார் (மாற்றுச் செலவு குறையும்).

## 5. பிழைகள்

- `400`: speaker பெயர் தவறு (சிறிய எழுத்தில் எழுதவும்; v3 பெயர் v4-இல் செல்லாது) அல்லது 2500 எழுத்து மீறல்.
- `403`: கீ தவறு/இல்லை (401 அல்ல, 403 வரும்!). - `429`: வேகக் கட்டுப்பாடு — 3 வினாடி இடைவெளியுடன் மீண்டும் முயலவும் (இந்த ரெபோ ஸ்கிரிப்டுகளில் retry உள்ளது).
