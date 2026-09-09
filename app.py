import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import io
import tempfile
import os

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EchoTranslator",
    page_icon="🌐",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE MAPS
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect":             "auto",
    "Afrikaans":               "af",
    "Arabic":                  "ar",
    "Bengali":                 "bn",
    "Chinese (Simplified)":    "zh-CN",
    "Chinese (Traditional)":   "zh-TW",
    "Croatian":                "hr",
    "Czech":                   "cs",
    "Danish":                  "da",
    "Dutch":                   "nl",
    "English":                 "en",
    "Finnish":                 "fi",
    "French":                  "fr",
    "German":                  "de",
    "Greek":                   "el",
    "Gujarati":                "gu",
    "Hebrew":                  "iw",
    "Hindi":                   "hi",
    "Hungarian":               "hu",
    "Indonesian":              "id",
    "Italian":                 "it",
    "Japanese":                "ja",
    "Korean":                  "ko",
    "Malay":                   "ms",
    "Marathi":                 "mr",
    "Norwegian":               "no",
    "Persian":                 "fa",
    "Polish":                  "pl",
    "Portuguese":              "pt",
    "Punjabi":                 "pa",
    "Romanian":                "ro",
    "Russian":                 "ru",
    "Spanish":                 "es",
    "Swahili":                 "sw",
    "Swedish":                 "sv",
    "Tamil":                   "ta",
    "Telugu":                  "te",
    "Thai":                    "th",
    "Turkish":                 "tr",
    "Ukrainian":               "uk",
    "Urdu":                    "ur",
    "Vietnamese":              "vi",
    "Welsh":                   "cy",
}

TARGET_LANGUAGES = {k: v for k, v in LANGUAGES.items() if k != "Auto Detect"}

GTTS_CODE_MAP = {
    "zh-CN": "zh",
    "zh-TW": "zh-TW",
    "iw":    "iw",
}

SR_LANG_MAP = {
    "af": "af-ZA", "ar": "ar-SA", "bn": "bn-IN",
    "zh-CN": "zh-CN", "zh-TW": "zh-TW", "hr": "hr-HR",
    "cs": "cs-CZ", "da": "da-DK", "nl": "nl-NL",
    "en": "en-US", "fi": "fi-FI", "fr": "fr-FR",
    "de": "de-DE", "el": "el-GR", "gu": "gu-IN",
    "iw": "iw-IL", "hi": "hi-IN", "hu": "hu-HU",
    "id": "id-ID", "it": "it-IT", "ja": "ja-JP",
    "ko": "ko-KR", "ms": "ms-MY", "mr": "mr-IN",
    "no": "no-NO", "fa": "fa-IR", "pl": "pl-PL",
    "pt": "pt-PT", "pa": "pa-IN", "ro": "ro-RO",
    "ru": "ru-RU", "es": "es-ES", "sw": "sw-KE",
    "sv": "sv-SE", "ta": "ta-IN", "te": "te-IN",
    "th": "th-TH", "tr": "tr-TR", "uk": "uk-UA",
    "ur": "ur-PK", "vi": "vi-VN", "cy": "cy-GB",
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def translate_text(text: str, source: str, target: str) -> str:
    """Translate using deep-translator — Python 3.13 compatible."""
    try:
        if not text or not text.strip():
            return ""
        src = "auto" if source == "auto" else source.lower()
        tgt = target.lower()
        if src == tgt:
            return text
        result = GoogleTranslator(source=src, target=tgt).translate(text.strip())
        if not result or not result.strip():
            return "⚠️ Translation returned empty. Please try again."
        return result
    except Exception as exc:
        err = str(exc).lower()
        if "translation not found" in err or "not valid" in err:
            return "⚠️ Could not translate. Try shorter text or a different language pair."
        if "connect" in err or "network" in err or "timeout" in err:
            return "⚠️ Network error — check your internet connection."
        return "⚠️ Translation failed. Please try again in a moment."


def text_to_speech(text: str, lang_code: str):
    """Return BytesIO MP3 or None."""
    try:
        gtts_lang = GTTS_CODE_MAP.get(lang_code, lang_code)
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except Exception:
        return None


def audio_to_text(uploaded_file, src_lang_code: str):
    """Transcribe uploaded audio. Returns (transcript, error)."""
    recognizer = sr.Recognizer()
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    wav_path = tmp_path
    try:
        if ext != ".wav":
            try:
                from pydub import AudioSegment
                seg = AudioSegment.from_file(tmp_path)
                wav_path = tmp_path.replace(ext, ".wav")
                seg.export(wav_path, format="wav")
            except Exception:
                return None, "Could not convert audio. Please upload a WAV file or ensure ffmpeg is installed."
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
        sr_lang = SR_LANG_MAP.get(src_lang_code, "en-US")
        transcript = recognizer.recognize_google(audio_data, language=sr_lang)
        return transcript, None
    except sr.UnknownValueError:
        return None, "Could not understand the audio. Please speak clearly."
    except sr.RequestError as exc:
        return None, f"Speech Recognition error: {exc}"
    except Exception as exc:
        return None, f"Unexpected error: {exc}"
    finally:
        for p in {tmp_path, wav_path}:
            try:
                os.unlink(p)
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for k, v in {
    "text_result": "",
    "audio_original": "",
    "audio_translated": "",
    "audio_tts": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────────────────────────────────────
st.title("🌐 EchoTranslator")
st.caption("Instantly translate text & audio across 40+ languages — powered by Google AI")
st.divider()

tab_text, tab_audio = st.tabs(["📝 Text Translation", "🎤 Audio Translation"])

# ══ TAB 1 — TEXT TRANSLATION ══════════════════════════════════════════════════
with tab_text:
    st.subheader("📝 Text Translation")

    col1, col2 = st.columns(2)
    with col1:
        src_lang_name = st.selectbox("Source Language", list(LANGUAGES.keys()), key="src_lang")
    with col2:
        tgt_lang_name = st.selectbox("Target Language", list(TARGET_LANGUAGES.keys()),
                                      index=list(TARGET_LANGUAGES.keys()).index("Spanish"),
                                      key="tgt_lang")

    src_code = LANGUAGES[src_lang_name]
    tgt_code = TARGET_LANGUAGES[tgt_lang_name]

    src_text = st.text_area("Enter text to translate", height=150, placeholder="Type your text here…")

    if st.button("Translate Text", type="primary"):
        if src_text and src_text.strip():
            with st.spinner("Translating…"):
                st.session_state["text_result"] = translate_text(src_text, src_code, tgt_code)
        else:
            st.warning("Please enter some text first.")

    if st.session_state["text_result"]:
        st.subheader("Translation")
        st.success(st.session_state["text_result"])
        audio_buf = text_to_speech(st.session_state["text_result"], tgt_code)
        if audio_buf:
            st.subheader("🔊 Listen")
            st.audio(audio_buf, format="audio/mp3")

# ══ TAB 2 — AUDIO TRANSLATION ═════════════════════════════════════════════════
with tab_audio:
    st.subheader("🎤 Audio Translation")

    col1, col2 = st.columns(2)
    with col1:
        audio_src_name = st.selectbox("Audio Language (spoken in)", list(LANGUAGES.keys()),
                                       index=list(LANGUAGES.keys()).index("English"),
                                       key="audio_src")
    with col2:
        audio_tgt_name = st.selectbox("Translate To", list(TARGET_LANGUAGES.keys()),
                                       index=list(TARGET_LANGUAGES.keys()).index("Hindi"),
                                       key="audio_tgt")

    audio_src_code = LANGUAGES[audio_src_name]
    audio_tgt_code = TARGET_LANGUAGES[audio_tgt_name]

    uploaded = st.file_uploader("Upload audio file", type=["wav", "mp3", "ogg", "flac", "m4a"])

    if uploaded:
        st.audio(uploaded)
        if st.button("Transcribe & Translate", type="primary"):
            with st.spinner("Transcribing audio…"):
                transcript, err = audio_to_text(uploaded, audio_src_code)
            if err:
                st.error(f"⚠️ {err}")
                st.session_state["audio_original"] = ""
                st.session_state["audio_translated"] = ""
                st.session_state["audio_tts"] = None
            else:
                st.session_state["audio_original"] = transcript
                with st.spinner("Translating…"):
                    translated = translate_text(transcript, audio_src_code, audio_tgt_code)
                st.session_state["audio_translated"] = translated
                st.session_state["audio_tts"] = text_to_speech(translated, audio_tgt_code)

        if st.session_state["audio_original"]:
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Transcribed ({audio_src_name})")
                st.info(st.session_state["audio_original"])
            with col2:
                st.subheader(f"Translation ({audio_tgt_name})")
                st.success(st.session_state["audio_translated"])
                if st.session_state["audio_tts"]:
                    st.subheader("🔊 Listen")
                    st.audio(st.session_state["audio_tts"], format="audio/mp3")

st.divider()
st.caption("Made with ❤️ using Streamlit · Powered by Google AI")
