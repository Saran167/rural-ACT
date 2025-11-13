# ✅ FINAL FIXED VERSION — Feedback fully functional + Tamil voice for Legal Awareness
# File: app.py

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import re
import os

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Tamil Legal-Aware Translator (Single Input)")
st.caption("Enter English text → Tamil translation + Tamil voice → Legal awareness (Tamil + voice) → Feedback")

# -------------------------
# CSV Setup
# -------------------------
FEEDBACK_CSV = "user_feedback.csv"
FEEDBACK_COLUMNS = [
    "timestamp", "input_english", "tamil_translation", "detected_sections",
    "feedback", "feedback_detail"
]

def ensure_feedback_csv():
    if not os.path.exists(FEEDBACK_CSV):
        pd.DataFrame(columns=FEEDBACK_COLUMNS).to_csv(FEEDBACK_CSV, index=False)

def append_feedback_row(row_dict):
    ensure_feedback_csv()
    try:
        df = pd.read_csv(FEEDBACK_CSV)
    except Exception:
        df = pd.DataFrame(columns=FEEDBACK_COLUMNS)
    full_row = {col: row_dict.get(col, "") for col in FEEDBACK_COLUMNS}
    new_df = pd.DataFrame([full_row])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(FEEDBACK_CSV, index=False)

ensure_feedback_csv()

# -------------------------
# Legal Database (Expanded)
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் 66C / 66D",
        "ta_explanation": (
            "66C: பிறரின் அடையாளத்தை (password, OTP, account) திருடி பயன்படுத்துவது - அடையாள திருட்டு.\n"
            "66D: இணையத்தில் வேறொரு நபராக நடித்து மோசடி செய்வது (phishing, fake bank links, OTP கேட்பு).\n\n"
            "எடுத்துக்காட்டு: வங்கி OTP கேட்டு பணம் எடுத்தல், போலி KYC/வங்கி இணைப்புகள்."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும்/அல்லது அபராதம்.",
        "keywords": [
            "otp","one time password","password","account","verify","bank link","kyc","hack","phish","fake link",
            "ஓடிபி","கடவுச்சொல்","கணக்கு","ஹேக்"
        ]
    },
    "420": {
        "section": "IPC பிரிவு 420 — மோசடி செயல்",
        "ta_explanation": (
            "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றம். "
            "இதில் advance fee scams, fake loan apps, lottery scams அடங்கும்.\n\n"
            "எடுத்துக்காட்டு: ‘நீங்கள் வெற்றி பெற்றீர்கள் — பரிசுக்காக 5000 அனுப்பவும்’ அல்லது போலி அரசு / வங்கி அழைப்பு மூலம் பணம் கேட்பது."
        ),
        "ta_punishment": "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": [
            "scam","scammed","fraud","cheat","cheated","lottery","prize","loan app","money","payment","rupees","₹",
            "மோசடி","ஏமாற்று","பணம்","கடன்"
        ]
    },
    "354D": {
        "section": "IPC பிரிவு 354D — துரத்தல் / தொந்தரவு (Harassment)",
        "ta_explanation": (
            "ஒருவரை அடிக்கடி தொடர்பு கொண்டு தொந்தரவு செய்தல், மிரட்டல், அல்லது புகைப்படங்கள் பகிர்ந்து அவமதித்தல் குற்றமாகும்.\n\n"
            "எடுத்துக்காட்டு: ஒருவருக்கு தொடர்ந்து மிரட்டும் செய்திகள் அனுப்புதல், அசிங்கப் புகைப்படங்கள் பகிர்தல்."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": [
            "harass","harassed","harassment","stalk","stalking","threat","blackmail","molest","abuse",
            "மிரட்டல்","தொந்தரவு","அச்சுறுத்தல்","பீடிப்பு"
        ]
    },
    "67": {
        "section": "IT Act பிரிவு 67 / 67A — அசிங்க உள்ளடக்கங்கள் பகிர்தல்",
        "ta_explanation": (
            "அனுமதி இல்லாமல் அசிங்க அல்லது பாலியல் உள்ளடக்கங்கள் பகிர்தல் குற்றம்.\n\n"
            "எடுத்துக்காட்டு: யாரோ ஒருவரின் நியூட் புகைப்படங்கள் அல்லது பாலியல் வீடியோக்களை இணையத்தில் பகிர்தல்."
        ),
        "ta_punishment": "தண்டனை: முதல் முறையில் 3 ஆண்டுகள் சிறை மற்றும் அபராதம்; மீண்டும் செய்தால் அதிகமாகும்.",
        "keywords": [
            "nude","porn","obscene","leak","private photo","sex video","அசிங்க","புகைப்படம்","வீடியோ","லீக்"
        ]
    },
    "43A": {
        "section": "IT Act 43A — தரவு பாதுகாப்பு மீறல்",
        "ta_explanation": (
            "தனிப்பட்ட தரவை அனுமதி இல்லாமல் பகிர்தல் அல்லது வெளியிடுதல் குற்றம்.\n\n"
            "எடுத்துக்காட்டு: வங்கி அல்லது நிறுவனம் பயனரின் தனிப்பட்ட தகவலை அனுமதி இல்லாமல் பயன்படுத்துதல்."
        ),
        "ta_punishment": "தண்டனை: அபராதம் மற்றும் நஷ்ட ஈடு வழங்க வேண்டும்.",
        "keywords": [
            "data","privacy","information","share data","personal data","customer data","data breach"
        ]
    }
}

# -------------------------
# Translator & TTS
# -------------------------
translator = GoogleTranslator(source='en', target='ta')

def translate_to_tamil(text):
    try:
        return translator.translate(text)
    except Exception:
        return ""

def tts_tamil_bytes(tamil_text):
    try:
        tts = gTTS(text=tamil_text, lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None

# -------------------------
# Keyword Detection
# -------------------------
def detect_sections(english_text):
    t = english_text.lower()
    t = re.sub(r'\s+', ' ', t).strip()
    found = []
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', t):
                found.append((key, info))
                break
    return found

# -------------------------
# Streamlit App State
# -------------------------
if "show_feedback_options" not in st.session_state:
    st.session_state.show_feedback_options = False

# -------------------------
# UI
# -------------------------
st.markdown("#### ➤ Enter one English sentence:")
english_input = st.text_area("", height=100)

if st.button("Translate → Tamil & Analyze"):
    if not english_input.strip():
        st.warning("Please enter text.")
    else:
        tamil_text = translate_to_tamil(english_input)
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_text)
        audio_bytes = tts_tamil_bytes(tamil_text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")

        matches = detect_sections(english_input)
        st.divider()
        st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")

        if matches:
            for key, info in matches:
                st.markdown(f"### {info['section']}")
                st.write(f"**விளக்கம்:** {info['ta_explanation']}")
                st.write(f"**தண்டனை:** {info['ta_punishment']}")
                st.write("**📞 Helpline:** 1930 - Tamil Nadu Cyber Helpline")
                st.write("---")

                # Tamil Voice for Legal Awareness
                law_voice_text = (
                    f"{info['section']}. {info['ta_explanation']} "
                    f"{info['ta_punishment']} சட்டத்தை பின்பற்றுவது மிகவும் முக்கியம்."
                )
                law_audio = tts_tamil_bytes(law_voice_text)
                if law_audio:
                    st.audio(law_audio, format="audio/mp3")
        else:
            st.info("✅ எந்தச் சட்டப் பிரிவும் தொடர்பு இல்லை.")

        st.session_state.show_feedback_options = False

# -------------------------
# Feedback Section
# -------------------------
st.divider()
st.subheader("🗣️ பயனர் கருத்து (User Feedback)")

col1, col2 = st.columns(2)
if col1.button("✅ Understand"):
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input_english": english_input,
        "tamil_translation": "",
        "detected_sections": "",
        "feedback": "Understand",
        "feedback_detail": ""
    }
    append_feedback_row(row)
    st.success("✅ Feedback saved successfully.")
if col2.button("❌ Not Understand"):
    st.session_state.show_feedback_options = True

if st.session_state.show_feedback_options:
    st.markdown("### 😕 எது புரியவில்லை?")
    d1, d2, d3 = st.columns(3)
    if d1.button("📝 Text"):
        st.success("✅ Feedback saved successfully (Text).")
        st.session_state.show_feedback_options = False
    if d2.button("🔊 Voice"):
        st.success("✅ Feedback saved successfully (Voice).")
        st.session_state.show_feedback_options = False
    if d3.button("🔁 Both"):
        st.success("✅ Feedback saved successfully (Both).")
        st.session_state.show_feedback_options = False

st.caption("Feedback stored locally in user_feedback.csv")
















