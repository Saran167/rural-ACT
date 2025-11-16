# FINAL WORKING VERSION — Rural ACT (Translation + Voice + Legal Awareness + Feedback)

import streamlit as st
import requests
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import re
import os

# -------------------------------------------------------------
# Page Config
# -------------------------------------------------------------
st.set_page_config(page_title="Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Tamil Legal Awareness Translator")
st.caption("Enter English → Tamil Translation + Voice + Legal Awareness + Feedback")

# -------------------------------------------------------------
# Feedback CSV Setup
# -------------------------------------------------------------
FEEDBACK_CSV = "user_feedback.csv"
FEEDBACK_COLUMNS = [
    "timestamp", "input_english", "tamil_translation",
    "detected_sections", "feedback", "feedback_detail"
]

def ensure_feedback_csv():
    if not os.path.exists(FEEDBACK_CSV):
        pd.DataFrame(columns=FEEDBACK_COLUMNS).to_csv(FEEDBACK_CSV, index=False)

def append_feedback_row(row_dict):
    ensure_feedback_csv()
    try:
        df = pd.read_csv(FEEDBACK_CSV)
    except:
        df = pd.DataFrame(columns=FEEDBACK_COLUMNS)

    full_row = {col: row_dict.get(col, "") for col in FEEDBACK_COLUMNS}
    df = pd.concat([df, pd.DataFrame([full_row])], ignore_index=True)
    df.to_csv(FEEDBACK_CSV, index=False)

ensure_feedback_csv()

# -------------------------------------------------------------
# NEW — STRONGEST 3-LAYER TRANSLATION ENGINE
# -------------------------------------------------------------
def translate_to_tamil(text):

    # 1️⃣ Try GoogleTranslator (deep-translator)
    try:
        from deep_translator import GoogleTranslator
        result = GoogleTranslator(source='en', target='ta').translate(text)
        if result and result.strip():
            return result
    except:
        pass

    # 2️⃣ Try Translate Garden API (super stable)
    try:
        url = "https://translate-api.translate.garden/translate"
        payload = {
            "text": text,
            "source_language": "en",
            "target_language": "ta"
        }
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        if "translated_text" in data:
            return data["translated_text"]
    except:
        pass

    # 3️⃣ Final fallback — LibreTranslate
    try:
        url = "https://libretranslate.de/translate"
        payload = {"q": text, "source": "en", "target": "ta"}
        r = requests.post(url, data=payload, timeout=10)
        return r.json()["translatedText"]
    except:
        return None


# -------------------------------------------------------------
# Tamil Text-To-Speech
# -------------------------------------------------------------
def tts_tamil_bytes(tamil_text):
    try:
        tts = gTTS(text=tamil_text, lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except:
        return None


# -------------------------------------------------------------
# LEGAL DATABASE
# -------------------------------------------------------------
LEGAL_DB = {

    "354D": {
        "section": "IPC பிரிவு 354D - துரத்தல் / தொந்தரவு",
        "ta_explanation": (
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.\n"
            "எடுத்துக்காட்டு: ‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n"
            "செய்ய வேண்டியது: அனைத்து ஆதாரங்களையும் (screenshots, chat logs) சேமிக்கவும்; சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2024ல் Chennaiயில் cyberstalking செய்த நபர் கைது."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["harass", "harassed", "harassment", "stalk", "stalking", "threat", "blackmail"]
    },

    "66C/66D": {
        "section": "IT Act 66C / 66D - அடையாள திருட்டு / இணைய மோசடி",
        "ta_explanation": (
            "OTP, password, account விவரங்களை திருடி வேறொருவராக நடிப்பது குற்றமாகும்.\n"
            "எடுத்துக்காட்டு: வங்கி OTP கேட்டு பணம் எடுப்பது.\n"
            "செய்ய வேண்டியது: OTP பகிர வேண்டாம்; வங்கியில் உடனடியாக தொடர்புகொள்ளவும்.\n"
            "📞 உதவி எண்: 1930"
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["otp", "password", "verify", "bank link", "fake link"]
    },

    "420": {
        "section": "IPC பிரிவு 420 - மோசடி",
        "ta_explanation": (
            "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றமாகும்.\n"
            "எடுத்துக்காட்டு: ‘நீங்கள் வெற்றி பெற்றீர்கள் – பரிசுக்காக 5000 அனுப்பவும்’.\n"
            "செய்ய வேண்டியது: பணம் அனுப்ப வேண்டாம்; போலீசில் புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930"
        ),
        "ta_punishment": "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["fraud", "scam", "lottery", "money", "loan app"]
    }
}


# -------------------------------------------------------------
# Detect Legal Sections
# -------------------------------------------------------------
def detect_sections(english_text):
    t = english_text.lower()
    found = []
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if kw in t:
                found.append((key, info))
                break
    return found


# -------------------------------------------------------------
# SESSION STATES
# -------------------------------------------------------------
if "show_detail_buttons" not in st.session_state:
    st.session_state.show_detail_buttons = False

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""

if "detected_keys" not in st.session_state:
    st.session_state.detected_keys = []


# -------------------------------------------------------------
# UI — Input
# -------------------------------------------------------------
st.markdown("### ➤ Enter English text:")
english_input = st.text_area("", height=120)

if st.button("Translate → Tamil & Analyze"):

    if not english_input.strip():
        st.warning("Please enter some English text.")
    else:
        tamil_text = translate_to_tamil(english_input)

        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")

        if tamil_text:
            st.success(tamil_text)
        else:
            st.error("⚠️ Translation temporarily unavailable.")
            tamil_text = None

        # Voice
        st.subheader("🔊 Tamil Voice:")
        if tamil_text:
            audio_bytes = tts_tamil_bytes(tamil_text)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")
        else:
            st.info("Voice available only after successful translation.")

        # Save to session
        st.session_state.last_input = english_input
        st.session_state.last_translation = tamil_text if tamil_text else ""
        st.session_state.detected_keys = [k for k, _ in detect_sections(english_input)]

        # Legal Awareness
        st.divider()
        st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")

        matches = detect_sections(english_input)
        if matches:
            for key, info in matches:
                st.markdown(f"### {info['section']}")
                st.write(info["ta_explanation"])
                st.write(info["ta_punishment"])
                st.write("---")
        else:
            st.info("இந்த செய்திக்கு தொடர்புடைய சட்டம் எதுவும் கண்டறியப்படவில்லை.")


# -------------------------------------------------------------
# FEEDBACK SECTION
# -------------------------------------------------------------
st.divider()
st.subheader("🗣️ பயனர் கருத்து (User Feedback)")

if st.session_state.last_input:

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Understand"):
            row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "input_english": st.session_state.last_input,
                "tamil_translation": st.session_state.last_translation,
                "detected_sections": ",".join(st.session_state.detected_keys),
                "feedback": "Understand",
                "feedback_detail": ""
            }
            append_feedback_row(row)
            st.success("Feedback saved successfully.")

    with col2:
        if st.button("❌ Not Understand"):
            st.session_state.show_detail_buttons = True

    if st.session_state.show_detail_buttons:
        st.markdown("### What was not clear?")
        d1, d2, d3 = st.columns(3)

        with d1:
            if st.button("📝 Text"):
                append_feedback_row({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "input_english": st.session_state.last_input,
                    "tamil_translation": st.session_state.last_translation,
                    "detected_sections": ",".join(st.session_state.detected_keys),
                    "feedback": "Not Understand",
                    "feedback_detail": "Text"
                })
                st.success("Feedback saved (Text).")
                st.session_state.show_detail_buttons = False

        with d2:
            if st.button("🔊 Voice"):
                append_feedback_row({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "input_english": st.session_state.last_input,
                    "tamil_translation": st.session_state.last_translation,
                    "detected_sections": ",".join(st.session_state.detected_keys),
                    "feedback": "Not Understand",
                    "feedback_detail": "Voice"
                })
                st.success("Feedback saved (Voice).")
                st.session_state.show_detail_buttons = False

        with d3:
            if st.button("🔁 Both"):
                append_feedback_row({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "input_english": st.session_state.last_input,
                    "tamil_translation": st.session_state.last_translation,
                    "detected_sections": ",".join(st.session_state.detected_keys),
                    "feedback": "Not Understand",
                    "feedback_detail": "Both"
                })
                st.success("Feedback saved (Both).")
                st.session_state.show_detail_buttons = False

else:
    st.info("Translate something first to give feedback.")


























