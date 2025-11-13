# ✅ FINAL VERSION — English→Tamil Translator + Tamil Voice + Legal Awareness + Feedback (FULL)
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
st.set_page_config(page_title="Rural ACT - Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Rural ACT: Tamil Legal Awareness Translator")
st.caption("Translate English ➜ Tamil • Hear in Tamil Voice • Know Your Rights • Give Feedback")

# -------------------------
# Feedback CSV setup
# -------------------------
CSV_PATH = "user_feedback.csv"
COLUMNS = ["timestamp", "input_english", "tamil_translation", "detected_sections", "feedback", "feedback_detail"]

if not os.path.exists(CSV_PATH):
    pd.DataFrame(columns=COLUMNS).to_csv(CSV_PATH, index=False)

def save_feedback(data):
    df = pd.read_csv(CSV_PATH)
    df.loc[len(df)] = [data.get(c, "") for c in COLUMNS]
    df.to_csv(CSV_PATH, index=False)

# -------------------------
# Translator & TTS helpers
# -------------------------
translator = GoogleTranslator(source="en", target="ta")

def translate_tamil(text):
    try:
        return translator.translate(text)
    except Exception:
        return ""

def tts_tamil(text):
    try:
        tts = gTTS(text=text, lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None

# -------------------------
# Legal Awareness Database (Expanded)
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் பிரிவு 66C / 66D — இணைய மோசடி மற்றும் அடையாள திருட்டு",
        "risk": "🔴 உயர் ஆபத்து (High Risk)",
        "content": (
            "📖 **விளக்கம்:** பிறரின் OTP, கடவுச்சொல், வங்கி விவரங்களை திருடி பயன்படுத்துவது குற்றம். "
            "இது ஆன்லைன் அடையாள திருட்டு மற்றும் இணைய மோசடியாகும்.\n\n"
            "📚 **எடுத்துக்காட்டு:** 'உங்கள் வங்கி கணக்கு முடக்கப்பட்டது, OTP அனுப்பவும்' போன்ற போலி இணைப்புகள்.\n\n"
            "⚖️ **தண்டனை:** 3 ஆண்டுகள் சிறை மற்றும் அபராதம்.\n\n"
            "🧭 **செய்ய வேண்டியது:** OTP/Password பகிர வேண்டாம்; வங்கி மற்றும் சைபர் போலீசில் புகார் செய்யவும்.\n\n"
            "📞 **Helpline:** 1930 - Tamil Nadu Cyber Helpline"
        ),
        "keywords": ["otp", "password", "account", "bank", "kyc", "phish", "hack", "fake", "link", "ஓடிபி", "ஹேக்", "கடவுச்சொல்"]
    },
    "420": {
        "section": "IPC பிரிவு 420 — மோசடி செயல் (Cheating and Fraud)",
        "risk": "🔴 உயர் ஆபத்து (High Risk)",
        "content": (
            "📖 **விளக்கம்:** பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றமாகும். இதில் போலி கடன் செயலிகள், லாட்டரி, "
            "வேலை வாய்ப்பு மோசடிகள், மற்றும் ஆன்லைன் பரிசு மோசடிகள் அடங்கும்.\n\n"
            "📚 **எடுத்துக்காட்டு:** ‘நீங்கள் ரூ.50,000 வென்றுள்ளீர்கள், பரிசுக்காக ₹5000 அனுப்பவும்’ என்ற போலி செய்திகள்.\n\n"
            "⚖️ **தண்டனை:** 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.\n\n"
            "🧭 **செய்ய வேண்டியது:** பணம் அனுப்பாதீர்கள்; அதிகாரப்பூர்வ தளங்களில் சரிபார்க்கவும்.\n\n"
            "📞 **Helpline:** 1930 - Tamil Nadu Cyber Helpline"
        ),
        "keywords": ["fraud", "scam", "cheated", "money", "loan", "lottery", "prize", "மோசடி", "ஏமாற்று", "பணம்", "கடன்"]
    },
    "354D": {
        "section": "IPC பிரிவு 354D — துரத்தல் மற்றும் தொந்தரவு (Stalking / Harassment)",
        "risk": "🟠 நடுத்தர ஆபத்து (Medium Risk)",
        "content": (
            "📖 **விளக்கம்:** ஒருவரை தொடர்ந்து தொடர்பு கொள்வது, மிரட்டுவது அல்லது அவமதிப்பது குற்றமாகும். "
            "இது ஆன்லைன் துரத்தல் (cyberstalking) ஆகும்.\n\n"
            "📚 **எடுத்துக்காட்டு:** ‘என்னுடன் பேசாவிட்டால் விளைவுகள் உண்டு’ என்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n\n"
            "⚖️ **தண்டனை:** 3 ஆண்டுகள் சிறை மற்றும் அபராதம் (IPC 354D).\n\n"
            "🧭 **செய்ய வேண்டியது:** ஆதாரங்களை (messages, screenshots) சேமித்து போலீசில் புகார் செய்யவும்.\n\n"
            "📞 **Helpline:** 1091 (Women Helpline) / 1930 (Cyber Crime)"
        ),
        "keywords": ["harass", "harassed", "harassment", "threat", "stalk", "blackmail", "molest", "abuse", "மிரட்டல்", "தொந்தரவு"]
    },
    "67": {
        "section": "IT Act 67 / 67A — அசிங்க உள்ளடக்கங்களை பகிர்தல்",
        "risk": "🔴 உயர் ஆபத்து (High Risk)",
        "content": (
            "📖 **விளக்கம்:** அசிங்க, பாலியல் அல்லது தனிப்பட்ட புகைப்படங்கள் மற்றும் வீடியோக்களை பகிர்தல் குற்றம்.\n\n"
            "📚 **எடுத்துக்காட்டு:** ஒருவரின் தனிப்பட்ட புகைப்படங்களை சமூக ஊடகங்களில் வெளியிடுதல்.\n\n"
            "⚖️ **தண்டனை:** முதல் முறையில் 3 ஆண்டுகள் சிறை மற்றும் அபராதம்; மீண்டும் செய்தால் அதிகமாகும்.\n\n"
            "🧭 **செய்ய வேண்டியது:** ஆதாரங்களை சேமித்து cybercrime.gov.in இல் புகார் செய்யவும்.\n\n"
            "📞 **Helpline:** 1930 - Cyber Helpline"
        ),
        "keywords": ["nude", "leak", "video", "photo", "porn", "அசிங்க", "புகைப்படம்", "வீடியோ"]
    }
}

# -------------------------
# Section Detection
# -------------------------
def detect_sections(text):
    t = text.lower()
    found = []
    for k, v in LEGAL_DB.items():
        for kw in v["keywords"]:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', t):
                found.append(v)
                break
    return found

# -------------------------
# App UI
# -------------------------
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False

st.markdown("### ✉️ Enter an English message below:")
english_text = st.text_area("", height=100)

if st.button("Translate ➜ Tamil & Analyze"):
    if not english_text.strip():
        st.warning("Please enter text.")
    else:
        tamil_text = translate_tamil(english_text)
        st.subheader("🈶 Tamil Translation:")
        st.success(tamil_text)

        audio = tts_tamil(tamil_text)
        if audio: st.audio(audio, format="audio/mp3")

        results = detect_sections(english_text)
        st.divider()
        st.subheader("⚖️ Legal Awareness (தமிழில்):")

        if results:
            for info in results:
                st.markdown(f"### {info['section']}")
                st.markdown(info["risk"])
                st.markdown(info["content"])
                st.markdown("---")

                audio_legal = tts_tamil(info["section"] + ". " + re.sub(r'\*\*|\#', '', info["content"]))
                if audio_legal:
                    st.audio(audio_legal, format="audio/mp3")
        else:
            st.info("✅ எந்தச் சட்டப்பிரிவும் கண்டறியப்படவில்லை.")

        st.session_state.show_feedback = True

# -------------------------
# Feedback
# -------------------------
if st.session_state.show_feedback:
    st.divider()
    st.subheader("🗣️ பயனர் கருத்து (User Feedback)")
    col1, col2 = st.columns(2)
    if col1.button("✅ Understand"):
        save_feedback({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input_english": english_text,
            "tamil_translation": tamil_text,
            "detected_sections": " | ".join([r['section'] for r in detect_sections(english_text)]),
            "feedback": "Understand"
        })
        st.success("✅ Feedback saved successfully.")

    if col2.button("❌ Not Understand"):
        st.session_state.show_feedback_options = True

    if "show_feedback_options" in st.session_state and st.session_state.show_feedback_options:
        st.markdown("### 😕 எது புரியவில்லை?")
        c1, c2, c3 = st.columns(3)
        for opt, label in zip(["Text", "Voice", "Both"], ["📝 Text", "🔊 Voice", "🔁 Both"]):
            if locals()[f"c{['Text','Voice','Both'].index(opt)+1}"].button(label):
                save_feedback({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "input_english": english_text,
                    "tamil_translation": tamil_text,
                    "detected_sections": " | ".join([r['section'] for r in detect_sections(english_text)]),
                    "feedback": "Not Understand",
                    "feedback_detail": opt
                })
                st.success(f"✅ Feedback saved successfully ({opt}).")
                st.session_state.show_feedback_options = False

st.caption("Data stored in user_feedback.csv")


















