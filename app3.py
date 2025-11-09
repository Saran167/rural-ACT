# -------------------------
# 📘 English → Tamil Legal Awareness App
# -------------------------
import streamlit as st
from googletrans import Translator
from gtts import gTTS
import tempfile
import os

# -------------------------
# Initialize translator
# -------------------------
translator = Translator()

# -------------------------
# Legal Awareness Database
# -------------------------
legal_db = {
    "harass": {
        "section": "IPC Section 354",
        "tamil": "பிரிவு 354 – பெண்களை தொந்தரவு செய்வது: பெண்களை தொந்தரவு செய்தல் அல்லது மரியாதை குலைக்கும் செயல்கள் குற்றமாகும். தண்டனை: 1 ஆண்டு முதல் 5 ஆண்டு வரை சிறைத்தண்டனை மற்றும் அபராதம்.",
        "english": "Section 354 – Outraging the Modesty of a Woman: Harassing or assaulting a woman with intent to outrage her modesty is punishable with imprisonment from 1 to 5 years and fine."
    },
    "cheat": {
        "section": "IPC Section 420",
        "tamil": "பிரிவு 420 – மோசடி: ஏமாற்றுதல் அல்லது தவறாகப் பணம் பெற்றல் குற்றமாகும். தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "english": "Section 420 – Cheating: Dishonestly inducing a person to deliver money or property is a crime. Punishment: Imprisonment up to 7 years and fine."
    },
    "bank": {
        "section": "IT Act Section 66D",
        "tamil": "தகவல் தொழில்நுட்பச் சட்டம் பிரிவு 66D – ஆன்லைன் மோசடி: போலி வலைத்தளங்கள் அல்லது வங்கிக் கணக்குகள் மூலம் மோசடி செய்தல் குற்றமாகும். தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "english": "IT Act Section 66D – Online Fraud: Cheating using fake websites or bank accounts is punishable with imprisonment up to 3 years and fine."
    },
    "money": {
        "section": "IPC Section 406",
        "tamil": "பிரிவு 406 – நம்பிக்கையின்மையால் பணம் அல்லது சொத்தை தவறாகப் பயன்படுத்துதல் குற்றமாகும். தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "english": "Section 406 – Criminal Breach of Trust: Misappropriation of money or property entrusted to someone. Punishment: Up to 3 years imprisonment and fine."
    },
    "photo": {
        "section": "IT Act Section 67",
        "tamil": "தகவல் தொழில்நுட்பச் சட்டம் பிரிவு 67 – ஆபாசப் படங்கள் பகிர்வு குற்றமாகும். தண்டனை: முதல் குற்றத்திற்கு 3 ஆண்டுகள் சிறை மற்றும் அபராதம்.",
        "english": "IT Act Section 67 – Publishing or transmitting obscene images is a punishable offence. Punishment: Up to 3 years imprisonment and fine."
    },
    "video": {
        "section": "IT Act Section 67A",
        "tamil": "பிரிவு 67A – பாலியல் உள்ளடக்கம் கொண்ட வீடியோக்களை பகிர்வது குற்றமாகும். தண்டனை: 5 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "english": "Section 67A – Publishing or transmitting sexually explicit videos is punishable with up to 5 years imprisonment and fine."
    },
    "threat": {
        "section": "IPC Section 503",
        "tamil": "பிரிவு 503 – மிரட்டல் குற்றமாகும். தண்டனை: 2 ஆண்டுகள் வரை சிறை அல்லது அபராதம்.",
        "english": "Section 503 – Criminal Intimidation: Threatening someone with injury to person or reputation. Punishment: Up to 2 years imprisonment or fine."
    }
}

# -------------------------
# Streamlit App Design
# -------------------------
st.set_page_config(page_title="English → Tamil Legal Awareness", page_icon="⚖️", layout="centered")
st.title("⚖️ English → Tamil Legal Awareness App")
st.write("Enter any English sentence or SMS to know related Tamil legal awareness information.")

# -------------------------
# Input box
# -------------------------
text_input = st.text_area("📝 Enter your English message:")

if text_input:
    # Translate to Tamil
    translated = translator.translate(text_input, src="en", dest="ta").text
    st.subheader("🗣️ Tamil Translation:")
    st.success(translated)

    # Generate Tamil voice
    tts = gTTS(translated, lang="ta")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        audio_path = tmp.name
    st.audio(audio_path, format="audio/mp3")

    # -------------------------
    # Detect keywords and show legal awareness
    # -------------------------
    st.markdown("---")
    st.subheader("📜 Legal Awareness")

    found = False
    for keyword, info in legal_db.items():
        if keyword.lower() in text_input.lower():
            found = True
            # Default Tamil view with English toggle
            with st.expander(f"{info['section']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**🗣 Tamil:** {info['tamil']}")
                with col2:
                    if st.button(f"🇬🇧 View English – {info['section']}", key=keyword):
                        st.info(info["english"])

    if not found:
        st.warning("⚠️ No specific legal section found for this message. Please check your input.")

    # -------------------------
    # User Feedback Section
    # -------------------------
    st.markdown("---")
    st.subheader("🧠 User Feedback")
    feedback = st.radio("Did you understand the awareness message?", ("✅ Understand", "❌ Not Understand"))

    if feedback == "❌ Not Understand":
        option = st.radio("How do you want clarification?", ("🗣️ Voice", "💬 Text", "🔁 Both"))
        st.info(f"You selected: {option}. Future versions will improve based on this feedback.")






