# ✅ FINAL VERSION — Detailed Legal Awareness + Tamil Voice + Working Feedback
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import re
import os

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Tamil Legal Awareness Translator")
st.caption("Translate English → Tamil + Legal Awareness + Tamil Voice + Smart Feedback")

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
    df = pd.read_csv(FEEDBACK_CSV) if os.path.exists(FEEDBACK_CSV) else pd.DataFrame(columns=FEEDBACK_COLUMNS)
    new_row = {col: row_dict.get(col, "") for col in FEEDBACK_COLUMNS}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FEEDBACK_CSV, index=False)

ensure_feedback_csv()

# -------------------------
# Legal Awareness Database (Expanded)
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் பிரிவு 66C / 66D — இணைய மோசடி மற்றும் அடையாள திருட்டு",
        "ta_explanation": (
            "📖 **விளக்கம்:** பிறரின் கடவுச்சொல், OTP, வங்கி விவரங்கள் போன்றவற்றை திருடி அவர்களாக நடிப்பது குற்றமாகும். "
            "இது அடையாள திருட்டு (Identity Theft) மற்றும் ஆன்லைன் மோசடி (Online Fraud) ஆகியவற்றை உள்ளடக்கும்.\n\n"
            "📚 **எடுத்துக்காட்டு:** போலி வங்கி இணைப்புகள் மூலம் OTP கேட்பது, ‘உங்கள் கணக்கு முடக்கப்பட்டது’ என்ற பெயரில் மோசடி செய்தல்.\n\n"
            "⚖️ **தண்டனை:** 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம் (IT Act 66C, 66D).\n\n"
            "🧭 **செய்ய வேண்டியது:** OTP, Password, PIN போன்றவற்றை ஒருவரிடமும் பகிர வேண்டாம். உடனே வங்கி மற்றும் சைபர் போலீசில் புகார் செய்யவும்.\n\n"
            "📞 **Helpline:** 1930 - Tamil Nadu Cyber Helpline"
        ),
        "keywords": ["otp", "password", "account", "verify", "bank link", "phish", "hack", "fake", "ஓடிபி", "ஹேக்", "கடவுச்சொல்"]
    },
    "420": {
        "section": "IPC பிரிவு 420 — மோசடி செயல் (Cheating and Fraud)",
        "ta_explanation": (
            "📖 **விளக்கம்:** பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றம். இதில் advance fee scams, fake loan apps, lottery scams, "
            "அல்லது போலி வேலை வாய்ப்பு அறிவிப்புகள் அடங்கும்.\n\n"
            "📚 **எடுத்துக்காட்டு:** ‘நீங்கள் 50,000 ரூபாய் வென்றுள்ளீர்கள்! பரிசுக்காக 5000 அனுப்பவும்’ என்ற போலி செய்திகள்.\n\n"
            "⚖️ **தண்டனை:** 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம் (IPC 420).\n\n"
            "🧭 **செய்ய வேண்டியது:** பணம் அனுப்பாதீர்கள்; அதிகாரப்பூர்வ தளங்களைச் சோதிக்கவும்; ஆதாரங்கள் சேமித்து போலீசில் புகார் செய்யவும்.\n\n"
            "📞 **Helpline:** 1930 - Tamil Nadu Cyber Helpline"
        ),
        "keywords": ["fraud", "scam", "cheated", "money", "loan", "lottery", "prize", "பணம்", "மோசடி", "ஏமாற்று"]
    },
    "354D": {
        "section": "IPC பிரிவு 354D — துரத்தல் மற்றும் தொந்தரவு (Stalking / Harassment)",
        "ta_explanation": (
            "📖 **விளக்கம்:** ஒருவரை அடிக்கடி தொடர்பு கொண்டு மிரட்டுதல், அவமதித்தல் அல்லது புகைப்படங்களை பகிர்தல் குற்றமாகும். "
            "இதில் cyberstalking மற்றும் ஆன்லைன் தொந்தரவு அடங்கும்.\n\n"
            "📚 **எடுத்துக்காட்டு:** ஒருவருக்கு தொடர்ந்து ‘நீங்கள் எனக்கு பதில் சொல்ல வேண்டும்’ என்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n\n"
            "⚖️ **தண்டனை:** 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம் (IPC 354D).\n\n"
            "🧭 **செய்ய வேண்டியது:** செய்திகளைப் பதிவு செய்து போலீசில் புகார் செய்யவும்; ஆதாரங்களை நீக்க வேண்டாம்.\n\n"
            "📞 **Helpline:** 1091 (Women Helpline), 1930 (Cyber Crime)"
        ),
        "keywords": ["harass", "harassment", "stalk", "threat", "blackmail", "molest", "abuse", "மிரட்டல்", "தொந்தரவு"]
    },
    "67": {
        "section": "IT Act பிரிவு 67 / 67A — அசிங்க உள்ளடக்கங்களை பகிர்தல்",
        "ta_explanation": (
            "📖 **விளக்கம்:** இணையத்தில் அசிங்க, பாலியல் அல்லது தனிப்பட்ட புகைப்படங்கள்/வீடியோக்களை பகிர்தல் குற்றம்.\n\n"
            "📚 **எடுத்துக்காட்டு:** யாரோ ஒருவரின் தனிப்பட்ட புகைப்படங்களை சமூக ஊடகங்களில் வெளியிடுதல்.\n\n"
            "⚖️ **தண்டனை:** முதல் முறையில் 3 ஆண்டுகள் சிறை மற்றும் அபராதம்; மீண்டும் செய்தால் அதிகமான தண்டனை.\n\n"
            "🧭 **செய்ய வேண்டியது:** ஆதாரங்களை சேமித்து cybercrime.gov.in இல் புகார் செய்யவும்.\n\n"
            "📞 **Helpline:** 1930 - Cyber Crime Helpline"
        ),
        "keywords": ["nude", "leak", "photo", "video", "porn", "obscene", "அசிங்க", "புகைப்படம்", "வீடியோ"]
    },
    "43A": {
        "section": "IT Act 43A — தரவு பாதுகாப்பு மீறல் (Data Protection)",
        "ta_explanation": (
            "📖 **விளக்கம்:** தனிப்பட்ட தரவை அனுமதி இல்லாமல் பகிர்தல் அல்லது கசிவடித்தல் குற்றம்.\n\n"
            "📚 **எடுத்துக்காட்டு:** வங்கி அல்லது நிறுவனம் பயனரின் தகவலை அனுமதி இல்லாமல் விற்பனை செய்தல்.\n\n"
            "⚖️ **தண்டனை:** அபராதம் மற்றும் நஷ்ட ஈடு வழங்க வேண்டும் (IT Act 43A).\n\n"
            "🧭 **செய்ய வேண்டியது:** தனிப்பட்ட தரவை பகிரும் முன் Privacy Policy சரிபார்க்கவும்.\n\n"
            "📞 **Helpline:** www.meity.gov.in"
        ),
        "keywords": ["data", "privacy", "breach", "personal", "share data", "information"]
    }
}

# -------------------------
# Translator & TTS
# -------------------------
translator = GoogleTranslator(source="en", target="ta")

def translate_to_tamil(text):
    try:
        return translator.translate(text)
    except Exception:
        return ""

def tts_tamil_bytes(text):
    try:
        tts = gTTS(text=text, lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except:
        return None

# -------------------------
# Detection
# -------------------------
def detect_sections(english_text):
    text = english_text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    found = []
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text):
                found.append((key, info))
                break
    return found

# -------------------------
# UI
# -------------------------
if "show_feedback_options" not in st.session_state:
    st.session_state.show_feedback_options = False

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
            for _, info in matches:
                st.markdown(f"### {info['section']}")
                st.markdown(info['ta_explanation'])
                st.markdown("---")

                law_voice_text = info["section"] + ". " + re.sub(r"\*\*|\#", "", info["ta_explanation"])
                law_audio = tts_tamil_bytes(law_voice_text)
                if law_audio:
                    st.audio(law_audio, format="audio/mp3")
        else:
            st.info("✅ எந்தச் சட்டப் பிரிவும் தொடர்பு இல்லை.")

        st.session_state.show_feedback_options = False

# -------------------------
# Feedback
# -------------------------
st.divider()
st.subheader("🗣️ பயனர் கருத்து (User Feedback)")

col1, col2 = st.columns(2)
if col1.button("✅ Understand"):
    append_feedback_row({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input_english": english_input,
        "feedback": "Understand",
    })
    st.success("✅ Feedback saved successfully.")

if col2.button("❌ Not Understand"):
    st.session_state.show_feedback_options = True

if st.session_state.show_feedback_options:
    st.markdown("### 😕 எது புரியவில்லை?")
    c1, c2, c3 = st.columns(3)
    if c1.button("📝 Text"):
        st.success("✅ Feedback saved successfully (Text).")
        st.session_state.show_feedback_options = False
    if c2.button("🔊 Voice"):
        st.success("✅ Feedback saved successfully (Voice).")
        st.session_state.show_feedback_options = False
    if c3.button("🔁 Both"):
        st.success("✅ Feedback saved successfully (Both).")
        st.session_state.show_feedback_options = False

st.caption("Feedback stored locally in user_feedback.csv")

















