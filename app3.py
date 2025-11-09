# app.py
# English input -> Tamil translation + Tamil voice -> Tamil legal awareness -> Feedback (icons) -> Save CSV
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import re
import os

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Tamil Legal-Aware Translator (Input)")
st.caption("Enter English text → Tamil translation + Tamil voice → Legal awareness (Tamil) → Feedback")

# -------------------------
# Feedback CSV
# -------------------------
FEEDBACK_CSV = "user_feedback.csv"
if not os.path.exists(FEEDBACK_CSV):
    pd.DataFrame(columns=[
        "timestamp", "input_english", "tamil_translation", "detected_sections",
        "feedback", "feedback_detail"
    ]).to_csv(FEEDBACK_CSV, index=False)

# -------------------------
# Legal DB (Tamil focused, expanded)
# Add or extend entries as needed
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் 66C / 66D",
        "ta_explanation": (
            "66C: பிறரின் அடையாளத்தை (password, OTP, account) திருடி பயன்படுத்துவது - அடையாள திருட்டு.\n"
            "66D: இணையத்தில் வேறொரு நபராக நடித்து மோசடி செய்வது (phishing, fake bank links, OTP கேட்பு).\n\n"
            "எடுத்துக் கூடு: பேங்கி̆ங் OTP கேட்டு பணம் எடுத்தல், போலி KYC/வங்கி இணைப்புகள்.\n\n"
            "செய்ய வேண்டியது: OTP/Password ஒருவரிடம் பகிர வேண்டாம். உடனே வங்கி மற்றும் சைபர் போலீசில் புகார் செய்யவும்."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும்/அல்லது அபராதம் (சட்டப்படி).",
        "keywords": [
            "otp","one time password","password","pwd","login","account","verify link","verify your account",
            "phish","phishing","fake link","bank link","k y c","kyc","bank notice","hacked","hack",
            "ஓடிபி","கடவுச்சொல்","கணக்கு","ஹேக்","இணைப்பு"
        ]
    },
    "420": {
        "section": "IPC பிரிவு 420",
        "ta_explanation": (
            "மோசடி: பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல். இதில் advance fee scams, fake loan apps, lottery scams அடங்கும்.\n\n"
            "எடுத்துக்காட்டு: ‘நீங்கள் வெற்றி பெற்றீர்கள் — பரிசுக்காக 5000 அனுப்பவும்’ அல்லது போலி அரசு / வங்கி அழைப்பு மூலம் பணம் கேட்பது.\n\n"
            "செய்ய வேண்டியது: பணம் அனுப்பாதீர்கள்; அதிகாரப்பூர்வ தளத்தைச் சோதிக்கவும்; அனைத்து சான்றுகளையும் (SMS, UPI screenshot) சேமிக்கவும்; போலீசில் புகார் செய்யவும்."
        ),
        "ta_punishment": "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": [
            "scam","scammed","fraud","cheat","cheated","lottery","prize","advance fee","send money","transfer money",
            "loan app","fake loan","collect money","payment","rupees","₹","money","paid","payment failed",
            "மோசடி","ஏமாற்று","பணம்","கடன்","லாட்டரி"
        ]
    },
    "406": {
        "section": "IPC பிரிவு 406",
        "ta_explanation": (
            "நம்பிக்கையின்மையால் சொத்து/பணத்தை தவறாக பயன்படுத்துதல் (Criminal breach of trust).\n\n"
            "எடுத்துக்காட்டு: கடன் எடுத்தவர் பணத்தை திருப்பிச் செய்யவில்லை அல்லது ஒப்படைக்கப்பட்ட பொருட்களை திருடிவிடுதல்.\n\n"
            "செய்ய வேண்டியது: எழுத்துப்பூர்வ உடன்படிக்கைகள் வைத்திருங்கள்; ஆதாரங்கள் சேகரிக்கவும்; போலீஸ் அல்லது சட்ட ஆலோசனை பெறவும்."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "keywords": [
            "breach of trust","breach trust","embezzle","did not return loan","misuse funds","stole money",
            "நம்பிக்கை","திருட்டு","கடன் திருப்பவில்லை"
        ]
    },
    "354D": {
        "section": "IPC பிரிவு 354D",
        "ta_explanation": (
            "அடிக்கடி ஒருவரை தொந்தரவு செய்தல்/துரத்துதல் (cyberstalking / harassment).\n\n"
            "எடுத்துக்காட்டு: ஒருவருக்கு தொடர்ந்து மிரட்டுதலான செய்திகள் அனுப்புதல், புகைப்படங்கள் பகிர்ந்து அவமதித்தல்.\n\n"
            "செய்ய வேண்டியது: முழு ஆதாரங்கள் (screenshots, call logs) சேமிக்கவும்; உடனே போலீஸில் அல்லது cyber cell-ல் புகார் அளிக்கவும்."
        ),
        "ta_punishment": "தண்டனை: குற்றத்தின் தீவிரத்தின்படி சிறை மற்றும் அபராதம்.",
        "keywords": [
            "harass","harassed","harassment","stalk","stalking","stalker","follow","following","threat","threaten",
            "blackmail","blackmailed","molest","abuse","மிரட்டி","அச்சுறுத்து","தொடர்ந்து","தொடர்ச்சியாக"
        ]
    },
    "67": {
        "section": "IT Act பிரிவு 67 / 67A",
        "ta_explanation": (
            "அனுமதி இல்லாமல் பாலின/அசிங்க உள்ளடக்கங்கள் பகிர்தல் (obscene images/videos).\n\n"
            "எடுத்துக்காட்டு: யாரோ ஒருவரின் நியூட் புகைப்படங்களை பகிர்தல் அல்லது பாலியல் வீடியோக்களை இணையத்தில் வெளியிடுதல்.\n\n"
            "செய்ய வேண்டியது: உடனே ஆதாரங்களை சேமித்து சைபர் போலீசில் புகார் செய்யவும்; சமூக ஊடகங்களில் report/flag செய்யவும்."
        ),
        "ta_punishment": "தண்டனை: முதல் முறையில் 3 ஆண்டுகள் மற்றும் அபராதம்; மீண்டும் செய்தால் அதிகமாகும்.",
        "keywords": [
            "nude","porn","obscene","private photo","leak","leaked","share photo","sex video","child porn",
            "அசிங்க","புகைப்படம்","வீடியோ","லீக்"
        ]
    }
}

# -------------------------
# Translator & TTS helpers
# -------------------------
translator = GoogleTranslator(source='en', target='ta')

def translate_to_tamil(text):
    try:
        return translator.translate(text)
    except Exception:
        # fallback: return empty or input
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
# Robust detection
# -------------------------
def detect_sections(english_text):
    t = english_text.lower()
    t = re.sub(r'[\t\n\r]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    found = []
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            kw_l = kw.lower().strip()
            if ' ' in kw_l:
                if kw_l in t:
                    found.append((key, info))
                    break
            else:
                pattern = r'\b' + re.escape(kw_l) + r'\b'
                if re.search(pattern, t):
                    found.append((key, info))
                    break
    return found

# -------------------------
# Session state for feedback flow
# -------------------------
if "show_detail_buttons" not in st.session_state:
    st.session_state.show_detail_buttons = False
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""
if "detected_keys" not in st.session_state:
    st.session_state.detected_keys = []

# -------------------------
# Input UI
# -------------------------
st.markdown("#### ➤ Enter **one English sentence** (type or paste SMS/notification):")
english_input = st.text_area("", height=110, key="input_box")

if st.button("Translate → Tamil & Analyze"):
    if not english_input.strip():
        st.warning("Please enter some English text.")
    else:
        # Translate
        tamil_text = translate_to_tamil(english_input)
        if not tamil_text:
            st.error("Translation failed. Check network or try again.")
            tamil_text = ""

        # Show Tamil translation
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_text)

        # Play Tamil voice
        audio_bytes = tts_tamil_bytes(tamil_text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
        else:
            st.info("Audio not available (TTS issue).")

        # Save last state
        st.session_state.last_input = english_input
        st.session_state.last_translation = tamil_text

        # Detect legal sections
        matches = detect_sections(english_input)
        st.session_state.detected_keys = [k for k, _ in matches]

        # Display legal awareness (Tamil only)
        st.divider()
        st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")
        if matches:
            for key, info in matches:
                st.markdown(f"### {info['section']}")
                st.write(f"**விளக்கம்:** {info['ta_explanation']}")
                st.write(f"**தண்டனை:** {info['ta_punishment']}")
                st.write("---")
        else:
            st.info("✅ இந்த செய்திக்கு தொடர்புடைய சட்டப் பகுதி கண்டறியப்படவில்லை.")

        # Reset feedback detail buttons flag and show feedback area
        st.session_state.show_detail_buttons = False

# -------------------------
# Feedback UI (always shown after translation attempt)
# -------------------------
st.divider()
st.subheader("🗣️ பயனர் கருத்து (User Feedback)")

# Show feedback only if there is a last translation saved
if st.session_state.last_input:
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("✅ Understand"):
            # Save positive feedback
            df = pd.read_csv(FEEDBACK_CSV)
            df.loc[len(df)] = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                st.session_state.last_input,
                st.session_state.last_translation,
                ",".join(st.session_state.detected_keys) if st.session_state.detected_keys else "",
                "Understand",
                ""
            ]
            df.to_csv(FEEDBACK_CSV, index=False)
            st.success("✅ Feedback saved successfully.")
    with col2:
        if st.button("❌ Not Understand"):
            # show detail choices
            st.session_state.show_detail_buttons = True

    # if user clicked Not Understand, show the three icon buttons (no navigation away)
    if st.session_state.show_detail_buttons:
        st.markdown("### 😕 எது புரியவில்லை? (What was not clear?)")
        d1, d2, d3 = st.columns(3)
        with d1:
            if st.button("📝 Text"):
                df = pd.read_csv(FEEDBACK_CSV)
                df.loc[len(df)] = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    st.session_state.last_input,
                    st.session_state.last_translation,
                    ",".join(st.session_state.detected_keys) if st.session_state.detected_keys else "",
                    "Not Understand",
                    "Text"
                ]
                df.to_csv(FEEDBACK_CSV, index=False)
                st.success("✅ Feedback saved successfully (Text).")
                st.session_state.show_detail_buttons = False
        with d2:
            if st.button("🔊 Voice"):
                df = pd.read_csv(FEEDBACK_CSV)
                df.loc[len(df)] = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    st.session_state.last_input,
                    st.session_state.last_translation,
                    ",".join(st.session_state.detected_keys) if st.session_state.detected_keys else "",
                    "Not Understand",
                    "Voice"
                ]
                df.to_csv(FEEDBACK_CSV, index=False)
                st.success("✅ Feedback saved successfully (Voice).")
                st.session_state.show_detail_buttons = False
        with d3:
            if st.button("🔁 Both"):
                df = pd.read_csv(FEEDBACK_CSV)
                df.loc[len(df)] = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    st.session_state.last_input,
                    st.session_state.last_translation,
                    ",".join(st.session_state.detected_keys) if st.session_state.detected_keys else "",
                    "Not Understand",
                    "Both"
                ]
                df.to_csv(FEEDBACK_CSV, index=False)
                st.success("✅ Feedback saved successfully (Both).")
                st.session_state.show_detail_buttons = False
else:
    st.info("Translate something first — then give feedback.")

st.markdown("---")
st.caption("Feedback stored locally in user_feedback.csv — you can download it from your Streamlit Cloud app files.")












