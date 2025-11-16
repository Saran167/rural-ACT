import streamlit as st
from gtts import gTTS
import base64
import pandas as pd
import os
import re
import requests
from datetime import datetime

st.set_page_config(page_title="Tamil Legal Awareness Translator", layout="wide")

# ------------------------------------
# 1. TRANSLATION FUNCTION (FIXED)
# ------------------------------------
def translate_to_tamil(text):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": "en|ta"}
        response = requests.get(url, params=params).json()
        return response["responseData"]["translatedText"]
    except:
        return None

# ------------------------------------
# 2. TEXT TO SPEECH (TAMIL AUDIO)
# ------------------------------------
def generate_tamil_audio(tamil_text):
    try:
        tts = gTTS(tamil_text, lang="ta")
        file_path = "audio.mp3"
        tts.save(file_path)
        return file_path
    except:
        return None

# ------------------------------------
# 3. LEGAL AWARENESS DETECTION
# ------------------------------------
def get_legal_awareness(user_text):

    text = user_text.lower()

    # --- Harassment (Your friend's message case) ---
    if "harass" in text or "stalk" in text or "follow" in text:
        return """
⚖️ **சட்ட விழிப்புணர்வு (தமிழில்):**

**IPC பிரிவு 354D - துரத்தல் / தொந்தரவு (Stalking / Harassment)**  
ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.

**எடுத்துக்காட்டு:**  
‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள் அனுப்புதல்.

**செய்ய வேண்டியது:**  
அனைத்து ஆதாரங்களையும் (screenshots, chat logs) சேமிக்கவும்;  
சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.

📞 **உதவி எண்:** 1930 – Tamil Nadu Cyber Helpline  
📚 **எடுத்துக்காட்டு:** 2024ல் Chennaiயில் cyberstalking செய்த நபர் கைது.  
**தண்டனை:** 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.
"""

    # --- OTP / Bank Fraud ---
    if "otp" in text or "account" in text or "bank" in text:
        return """
⚖️ **IT Act 66C / 66D – OTP & Banking Fraud**

OTP, password, account details திருடி வேறொருவராக நடிப்பது குற்றம்.  
**தண்டனை:** 3 ஆண்டுகள் சிறை + அபராதம்.

🧭 **என்ன செய்யலாம்:**  
OTP பகிர வேண்டாம்; வங்கியை உடனே தொடர்புகொள்ளவும்.  
www.cybercrime.gov.in இல் புகார் செய்யவும்.

📞 **Helpline:** 1930
"""

    # --- Loan scam ---
    if "loan" in text:
        return """
⚖️ **IPC 420 – Loan Scam / Cheating**

பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றம்.  
இது fake loan apps, lottery scams போன்றவற்றை உட்கொள்ளும்.

**தண்டனை:** 7 ஆண்டுகள் சிறை + அபராதம்  
📞 Helpline: 1930
"""

    # --- Default fallback ---
    return "⚖️ எந்த குறிப்பிட்ட சட்ட பிரிவும் கண்டறியப்படவில்லை. ஆனால் எச்சரிக்கையாக இருங்கள்."

# ------------------------------------
# 4. SAVE FEEDBACK
# ------------------------------------
def save_feedback(original, tamil, legal, fb_type, fb_detail):
    data = {
        "English Text": original,
        "Tamil Translation": tamil,
        "Legal Awareness": legal,
        "Feedback Type": fb_type,
        "Feedback Detail": fb_detail,
        "Timestamp": datetime.now()
    }

    df = pd.DataFrame([data])

    file = "user_feedback.csv"

    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False, index=False)
    else:
        df.to_csv(file, index=False)

# ------------------------------------
# UI STARTS
# ------------------------------------
st.title("🌾 Tamil Legal Awareness Translator")
st.subheader("Enter English → Get Tamil Translation + Voice + Legal Awareness + Feedback")

user_input = st.text_area("Enter English Sentence:")

if st.button("Translate & Analyze"):
    if not user_input.strip():
        st.warning("Please enter a sentence.")
    else:
        # Translate
        tamil_text = translate_to_tamil(user_input)

        if tamil_text:
            st.success("🈶 தமிழில் மொழிபெயர்ப்பு:")
            st.write(tamil_text)
        else:
            st.error("⚠️ Translation temporarily unavailable.")
            tamil_text = None

        # Audio
        if tamil_text:
            audio_file = generate_tamil_audio(tamil_text)
            if audio_file:
                st.audio(audio_file, format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")

        # Legal Awareness
        legal_output = get_legal_awareness(user_input)

        st.write("### ⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")
        st.write(legal_output)

        # Feedback Section
        st.write("### 🗳️ Feedback")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Understand"):
                save_feedback(user_input, tamil_text, legal_output, "Understand", "-")
                st.success("Feedback saved successfully.")

        with col2:
            if st.button("👎 Not Understand"):
                detail = st.radio("Which part is unclear?", ["Translation", "Voice", "Legal Awareness", "All"])
                if st.button("Submit Feedback"):
                    save_feedback(user_input, tamil_text, legal_output, "Not Understand", detail)
                    st.success("Feedback saved successfully.")
























