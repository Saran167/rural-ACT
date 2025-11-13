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
st.title("🛡️ Tamil Legal Awareness Translator")
st.caption("Enter English text → Tamil translation + voice → Legal awareness (Tamil) → Feedback")

# -------------------------
# Feedback CSV setup
# -------------------------
FEEDBACK_CSV = "user_feedback.csv"
FEEDBACK_COLUMNS = ["timestamp", "input_english", "tamil_translation", "detected_sections", "feedback", "feedback_detail"]

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
    df = pd.concat([df, pd.DataFrame([full_row])], ignore_index=True)
    df.to_csv(FEEDBACK_CSV, index=False)

ensure_feedback_csv()

# -------------------------
# Legal Awareness Database
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் 66C / 66D",
        "ta_explanation": (
            "66C: பிறரின் அடையாளத்தை (password, OTP, account) திருடி பயன்படுத்துவது குற்றம்.\n"
            "66D: இணையத்தில் வேறொருவராக நடித்து மோசடி செய்வது (phishing, fake links, OTP கேட்பு) குற்றம்.\n\n"
            "எடுத்துக்காட்டு: போலி வங்கி OTP கேட்டு பணம் எடுத்தல், போலி KYC/வங்கி இணைப்புகள் அனுப்புதல்.\n\n"
            "செய்ய வேண்டியது: OTP/Password ஒருவரிடம் பகிர வேண்டாம். உடனே வங்கி மற்றும் சைபர் போலீசில் புகார் செய்யவும்.\n\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2023ல் போலி OTP மூலம் ரூ.1.5 லட்சம் மோசடி – குற்றவாளி கைது."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் சிறை மற்றும் அபராதம்.",
        "keywords": ["otp", "password", "verify", "account", "phishing", "fake link", "kyc", "bank", "login"]
    },
    "420": {
        "section": "IPC பிரிவு 420 - மோசடி செயல்",
        "ta_explanation": (
            "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றம். இதில் advance fee scams, fake loan apps, lottery scams அடங்கும்.\n\n"
            "எடுத்துக்காட்டு: ‘நீங்கள் வெற்றி பெற்றீர்கள் — பரிசுக்காக 5000 அனுப்பவும்’ அல்லது போலி அரசு / வங்கி அழைப்பு மூலம் பணம் கேட்பது.\n\n"
            "செய்ய வேண்டியது: பணம் அனுப்பாதீர்கள்; அதிகாரப்பூர்வ தளத்தைச் சோதிக்கவும்; அனைத்து சான்றுகளையும் சேமிக்கவும்; போலீசில் புகார் செய்யவும்.\n\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline"
        ),
        "ta_punishment": "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["fraud", "scam", "cheat", "lottery", "loan", "money", "rupees", "payment", "மோசடி"]
    },
    "354D": {
        "section": "IPC பிரிவு 354D - துரத்தல்/தொந்தரவு (Stalking)",
        "ta_explanation": (
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் ஆகியவை குற்றமாகும்.\n\n"
            "எடுத்துக்காட்டு: ‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n\n"
            "செய்ய வேண்டியது: அனைத்து ஆதாரங்களையும் (screenshots, chat logs) சேமிக்கவும்; சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.\n\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2024ல் Chennaiயில் பெண்மணி மீது cyberstalking செய்த நபர் கைது."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["harass", "harassed", "harassment", "stalk", "stalking", "blackmail", "threat", "abuse"]
    },
    "67": {
        "section": "IT Act பிரிவு 67 / 67A - அசிங்க உள்ளடக்கம் பகிர்வு",
        "ta_explanation": (
            "பாலியல் அல்லது அசிங்க உள்ளடக்கங்களை இணையத்தில் பகிர்தல் அல்லது பரப்புதல் குற்றமாகும்.\n\n"
            "எடுத்துக்காட்டு: யாரோ ஒருவரின் நியூட் புகைப்படங்களை அனுமதி இல்லாமல் பகிர்தல் அல்லது பதிவிடுதல்.\n\n"
            "செய்ய வேண்டியது: உடனே ஆதாரங்களை சேமித்து cybercrime.gov.in தளத்தில் புகார் செய்யவும்.\n\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2023ல் obscene video share செய்த நபர் மீது 67A பிரிவில் நடவடிக்கை."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் சிறை மற்றும் அபராதம்.",
        "keywords": ["nude", "obscene", "leak", "video", "photo", "அசிங்க", "புகைப்படம்"]
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
# Keyword detection
# -------------------------
def detect_sections(english_text):
    text = english_text.lower()
    found = []
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text):
                found.append((key, info))
                break
    return found

# -------------------------
# Streamlit UI
# -------------------------
if "show_detail_buttons" not in st.session_state:
    st.session_state.show_detail_buttons = False

english_input = st.text_area("✍️ Enter English sentence:", height=120)

if st.button("Translate → Tamil & Analyze"):
    if not english_input.strip():
        st.warning("Please enter English text.")
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
                st.write("---")
        else:
            st.info("✅ எந்த சட்ட பிரிவும் கண்டறியப்படவில்லை.")

        # Store latest session data
        st.session_state.last_input = english_input
        st.session_state.last_translation = tamil_text
        st.session_state.detected_keys = [k for k, _ in matches]

# -------------------------
# Feedback Section (Fixed & Simple)
# -------------------------
st.divider()
st.subheader("🗣️ பயனர் கருத்து (User Feedback)")

if "last_input" in st.session_state and st.session_state.last_input:
    col1, col2 = st.columns(2)
    if col1.button("✅ Understand"):
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input_english": st.session_state.last_input,
            "tamil_translation": st.session_state.last_translation,
            "detected_sections": ",".join(st.session_state.detected_keys) if st.session_state.detected_keys else "",
            "feedback": "Understand",
            "feedback_detail": ""
        }
        append_feedback_row(row)
        st.success("✅ Feedback saved successfully.")

    if col2.button("❌ Not Understand"):
        st.session_state.show_detail_buttons = True

    if st.session_state.show_detail_buttons:
        st.markdown("### 😕 எது புரியவில்லை? (What was not clear?)")
        d1, d2, d3 = st.columns(3)

        if d1.button("📝 Text"):
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

        if d2.button("🔊 Voice"):
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

        if d3.button("🔁 Both"):
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
    st.info("Translate something first — then give feedback.")



















