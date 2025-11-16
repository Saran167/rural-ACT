import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import pandas as pd
import re
from datetime import datetime
import os

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Tamil Legal Awareness Translator")
st.caption("English → Tamil Text + Tamil Voice + Legal Awareness + Feedback")

# -----------------------------
# CSV FEEDBACK SETUP
# -----------------------------
CSV_FILE = "user_feedback.csv"

columns = [
    "timestamp", "english_input", "tamil_translation",
    "detected_sections", "feedback", "feedback_detail"
]

# Create CSV if missing
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=columns).to_csv(CSV_FILE, index=False)


def save_feedback(row):
    """Append feedback row safely."""
    try:
        df = pd.read_csv(CSV_FILE)
    except:
        df = pd.DataFrame(columns=columns)

    for col in columns:
        if col not in row:
            row[col] = ""

    df.loc[len(df)] = row
    df.to_csv(CSV_FILE, index=False)


# -----------------------------
# LEGAL DATABASE (UPDATED)
# -----------------------------
LEGAL_DB = {
    "354D": {
        "section": "IPC பிரிவு 354D – துரத்தல் / தொந்தரவு (Stalking/Harassment)",
        "description": (
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் ஆகியவை குற்றமாகும்.\n\n"
            "எடுத்துக்காட்டு:\n"
            "‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n\n"
            "செய்ய வேண்டியது:\n"
            "அனைத்து ஆதாரங்களையும் (screenshots, chat logs) சேமிக்கவும்; "
            "சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.\n\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2024ல் Chennaiயில் cyberstalking செய்த நபர் கைது.\n\n"
            "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்."
        ),
        "keywords": ["harass", "harassed", "harassment", "stalk", "threat", "blackmail", "torture"]
    },

    "66C/66D": {
        "section": "IT Act பிரிவு 66C / 66D – OTP & Online Fraud",
        "description": (
            "OTP, password, account details கேட்டு ஏமாற்றுவது குற்றம்.\n\n"
            "எடுத்துக்காட்டு:\n"
            "வங்கி OTP கேட்டு பணம் எடுப்பது, போலி bank/KYC links.\n\n"
            "செய்ய வேண்டியது:\n"
            "OTP யாரிடமும் பகிர வேண்டாம்; உடனே வங்கி + சைபர் செல் தொடர்பு கொள்ளவும்.\n\n"
            "📞 1930 – Cyber Crime Helpline\n\n"
            "தண்டனை: 3 ஆண்டுகள் சிறை + அபராதம்."
        ),
        "keywords": ["otp", "password", "bank", "verify", "kyc", "account"]
    },

    "420": {
        "section": "IPC பிரிவு 420 – மோசடி (Cheating/Fraud)",
        "description": (
            "பிறரை ஏமாற்றி பணம் பெறுவது குற்றமாகும்.\n\n"
            "எடுத்துக்காட்டு:\n"
            "‘நீங்கள் பரிசு வென்றுள்ளீர்கள் – 5000 ரூபாய் அனுப்புங்கள்’ போன்ற செய்திகள்.\n\n"
            "செய்ய வேண்டியது:\n"
            "பணம் அனுப்ப வேண்டாம்; அதிகாரப்பூர்வ தளத்தை மட்டும் பயன்படுத்தவும்.\n\n"
            "📞 1930 – Cyber Fraud Helpline\n\n"
            "தண்டனை: 7 ஆண்டுகள் சிறை + அபராதம்."
        ),
        "keywords": ["money", "fraud", "scam", "cheated", "lottery", "payment", "send money"]
    }
}


# -----------------------------
# HELPERS
# -----------------------------
def tamil_translate(text):
    """Translate English → Tamil safely."""
    try:
        return GoogleTranslator(source='en', target='ta').translate(text)
    except:
        return None


def tamil_voice(text):
    """Generate Tamil MP3 audio."""
    try:
        tts = gTTS(text=text, lang='ta')
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except:
        return None


def detect_sections(text):
    """Check which legal sections match."""
    text = text.lower()
    found = []

    for sec, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if re.search(r"\b" + re.escape(kw.lower()) + r"\b", text):
                found.append(info)
                break

    return found


# -----------------------------
# UI INPUT
# -----------------------------
st.subheader("➤ Enter English text:")
english = st.text_area("", height=100)

if st.button("Translate & Analyze"):
    if not english.strip():
        st.warning("Please enter text.")
    else:
        # Translation
        tamil = tamil_translate(english)

        st.subheader("🈶 தமிழ் மொழிபெயர்ப்பு:")
        if tamil:
            st.success(tamil)
        else:
            st.error("⚠️ Translation temporarily unavailable.")

        # Voice
        st.subheader("🔊 Tamil Voice:")
        if tamil:
            audio = tamil_voice(tamil)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")
        else:
            st.info("Voice available only after translation.")

        # Legal Awareness
        st.subheader("⚖️ சட்ட விழிப்புணர்வு:")
        matched = detect_sections(english)

        if matched:
            for info in matched:
                st.markdown(f"### {info['section']}")
                st.write(info['description'])
                st.markdown("---")
        else:
            st.info("இந்த செய்தியில் சட்ட தொடர்பு கண்டறியப்படவில்லை.")

        # Save for feedback
        st.session_state.last_eng = english
        st.session_state.last_ta = tamil if tamil else ""
        st.session_state.last_sections = ", ".join([m["section"] for m in matched])


# -----------------------------
# FEEDBACK
# -----------------------------
st.divider()
st.header("🗣️ User Feedback")

if "last_eng" in st.session_state and st.session_state.last_eng:

    c1, c2 = st.columns(2)

    if c1.button("✔️ Understand"):
        save_feedback({
            "timestamp": datetime.now(),
            "english_input": st.session_state.last_eng,
            "tamil_translation": st.session_state.last_ta,
            "detected_sections": st.session_state.last_sections,
            "feedback": "Understand",
            "feedback_detail": ""
        })
        st.success("Feedback saved successfully.")

    if c2.button("❌ Not Understand"):
        st.session_state.show_more = True

    if st.session_state.get("show_more", False):
        st.subheader("What was unclear?")
        d1, d2, d3 = st.columns(3)

        if d1.button("📝 Text"):
            save_feedback({
                "timestamp": datetime.now(),
                "english_input": st.session_state.last_eng,
                "tamil_translation": st.session_state.last_ta,
                "detected_sections": st.session_state.last_sections,
                "feedback": "Not Understand",
                "feedback_detail": "Text"
            })
            st.success("Feedback saved successfully.")

        if d2.button("🔊 Voice"):
            save_feedback({
                "timestamp": datetime.now(),
                "english_input": st.session_state.last_eng,
                "tamil_translation": st.session_state.last_ta,
                "detected_sections": st.session_state.last_sections,
                "feedback": "Not Understand",
                "feedback_detail": "Voice"
            })
            st.success("Feedback saved successfully.")

        if d3.button("🔁 Both"):
            save_feedback({
                "timestamp": datetime.now(),
                "english_input": st.session_state.last_eng,
                "tamil_translation": st.session_state.last_ta,
                "detected_sections": st.session_state.last_sections,
                "feedback": "Not Understand",
                "feedback_detail": "Both"
            })
            st.success("Feedback saved successfully.")

else:
    st.info("Submit text first to enable feedback.")



































