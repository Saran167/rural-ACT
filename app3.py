import streamlit as st
from google_translate import Translator
from gtts import gTTS
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="Tamil Legal Awareness Translator", layout="centered")

translator = Translator()

# -----------------------------------
# TRANSLATION (NEW – SUPER STABLE)
# -----------------------------------
def translate_to_tamil(text):
    try:
        result = translator.translate(text, target_language="ta")
        return result["translatedText"]
    except:
        return None


# -----------------------------------
# TTS – ALWAYS WORKS
# -----------------------------------
def generate_tts(text):
    try:
        tts = gTTS(text=text, lang="ta")
        tts.save("tamil_voice.mp3")
        return "tamil_voice.mp3"
    except:
        return None


# -----------------------------------
# LEGAL RULE ENGINE
# -----------------------------------
def detect_legal_sections(text):
    text_lower = text.lower()

    if re.search(r"otp|fraud|money|won|bank|loan|scam", text_lower):
        return (
            "IPC 420 – மோசடி",
            "பணம் அல்லது சொத்தைப் பெற ஏமாற்றுவது குற்றமாகும்.",
            "எடுத்துக்காட்டு: பரிசு வென்றதாக கூறி பணம் கேட்பது.",
            "செய்ய வேண்டியது: OTP பகிர வேண்டாம். 1930 அழைக்கவும்.",
            "தண்டனை: 7 ஆண்டுகள் சிறை + அபராதம்"
        )

    if re.search(r"harass|harassed|stalk|threat|torture|blackmail", text_lower):
        return (
            "IPC 354D – தொந்தரவு / Stalking",
            "பின்தொடர்தல், மிரட்டல் செய்தல் குற்றமாகும்.",
            "எடுத்துக்காட்டு: ‘உன் படங்களை வெளியிடுவேன்’ என்று மிரட்டுவது.",
            "செய்ய வேண்டியது: screenshots சேமிக்கவும்; cyber cell-ல் புகார் செய்யவும்.",
            "தண்டனை: 3 ஆண்டுகள் சிறை + அபராதம்"
        )

    return (
        "சட்டப் பிரிவு இல்லை",
        "இந்த செய்தியில் குற்ற நோக்கம் கண்டறியப்படவில்லை.",
        "எடுத்துக்காட்டு: பொதுவான தகவல்.",
        "செய்ய வேண்டியது: எச்சரிக்கையாக இருங்கள்.",
        "தண்டனை: இல்லை"
    )


# -----------------------------------
# SAVE FEEDBACK
# -----------------------------------
def save_feedback(eng, tamil, section, fb, detail):
    df = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "english": eng,
        "tamil": tamil,
        "section": section,
        "feedback": fb,
        "detail": detail
    }])

    df.to_csv("user_feedback.csv", mode="a", header=False, index=False, encoding="utf-8")


# -----------------------------------
# STREAMLIT UI
# -----------------------------------
st.title("🛡️ Tamil Legal Awareness Translator")

text = st.text_area("Enter English text here:")

if st.button("Translate & Analyze"):
    if not text.strip():
        st.error("Please enter text!")
    else:
        tamil = translate_to_tamil(text)

        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        if tamil:
            st.success(tamil)
        else:
            st.error("Translation temporarily unavailable.")

        st.subheader("🔊 Tamil Voice:")
        if tamil:
            audio_file = generate_tts(tamil)
            if audio_file:
                with open(audio_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
            else:
                st.error("Tamil voice could not be generated.")
        else:
            st.info("Voice loads only after translation.")

        # Legal Awareness
        section, desc, example, action, punishment = detect_legal_sections(text)

        st.subheader("⚖️ சட்ட விழிப்புணர்வு:")
        st.write(f"**{section}**")
        st.write(desc)
        st.write(example)
        st.write(action)
        st.write(punishment)

        # Feedback
        st.subheader("📝 Feedback")
        fb = st.radio("Did you understand?", ["Understand", "Not Understand"])
        detail = ""

        if fb == "Not Understand":
            detail = st.radio("Which format?", ["Text", "Voice", "Both"])

        if st.button("Submit Feedback"):
            save_feedback(text, tamil, section, fb, detail)
            st.success("Feedback saved successfully!")

































