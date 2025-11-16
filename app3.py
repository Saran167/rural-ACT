import streamlit as st
from gtts import gTTS
import requests
from io import BytesIO
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="Rural ACT - Tamil Legal Awareness Translator")

# ----------------------------------------------------
# 1. TRANSLATION (Stable – MyMemory API)
# ----------------------------------------------------
def translate_to_tamil(text):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": "en|ta"}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if "responseData" in data:
            return data["responseData"]["translatedText"]
        return None
    except:
        return None


# ----------------------------------------------------
# 2. TAMIL VOICE
# ----------------------------------------------------
def generate_tamil_voice(text):
    try:
        tts = gTTS(text=text, lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except:
        return None


# ----------------------------------------------------
# 3. LEGAL KEYWORD DETECTION
# ----------------------------------------------------
def get_legal_awareness(text):
    text = text.lower()

    rules = {
        r"(otp|verify|bank|account|password)": (
            "IT Act 66C/66D – OTP Fraud",
            "இது OTP/வங்கி மோசடி செய்தியாக இருக்கலாம். OTP-ஐ யாருக்கும் கொடுக்க வேண்டாம்."
        ),
        r"(loan|money|scheme|offer)": (
            "IPC 420 – Cheating / Scam",
            "பணம், கடன், லாட்டரி போன்ற சலுகைகள் மோசடி."
        ),
        r"(harass|stalk|follow|threat|disturb)": (
            "IPC 354D – Harassment / Stalking",
            "தொடர்ந்து பின்தொடர்தல்/தொந்தரவு செய்தல் குற்றம்."
        ),
        r"(abuse|obscene|nude|adult|vulgar)": (
            "IT Act 67 – Obscene Content",
            "அசிங்கமான/சட்டவிரோத உள்ளடக்கம் அனுப்புதல் குற்றம்."
        ),
        r"(cheat|fraud|fake)": (
            "IPC 420 – Fraud",
            "இதில் மோசடி நோக்கம் உள்ளது."
        )
    }

    for pattern, (section, desc) in rules.items():
        if re.search(pattern, text):
            return section, desc

    return "No Legal Issue Detected", "சட்ட விரோதம் என எதுவும் கண்டறியப்படவில்லை."


# ----------------------------------------------------
# 4. FEEDBACK SAVE
# ----------------------------------------------------
def save_feedback(eng, tam, law, fb_type):
    data = {
        "English Message": eng,
        "Tamil Translation": tam,
        "Detected Law": law,
        "Feedback": fb_type,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.DataFrame([data])

    try:
        df.to_csv("user_feedback.csv", mode="a", header=False, index=False)
    except:
        df.to_csv("user_feedback.csv", mode="w", header=True, index=False)


# ----------------------------------------------------
# 5. STREAMLIT UI
# ----------------------------------------------------
st.title("🌾 Rural ACT – Tamil Legal Awareness Translator")
st.write("Enter English message → Get Tamil Translation + Voice + Legal Awareness")

english_input = st.text_area("✍️ Enter English Sentence")

if st.button("Translate & Analyze"):
    if english_input.strip() == "":
        st.warning("Please enter a message.")
    else:

        # Translation
        tamil_text = translate_to_tamil(english_input)

        if tamil_text:
            st.subheader("🈶 Tamil Translation:")
            st.success(tamil_text)

            # Voice
            voice = generate_tamil_voice(tamil_text)
            if voice:
                st.subheader("🔊 Tamil Voice:")
                st.audio(voice, format="audio/mp3")
            else:
                st.error("⚠️ Tamil voice could not be generated.")
        else:
            st.error("⚠️ Translation temporarily unavailable.")
            tamil_text = None

        # Legal Awareness
        section, desc = get_legal_awareness(english_input)

        st.subheader("⚖️ Tamil Legal Awareness:")
        st.info(f"**{section}**\n\n{desc}")

        # Feedback
        st.subheader("📝 Feedback")
        col1, col2 = st.columns(2)

        if col1.button("👍 Understand"):
            save_feedback(english_input, tamil_text, section, "Understand")
            st.success("Thank you! Feedback saved.")

        if col2.button("👎 Not Understand"):
            save_feedback(english_input, tamil_text, section, "Not Understand")
            st.success("Feedback saved for improvement.")






































