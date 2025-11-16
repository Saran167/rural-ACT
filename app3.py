import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
import re
import os

st.set_page_config(page_title="Tamil Legal Awareness Translator", layout="centered")

st.title("🛡️ Tamil Legal Awareness Translator")
st.write("Enter English → Get Tamil Translation + Voice + Legal Awareness + Feedback")

# ---------------------------
# 1. FUNCTION: Translation (MyMemory API - stable)
# ---------------------------
def translate_to_tamil(text):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": "en|ta"}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            tamil_translation = data["responseData"]["translatedText"]
            return tamil_translation
        else:
            return None
    except:
        return None


# ---------------------------
# 2. FUNCTION: Tamil Voice Generation (FIXED & WORKING)
# ---------------------------
def generate_tamil_voice(text):
    try:
        tts = gTTS(text=text, lang="ta", slow=False)
        file_path = "tamil_voice.mp3"
        tts.save(file_path)

        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        return audio_bytes
    except:
        return None


# ---------------------------
# 3. FUNCTION: Legal Awareness Detection
# ---------------------------
def legal_awareness(text):

    text_lower = text.lower()

    # ---- 354D Harassment ----
    if any(word in text_lower for word in ["harass", "harassed", "stalk", "threat"]):
        return """
### ⚖️ IPC Section 354D – Stalking / Harassment  
ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.  

**எடுத்துக்காட்டு:**  
‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ என்று மிரட்டல் செய்திகள் அனுப்புதல்.  

**செய்ய வேண்டியது:**  
• screenshots, chat logs போன்ற ஆதாரங்களை சேமிக்கவும்  
• சைபர் போலீசில் உடனடியாக புகார் செய்யவும்  

📞 **உதவி எண்:** 1930 - Tamil Nadu Cyber Helpline  
📚 **உதாரணம்:** 2024ல் Chennai–யில் cyberstalking செய்த நபர் கைது.  

**தண்டனை:** 3 ஆண்டுகள் வரை சிறை + அபராதம்  
"""

    # ---- OTP/Cyber Fraud ----
    if any(w in text_lower for w in ["otp", "account", "bank", "verification"]):
        return """
### ⚖️ IT Act 66C / 66D – OTP & Cyber Fraud  
OTP, password, account details கேட்டு ஏமாற்றுவது குற்றம்.

**எடுத்துக்காட்டு:**  
‘உங்கள் கணக்கு தடுக்கப்பட்டுள்ளது, OTP ஐ தெரிவிக்கவும்’  

**செய்ய வேண்டியது:**  
• OTP பகிர வேண்டாம்  
• உடனே 1930க்குக் கால் செய்யவும்  

📞 Helpline: 1930  
**தண்டனை:** 3 ஆண்டுகள் சிறை + அபராதம்  
"""

    # ---- Money Scam / Loan Scam ----
    if any(w in text_lower for w in ["money", "loan", "transfer", "send", "payment"]):
        return """
### ⚖️ IPC Section 420 – Cheating / Money Scam  
பிறரை ஏமாற்றி பணம் பெறுதல் குற்றம்.

**எடுத்துக்காட்டு:**  
‘நீங்கள் லாட்டரி வென்றுள்ளீர்கள் – processing fee அனுப்பவும்’  

**செய்ய வேண்டியது:**  
• பணம் அனுப்ப வேண்டாம்  
• மோசடி என சந்தேகிக்கும்போது 1930 அழைக்கவும்  

**தண்டனை:** 7 ஆண்டுகள் வரை சிறை  
"""

    # ---- Default Case ----
    return "⚖️ No legal risk detected in this message."


# ---------------------------
# 4. FUNCTION: Save Feedback
# ---------------------------
def save_feedback(eng, tam, section, fb_type, fb_detail):
    df = pd.DataFrame([[eng, tam, section, fb_type, fb_detail]],
                      columns=["English", "Tamil", "Section", "Feedback", "Detail"])

    if os.path.exists("user_feedback.csv"):
        old = pd.read_csv("user_feedback.csv")
        df = pd.concat([old, df], ignore_index=True)

    df.to_csv("user_feedback.csv", index=False)


# ---------------------------
# STREAMLIT UI
# ---------------------------

text = st.text_area("➤ Enter English sentence:")

if st.button("Translate & Analyze"):
    
    if text.strip() == "":
        st.warning("Please enter a sentence.")
        st.stop()

    # ---- Translation ----
    tamil = translate_to_tamil(text)

    st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")

    if tamil:
        st.success(tamil)
    else:
        st.error("⚠️ Translation temporarily unavailable.")

    # ---- Voice ----
    st.subheader("🔊 Tamil Voice:")
    if tamil:
        audio = generate_tamil_voice(tamil)

        if audio:
            st.audio(audio, format="audio/mp3")
        else:
            st.error("⚠️ Tamil voice could not be generated.")
    else:
        st.info("Voice available only after translation.")

    # ---- Legal Awareness ----
    st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")
    section = legal_awareness(text)
    st.write(section)

    # ---- FEEDBACK ----
    st.subheader("📝 User Feedback")

    fb = st.radio("Did you understand the output?", ["Understand", "Not Understand"])

    if fb == "Not Understand":
        detail = st.radio("Which part was unclear?", ["Text", "Voice", "Both"])
    else:
        detail = "-"

    if st.button("Submit Feedback"):
        save_feedback(text, tamil if tamil else "-", section, fb, detail)
        st.success("✅ Feedback saved successfully!")







































