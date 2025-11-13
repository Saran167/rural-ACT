# app.py — Final Version (with Tamil Voice for Legal Awareness + Feedback System)
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
st.title("🛡️ Rural ACT: Tamil Legal Awareness Translator")
st.caption("Translate English → Tamil + Voice + Legal Awareness + Smart Feedback")

# -------------------------
# Feedback CSV setup
# -------------------------
FEEDBACK_CSV = "user_feedback.csv"
COLUMNS = ["timestamp", "input_english", "tamil_translation", "detected_sections", "feedback", "feedback_detail"]

if not os.path.exists(FEEDBACK_CSV):
    pd.DataFrame(columns=COLUMNS).to_csv(FEEDBACK_CSV, index=False)

def append_feedback(data):
    """Append feedback safely"""
    try:
        df = pd.read_csv(FEEDBACK_CSV)
    except Exception:
        df = pd.DataFrame(columns=COLUMNS)
    new = pd.DataFrame([data])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(FEEDBACK_CSV, index=False)

# -------------------------
# Legal Knowledge Base (Expanded)
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் பிரிவு 66C / 66D",
        "ta_explanation": (
            "66C: பிறரின் அடையாளத்தை (password, OTP, account) திருடி பயன்படுத்துவது அடையாள திருட்டாகும்.\n"
            "66D: இணையத்தில் போலியாக நடித்து (fake bank calls, phishing, fraud links) ஏமாற்றுவது குற்றமாகும்.\n\n"
            "👉 எடுத்துக்காட்டு: போலி வங்கி SMS, KYC link மூலம் OTP கேட்டு பணம் எடுப்பது.\n"
            "👉 செய்ய வேண்டியது: OTP/Password யாருக்கும் சொல்ல வேண்டாம்; வங்கியிலும் சைபர் போலீஸிலும் உடனே புகார் செய்யவும்."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "keywords": ["otp","password","bank","kyc","phishing","fake link","hack","ஹேக்","பாஸ்வேர்டு","ஓடிபி"]
    },
    "420": {
        "section": "IPC பிரிவு 420 – மோசடி மற்றும் ஏமாற்றல்",
        "ta_explanation": (
            "பிறரை ஏமாற்றி பணம், பொருள் அல்லது நன்மை பெறுவது குற்றமாகும்.\n\n"
            "👉 எடுத்துக்காட்டு: போலி பரிசு/லாட்டரி, job scam, loan app fraud, fake investment link.\n"
            "👉 செய்ய வேண்டியது: பணம் அனுப்பாதீர்கள், அரசு தளங்களில் சரிபார்க்கவும், ஆதாரங்களை சேமிக்கவும்."
        ),
        "ta_punishment": "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["fraud","scam","cheat","money","loan","lottery","பணம்","மோசடி","ஏமாற்று"]
    },
    "406": {
        "section": "IPC பிரிவு 406 – நம்பிக்கை மீறல் (Criminal Breach of Trust)",
        "ta_explanation": (
            "ஒருவரிடம் ஒப்படைக்கப்பட்ட சொத்து/பணத்தை தவறாக பயன்படுத்துதல் குற்றமாகும்.\n\n"
            "👉 எடுத்துக்காட்டு: கடன் திருப்பவில்லை, நம்பிக்கை வைத்து கொடுத்த பொருளை திருப்பவில்லை.\n"
            "👉 செய்ய வேண்டியது: எழுத்துப்பூர்வ சான்றுகள் வைத்திருங்கள்; போலீஸில் புகார் செய்யவும்."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம்.",
        "keywords": ["breach","trust","loan","return money","நம்பிக்கை","கடன்"]
    },
    "354D": {
        "section": "IPC பிரிவு 354D – துரத்தல் மற்றும் தொந்தரவு (Stalking / Harassment)",
        "ta_explanation": (
            "ஒருவரை மீண்டும் மீண்டும் தொடர்பு கொள்ளுதல் அல்லது மிரட்டுதல், இணையத்தில் தொந்தரவு செய்தல் குற்றமாகும்.\n\n"
            "👉 எடுத்துக்காட்டு: தொடர்ச்சியாக messages அனுப்புதல், பிளாக்மெயில் செய்தல், புகைப்படம் பகிர்தல்.\n"
            "👉 செய்ய வேண்டியது: screenshots சேமிக்கவும்; சைபர் போலீஸில் புகார் செய்யவும்."
        ),
        "ta_punishment": "தண்டனை: சிறை மற்றும் அபராதம் (குற்றத்தின் தீவிரத்தைப் பொறுத்து).",
        "keywords": ["harass","harassment","threat","blackmail","follow","மிரட்டு","தொந்தரவு"]
    },
    "67": {
        "section": "IT Act பிரிவு 67 / 67A – அசிங்கமான உள்ளடக்க பகிர்வு",
        "ta_explanation": (
            "பாலியல் / தனிப்பட்ட புகைப்படம் அல்லது வீடியோவை அனுமதி இல்லாமல் பகிர்வது குற்றமாகும்.\n\n"
            "👉 எடுத்துக்காட்டு: யாரோ ஒருவரின் private photo/video இணையத்தில் வெளியிடுதல்.\n"
            "👉 செய்ய வேண்டியது: புகார் செய்யவும், சமூக ஊடகங்களில் report செய்யவும்."
        ),
        "ta_punishment": "தண்டனை: முதல் முறையில் 3 ஆண்டுகள் சிறை, மீண்டும் செய்தால் அதிகமாகும்.",
        "keywords": ["photo","video","leak","nude","obscene","அசிங்க","புகைப்படம்","வீடியோ"]
    }
}

# -------------------------
# Translation & TTS
# -------------------------
translator = GoogleTranslator(source='en', target='ta')

def translate_tamil(text):
    try:
        return translator.translate(text)
    except:
        return "மொழிபெயர்ப்பு தோல்வியடைந்தது."

def tamil_tts(text):
    try:
        tts = gTTS(text=text, lang="ta")
        audio = BytesIO()
        tts.write_to_fp(audio)
        return audio.getvalue()
    except:
        return None

# -------------------------
# Legal detection
# -------------------------
def detect_laws(text):
    found = []
    text = text.lower()
    for sec, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text):
                found.append(info)
                break
    return found

# -------------------------
# User Input
# -------------------------
st.markdown("### ✉️ Enter English text (SMS / message):")
eng = st.text_area("", height=110)

if st.button("Translate & Show Awareness"):
    if eng.strip() == "":
        st.warning("Please enter an English sentence.")
    else:
        ta_text = translate_tamil(eng)
        st.subheader("🈶 Tamil Translation:")
        st.success(ta_text)

        audio = tamil_tts(ta_text)
        if audio:
            st.audio(audio, format="audio/mp3")

        # Detect and show legal awareness
        laws = detect_laws(eng)
        st.divider()
        st.subheader("⚖️ Legal Awareness (தமிழில்):")

        if laws:
            for law in laws:
                st.markdown(f"### {law['section']}")
                st.write(f"**விளக்கம்:** {law['ta_explanation']}")
                st.write(f"**தண்டனை:** {law['ta_punishment']}")
                # 🔊 Tamil voice for legal section
                legal_voice = tamil_tts(f"{law['section']} {law['ta_explanation']} {law['ta_punishment']}")
                if legal_voice:
                    st.audio(legal_voice, format="audio/mp3")
                st.write("---")
        else:
            st.info("✅ No legal issue found in this sentence.")

        # Save latest translation for feedback
        st.session_state.last_input = eng
        st.session_state.last_translation = ta_text

# -------------------------
# Feedback Section
# -------------------------
st.divider()
st.subheader("🗣️ User Feedback")

if "last_input" in st.session_state and st.session_state.last_input:
    col1, col2 = st.columns(2)
    if col1.button("✅ Understand"):
        append_feedback({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input_english": st.session_state.last_input,
            "tamil_translation": st.session_state.last_translation,
            "detected_sections": "",
            "feedback": "Understand",
            "feedback_detail": ""
        })
        st.success("✅ Feedback saved successfully.")

    if col2.button("❌ Not Understand"):
        st.session_state.show_detail = True

    if st.session_state.get("show_detail", False):
        st.markdown("### 😕 What was not clear?")
        d1, d2, d3 = st.columns(3)
        if d1.button("📝 Text"):
            append_feedback({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "input_english": st.session_state.last_input,
                "tamil_translation": st.session_state.last_translation,
                "detected_sections": "",
                "feedback": "Not Understand",
                "feedback_detail": "Text"
            })
            st.success("✅ Feedback saved successfully (Text).")
            st.session_state.show_detail = False
        if d2.button("🔊 Voice"):
            append_feedback({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "input_english": st.session_state.last_input,
                "tamil_translation": st.session_state.last_translation,
                "detected_sections": "",
                "feedback": "Not Understand",
                "feedback_detail": "Voice"
            })
            st.success("✅ Feedback saved successfully (Voice).")
            st.session_state.show_detail = False
        if d3.button("🔁 Both"):
            append_feedback({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "input_english": st.session_state.last_input,
                "tamil_translation": st.session_state.last_translation,
                "detected_sections": "",
                "feedback": "Not Understand",
                "feedback_detail": "Both"
            })
            st.success("✅ Feedback saved successfully (Both).")
            st.session_state.show_detail = False
else:
    st.info("Translate a sentence first to enable feedback.")

st.markdown("---")
st.caption("🪶 Feedbacks stored in user_feedback.csv for analysis.")














