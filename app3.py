import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import pandas as pd
from datetime import datetime
import re
import os

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(page_title="Tamil Legal Awareness", layout="centered")

st.title("🛡️ Tamil Legal Awareness Translator")
st.caption("English → Tamil Translation + Tamil Voice + Legal Awareness + Feedback")

# ---------------------------------------------------
# Translation Function
# ---------------------------------------------------
translator = GoogleTranslator(source="en", target="ta")

def translate_tamil(text):
    try:
        return translator.translate(text)
    except:
        return None  # translation failed

# ---------------------------------------------------
# Tamil TTS Function
# ---------------------------------------------------
def tts_tamil(text):
    try:
        tts = gTTS(text=text, lang="ta")
        fp = BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except:
        return None

# ---------------------------------------------------
# Legal Section Detection
# ---------------------------------------------------
def detect_legal(text):
    t = text.lower()

    # Harassment / Stalking
    if re.search(r"harass|harassed|stalk|threat|blackmail|torture|follow", t):
        return (
            "IPC 354D – துரத்தல் / தொந்தரவு (Stalking / Harassment)",
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், மிரட்டல் குற்றமாகும்.",
            "எடுத்துக்காட்டு: 'நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்' என மிரட்டுதல்.",
            "செய்ய வேண்டியது: screenshots / chat logs சேமிக்கவும்; cyber cell-ல் புகார் செய்யவும்.",
            "தண்டனை: 3 ஆண்டுகள் வரை சிறை + அபராதம்."
        )

    # Fraud / OTP / Money Scam
    if re.search(r"otp|fraud|scam|bank|loan|money|prize", t):
        return (
            "IPC 420 – மோசடி",
            "பிறரை ஏமாற்றி பணம் பெறுவது குற்றம்.",
            "எடுத்துக்காட்டு: 'நீங்கள் பரிசு வென்றுள்ளீர்கள்' என்று பணம் கேட்பது.",
            "செய்ய வேண்டியது: OTP பகிர வேண்டாம்; 1930 உதவி எண்ணுக்கு அழைக்கவும்.",
            "தண்டனை: 7 ஆண்டுகள் வரை சிறை + அபராதம்."
        )

    # No Law Detected
    return (
        "சட்டம் பொருந்தவில்லை",
        "இந்த செய்தியில் சட்டவிரோதமான தகவல் இல்லை.",
        "எடுத்துக்காட்டு: சாதாரண தகவல்.",
        "செய்ய வேண்டியது: எச்சரிக்கையாக இருக்கவும்.",
        "தண்டனை: -"
    )

# ---------------------------------------------------
# Save Feedback to CSV
# ---------------------------------------------------
def save_feedback(eng, tam, sec, fb, detail):
    filename = "user_feedback.csv"

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "english": eng,
        "tamil": tam,
        "section": sec,
        "feedback": fb,
        "detail": detail
    }

    newdf = pd.DataFrame([row])

    if not os.path.exists(filename):
        newdf.to_csv(filename, index=False)
    else:
        newdf.to_csv(filename, mode="a", index=False, header=False)

# ---------------------------------------------------
# UI Section
# ---------------------------------------------------
eng = st.text_area("➤ Enter English sentence:")

if st.button("Translate & Analyze"):
    if not eng.strip():
        st.error("Please enter a message")
    else:
        tamil = translate_tamil(eng)

        # Tamil Translation
        st.subheader("🈶 Tamil Translation:")
        if tamil:
            st.success(tamil)
        else:
            st.error("⚠️ Translation temporarily unavailable.")

        # Tamil Voice
        st.subheader("🔊 Tamil Voice:")
        if tamil:
            audio = tts_tamil(tamil)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")
        else:
            st.info("Voice available only after successful translation.")

        # Legal Awareness
        st.subheader("⚖️ Legal Awareness (Tamil):")
        sec, desc, ex, act, pun = detect_legal(eng)
        st.write(f"### {sec}")
        st.write(desc)
        st.write(ex)
        st.write(act)
        st.write("**" + pun + "**")

        # Feedback Section
        st.subheader("📝 Feedback")
        fb = st.radio("Your understanding:", ["Understand", "Not Understand"])
        detail = ""

        if fb == "Not Understand":
            detail = st.radio("Select:", ["Text", "Voice", "Both"])

        if st.button("Submit Feedback"):
            save_feedback(eng, tamil, sec, fb, detail)
            st.success("Feedback saved successfully!")


































