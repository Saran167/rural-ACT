# -*- coding: utf-8 -*-
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import re, os

# ---------------------------------
# Page Setup
# ---------------------------------
st.set_page_config(page_title="Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("🛡️ Tamil Legal Awareness Translator")
st.caption("Enter English → Get Tamil Translation + Voice + Legal Awareness + Feedback")

# ---------------------------------
# Feedback CSV Setup
# ---------------------------------
FEEDBACK_CSV = "user_feedback.csv"
FEEDBACK_COLUMNS = ["timestamp","input_english","tamil_translation","detected_sections","feedback","feedback_detail"]

def ensure_feedback_csv():
    if not os.path.exists(FEEDBACK_CSV):
        pd.DataFrame(columns=FEEDBACK_COLUMNS).to_csv(FEEDBACK_CSV, index=False)

def append_feedback(row):
    ensure_feedback_csv()
    try:
        df = pd.read_csv(FEEDBACK_CSV)
    except Exception:
        df = pd.DataFrame(columns=FEEDBACK_COLUMNS)
    full_row = {col: row.get(col, "") for col in FEEDBACK_COLUMNS}
    df.loc[len(df)] = full_row
    df.to_csv(FEEDBACK_CSV, index=False)

ensure_feedback_csv()

# ---------------------------------
# Legal Database (Expanded, Line by Line)
# ---------------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "தகவல் தொழில்நுட்பச் சட்டம் 66C / 66D",
        "ta_explanation": (
            "66C: பிறரின் அடையாளத்தை (password, OTP, account) திருடி பயன்படுத்துவது குற்றமாகும்.\n"
            "66D: இணையத்தில் வேறொருவராக நடித்து மோசடி செய்வது (phishing, fake links, OTP கேட்பு).\n"
            "எடுத்துக்காட்டு: வங்கி OTP கேட்டு பணம் எடுத்தல், போலி KYC இணைப்புகள்.\n"
            "செய்ய வேண்டியது: OTP/Password பகிர வேண்டாம்; உடனே வங்கி மற்றும் சைபர் போலீசில் புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2023ல் போலி OTP மூலம் ரூ.1.5 லட்சம் மோசடி – குற்றவாளி கைது."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "keywords": ["otp","password","phishing","fake","bank","kyc","hacked","hack","ஓடிபி","ஹேக்","கணக்கு"]
    },
    "420": {
        "section": "IPC பிரிவு 420 - மோசடி",
        "ta_explanation": (
            "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றமாகும்.\n"
            "இதில் advance fee scams, fake loan apps, lottery scams அடங்கும்.\n"
            "எடுத்துக்காட்டு: ‘நீங்கள் வெற்றி பெற்றீர்கள் — பரிசுக்காக 5000 அனுப்பவும்’ அல்லது போலி அரசு அழைப்பு மூலம் பணம் கேட்பது.\n"
            "செய்ய வேண்டியது: பணம் அனுப்பாதீர்கள்; அதிகாரப்பூர்வ தளத்தைச் சோதிக்கவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2022ல் போலி கடன் செயலி மூலம் ரூ.2 லட்சம் மோசடி."
        ),
        "ta_punishment": "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["scam","fraud","cheat","money","loan","lottery","prize","rupees","payment","மோசடி","ஏமாற்று","பணம்"]
    },
    "406": {
        "section": "IPC பிரிவு 406 - நம்பிக்கை மீறல் (Criminal Breach of Trust)",
        "ta_explanation": (
            "நம்பிக்கையுடன் ஒப்படைக்கப்பட்ட சொத்தை தவறாக பயன்படுத்துதல் குற்றம்.\n"
            "எடுத்துக்காட்டு: கடன் வாங்கி திருப்பாதல் அல்லது ஒப்படைக்கப்பட்ட பொருட்களை திருடல்.\n"
            "செய்ய வேண்டியது: ஆதாரங்கள் வைத்திருங்கள்; போலீஸில் புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2021ல் நம்பிக்கை மீறல் வழக்கில் தொழிலதிபர் கைது."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "keywords": ["breach","trust","loan","did not return","misuse","embezzle","திருப்பவில்லை","நம்பிக்கை"]
    },
    "354D": {
        "section": "IPC பிரிவு 354D - துரத்தல் / தொந்தரவு (Stalking/Harassment)",
        "ta_explanation": (
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.\n"
            "எடுத்துக்காட்டு: ‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n"
            "செய்ய வேண்டியது: அனைத்து ஆதாரங்களையும் (screenshots, chat logs) சேமிக்கவும்; சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2024ல் Chennaiயில் cyberstalking செய்த நபர் கைது."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["harass","harassed","harassment","stalk","threat","blackmail","மிரட்டி","துன்புறுத்து","தொடர்ந்து"]
    },
    "67": {
        "section": "IT Act பிரிவு 67 / 67A - அசிங்க உள்ளடக்க பகிர்வு",
        "ta_explanation": (
            "அனுமதி இல்லாமல் பாலியல்/அசிங்க உள்ளடக்கங்களை பகிர்வது குற்றம்.\n"
            "எடுத்துக்காட்டு: தனிப்பட்ட புகைப்படம் அல்லது வீடியோவை சமூக ஊடகங்களில் பகிர்தல்.\n"
            "செய்ய வேண்டியது: ஆதாரங்களை சேமிக்கவும்; சைபர் போலீசில் புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2023ல் தனிப்பட்ட வீடியோவை வெளியிட்ட நபர் கைது."
        ),
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் சிறை மற்றும் அபராதம்; மீண்டும் செய்தால் அதிக தண்டனை.",
        "keywords": ["nude","photo","leak","video","obscene","அசிங்க","புகைப்படம்","வீடியோ"]
    }
}

# ---------------------------------
# Helpers
# ---------------------------------
translator = GoogleTranslator(source='en', target='ta')

def translate_to_tamil(text):
    try:
        return translator.translate(text)
    except Exception:
        return ""

def tts_tamil_audio(text):
    try:
        tts = gTTS(text=text, lang='ta')
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None

def detect_legal_sections(text):
    found = []
    t = text.lower()
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if re.search(r"\b" + re.escape(kw.lower()) + r"\b", t):
                found.append((key, info))
                break
    return found

# ---------------------------------
# Streamlit App Logic
# ---------------------------------
if "show_detail_buttons" not in st.session_state:
    st.session_state.show_detail_buttons = False

st.markdown("#### ➤ Enter English sentence:")
english_text = st.text_area("", height=100)

if st.button("Translate → Tamil & Analyze"):
    if not english_text.strip():
        st.warning("Please enter text.")
    else:
        tamil_text = translate_to_tamil(english_text)
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_text)
        audio = tts_tamil_audio(tamil_text)
        if audio: st.audio(audio, format="audio/mp3")

        matches = detect_legal_sections(english_text)
        st.divider()
        st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")

        if matches:
            for key, info in matches:
                st.markdown(f"### {info['section']}")
                st.text(info["ta_explanation"])
                st.text(info["ta_punishment"])
                # Tamil voice for legal text
                legal_audio = tts_tamil_audio(info["ta_explanation"] + " " + info["ta_punishment"])
                if legal_audio:
                    st.audio(legal_audio, format="audio/mp3")
                st.write("---")
        else:
            st.info("✅ இந்த செய்திக்கு தொடர்புடைய சட்டப் பகுதி கண்டறியப்படவில்லை.")

        # Save translation session
        st.session_state["last_input"] = english_text
        st.session_state["last_tamil"] = tamil_text
        st.session_state["last_sections"] = [k for k, _ in matches]
        st.session_state.show_detail_buttons = False

# ---------------------------------
# Feedback Section
# ---------------------------------
st.divider()
st.subheader("🗣️ பயனர் கருத்து (User Feedback)")

if "last_input" in st.session_state:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Understand"):
            append_feedback({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "input_english": st.session_state["last_input"],
                "tamil_translation": st.session_state["last_tamil"],
                "detected_sections": ",".join(st.session_state["last_sections"]),
                "feedback": "Understand",
                "feedback_detail": ""
            })
            st.success("✅ Feedback saved successfully.")
    with c2:
        if st.button("❌ Not Understand"):
            st.session_state.show_detail_buttons = True

    if st.session_state.show_detail_buttons:
        st.markdown("### 😕 எது புரியவில்லை?")
        d1, d2, d3 = st.columns(3)
        if d1.button("📝 Text"):
            append_feedback({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             "input_english": st.session_state["last_input"],
                             "tamil_translation": st.session_state["last_tamil"],
                             "detected_sections": ",".join(st.session_state["last_sections"]),
                             "feedback": "Not Understand","feedback_detail": "Text"})
            st.success("✅ Feedback saved successfully.")
            st.session_state.show_detail_buttons = False
        if d2.button("🔊 Voice"):
            append_feedback({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             "input_english": st.session_state["last_input"],
                             "tamil_translation": st.session_state["last_tamil"],
                             "detected_sections": ",".join(st.session_state["last_sections"]),
                             "feedback": "Not Understand","feedback_detail": "Voice"})
            st.success("✅ Feedback saved successfully.")
            st.session_state.show_detail_buttons = False
        if d3.button("🔁 Both"):
            append_feedback({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             "input_english": st.session_state["last_input"],
                             "tamil_translation": st.session_state["last_tamil"],
                             "detected_sections": ",".join(st.session_state["last_sections"]),
                             "feedback": "Not Understand","feedback_detail": "Both"})
            st.success("✅ Feedback saved successfully.")
            st.session_state.show_detail_buttons = False
else:
    st.info("Translate something first before giving feedback.")

st.markdown("---")
st.caption("Developed for rural users — English ➜ Tamil translation, Tamil voice, Legal awareness, and Smart Feedback.")





















