import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
import re, os
from datetime import datetime

st.title("Tamil Legal Awareness Translator")
st.caption("English → Tamil Text + Tamil Voice + Legal Info + Feedback")

# ---------------------- TRANSLATION ----------------------
def translate_to_tamil(text):
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text)
    except:
        return "⚠️ Translation temporarily unavailable. Try again."

# ---------------------- TTS ----------------------
def get_tts_audio(tamil_text):
    try:
        file_path = "audio_output.mp3"
        tts = gTTS(tamil_text, lang='ta')
        tts.save(file_path)
        return file_path
    except:
        return None

# ---------------------- LEGAL DETECTION ----------------------
def get_legal_info(text):
    t = text.lower()

    # HARASSMENT
    if ("harass" in t) or ("stalk" in t) or ("threat" in t):
        return """### IPC பிரிவு 354D - துரத்தல் / தொந்தரவு (Stalking / Harassment)

ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.

**எடுத்துக்காட்டு:** ‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள்.

**செய்ய வேண்டியது:** screenshots, chat logs சேமிக்கவும்; சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.

📞 **உதவி எண்:** 1930  
📚 **எடுத்துக்காட்டு:** 2024 - Chennaiயில் cyberstalking செய்த நபர் கைது.

**தண்டனை:** 3 ஆண்டுகள் சிறை + அபராதம்.
"""
    # OTP / BANK FRAUD
    if ("otp" in t) or ("bank" in t) or ("password" in t):
        return """### IT Act 66C / 66D - OTP Fraud / Identity Theft

OTP, password, PIN கேட்பது ஆன்லைன் மோசடி.

**எடுத்துக்காட்டு:** ‘உங்கள் கணக்கு முடக்கப்பட்டுள்ளது – OTP கொடுக்கவும்’.

**செய்ய வேண்டியது:** OTP பகிர வேண்டாம்; உடனே 1930-ல் புகார் செய்யவும்.

📞 **உதவி எண்:** 1930  
**தண்டனை:** 3 ஆண்டுகள் சிறை + அபராதம்.
"""
    # MONEY / CHEATING
    if ("money" in t) or ("cheat" in t) or ("scam" in t):
        return """### IPC பிரிவு 420 - மோசடி / ஏமாற்றுதல்

பிறரை ஏமாற்றி பணம் பெறுதல் குற்றம்.

**எடுத்துக்காட்டு:** ‘பரிசு வென்றுள்ளீர்கள் — 5000 அனுப்புங்கள்’.

**செய்ய வேண்டியது:** பணம் அனுப்ப வேண்டாம்; புகார் செய்யவும்.

📞 **உதவி எண்:** 1930  
**தண்டனை:** 7 ஆண்டுகள் சிறை + அபராதம்.
"""

    return "சட்ட தொடர்பான எந்த குற்றமும் கண்டறியப்படவில்லை."

# ---------------------- FEEDBACK SAVER ----------------------
def save_feedback(input_text, tamil_text, law_info, feedback_type):
    row = {
        "Timestamp": datetime.now(),
        "English_Text": input_text,
        "Tamil_Text": tamil_text,
        "Legal_Info": law_info,
        "Feedback": feedback_type
    }

    if os.path.exists("feedback.csv"):
        pd.DataFrame([row]).to_csv("feedback.csv", mode='a', header=False, index=False)
    else:
        pd.DataFrame([row]).to_csv("feedback.csv", index=False)

# ---------------------- UI ----------------------
english_text = st.text_input("➤ Enter English sentence:")

if st.button("Translate & Analyze"):
    if english_text.strip() == "":
        st.warning("Please enter text.")
    else:
        tamil_output = translate_to_tamil(english_text)
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_output)

        audio_file = get_tts_audio(tamil_output)
        if audio_file:
            st.audio(audio_file)
        else:
            st.error("⚠️ Tamil voice could not be generated.")

        st.subheader("⚖️ சட்ட விழிப்புணர்வு:")
        legal_info = get_legal_info(english_text)
        st.markdown(legal_info)

        st.subheader("📥 Feedback")
        if st.button("Understand 👍"):
            save_feedback(english_text, tamil_output, legal_info, "Understand")
            st.success("Feedback saved successfully ✔")

        if st.button("Not Understand 👎"):
            save_feedback(english_text, tamil_output, legal_info, "Not Understand")
            st.success("Feedback saved ✔ (Not Understand)")






















