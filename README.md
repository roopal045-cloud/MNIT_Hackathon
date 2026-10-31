<div align="center">

# 🌾 DHARA (धारा)

### **Ask by voice in Hindi or Marathi. Get a sourced answer from official documents. In an emergency, skip the AI and call the right number.**

![Status](https://img.shields.io/badge/status-hackathon%20prototype-orange)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector%20search-purple)
![Languages](https://img.shields.io/badge/languages-Hindi%20%7C%20Marathi-green)
![License](https://img.shields.io/badge/license-MIT-green)
![Hackathon](https://img.shields.io/badge/MNIT-Hackathon-red)

<!-- 🎬 REPLACE with your banner screenshot or GIF -->


**[▶ Watch the 3-minute demo](ADD_VIDEO_LINK_HERE)**

</div>

---

## 🚨 The Problem

Government scheme rules, crop-insurance deadlines and emergency steps are written in English or formal Hindi. Many rural citizens cannot read them, and a missed deadline means lost money. **Example:** crop insurance (PMFBY) requires the farmer to report field damage **within 72 hours**. Most farmers never hear this in time.

## 💡 The Solution

**DHARA** is a voice-first assistant. A farmer speaks a question in **Hindi or Marathi** and hears a short, simple answer in the same language. Every answer **shows the official document, page and sentence it came from.** If the documents don't contain the answer, DHARA **refuses politely** and sends the user to the panchayat office, a CSC centre or the Kisan Call Centre.

> **Demo story:** Sunita farms 2 acres of cotton near Nashik. Her field was flooded or hit by hail. She asks in Marathi, and DHARA tells her she must report within **72 hours**, with the exact line and page from the PMFBY guidelines.

## 🏆 Why DHARA Stands Out

| | |
|---|---|
| 🔒 **Grounded, not guessed** | The AI only rewords text found in official PDFs. It never answers from its own memory. |
| 📎 **Verifiable** | Every answer carries a document name, page number and the matching sentence. |
| 🛑 **Knows when to say no** | Weak search match or AI failure means a polite refusal, never a made-up answer. |
| 🚑 **Emergency path has no AI** | Fire, snakebite and similar phrases bypass search and AI. They return a pre-written reply, a one-tap call button and nearby hospitals. |

## ✨ Key Features

- 🎙️ **Voice in, voice out:** speech-to-text with Whisper, spoken replies with gTTS, in Hindi and Marathi.
- 📚 **Answers from official documents:** searches PMFBY crop insurance, PM-Kisan and PMMVY guidelines (508 indexed chunks) and shows the source page and snippet.
- 🚨 **Instant emergency mode:** 7 emergency types (fire, accident, snakebite, labour/bleeding, pesticide poisoning, heart/breathing, flood), detected in Hindi and Marathi with no AI delay.
- 🏥 **Nearest hospitals:** sorted by distance from the user's location, with a Google Maps link. Location is used for one request and never stored.
- 👩‍⚕️ **ASHA worker mode:** health-worker role gets answers as 2 to 3 short lines.
- 📶 **Low-data mode:** shorter spoken replies for weak connections.
- 🧪 **Prototype screens (clearly labelled):** application draft + checklist, SMS mode for feature phones, and a panchayat dashboard with **simulated** counts.

## 🏗️ Architecture & Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vanilla HTML, CSS and JavaScript (no build step), browser MediaRecorder for the mic, mock-data fallback if the backend is offline |
| **Backend** | Python 3.13, FastAPI, Uvicorn |
| **Speech-to-text** | faster-whisper (`small` model, CPU, int8) |
| **Search (RAG)** | ChromaDB + `intfloat/multilingual-e5-base` embeddings (Hindi, Marathi, English) |
| **Answer wording** | Google Gemini (`google-genai`), with retries and a backup model |
| **Text-to-speech** | gTTS |
| **Data** | 3 official PDFs, emergency JSON (7 types), Nashik hospital JSON, PMFBY rules JSON |

### 🔄 How It Works

```
 🎙️ Voice / ⌨️ Text  (Hindi or Marathi)
          │
          ▼
   ┌──────────────┐   speech → text (Whisper)
   │   FastAPI    │
   │   POST /ask  │
   └──────┬───────┘
          │
          ▼
 ┌─────────────────────┐   YES   ┌──────────────────────────────────┐
 │ Emergency phrase?   │────────►│ Pre-written reply (NO AI, NO RAG)│
 └─────────┬───────────┘         │ number + call button + safety    │
           │ NO                  │ line + nearest hospitals         │
           ▼                     └──────────────────────────────────┘
 ┌─────────────────────┐
 │ Search official PDFs│  ChromaDB + multilingual-e5
 │ (score ≥ 0.70?)     │
 └─────────┬───────────┘
     weak  │  strong
     ┌─────┴─────┐
     ▼           ▼
 Polite     Gemini rewords ONLY the found text
 refusal    (simple words, 3 short sentences)
     │           │
     └─────┬─────┘
           ▼
  🔊 gTTS voice + 📎 source (document · page · sentence)
```

<details>
<summary>📁 <b>Project structure</b></summary>

```
MNIT_Hackathon/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, /audio files
│   │   ├── models.py            # API contract (Pydantic)
│   │   ├── routers/             # ask, emergency, draft*, sms*, panchayat*
│   │   └── services/            # asr, rag, llm, tts, emergency
│   └── requirements.txt
├── data/
│   ├── raw/                     # official PDFs (PMFBY, PM-Kisan, Mission Shakti/PMMVY)
│   ├── ingest.py                # builds the search index
│   ├── emergency/               # emergency.json + VERIFICATION.md
│   ├── hospitals/               # nashik_fallback.json
│   ├── rules/                   # PMFBY rules + eligibility engine
│   └── testset/                 # test phrases and personas
├── frontend/                    # index.html, app.js, screens.js, styles.css
├── demo-script.md
└── .env.example
```
<sub>* prototype / simulated</sub>
</details>

## 🚀 Quick Start

### Prerequisites
- Python 3.13 (3.10+ should work)
- Git
- A free **Gemini API key** from Google AI Studio
- Internet connection (Gemini and gTTS need it)
- About 1 GB free disk space for the AI models

### 1. Clone and install

```bash
git clone https://github.com/roopal045-cloud/MNIT_Hackathon.git
cd MNIT_Hackathon/backend
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```
```bash
# macOS / Linux
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
```

### 2. Configure `.env`

Create a file named `backend/.env` (it is git-ignored). Use `.env.example` as the template:

```env
GEMINI_API_KEY=your_key_here
# Optional overrides
# GEMINI_MODEL=
# GEMINI_FALLBACK_MODEL=
# WHISPER_MODEL=small
```

### 3. Build the search index (one time)

```bash
python ../data/ingest.py
```
> ⏳ The first run downloads the ~470 MB embedding model and can take a while. It creates `data/processed/chroma`.

### 4. Run the backend

```bash
python -m uvicorn app.main:app --reload
```
Open **http://127.0.0.1:8000/docs** for the interactive API.
> The first question loads the search model and can take up to a minute. Later ones are fast.

### 5. Run the frontend

In a second terminal:

```bash
cd MNIT_Hackathon/frontend
python -m http.server 5500
```
Open **http://localhost:5500**. The app talks to the backend at the address in `frontend/config.js` (`API_BASE_URL`, default `http://127.0.0.1:8000`).

## 📡 API Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ask` | POST (multipart) | Audio **or** text question → sourced answer, or emergency reply, or polite refusal |
| `/emergency` | POST (JSON) | Emergency number, call link, safety line and nearest hospitals |
| `/draft` | POST | *Prototype:* application checklist |
| `/sms` | POST | *Prototype:* feature-phone keyword replies (`FASAL`, `EMERGENCY`) |
| `/panchayat/stats` | GET | *Simulated:* topic counts for the dashboard |

<details>
<summary><b>POST /ask</b> · fields and real example response</summary>

**Form fields:** `audio` (file) or `text`, `language` (`hi` | `mr`), `mode` (`normal` | `low_data`), `role` (`farmer` | `asha`)

```json
{
  "transcript": "माझ्या कापसाच्या पिकाचे पुरामुळे किंवा गारपिटीमुळे नुकसान झाले आहे",
  "language": "mr",
  "is_emergency": false,
  "answer_text": "पिकाचे नुकसान झाल्यास 72 तासांच्या आत विमा कंपनी किंवा संबंधित वित्तीय संस्थेकडे माहिती देणे आवश्यक आहे. ...",
  "audio_url": "/audio/26acc222a6848137.mp3",
  "source": {
    "doc": "Revised_Operational_Guidelines.pdf",
    "page": "55",
    "snippet": "21.5.4.1 Time and method of reporting the loss/claims • Immediate intimation (within 72 hours) by the insured farmer ..."
  },
  "confidence": 0.848,
  "refused": false,
  "offer_application": "crop_damage"
}
```
</details>

<details>
<summary><b>POST /emergency</b> · request and response shape</summary>

```json
// Request
{ "language": "mr", "type": "snakebite", "lat": 19.99, "lon": 73.78 }

// Response
{
  "type": "snakebite",
  "number": "108",
  "call_uri": "tel:108",
  "message_text": "...",
  "audio_url": null,
  "safety_line": "...",
  "hospitals": [ { "name": "...", "distance_km": 0.7, "maps_url": "https://www.google.com/maps/search/?api=1&query=..." } ]
}
```
`lat` and `lon` are optional. Without them, distances show as unknown.
</details>

## 🛡️ Safety & Responsible AI

- **No medical diagnosis and no pesticide dosage.** The AI is instructed never to give either.
- **No Aadhaar or ID numbers** are collected anywhere.
- **Nothing is submitted** to any government system. Drafts are previews only.
- **Emergency numbers** were checked against official `.gov.in` pages (see `data/emergency/VERIFICATION.md`). Safety-line wording and Hindi/Marathi phrasing are **pending native-speaker review**, and the app is not for real-world emergency use until that is done.
- Prototype features are always labelled **"prototype"** or **"simulated"**.

## 🗺️ Roadmap

- [ ] 🧑‍🌾 **More languages:** Tamil is already planned in the UI, followed by other Indian languages
- [ ] 📄 **Real application PDFs:** generate the claim draft from the user's spoken answers
- [ ] 📱 **Live SMS gateway:** run the same rules over real SMS for feature phones
- [ ] 🏥 **Verified hospital directory** for more districts, with official phone numbers
- [ ] 📊 **Real panchayat dashboard** built from anonymised question counts
- [ ] ✅ **Native-speaker review** of all Hindi/Marathi emergency text

## 👥 Team

**Team Cipher** · Built for the MNIT Hackathon

## 📜 License

Released under the [MIT License](LICENSE). © 2026 Team Cipher

<div align="center">

**DHARA: answer first, then help the user act.** 🌾

</div>
