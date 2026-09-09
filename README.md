# 🌐 EchoTranslator

> **Instantly translate text and audio across 40+ languages — powered by Google AI**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Translate](https://img.shields.io/badge/Google%20Translate-API-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🚀 Live Demo

🔗 **[Try it live → tahaniazi786-echotranslator-app-0bve94.streamlit.app](https://tahaniazi786-echotranslator-app-0bve94.streamlit.app)**

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Text Translation** | Translate any text between 40+ languages instantly |
| 🎤 **Audio Translation** | Upload audio → auto-transcribe → translate |
| 🔊 **Text-to-Speech** | Listen to your translation in the target language |
| 🔁 **Swap Languages** | One-click swap between source and target |
| 🌍 **40+ Languages** | English, Hindi, Arabic, French, Spanish, Urdu, Japanese, and more |
| 🎵 **Audio Formats** | Supports WAV, MP3, OGG, FLAC, M4A uploads |

---

## 🖥️ Screenshot

> _A dark, modern UI with gradient accents and glassmorphism design_

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Entire project |
| **UI Framework** | Streamlit | Web interface — no HTML/CSS/JS needed |
| **Translation** | googletrans 4.0.0-rc1 | Google Translate (free) |
| **Speech-to-Text** | SpeechRecognition + Google STT API | Audio → Text |
| **Text-to-Speech** | gTTS (Google Text-to-Speech) | Text → MP3 audio |
| **Audio Processing** | pydub + ffmpeg | Convert MP3/OGG/FLAC → WAV |

---

## 📁 Project Structure

```
EchoTranslator/
│
├── app.py              ← Main Streamlit app (UI + all logic)
├── requirements.txt    ← Python dependencies
├── packages.txt        ← System packages (ffmpeg for Streamlit Cloud)
└── README.md           ← You are here
```

---

## ⚙️ How It Works

### 📝 Text Translation
```
User types text
      ↓
googletrans sends to Google Translate API
      ↓
Translated text displayed
      ↓
gTTS converts translation → MP3 audio
      ↓
User can listen in browser
```

### 🎤 Audio Translation
```
User uploads audio file (WAV/MP3/OGG/FLAC/M4A)
      ↓
pydub + ffmpeg converts to WAV (if needed)
      ↓
SpeechRecognition → Google STT API → transcript
      ↓
googletrans translates transcript
      ↓
gTTS converts to audio → playback in browser
```

---

## 🌍 Supported Languages

<details>
<summary>Click to see all 40+ languages</summary>

| Language | Code | Language | Code |
|---|---|---|---|
| Auto Detect | auto | Italian | it |
| Afrikaans | af | Japanese | ja |
| Arabic | ar | Korean | ko |
| Bengali | bn | Malay | ms |
| Chinese (Simplified) | zh-CN | Marathi | mr |
| Chinese (Traditional) | zh-TW | Norwegian | no |
| Croatian | hr | Persian | fa |
| Czech | cs | Polish | pl |
| Danish | da | Portuguese | pt |
| Dutch | nl | Punjabi | pa |
| English | en | Romanian | ro |
| Finnish | fi | Russian | ru |
| French | fr | Spanish | es |
| German | de | Swahili | sw |
| Greek | el | Swedish | sv |
| Gujarati | gu | Tamil | ta |
| Hebrew | iw | Telugu | te |
| Hindi | hi | Thai | th |
| Hungarian | hu | Turkish | tr |
| Indonesian | id | Ukrainian | uk |
| Urdu | ur | Vietnamese | vi |
| Welsh | cy | | |

</details>

---

## 🔧 Local Setup

### Prerequisites
- Python 3.10+
- ffmpeg installed on your system

### 1. Clone the repository
```bash
git clone https://github.com/Tahaniazi786/EchoTranslator.git
cd EchoTranslator
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install ffmpeg (for audio conversion)

**Windows:**
```bash
winget install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎉

---

## ☁️ Deploy on Streamlit Cloud

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Click **Deploy** — Streamlit Cloud handles `requirements.txt` and `packages.txt` automatically ✅

---

## 📦 Dependencies

```txt
streamlit>=1.32.0
googletrans==4.0.0-rc1
SpeechRecognition>=3.10.0
gTTS>=2.4.0
pydub>=0.25.1
httpx==0.13.3
```

> ⚠️ `httpx==0.13.3` must stay pinned — `googletrans 4.0.0-rc1` is incompatible with newer httpx versions.

---

## 🐛 Known Limitations

- Google STT API (free tier) may have rate limits on heavy usage
- Some languages are not supported by gTTS for audio output — audio will be skipped silently
- `googletrans` is an unofficial Google Translate wrapper — may occasionally be rate-limited

---

## 👨‍💻 Developer

**Mohd Taha Salim**  
AIML Intern @ Safcurl Technologies  
GitHub: [@Tahaniazi786](https://github.com/Tahaniazi786)

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<div align="center">
  Made with ❤️ using Streamlit · Powered by Google AI
</div>
