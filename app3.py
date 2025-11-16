import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import pandas as pd
import re
from datetime import datetime
import os

st.set_page_config(page_title="Tamil Legal Awareness Translator", layout="centered")

# ============================
#  FUNCTION: TAMIL TRANSLATION
# ============================
def translate_to_tamil(text):
    try:
        translator = GoogleTranslator(source='auto', target='ta')
        tamil_text = translator.translate(text)
        if tamil_text and tamil_text.strip():
            return tamil_text
        else:
            return None
    except:
        return None


# ============================
#  FUNCTION: TAMIL TTS FIXED
# ============================
def generate_tamil_voice(text):
    try:
        tts = gTTS(text=text, lang="ta")
        tts.save("tamil_voice.mp3")

        # Read file as base64 for Streamlit audio
        with open("tamil_voice.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()
        return audio_bytes

    except Exception as e:
        return None


# ============================================
#  FUNCTION: LEGAL RULE-BASED DETECTION
# ============================================
def get_legal_awareness(user_text):

    text = user_text.lower()

    # --- Harassment / Stalking ---
    if any(word in text for word in ["harass", "stalk", "follow me", "threat", "blackmail"]):
        return (
            "⚖️ சட்ட விழிப்புணர்வு (தமிழில்):\n"
            "IPC பிரிவு 354D - துரத்தல் / தொந்தரவு (Stalking/Harassment)\n"
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.\n\n"
            "எடுத்துக்காட்டு: ‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n"
            "செய்ய வேண்டியது: அனைத்து ஆதாரங்களையும் சேமிக்கவும்; சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930\n"
            "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்."
        )

    # --- OTP Scam / Fraud ---
    if any(word in text for word in ["otp", "bank", "account", "verify", "password"]):
        return (
            "⚖️ சட்ட விழிப்புணர்வு (தமிழில்):\n"
            "IT Act 66C / 66D - OTP / Account Fraud\n"
            "OTP, password, bank account விவரங்களை கேட்டு ஏமாற்றுவது குற்றம்.\n\n"
            "எடுத்துக்காட்டு: 'உங்கள் OTP ஐ பகிரவும்' போன்ற செய்திகள்.\n"
            "📞 உதவி எண்: 1930\n"
            "தண்டனை: 3 ஆண்டுகள் சிறை + அபராதம்."
        )

    # --- Money Fraud / Loan Scam ---
    if any(word in text for word in ["money", "loan", "pay", "amount", "rupees"]):
        return (
            "⚖️ சட்ட விழிப்புணர்வு (தமிழில்):\n"
            "IPC 420 - மோசடி / Fraud\n"
            "பணம் கேட்டு ஏமாற்றுவது குற்றம்.\n\n"
            "எடுத்துக்காட்டு: போலி loan apps, lottery scam.\n"
            "📞 உதவி எண்: 1930\n"
            "தண்டனை: 7 ஆண்டுகள் வரை சிறை."
        )

    return "⚖️ இந்த செய்தியில் எந்த சட்ட பிரச்சனையும் கண்டறியப்படவில்லை."


# ============================================
#  SAVE USER FEEDBACK TO CSV
# ============================================
def save_feedback(eng, tamil, legal, fb_type):
    data = {
        "English Text": [eng],
        "Tamil Text": [tamil],
        "Legal Section": [legal],
        "Feedback": [fb_type],
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    df = pd.DataFrame(data)

    # Append or create
    if not os.path.exists("user_feedback.csv"):
        df.to_csv("user_feedback.csv", index=False)
    else:
        df.to_csv("user_feedback.csv", mode='a', header=False, index=False)


# ============================================
#  STREAMLIT UI
# ============================================
st.title("🌾 Tamil Legal Awareness Translator")
st.subheader("Enter English → Get Tamil Translation + Voice + Legal Awareness + Feedback")

user_input = st.text_area("➤ Enter English sentence:")

if st.button("Translate & Analyze"):

    if not user_input.strip():
        st.warning("Please enter a sentence.")
        st.stop()

    # --- Translation ---
    tamil_output = translate_to_tamil(user_input)

    st.markdown("### 🈶 தமிழில் மொழிபெயர்ப்பு:")
    if tamil_output:
        st.success(tamil_output)
    else:
        st.error("⚠️ Translation temporarily unavailable.")

    # --- Voice ---
    st.markdown("### 🔊 Tamil Voice:")
    if tamil_output:
        audio_data = generate_tamil_voice(tamil_output)
        if audio_data:
            st.audio(audio_data, format="audio/mp3")
        else:
            st.error("⚠️ Tamil voice could not be generated.")
    else:
        st.info("Voice available only after successful translation.")

    # --- Legal Awareness ---
    st.markdown("### ⚖️ Legal Awareness:")
    law = get_legal_awareness(user_input)
    st.info(law)

    # --- Feedback buttons ---
    st.markdown("### 📝 Feedback")
    col1, col2 = st.columns(2)

    if col1.button("✔ Understand"):
        save_feedback(user_input, tamil_output, law, "Understand")
        st.success("Thank you! Feedback saved successfully.")

    if col2.button("✘ Not Understand"):
        save_feedback(user_input, tamil_output, law, "Not Understand")
        st.success("Thank you! Feedback saved successfully.")





























