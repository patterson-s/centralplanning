import streamlit as st
import psycopg2
from audio_recorder_streamlit import audio_recorder
from datetime import datetime, timezone

LANGUAGES = ["en", "fr", "de"]
LANGUAGE_LABELS = {"en": "English", "fr": "Français", "de": "Deutsch"}
LANGUAGE_FLAGS = {"en": "🇬🇧", "fr": "🇫🇷", "de": "🇩🇪"}

st.set_page_config(page_title="Voice Notes", page_icon="🎙️", layout="centered")
st.title("🎙️ Voice Notes")

if "language" not in st.session_state:
    st.session_state.language = "en"

lang = st.session_state.language
label = f"{LANGUAGE_FLAGS[lang]} {LANGUAGE_LABELS[lang]}"
if st.button(label, help="Tap to switch language"):
    idx = LANGUAGES.index(st.session_state.language)
    st.session_state.language = LANGUAGES[(idx + 1) % len(LANGUAGES)]
    st.rerun()

context = st.text_area(
    "Context (optional)",
    placeholder="e.g. IR paper notes, chapter 3 ideas…",
    key="context_text",
)

st.write("---")
st.write("**Tap to record:**")
audio_bytes = audio_recorder(
    pause_threshold=2.5,
    sample_rate=16000,
    icon_size="2x",
    recording_color="#e84040",
    neutral_color="#404040",
)

if audio_bytes:
    filename = f"rec_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.wav"
    try:
        conn = psycopg2.connect(st.secrets["NEON_DATABASE_URL"])
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO audio_recordings (context_text, language, audio_data, audio_filename)
            VALUES (%s, %s, %s, %s)
            """,
            (
                st.session_state.get("context_text", ""),
                st.session_state.language,
                psycopg2.Binary(audio_bytes),
                filename,
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"Saved — {LANGUAGE_LABELS[st.session_state.language]}")
    except Exception as e:
        st.error(f"Upload failed: {e}")
