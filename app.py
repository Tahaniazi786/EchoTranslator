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
    page_title="EchoTranslator | Multi-Language Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { font-family: 'Inter', sans-serif; box-sizing: border-box; }

/* ── APP BACKGROUND ── */
.stApp {
    background: radial-gradient(ellipse at top left, #1a0533 0%, #080818 40%, #0c1a3a 100%);
    min-height: 100vh;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 3rem 3rem; max-width: 1300px; }

/* ── HERO ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 900;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #a855f7 0%, #6366f1 40%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}
.hero-sub {
    color: #7c8db0;
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.01em;
}
.pill-row {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 50px;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    color: #94a3b8;
    font-weight: 500;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 5px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.35) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

/* ── LABELS ── */
.stSelectbox label, .stTextArea label, .stFileUploader label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 4px !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(100,80,200,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    transition: border 0.2s ease !important;
}
.stSelectbox > div > div:hover {
    border-color: rgba(124,58,237,0.6) !important;
}

/* ── TEXT AREA ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(100,80,200,0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 1rem !important;
    line-height: 1.65 !important;
    resize: vertical !important;
    transition: border 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.18) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #475569 !important; }

/* ── TRANSLATION OUTPUT ── */
.trans-output {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    color: #e2e8f0;
    font-size: 1rem;
    min-height: 180px;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
}
.trans-placeholder {
    color: #374151;
    font-style: italic;
}
.char-count {
    text-align: right;
    color: #475569;
    font-size: 0.72rem;
    margin-top: 5px;
    font-weight: 500;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.45) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── SWAP BUTTON ── */
div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    font-size: 1.4rem !important;
    padding: 0.4rem !important;
    border-radius: 50% !important;
    box-shadow: none !important;
    color: #94a3b8 !important;
}

/* ── FILE UPLOADER ── */
.stFileUploader > div {
    background: rgba(99,102,241,0.05) !important;
    border: 2px dashed rgba(99,102,241,0.35) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s ease !important;
}
.stFileUploader > div:hover {
    border-color: rgba(124,58,237,0.6) !important;
}

/* ── INFO / SUCCESS / ERROR BOXES ── */
.stSuccess { border-radius: 10px !important; }
.stInfo    { border-radius: 10px !important; }
.stError   { border-radius: 10px !important; }
.stWarning { border-radius: 10px !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.08) !important; margin: 1.5rem 0 !important; }

/* ── AUDIO PLAYER ── */
audio { width: 100%; border-radius: 10px; margin-top: 0.5rem; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #7c3aed !important; }

/* ── SECTION HEADERS ── */
.section-label {
    color: #7c8db0;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.lang-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    color: #a78bfa;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    margin-top: 3rem;
    color: #374151;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE DATA
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect":           "auto",
    "Afrikaans":             "af",
    "Arabic":                "ar",
    "Bengali":               "bn",
    "Chinese (Simplified)":  "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Croatian":              "hr",
    "Czech":                 "cs",
    "Danish":                "da",
    "Dutch":                 "nl",
    "English":               "en",
    "Finnish":               "fi",
    "French":                "fr",
    "German":                "de",
    "Greek":                 "el",
    "Gujarati":              "gu",
    "Hebrew":                "iw",
    "Hindi":                 "hi",
    "Hungarian":             "hu",
    "Indonesian":            "id",
    "Italian":               "it",
    "Japanese":              "ja",
    "Korean":                "ko",
    "Malay":                 "ms",
    "Marathi":               "mr",
    "Norwegian":             "no",
    "Persian":               "fa",
    "Polish":                "pl",
    "Portuguese":            "pt",
    "Punjabi":               "pa",
    "Romanian":              "ro",
    "Russian":               "ru",
    "Spanish":               "es",
    "Swahili":               "sw",
    "Swedish":               "sv",
    "Tamil":                 "ta",
    "Telugu":                "te",
    "Thai":                  "th",
    "Turkish":               "tr",
    "Ukrainian":             "uk",
    "Urdu":                  "ur",
    "Vietnamese":            "vi",
    "Welsh":                 "cy",
}

# Subset for target (no Auto Detect)
TARGET_LANGUAGES = {k: v for k, v in LANGUAGES.items() if k != "Auto Detect"}

# gTTS language code mapping (some codes differ from Google Translate)
GTTS_CODE_MAP = {
    "zh-CN": "zh",
    "zh-TW": "zh-TW",
    "iw":    "iw",
}

# SR language code mapping for Google Speech Recognition
SR_LANG_MAP = {
    "auto":  "en-US",
    "af":    "af-ZA",
    "ar":    "ar-SA",
    "bn":    "bn-BD",
    "zh-CN": "zh-CN",
    "zh-TW": "zh-TW",
    "hr":    "hr-HR",
    "cs":    "cs-CZ",
    "da":    "da-DK",
    "nl":    "nl-NL",
    "en":    "en-US",
    "fi":    "fi-FI",
    "fr":    "fr-FR",
    "de":    "de-DE",
    "el":    "el-GR",
    "gu":    "gu-IN",
    "iw":    "iw-IL",
    "hi":    "hi-IN",
    "hu":    "hu-HU",
    "id":    "id-ID",
    "it":    "it-IT",
    "ja":    "ja-JP",
    "ko":    "ko-KR",
    "ms":    "ms-MY",
    "mr":    "mr-IN",
    "no":    "no-NO",
    "pl":    "pl-PL",
    "pt":    "pt-BR",
    "ro":    "ro-RO",
    "ru":    "ru-RU",
    "es":    "es-ES",
    "sw":    "sw-KE",
    "sv":    "sv-SE",
    "ta":    "ta-IN",
    "te":    "te-IN",
    "th":    "th-TH",
    "tr":    "tr-TR",
    "uk":    "uk-UA",
    "ur":    "ur-PK",
    "vi":    "vi-VN",
    "cy":    "cy-GB",
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def translate_text(text: str, source: str, target: str) -> str:
    """Translate text using deep-translator (Google Translate backend, Python 3.13 compatible)."""
    try:
        # Guard: empty input
        if not text or not text.strip():
            return ""

        # Guard: same language — no translation needed
        src = "auto" if source == "auto" else source.lower()
        tgt = target.lower()
        if src == tgt:
            return text

        translator = GoogleTranslator(source=src, target=tgt)
        result = translator.translate(text.strip())

        # Guard: empty result
        if not result or not result.strip():
            return "⚠️ Translation returned empty. Please try again."

        return result

    except Exception as exc:
        err = str(exc).lower()
        if "translation not found" in err or "not valid" in err:
            return "⚠️ Could not translate. Try shorter text or a different language pair."
        if "connect" in err or "network" in err or "timeout" in err:
            return "⚠️ Network error — check your internet connection and try again."
        return "⚠️ Translation failed. Please try again in a moment."


def text_to_speech(text: str, lang_code: str):
    """Return BytesIO MP3 audio or None on failure."""
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
    """
    Transcribe uploaded audio to text.
    Returns (transcript: str | None, error: str | None).
    """
    recognizer = sr.Recognizer()
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    wav_path = tmp_path
    try:
        # Convert non-WAV formats using pydub (requires ffmpeg via packages.txt)
        if ext != ".wav":
            try:
                from pydub import AudioSegment
                seg = AudioSegment.from_file(tmp_path)
                wav_path = tmp_path.replace(ext, ".wav")
                seg.export(wav_path, format="wav")
            except Exception:
                return None, (
                    "Could not convert audio format. "
                    "Please upload a WAV file, or ensure ffmpeg is installed."
                )

        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        sr_lang = SR_LANG_MAP.get(src_lang_code, "en-US")
        transcript = recognizer.recognize_google(audio_data, language=sr_lang)
        return transcript, None

    except sr.UnknownValueError:
        return None, "Could not understand the audio. Try speaking more clearly or reducing background noise."
    except sr.RequestError as exc:
        return None, f"Speech Recognition service error: {exc}"
    except Exception as exc:
        return None, f"Unexpected error: {exc}"
    finally:
        for p in {tmp_path, wav_path}:
            try:
                os.unlink(p)
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
defaults = {
    "text_result":      "",
    "audio_original":   "",
    "audio_translated": "",
    "audio_tts":        None,
    "text_src_lang":    "Auto Detect",
    "text_tgt_lang":    "Spanish",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <h1 class="hero-title">🌐 EchoTranslator</h1>
    <p class="hero-sub">Instantly translate text &amp; audio across 40+ languages — powered by Google AI</p>
    <div class="pill-row">
        <span class="pill">📝 Text Translation</span>
        <span class="pill">🎤 Audio → Text → Translation</span>
        <span class="pill">🔊 Text-to-Speech Output</span>
        <span class="pill">40+ Languages</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_text, tab_audio = st.tabs(["📝  Text Translation", "🎤  Audio Translation"])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEXT TRANSLATION
# ═════════════════════════════════════════════════════════════════════════════
with tab_text:
    lang_col1, swap_col, lang_col2 = st.columns([5, 1, 5])

    with lang_col1:
        src_lang_name = st.selectbox(
            "Source Language",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(st.session_state["text_src_lang"]),
            key="sel_src",
        )

    with swap_col:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("⇄", key="swap_btn", help="Swap languages"):
            if src_lang_name != "Auto Detect":
                st.session_state["text_src_lang"] = st.session_state["text_tgt_lang"]
                st.session_state["text_tgt_lang"] = src_lang_name
                st.session_state["text_result"] = ""
                st.rerun()

    with lang_col2:
        tgt_lang_name = st.selectbox(
            "Target Language",
            options=list(TARGET_LANGUAGES.keys()),
            index=list(TARGET_LANGUAGES.keys()).index(st.session_state["text_tgt_lang"]),
            key="sel_tgt",
        )

    # Update session cache for language names
    st.session_state["text_src_lang"] = src_lang_name
    st.session_state["text_tgt_lang"] = tgt_lang_name

    src_code = LANGUAGES[src_lang_name]
    tgt_code = TARGET_LANGUAGES[tgt_lang_name]

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<p class="section-label">✏️ Input Text</p>', unsafe_allow_html=True)
        src_text = st.text_area(
            "Input Text",
            placeholder="Type or paste your text here…",
            height=220,
            label_visibility="collapsed",
            key="src_text_area",
        )
        if src_text:
            st.markdown(
                f'<p class="char-count">{len(src_text):,} characters</p>',
                unsafe_allow_html=True,
            )

        if st.button("🌐  Translate", key="translate_btn"):
            if src_text and src_text.strip():
                with st.spinner("Translating…"):
                    st.session_state["text_result"] = translate_text(src_text, src_code, tgt_code)
            else:
                st.warning("Please enter some text to translate.")

    with right_col:
        st.markdown(
            f'<p class="section-label">🌍 Translation '
            f'<span class="lang-badge">→ {tgt_lang_name}</span></p>',
            unsafe_allow_html=True,
        )
        result = st.session_state["text_result"]
        if result:
            st.markdown(f'<div class="trans-output">{result}</div>', unsafe_allow_html=True)
            # TTS playback
            tts_audio = text_to_speech(result, tgt_code)
            if tts_audio:
                st.markdown(
                    "<p class='section-label' style='margin-top:1rem'>🔊 Listen</p>",
                    unsafe_allow_html=True,
                )
                st.audio(tts_audio, format="audio/mp3")
        else:
            st.markdown(
                '<div class="trans-output">'
                '<span class="trans-placeholder">Your translation will appear here…</span>'
                "</div>",
                unsafe_allow_html=True,
            )

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — AUDIO TRANSLATION
# ═════════════════════════════════════════════════════════════════════════════
with tab_audio:
    a_col1, a_col2 = st.columns(2)

    with a_col1:
        audio_src_name = st.selectbox(
            "Audio Spoken Language",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index("English"),
            key="audio_src_lang",
        )

    with a_col2:
        audio_tgt_name = st.selectbox(
            "Translate To",
            options=list(TARGET_LANGUAGES.keys()),
            index=list(TARGET_LANGUAGES.keys()).index("Spanish"),
            key="audio_tgt_lang",
        )

    audio_src_code = LANGUAGES[audio_src_name]
    audio_tgt_code = TARGET_LANGUAGES[audio_tgt_name]

    st.markdown("<hr>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload an audio file",
        type=["wav", "mp3", "ogg", "flac", "m4a"],
        help="Supported: WAV, MP3, OGG, FLAC, M4A",
        key="audio_upload",
    )

    if uploaded:
        st.markdown('<p class="section-label" style="margin-top:1rem">▶️ Uploaded Audio</p>', unsafe_allow_html=True)
        st.audio(uploaded)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("🔤  Transcribe & Translate", key="transcribe_btn"):
            with st.spinner("🎧 Transcribing audio…"):
                transcript, err = audio_to_text(uploaded, audio_src_code)

            if err:
                st.error(f"⚠️ {err}")
                st.session_state["audio_original"]   = ""
                st.session_state["audio_translated"] = ""
                st.session_state["audio_tts"]        = None
            else:
                st.session_state["audio_original"] = transcript
                with st.spinner("🌐 Translating…"):
                    translated = translate_text(transcript, audio_src_code, audio_tgt_code)
                st.session_state["audio_translated"] = translated
                st.session_state["audio_tts"] = text_to_speech(translated, audio_tgt_code)

        # Display results
        if st.session_state["audio_original"]:
            st.markdown("<hr>", unsafe_allow_html=True)
            res_col1, res_col2 = st.columns(2)

            with res_col1:
                st.markdown(
                    f'<p class="section-label">📄 Transcribed Text '
                    f'<span class="lang-badge">{audio_src_name}</span></p>',
                    unsafe_allow_html=True,
                )
                st.info(st.session_state["audio_original"])

            with res_col2:
                st.markdown(
                    f'<p class="section-label">🌍 Translation '
                    f'<span class="lang-badge">{audio_tgt_name}</span></p>',
                    unsafe_allow_html=True,
                )
                st.success(st.session_state["audio_translated"])

                if st.session_state["audio_tts"]:
                    st.markdown('<p class="section-label" style="margin-top:0.8rem">🔊 Listen</p>', unsafe_allow_html=True)
                    st.audio(st.session_state["audio_tts"], format="audio/mp3")
    else:
        st.markdown("""
        <div style="
            text-align:center;
            padding: 3rem 2rem;
            background: rgba(99,102,241,0.04);
            border: 1px dashed rgba(99,102,241,0.2);
            border-radius: 14px;
            margin-top: 1rem;
        ">
            <div style="font-size:3rem;margin-bottom:0.7rem">🎤</div>
            <p style="color:#64748b;font-size:1rem;margin:0;font-weight:500">
                Upload an audio file above to get started
            </p>
            <p style="color:#374151;font-size:0.82rem;margin-top:0.4rem">
                Supports WAV · MP3 · OGG · FLAC · M4A
            </p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <hr>
    Made with ❤️ using <strong style="color:#7c3aed">Streamlit</strong> ·
    Powered by Google Translate &amp; Google Speech APIs
</div>
""", unsafe_allow_html=True)
