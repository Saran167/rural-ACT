# ==============================================
# 🌾 RURAL ACT - Tamil Legal Awareness Translator (Final)
# ==============================================

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import re
import os

# ----------------------------------------------
# PAGE CONFIG
# ----------------------------------------------
st.set_page_config(page_title="Rural ACT - Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Rural ACT: Tamil Legal Awareness Translator")
st.caption("English ➜ Tamil Translation • Voice Output • Legal Awareness • Smart Feedback")

# ----------------------------------------------
# FEEDBACK STORAGE SETUP
# ----------------------------------------------
FEEDBACK_FILE = "user_feedback.csv"
COLUMNS = ["timestamp", "english_input", "tamil_translation", "detected_sections", "feedback", "feedback_detail"]

if not os.path.exists(FEEDBACK_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(FEEDBACK_FILE, index=False)

def save_feedback(data):
    df = pd.read_csv(FEEDBACK_FILE)
    df.loc[len(df)] = data
    df.to_csv(FEEDBACK_FILE, index=False)

# ----------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------
def translate_to_tamil(text):
    try:
        return GoogleTranslator(source="en", target="ta").translate(text)
    except:
        return ""

def make_tts(text):
    """Convert Tamil text to speech bytes"""
    try:
        tts = gTTS(text=text, lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except:
        return None

def section_audio_text(section):
    """Combine law explanation as full Tamil text for voice"""
    combined = (
        f"{section['section']}.\n"
        f"விளக்கம்: {section['ta_explanation']}.\n"
        f"தண்டனை: {section['ta_punishment']}.\n"
        f"ஆபத்து நிலை: {section['risk_level']}.\n"
        f"செய்ய வேண்டியது: {section['action_plan']}.\n"
        f"தொடர்பு: {section['helpline']}.\n"
        f"உதாரணம்: {section['case_example']}"
    )
    return combined

# ----------------------------------------------
# LEGAL DATABASE
# ----------------------------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் 66C / 66D",
        "ta_explanation": "OTP, password, account details திருடி வேறொருவராக நடிப்பது குற்றம்.",
        "ta_punishment": "3 ஆண்டுகள் சிறை மற்றும் அபராதம்.",
        "risk_level": "🔴 High (Cyber Fraud)",
        "action_plan": "வங்கியில் உடனடியாக தொடர்புகொண்டு OTP பகிர வேண்டாம்; www.cybercrime.gov.in இல் புகார் செய்யவும்.",
        "helpline": "📞 1930 - Tamil Nadu Cyber Helpline",
        "case_example": "2023ல் போலி OTP மூலம் ரூ.1.5 லட்சம் மோசடி – குற்றவாளி கைது.",
        "keywords": ["otp","password","bank","phish","fake link","kyc","ஹேக்","ஓடிபி","கடவுச்சொல்"]
    },
    "420": {
        "section": "IPC பிரிவு 420 – மோசடி மற்றும் ஏமாற்றல்",
        "ta_explanation": "போலி வேலை, லாட்டரி அல்லது பரிசு மூலம் பணம் கேட்பது குற்றம்.",
        "ta_punishment": "7 ஆண்டுகள் சிறை மற்றும் அபராதம்.",
        "risk_level": "🔴 High (Financial Fraud)",
        "action_plan": "பணம் அனுப்ப வேண்டாம்; அதிகாரப்பூர்வ தளத்தை உறுதி செய்யவும்; புகார் அளிக்கவும்.",
        "helpline": "📞 1930 | 🌐 www.cybercrime.gov.in",
        "case_example": "2024ல் சென்னையில் போலி பரிசு மெசேஜ் மூலம் 12 பேரிடம் மோசடி செய்தவர் கைது.",
        "keywords": ["scam","cheat","fraud","lottery","money","payment","மோசடி","ஏமாற்று","பணம்"]
    },
    "406": {
        "section": "IPC பிரிவு 406 – நம்பிக்கை மீறல் (Breach of Trust)",
        "ta_explanation": "பிறர் நம்பிக்கையை தவறாக பயன்படுத்தி சொத்து அல்லது பணத்தை கையாடல் செய்தல் குற்றம்.",
        "ta_punishment": "3 ஆண்டுகள் சிறை அல்லது அபராதம்.",
        "risk_level": "🟡 Medium",
        "action_plan": "எழுத்துப்பூர்வ ஒப்பந்தங்களை வைத்திருங்கள்; சட்ட ஆலோசனை பெறவும்.",
        "helpline": "📞 1930",
        "case_example": "2022ல் கடன் திருப்பாதவர் மீது 406 பிரிவில் வழக்கு பதிவு செய்யப்பட்டது.",
        "keywords": ["trust","loan","breach","embezzle","திருப்பவில்லை","நம்பிக்கை"]
    },
    "354D": {
        "section": "IPC பிரிவு 354D – தொந்தரவு / சைபர் துரத்தல்",
        "ta_explanation": "ஒருவரை அடிக்கடி மிரட்டுதல், ஆன்லைனில் தொந்தரவு செய்தல் குற்றம்.",
        "ta_punishment": "3 முதல் 5 ஆண்டுகள் சிறை மற்றும் அபராதம்.",
        "risk_level": "🔴 High (Cyber Harassment)",
        "action_plan": "எல்லா ஆதாரங்களையும் சேமிக்கவும்; உடனே cybercrime.gov.in இல் புகார் அளிக்கவும்.",
        "helpline": "📞 1930 | 🌐 www.cybercrime.gov.in",
        "case_example": "2024ல் சமூக ஊடகத்தில் தொந்தரவு செய்தவர் கைது – 3 ஆண்டுகள் சிறை.",
        "keywords": ["harass","stalk","threat","blackmail","abuse","மிரட்டி","அச்சுறுத்து","தொடர்ந்து"]
    },
    "67": {
        "section": "IT Act 67 / 67A – அசிங்க உள்ளடக்கம் பகிர்வு",
        "ta_explanation": "அசிங்கமான புகைப்படம், வீடியோ பகிர்தல் குற்றம்.",
        "ta_punishment": "3 ஆண்டுகள் சிறை; மீண்டும் செய்தால் அதிக தண்டனை.",
        "risk_level": "🔴 High",
        "action_plan": "ஆதாரங்களை சேமித்து cyber cell-ல் புகார் செய்யவும்.",
        "helpline": "📞 1930",
        "case_example": "2023ல் தனிப்பட்ட வீடியோ வெளியிட்டவர் கைது.",
        "keywords": ["nude","porn","video","leak","அசிங்க","புகைப்படம்"]
    },
    "509": {
        "section": "IPC பிரிவு 509 – பெண்களை அவமதித்தல்",
        "ta_explanation": "பெண்களை அவமதிக்கும் வார்த்தைகள் அல்லது செய்திகளை அனுப்புதல் குற்றம்.",
        "ta_punishment": "1 ஆண்டு சிறை மற்றும் அபராதம்.",
        "risk_level": "🟡 Medium",
        "action_plan": "அந்த தகவலை evidence-ஆக வைத்துக்கொண்டு புகார் செய்யவும்.",
        "helpline": "📞 1930",
        "case_example": "2023ல் obscene voice message அனுப்பியவர் 509 பிரிவில் கைது.",
        "keywords": ["abuse","insult","vulgar","voice message","அவமதிப்பு","சொல்"]
    },
    "43A": {
        "section": "IT Act 43A – தரவு பாதுகாப்பு மீறல்",
        "ta_explanation": "தனிப்பட்ட தரவை அனுமதி இல்லாமல் பகிர்தல் குற்றம்.",
        "ta_punishment": "அபராதம் மற்றும் நஷ்ட ஈடு வழங்க வேண்டும்.",
        "risk_level": "🟢 Low",
        "action_plan": "தரவை பகிரும் முன் அனுமதி பெறவும்; privacy policy பின்பற்றவும்.",
        "helpline": "🌐 www.meity.gov.in",
        "case_example": "2022ல் data leak செய்த நிறுவனம் மீது 43A பிரிவில் நடவடிக்கை.",
        "keywords": ["data","privacy","leak","share","தரவு","பகிர்வு"]
    }
}

# ----------------------------------------------
# DETECT SECTIONS
# ----------------------------------------------
def detect_laws(text):
    found = []
    for key, info in LEGAL_DB.items():
        for word in info["keywords"]:
            if re.search(rf"\b{re.escape(word.lower())}\b", text.lower()):
                found.append(info)
                break
    return found

# ----------------------------------------------
# UI INPUT SECTION
# ----------------------------------------------
english_text = st.text_area("✉️ Enter English message:", height=120, placeholder="Type or paste English text here...")

if st.button("Translate & Analyze"):
    if not english_text.strip():
        st.warning("Please enter some text.")
    else:
        tamil_text = translate_to_tamil(english_text)
        st.subheader("🈶 Tamil Translation:")
        st.success(tamil_text)

        trans_audio = make_tts(tamil_text)
        if trans_audio:
            st.audio(trans_audio, format="audio/mp3", start_time=0)
        else:
            st.error("Unable to generate Tamil audio.")

        # detect legal sections
        matched = detect_laws(english_text)
        st.divider()
        st.subheader("⚖️ Legal Awareness (தமிழில்):")

        if matched:
            for section in matched:
                st.markdown(f"### {section['section']}")
                st.write(f"**விளக்கம்:** {section['ta_explanation']}")
                st.write(f"**தண்டனை:** {section['ta_punishment']}")
                st.write(f"**ஆபத்து நிலை:** {section['risk_level']}")
                st.write(f"**🧭 என்ன செய்யலாம்:** {section['action_plan']}")
                st.write(f"**📞 Helpline:** {section['helpline']}")
                st.write(f"**📚 எடுத்துக்காட்டு:** {section['case_example']}")
                st.write("---")

                # voice for each section
                if st.button(f"🎧 Play Legal Voice – {section['section']}"):
                    audio_text = section_audio_text(section)
                    voice = make_tts(audio_text)
                    if voice:
                        st.audio(voice, format="audio/mp3", start_time=0)
                    else:
                        st.warning("Audio generation failed.")
        else:
            st.info("✅ No related legal section detected for this message.")

        # store session info
        st.session_state.last_eng = english_text
        st.session_state.last_tam = tamil_text
        st.session_state.last_sections = [s["section"] for s in matched]

# ----------------------------------------------
# FEEDBACK SYSTEM
# ----------------------------------------------
st.divider()
st.subheader("🗣️ User Feedback")

if "last_eng" in st.session_state:
    col1, col2 = st.columns(2)
    if col1.button("✅ Understand"):
        save_feedback([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            st.session_state.last_eng,
            st.session_state.last_tam,
            ", ".join(st.session_state.last_sections),
            "Understand",
            ""
        ])
        st.success("✅ Feedback saved successfully.")

    if col2.button("❌ Not Understand"):
        st.session_state.detail_mode = True

    if st.session_state.get("detail_mode", False):
        st.markdown("### 😕 What part was unclear?")
        b1, b2, b3 = st.columns(3)
        if b1.button("📝 Text"):
            detail = "Text"
        elif b2.button("🔊 Voice"):
            detail = "Voice"
        elif b3.button("🔁 Both"):
            detail = "Both"
        else:
            detail = None

        if detail:
            save_feedback([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                st.session_state.last_eng,
                st.session_state.last_tam,
                ", ".join(st.session_state.last_sections),
                "Not Understand",
                detail
            ])
            st.success(f"✅ Feedback saved successfully ({detail}).")
            st.session_state.detail_mode = False

else:
    st.info("Translate a message first to give feedback.")

st.markdown("---")
st.caption("All feedback saved in user_feedback.csv (Streamlit Cloud → Files tab).")















