import streamlit as st
from deep_translator import GoogleTranslator
from googletrans import Translator
from gtts import gTTS
import pandas as pd
import re, os
from datetime import datetime

st.title("Tamil Legal Awareness Translator")

def translate_to_tamil(text):
    # 1st Translator → deep-translator GoogleTranslator
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text)
    except:
        pass

    # 2nd Translator → googletrans fallback
    try:
        translator = Translator()
        result = translator.translate(text, dest='ta')
        return result.text
    except:
        return "⚠️ Translation Unavailable. Please try again."

# Tamil Voice Generator
def get_tts_audio(tamil_text):
    try:
        tts = gTTS(tamil_text, lang='ta')
        file_path = "output.mp3"
        tts.save(file_path)
        return file_path
    except:
        return None

# Legal Keyword Detection
def get_legal_info(text):
    text_low = text.lower()

    if "harass" in text_low or "stalk" in text_low:
        return """IPC பிரிவு 354D - துரத்தல் / தொந்தரவு (Stalking/Harassment)
ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.
📞 உதவி எண்: 1930
தண்டனை: 3 ஆண்டுகள் சிறை + அபராதம்."""
    
    if "otp" in text_low or "bank" in text_low:
        return """IT Act 66D - ஆன்லைன் மோசடி / OTP Fraud
வங்கிக் கணக்கு OTP / PIN கேட்பது சட்ட விரோதம்.
📞 1930-ல் உடனே புகார் செய்யவும்."""
    
    return "சட்ட தொடர்பான எதுவும் கண்டுபிடிக்கப்படவில்லை."

# Feedback Saver
def save_feedback(input_text, tamil_text, law_info, feedback_type):
    df = pd.DataFrame([{
        "Timestamp": datetime.now(),
        "English_Text": input_text,
        "Tamil_Output": tamil_text,
        "Legal_Info": law_info,
        "Feedback": feedback_type
    }])

    if os.path.exists("feedback.csv"):
        df.to_csv("feedback.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("feedback.csv", index=False)

# UI
english_text = st.text_input("Enter English sentence:")

if st.button("Translate & Analyze"):
    if english_text.strip()=="":
        st.warning("Please enter a sentence!")
    else:
        tamil_text = translate_to_tamil(english_text)
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.write(tamil_text)

        # Tamil Voice
        audio_file = get_tts_audio(tamil_text)
        if audio_file:
            st.audio(audio_file)
        else:
            st.error("⚠️ Voice generation failed. Try again.")

        # Legal Awareness
        st.subheader("⚖️ சட்ட விழிப்புணர்வு:")
        law_info = get_legal_info(english_text)
        st.write(law_info)

        # Feedback Buttons
        st.subheader("📥 Feedback")
        if st.button("Understand 👍"):
            save_feedback(english_text, tamil_text, law_info, "Understand")
            st.success("Feedback saved successfully ✔")

        if st.button("Not Understand 👎"):
            save_feedback(english_text, tamil_text, law_info, "Not Understand")
            st.success("Feedback saved ✔ (Not Understand)")






















