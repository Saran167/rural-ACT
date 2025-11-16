# -------------------------------
#   RURAL ACT – FINAL WORKING APP
# -------------------------------

import streamlit as st
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import requests
import re
import os


# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="Tamil Legal Awareness Translator", page_icon="⚖️", layout="centered")
st.title("🛡️ Tamil Legal Awareness Translator")
st.caption("Enter English → Get Tamil Translation + Voice + Legal Awareness + Feedback")


# ------------------------------------------------------
# FEEDBACK CSV SETUP
# ------------------------------------------------------
FEEDBACK_CSV = "user_feedback.csv"
COLUMNS = ["timestamp", "english_input", "tamil_output", "sections", "feedback", "type"]

def ensure_csv():
    if not os.path.exists(FEEDBACK_CSV):
        pd.DataFrame(columns=COLUMNS).to_csv(FEEDBACK_CSV, index=False)

def save_feedback(row):
    ensure_csv()
    try:
        df = pd.read_csv(FEEDBACK_CSV)
    except:
        df = pd.DataFrame(columns=COLUMNS)

    new_row = {col: row.get(col, "") for col in COLUMNS}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FEEDBACK_CSV, index=False)


ensure_csv()


# ------------------------------------------------------
# LEGAL DATABASE
# ------------------------------------------------------
LEGAL_DB = {
    "354D": {
        "section": "IPC பிரிவு 354D - துரத்தல் / தொந்தரவு (Stalking / Harassment)",
        "explanation": (
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், மிரட்டல் அனுப்புதல்—all are punishable.\n"
            "எடுத்துக்காட்டு: 'நீ பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்' என்று மிரட்டுதல்.\n"
            "செய்ய வேண்டியது: screenshots & chat logs சேமிக்கவும்; உடனே சைபர் போலீசில் புகார் செய்யவும்."
        ),
        "punishment": "3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["harass", "harassed", "harassment", "stalk", "stalking", "threat", "threaten", "blackmail"]
    },

    "420": {
        "section": "IPC பிரிவு 420 - மோசடி",
        "explanation": (
            "பிறரை ஏமாற்றி பணம்/சொத்தைப் பெறுதல் குற்றம்.\n"
            "எடுத்துக்காட்டு: 'நீங்கள் வென்றுள்ளீர்கள்—₹5000 அனுப்பவும்' போன்ற மோசடிகள்.\n"
            "செய்ய வேண்டியது: பணம் அனுப்ப வேண்டாம்; bank/cybercrime இணையத்தில் புகார் செய்யவும்."
        ),
        "punishment": "7 ஆண்டுகள் சிறை + அபராதம்.",
        "keywords": ["fraud", "scam", "scammed", "prize", "lottery", "money", "loan", "send money"]
    },

    "66C/66D": {
        "section": "IT Act 66C/66D - அடையாள திருட்டு & இணைய மோசடி",
        "explanation": (
            "OTP/Password/Account details திருடி வேறொருவராக நடிப்பது குற்றம்.\n"
            "எடுத்துக்காட்டு: போலி bank OTP calls, fake KYC links.\n"
            "செய்ய வேண்டியது: OTP பகிர வேண்டாம்; 1930 அழைக்கவும்; cybercrime.gov.in இல் புகார் செய்யவும்."
        ),
        "punishment": "3 ஆண்டுகள் சிறை + அபராதம்.",
        "keywords": ["otp", "password", "bank link", "verify", "account", "kyc", "phishing"]
    },

    "67": {
        "section": "IT Act 67 - அசிங்க உள்ளடக்கம் பகிர்தல்",
        "explanation": (
            "அசிங்க/தனிப்பட்ட புகைப்படம் அனுமதி இல்லாமல் பகிர்வது குற்றம்.\n"
            "எடுத்துக்காட்டு: personal photos leak.\n"
            "செய்ய வேண்டியது: evidence சேமிக்கவும்; cyber police புகார் செய்யவும்."
        ),
        "punishment": "3 ஆண்டுகள் சிறை + அபராதம்.",
        "keywords": ["nude", "leak", "obscene", "private photo"]
    }
}


# ------------------------------------------------------
# TRANSLATION FUNCTION (Google + LibreTranslate fallback)
# ------------------------------------------------------
def translate_to_tamil(text):

    # 1️⃣ Google Translator via deep-translator
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source='en', target='ta').translate(text)
        if translated:
            return translated
    except:
        pass

    # 2️⃣ LibreTranslate fallback (always works)
    try:
        url = "https://libretranslate.de/translate"
        payload = {
            "q": text,
            "source": "en",
            "target": "ta"
        }
        res = requests.post(url, data=payload)
        return res.json()["translatedText"]
    except:
        return None


# ------------------------------------------------------
# TAMIL VOICE FUNCTION
# ------------------------------------------------------
def tamil_voice(text):
    try:
        tts = gTTS(text=text, lang="ta")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        return buffer.getvalue()
    except:
        return None


# ------------------------------------------------------
# DETECT LEGAL SECTIONS
# ------------------------------------------------------
def detect_sections(text):
    text_low = text.lower()
    found = []
    for sec, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if re.search(r"\b" + re.escape(kw.lower()) + r"\b", text_low):
                found.append(sec)
                break
    return found


# ------------------------------------------------------
# MAIN UI
# ------------------------------------------------------
input_text = st.text_area("➤ Enter English sentence:")

if st.button("Translate & Analyze"):

    if not input_text.strip():
        st.error("Please enter some text.")
    else:
        tam = translate_to_tamil(input_text)

        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        if tam:
            st.success(tam)
        else:
            st.error("⚠️ Translation temporarily unavailable.")

        st.subheader("🔊 Tamil Voice:")
        if tam:
            audio = tamil_voice(tam)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")
        else:
            st.info("Voice available only after successful translation.")

        # LEGAL AWARENESS
        st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")
        sec_list = detect_sections(input_text)

        if sec_list:
            for sec in sec_list:
                db = LEGAL_DB[sec]
                st.markdown(f"### {db['section']}")
                st.write(db["explanation"])
                st.write(f"**தண்டனை:** {db['punishment']}")
                st.markdown("---")
        else:
            st.info("இந்த தகவலில் சட்ட மீறல் கண்டறியப்படவில்லை.")

        st.session_state["last_eng"] = input_text
        st.session_state["last_tam"] = tam
        st.session_state["last_sec"] = ", ".join(sec_list)


# ------------------------------------------------------
# FEEDBACK SECTION
# ------------------------------------------------------
st.subheader("🗣️ User Feedback")

if "last_eng" in st.session_state:

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Understand"):
            save_feedback({
                "timestamp": datetime.now(),
                "english_input": st.session_state["last_eng"],
                "tamil_output": st.session_state["last_tam"],
                "sections": st.session_state["last_sec"],
                "feedback": "Understand",
                "type": ""
            })
            st.success("Feedback saved successfully ✔️")

    with col2:
        if st.button("❌ Not Understand"):
            st.session_state["detail"] = True

    if st.session_state.get("detail", False):
        d1, d2, d3 = st.columns(3)

        with d1:
            if st.button("📝 Text"):
                save_feedback({
                    "timestamp": datetime.now(),
                    "english_input": st.session_state["last_eng"],
                    "tamil_output": st.session_state["last_tam"],
                    "sections": st.session_state["last_sec"],
                    "feedback": "Not Understand",
                    "type": "Text"
                })
                st.success("Feedback saved ✔️")
                st.session_state["detail"] = False

        with d2:
            if st.button("🔊 Voice"):
                save_feedback({
                    "timestamp": datetime.now(),
                    "english_input": st.session_state["last_eng"],
                    "tamil_output": st.session_state["last_tam"],
                    "sections": st.session_state["last_sec"],
                    "feedback": "Not Understand",
                    "type": "Voice"
                })
                st.success("Feedback saved ✔️")
                st.session_state["detail"] = False

        with d3:
            if st.button("🔁 Both"):
                save_feedback({
                    "timestamp": datetime.now(),
                    "english_input": st.session_state["last_eng"],
                    "tamil_output": st.session_state["last_tam"],
                    "sections": st.session_state["last_sec"],
                    "feedback": "Not Understand",
                    "type": "Both"
                })
                st.success("Feedback saved ✔️")
                st.session_state["detail"] = False
else:
    st.info("Translate something above to give feedback.")


























