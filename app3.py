import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
import re
import base64
from datetime import datetime
import requests

st.set_page_config(page_title="Tamil Legal Awareness Translator", layout="centered")

# --------------------------
# TRANSLATION FUNCTION (VERY STABLE)
# --------------------------
def translate_to_tamil(text):
    # First attempt: GoogleTranslator
    try:
        tamil = GoogleTranslator(source="auto", target="ta").translate(text)
        if tamil and tamil.strip():
            return tamil
    except:
        pass
    
    # Second fallback: MyMemory (never blocks)
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": "en|ta"}
        response = requests.get(url).json()
        return response["responseData"]["translatedText"]
    except:
        return None


# --------------------------
# TAMIL VOICE GENERATION
# --------------------------
def generate_tts(text):
    try:
        tts = gTTS(text, lang="ta")
        tts.save("tamil_voice.mp3")
        return "tamil_voice.mp3"
    except:
        return None


# --------------------------
# LEGAL AWARENESS ENGINE
# --------------------------
def detect_legal_sections(text):
    text_lower = text.lower()

    # IPC 420 – Fraud, Cheating
    if re.search(r"otp|fraud|lottery|money|bank|password|won|payment|offer", text_lower):
        return (
            "IPC பிரிவு 420 - மோசடி / ஏமாற்றுதல்",
            "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றமாகும். "
            "இதில் advance fee scams, fake loan apps, lottery scams போன்றவை அடங்கும்.",
            "எடுத்துக்காட்டு: ‘நீங்கள் பரிசு வென்றுள்ளீர்கள் — ரூ.5000 அனுப்பவும்’ போன்ற போலி செய்திகள்.",
            "செய்ய வேண்டியது: OTP பகிர வேண்டாம்; உடனடியாக வங்கியில் தகவல் தெரிவிக்கவும்.",
            "தண்டனை: 7 ஆண்டுகள் வரை சிறை + அபராதம்."
        )

    # IPC 354D – Harassment / Stalking
    if re.search(r"harass|harassed|stalk|follow|threat|blackmail|torture", text_lower):
        return (
            "IPC பிரிவு 354D - துரத்தல் / தொந்தரவு",
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், மிரட்டல் செய்தல் ஆகியவை குற்றமாகும்.",
            "எடுத்துக்காட்டு: ‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள்.",
            "செய்ய வேண்டியது: அனைத்து ஆதாரங்களையும் (screenshots, chats) சேமிக்கவும்; உடனடியாக Cyber Cell-ல் புகார் செய்யவும்.",
            "தண்டனை: 3 ஆண்டுகள் வரை சிறை + அபராதம்."
        )

    # IT Act 66C / 66D – Cyber Impersonation / Fraud
    if re.search(r"identity|login|verify|account|block|reactivate", text_lower):
        return (
            "IT Act 66C / 66D - இணையத் தவறான நபராக்கம் / சைபர் மோசடி",
            "OTP, password, account விவரங்களை கேட்டு வேறொருவராக நடிப்பது குற்றம்.",
            "எடுத்துக்காட்டு: ‘உங்கள் கணக்கு block — OTP அனுப்பவும்’ போன்ற செய்திகள்.",
            "செய்ய வேண்டியது: OTP பகிர வேண்டாம்; cybercrime.gov.in இல் புகார் செய்யவும்.",
            "தண்டனை: 3 ஆண்டுகள் சிறை + அபராதம்."
        )

    # No match
    return (
        "சட்டப் பிரிவு கண்டறியப்படவில்லை",
        "இந்தச் செய்தியில் நேரடி குற்றச்சாட்டு தகவல் இல்லை. ஆனால் எச்சரிக்கையாக இருங்கள்.",
        "எடுத்துக்காட்டு: பொதுவான தகவல் / குற்ற நோக்கம் இல்லை.",
        "செய்ய வேண்டியது: சந்தேகம் இருந்தால் 1930 அழைக்கவும்.",
        "தண்டனை: இல்லை."
    )


# --------------------------
# FEEDBACK SAVING
# --------------------------
def save_feedback(eng, tamil, section, fb_type, detail):
    df = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "english_text": eng,
        "tamil_translation": tamil,
        "legal_section": section,
        "feedback_type": fb_type,
        "feedback_detail": detail
    }])

    try:
        df.to_csv("user_feedback.csv", mode="a", header=False, index=False, encoding="utf-8")
    except:
        df.to_csv("user_feedback.csv", index=False, encoding="utf-8")


# --------------------------
# STREAMLIT UI
# --------------------------
st.title("🛡️ Tamil Legal Awareness Translator")
st.write("Enter English → Get Tamil Translation + Voice + Legal Awareness + Feedback")

user_input = st.text_area("✏️ Enter English sentence:")

if st.button("Translate & Analyze"):
    if not user_input.strip():
        st.error("⚠️ Please enter a sentence.")
    else:
        tamil_text = translate_to_tamil(user_input)

        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        if tamil_text:
            st.success(tamil_text)
        else:
            st.error("⚠️ Translation temporarily unavailable.")

        st.subheader("🔊 Tamil Voice:")
        if tamil_text:
            audio_file = generate_tts(tamil_text)
            if audio_file:
                with open(audio_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")
        else:
            st.info("Voice available only after successful translation.")

        # Legal Awareness
        section, desc, example, action, punishment = detect_legal_sections(user_input)

        st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")
        st.write(f"**{section}**")
        st.write(desc)
        st.write(example)
        st.write(action)
        st.write(punishment)

        # Feedback
        st.subheader("📝 Feedback")
        fb = st.radio("Did you understand the explanation?", ["Understand", "Not Understand"])

        detail = ""
        if fb == "Not Understand":
            detail = st.radio("Which format do you prefer?", ["Text", "Voice", "Both"])

        if st.button("Submit Feedback"):
            save_feedback(user_input, tamil_text, section, fb, detail)
            st.success("✅ Feedback saved successfully!")
































