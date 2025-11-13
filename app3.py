# app.py — Final Version: Tamil Legal Awareness Translator with Voice and Feedback

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import re
import os

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Tamil Legal Awareness Translator (Single Input)")
st.caption("Enter English → Tamil translation + Tamil voice + Legal awareness (Tamil voice) + Feedback")

# -------------------------
# CSV setup
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
# Legal Database (Expanded Tamil)
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் 66C / 66D",
        "ta_explanation": (
            "66C: பிறரின் அடையாளத்தை (password, OTP, account) திருடி பயன்படுத்துவது குற்றம்.\n"
            "66D: இணையத்தில் வேறொரு நபராக நடித்து மோசடி செய்வது குற்றம்.\n\n"
            "எடுத்துக்காட்டு: வங்கி OTP கேட்டு பணம் எடுத்தல் அல்லது போலி link மூலம் login கேட்பது.\n"
            "செய்ய வேண்டியது: OTP/Password யாரிடமும் பகிர வேண்டாம். வங்கி மற்றும் சைபர் போலீசில் புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline"
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "keywords": ["otp","password","bank","link","verify","account","phish","hack","login","kyc","ஓடிபி","கடவுச்சொல்","ஹேக்"]
    },
    "420": {
        "section": "IPC பிரிவு 420 - மோசடி (Cheating)",
        "ta_explanation": (
            "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றம். இதில் advance fee scams, loan apps, lottery scams அடங்கும்.\n"
            "எடுத்துக்காட்டு: 'நீங்கள் வெற்றி பெற்றீர்கள் — பரிசுக்காக 5000 அனுப்பவும்' என்ற போலி government/bank message.\n"
            "செய்ய வேண்டியது: பணம் அனுப்பாதீர்கள். வங்கியை நேரடியாக தொடர்பு கொள்ளவும்; அனைத்து ஆதாரங்களையும் (SMS, screenshot) சேமிக்கவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline"
        ),
        "ta_punishment": "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["fraud","cheat","cheated","money","loan","prize","scam","payment","bank","lottery","மோசடி","பணம்"]
    },
    "406": {
        "section": "IPC பிரிவு 406 - நம்பிக்கை மீறல் (Breach of Trust)",
        "ta_explanation": (
            "ஒப்படைக்கப்பட்ட சொத்தை நம்பிக்கையின்மை காரணமாக தவறாக பயன்படுத்துதல் குற்றம்.\n"
            "எடுத்துக்காட்டு: பணம் கடன் வாங்கி திருப்பி தராமல் போதல் அல்லது ஒப்படைக்கப்பட்ட பொருட்களை வைத்துக்கொள்வது.\n"
            "செய்ய வேண்டியது: ஒப்பந்தம் எழுதிக் கொள்ளவும்; ஆதாரங்களை சேமிக்கவும்; சட்ட ஆலோசனை பெறவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline"
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம்.",
        "keywords": ["trust","loan","not return","breach","embezzle","திருப்பவில்லை","நம்பிக்கை"]
    },
    "354D": {
        "section": "IPC பிரிவு 354D - துரத்தல்/தொந்தரவு (Stalking/Harassment)",
        "ta_explanation": (
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.\n"
            "எடுத்துக்காட்டு: ‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n"
            "செய்ய வேண்டியது: அனைத்து ஆதாரங்களையும் (screenshots, chat logs) சேமிக்கவும்; சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n📚 எடுத்துக்காட்டு: 2024ல் Chennaiயில் cyberstalking செய்த நபர் கைது."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["harass","harassed","harassment","stalk","threat","blackmail","மிரட்டி","துன்புறுத்து","தொடர்ந்து"]
    },
    "67": {
        "section": "IT Act பிரிவு 67 / 67A - அசிங்க உள்ளடக்கங்கள் பகிர்தல்",
        "ta_explanation": (
            "அசிங்கமான அல்லது பாலியல் உள்ளடக்கங்களை இணையத்தில் பகிர்தல் குற்றமாகும்.\n"
            "எடுத்துக்காட்டு: யாரோ ஒருவரின் புகைப்படத்தை அனுமதி இல்லாமல் பகிர்தல் அல்லது post செய்தல்.\n"
            "செய்ய வேண்டியது: சமூக ஊடகங்களில் report/flag செய்யவும்; சைபர் போலீசில் புகார் அளிக்கவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline"
        ),
        "ta_punishment": "தண்டனை: முதல் முறையில் 3 ஆண்டுகள் சிறை மற்றும் அபராதம்; மீண்டும் செய்தால் அதிகமாகும்.",
        "keywords": ["nude","porn","obscene","photo","leak","video","அசிங்க","புகைப்படம்","வீடியோ"]
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

def tts_tamil_audio(tamil_text):
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
    t = english_text.lower().strip()
    found = []
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', t):
                found.append((key, info))
                break
    return found

# -------------------------
# Streamlit UI
# -------------------------
if "show_detail_buttons" not in st.session_state:
    st.session_state.show_detail_buttons = False
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""
if "detected_keys" not in st.session_state:
    st.session_state.detected_keys = []

st.markdown("#### ➤ Enter your English message:")
english_input = st.text_area("", height=100)

if st.button("Translate → Tamil & Analyze"):
    if not english_input.strip():
        st.warning("Please enter English text.")
    else:
        tamil_text = translate_to_tamil(english_input)
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_text)

        # Tamil voice for translation
        audio_bytes = tts_tamil_audio(tamil_text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")

        matches = detect_sections(english_input)
        st.session_state.last_input = english_input
        st.session_state.last_translation = tamil_text
        st.session_state.detected_keys = [k for k, _ in matches]

        st.divider()
        st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")

        if matches:
            for key, info in matches:
                st.markdown(f"### {info['section']}")
                st.write(info["ta_explanation"])
                st.write(f"**தண்டனை:** {info['ta_punishment']}")
                st.write("---")
                # Tamil voice for legal awareness
                legal_voice = tts_tamil_audio(info["ta_explanation"])
                if legal_voice:
                    st.audio(legal_voice, format="audio/mp3")
        else:
            st.info("✅ எந்த சட்டப் பிரிவும் பொருந்தவில்லை.")

# -------------------------
# Feedback
# -------------------------
st.divider()
st.subheader("🗣️ பயனர் கருத்து (User Feedback)")

if st.session_state.last_input:
    c1, c2 = st.columns([1,1])
    with c1:
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
            st.success("✅ Feedback saved successfully.")
    with c2:
        if st.button("❌ Not Understand"):
            st.session_state.show_detail_buttons = True

    if st.session_state.show_detail_buttons:
        st.markdown("### 😕 எது புரியவில்லை?")
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
                st.success("✅ Feedback saved successfully.")
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
                st.success("✅ Feedback saved successfully.")
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
                st.success("✅ Feedback saved successfully.")
                st.session_state.show_detail_buttons = False
else:
    st.info("Please translate something first to give feedback.")

st.markdown("---")
st.caption("All feedback is stored in user_feedback.csv for future improvement.")




















