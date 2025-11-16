import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import pandas as pd
from datetime import datetime
import re
import os

st.set_page_config(page_title="Tamil Legal Awareness", layout="centered")

st.title("🛡️ Tamil Legal Awareness Translator")
st.caption("English → Tamil Translation + Voice + Legal Awareness + Feedback")

# ------------------ TRANSLATION -----------------------
translator = GoogleTranslator(source="en", target="ta")

def translate_tamil(text):
    try:
        return translator.translate(text)
    except:
        return None

# ------------------ TAMIL VOICE ------------------------
def tamil_voice(text):
    try:
        tts = gTTS(text=text, lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except:
        return None

# ------------------ LEGAL DETECTION ---------------------
def detect_legal(text):
    t = text.lower()

    # Harassment / Stalking
    if re.search(r"harass|harassed|stalk|threat|follow|blackmail", t):
        return (
            "IPC 354D – துரத்தல் / தொந்தரவு (Stalking / Harassment)",
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், மிரட்டல் குற்றம்.",
            "எடுத்துக்காட்டு: 'நீ என்னுடன் பேசவில்லை என்றால் உன் படங்களை வெளியிடுவேன்' என மிரட்டுதல்.",
            "செய்ய வேண்டியது: அனைத்து ஆதாரங்களையும் சேமிக்கவும்; cyber crime-ல் புகார் செய்யவும்.",
            "தண்டனை: 3 ஆண்டுகள் வரை சிறை + அபராதம்."
        )

    # OTP / Fraud / Money Scam
    if re.search(r"otp|fraud|scam|bank|loan|money|prize", t):
        return (
            "IPC 420 – மோசடி",
            "பிறரை ஏமாற்றி பணம் அல்லது நன்மை பெறுவது குற்றம்.",
            "எடுத்துக்காட்டு: பரிசு வென்றீர்கள் என்று சொல்லி advance money கேட்குதல்.",
            "செய்ய வேண்டியது: OTP பகிர வேண்டாம்; 1930 க்கு அழைத்து புகார் செய்யவும்.",
            "தண்டனை: 7 ஆண்டுகள் வரை சிறை + அபராதம்."
        )

    return (
        "சட்டப் பிரிவு இல்லை",
        "இந்த செய்தியில் சட்டவிரோதமான உள்ளடக்கம் கண்டுபிடிக்கவில்லை.",
        "எடுத்துக்காட்டு: சாதாரண தகவல்.",
        "செய்ய வேண்டியது: எச்சரிக்கையாக இருக்கவும்.",
        "தண்டனை: -"
    )

# ------------------ SAVE FEEDBACK -----------------------
def save_feedback(eng, tam, sec, fb, detail):
    file = "user_feedback.csv"
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "english": eng,
        "tamil": tam,
        "section": sec,
        "feedback": fb,
        "detail": detail
    }

    df_new = pd.DataFrame([row])

    if not os.path.exists(file):
        df_new.to_csv(file, index=False)
    else:
        df_new.to_csv(file, mode="a", index=False, header=False)

# ------------------ UI --------------------------
eng = st.text_area("➤ Enter English sentence:")

if st.button("Translate & Analyze"):
    if not eng.strip():
        st.error("Please enter something!")
    else:
        tamil = translate_tamil(eng)

        st.subheader("🈶 Tamil Translation:")
        if tamil:
            st.success(tamil)
        else:
            st.error("⚠️ Translation temporarily unavailable.")

        st.subheader("🔊 Tamil Voice:")
        if tamil:
            audio = tamil_voice(tamil)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")
        else:
            st.info("Voice available only after translation.")

        st.subheader("⚖️ Legal Awareness:")
        sec, desc, example, action, punishment = detect_legal(eng)

        st.write(f"### {sec}")
        st.write(desc)
        st.write(example)
        st.write(action)
        st.write("**" + punishment + "**")

        st.subheader("📝 Feedback")
        fb = st.radio("Select:", ["Understand", "Not Understand"])
        detail = ""

        if fb == "Not Understand":
            detail = st.radio("Need help in:", ["Text", "Voice", "Both"])

        if st.button("Submit Feedback"):
            save_feedback(eng, tamil if tamil else "", sec, fb, detail)
            st.success("Feedback saved successfully!")



































