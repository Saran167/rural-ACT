import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
import base64
import re
import requests
from datetime import datetime

st.set_page_config(page_title="Rural ACT", layout="wide")

# ---------------------------
# 1. TRANSLATION FUNCTION
# ---------------------------
def translate_text(text):
    text = text.strip()
    if not text:
        return ""

    # Method 1 — deep-translator
    try:
        return GoogleTranslator(source='en', target='ta').translate(text)
    except:
        pass

    # Method 2 — MyMemory API
    try:
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|ta"
        response = requests.get(url).json()
        if "responseData" in response:
            return response["responseData"]["translatedText"]
    except:
        pass

    # Method 3 — LibreTranslate API
    try:
        url = "https://libretranslate.de/translate"
        payload = {"q": text, "source": "en", "target": "ta"}
        response = requests.post(url, data=payload).json()
        if "translatedText" in response:
            return response["translatedText"]
    except:
        pass

    return None   # If all fail


# ---------------------------
# 2. TAMIL VOICE FUNCTION
# ---------------------------
def text_to_speech(tamil_text):
    try:
        tts = gTTS(tamil_text, lang='ta')
        audio_path = "voice.mp3"
        tts.save(audio_path)
        return audio_path
    except:
        return None


# ---------------------------
# 3. LEGAL AWARENESS ENGINE
# ---------------------------
def legal_section(text):
    text = text.lower()

    # Harassment / Stalking
    if any(w in text for w in ["harass", "stalk", "follow", "threat", "blackmail"]):
        return (
            "IPC பிரிவு 354D - துரத்தல் / தொந்தரவு (Stalking/Harassment)\n"
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய மிரட்டல் குற்றமாகும்.\n"
            "📞 உதவி எண்: 1930\n"
            "தண்டனை: 3 ஆண்டுகள் வரை சிறை + அபராதம்."
        )

    # OTP Fraud / Bank Fraud
    if any(w in text for w in ["otp", "bank", "account", "upi", "loan", "money", "verify"]):
        return (
            "IT Act 66C / 66D - ஆன்லைன் மோசடி & அடையாள திருட்டு\n"
            "OTP, கணக்கு எண், UPI PIN போன்ற தகவல் கேட்டால் அது மோசடி.\n"
            "📞 1930-ல் உடனடியாக புகார் செய்யவும்."
        )

    # Loan Scam / Money Scam
    if any(w in text for w in ["loan", "interest", "cash", "payment", "deposit"]):
        return (
            "IPC 420 - மோசடி (Cheating)\n"
            "பணம், லோன், டெபாசிட் கேட்கும் நபர்/அப் மோசடி செய்ய வாய்ப்பு.\n"
            "📞 1930-க்கு புகார் செய்யவும்."
        )

    return "தகவலின் அடிப்படையில் தெளிவான சட்ட பிரிவு இல்லை."


# ---------------------------
# 4. CSV SAVE FUNCTION
# ---------------------------
def save_feedback(eng, tam, section, fb_type):
    df = pd.DataFrame([{
        "English Text": eng,
        "Tamil Translation": tam,
        "Legal Section": section,
        "Feedback": fb_type,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    try:
        df.to_csv("user_feedback.csv", mode='a', header=False, index=False, encoding="utf-8")
    except:
        df.to_csv("user_feedback.csv", index=False, encoding="utf-8")


# ---------------------------
# UI STARTS HERE
# ---------------------------
st.title("🇮🇳 Rural ACT – Tamil Legal Awareness Translator")
st.write("Enter English → Get Tamil Translation + Voice + Legal Awareness")

text = st.text_area("Enter English Sentence:")

if st.button("Translate & Analyze"):
    if not text.strip():
        st.error("Please enter text.")
    else:
        tamil = translate_text(text)

        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        if tamil:
            st.success(tamil)
        else:
            st.error("⚠️ Translation temporarily unavailable.")

        # Tamil Voice
        st.subheader("🔊 Tamil Voice:")
        if tamil:
            audio_file = text_to_speech(tamil)
            if audio_file:
                audio_bytes = open(audio_file, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")
        else:
            st.info("Voice available only after successful translation.")

        # Legal Section
        st.subheader("⚖️ சட்ட விழிப்புணர்வு:")
        law = legal_section(text)
        st.warning(law)

        # Feedback
        st.subheader("📝 Feedback:")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Understand"):
                save_feedback(text, tamil, law, "Understand")
                st.success("Thank you for your feedback!")

        with col2:
            if st.button("👎 Not Understand"):
                save_feedback(text, tamil, law, "Not Understand")
                st.success("Thank you! We will improve the system.")




























