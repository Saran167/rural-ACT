import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os

# ---------------------------
# Translator & TTS
# ---------------------------
translator = Translator()

def translate_to_tamil(text):
    result = translator.translate(text, src='en', dest='ta')
    return result.text

def play_tamil_audio(text):
    tts = gTTS(text, lang='ta')
    tts.save("temp.mp3")
    st.audio("temp.mp3", format="audio/mp3")
    os.remove("temp.mp3")

# ---------------------------
# Legal Awareness Data
# ---------------------------
legal_sections = {
    "66": {
        "keywords": ["hacked", "cyber", "security", "account", "malware", "data", "virus"],
        "english": """Section 66 – Computer-related offences.
Includes hacking, data theft, or unauthorized access.
Punishment: Imprisonment up to 3 years or fine up to ₹5 lakhs or both.""",
        "tamil": """பிரிவு 66 – கணினி குற்றங்கள்.
ஹேக்கிங், தரவு திருட்டு அல்லது அனுமதியில்லா அணுகல் ஆகியவை இதில் அடங்கும்.
தண்டனை: அதிகபட்சம் 3 ஆண்டுகள் சிறை அல்லது ₹5 லட்சம் அபராதம் அல்லது இரண்டும்."""
    },
    "66D": {
        "keywords": ["cheated", "fraud", "money", "bank", "loan", "otp", "kyc", "scam"],
        "english": """Section 66D – Cheating by personation using computer resources.
Covers online scams, fake calls, OTP or bank fraud.
Punishment: Up to 3 years imprisonment and fine up to ₹1 lakh.""",
        "tamil": """பிரிவு 66D – கணினி வழியாக போலி வேடத்தில் ஏமாற்றுதல்.
ஆன்லைன் மோசடிகள், போலி அழைப்புகள், OTP அல்லது வங்கி மோசடிகள் இதில் அடங்கும்.
தண்டனை: அதிகபட்சம் 3 ஆண்டுகள் சிறை மற்றும் ₹1 லட்சம் அபராதம்."""
    },
    "354A": {
        "keywords": ["harassed", "molest", "sexual", "touch", "woman", "girl"],
        "english": """Section 354A – Sexual harassment of women.
Covers verbal or physical sexual harassment.
Punishment: Up to 3 years imprisonment or fine or both.""",
        "tamil": """பிரிவு 354A – பெண்களை பாலியல் துன்புறுத்தல்.
உடல் அல்லது வாய்வழி பாலியல் தொந்தரவு.
தண்டனை: அதிகபட்சம் 3 ஆண்டுகள் சிறை அல்லது அபராதம் அல்லது இரண்டும்."""
    },
    "420": {
        "keywords": ["money", "fraud", "loan", "cheat", "property", "fake", "document"],
        "english": """Section 420 – Cheating and dishonestly inducing delivery of property.
Covers fraud, fake documents, and dishonest transactions.
Punishment: Up to 7 years imprisonment and fine.""",
        "tamil": """பிரிவு 420 – ஏமாற்றம் மற்றும் சொத்து பெறுதல்.
மோசடி, போலி ஆவணங்கள் அல்லது ஏமாற்றமான பரிவர்த்தனைகள்.
தண்டனை: அதிகபட்சம் 7 ஆண்டுகள் சிறை மற்றும் அபராதம்."""
    },
    "67": {
        "keywords": ["photo", "video", "nude", "share", "internet", "obscene", "post"],
        "english": """Section 67 – Publishing or transmitting obscene material online.
Covers sharing obscene images or videos.
Punishment: Up to 5 years imprisonment and fine up to ₹10 lakhs.""",
        "tamil": """பிரிவு 67 – இணையத்தில் அசிங்கமான உள்ளடக்கங்களை பகிர்வு.
அசிங்கமான புகைப்படங்கள் அல்லது வீடியோக்கள் பகிர்வது இதில் அடங்கும்.
தண்டனை: அதிகபட்சம் 5 ஆண்டுகள் சிறை மற்றும் ₹10 லட்சம் அபராதம்."""
    }
}

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Legal Awareness Translator", layout="centered")
st.title("🛡️ Legal Awareness Translator – English ➜ Tamil")

user_input = st.text_area("Enter your text in English:", placeholder="Type or paste your message here...")

if st.button("Translate & Analyze"):
    if user_input.strip():
        # Tamil translation
        tamil_text = translate_to_tamil(user_input)
        st.subheader("🈶 Tamil Translation:")
        st.write(tamil_text)

        # Tamil Voice
        play_tamil_audio(tamil_text)

        # Detect Legal Section
        matched_sections = []
        for sec, info in legal_sections.items():
            for kw in info["keywords"]:
                if kw.lower() in user_input.lower():
                    matched_sections.append(sec)
                    break

        st.subheader("⚖️ Legal Awareness:")
        if matched_sections:
            for sec in matched_sections:
                info = legal_sections[sec]
                lang_choice = st.radio(f"View Section {sec} Details:", ["Tamil", "English"], key=sec)
                if lang_choice == "Tamil":
                    st.info(info["tamil"])
                else:
                    st.info(info["english"])
        else:
            st.warning("No specific legal section found for this text.")

        # Feedback
        st.subheader("🗣️ User Feedback:")
        fb = st.radio("Did you understand the translation?", ["Understand", "Not Understand"], horizontal=True)
        if fb == "Not Understand":
            fb_type = st.radio("Which part was unclear?", ["Voice", "Text", "Both"], horizontal=True)
            st.success(f"✅ Feedback saved: Not understood - {fb_type}")
        else:
            st.success("✅ Glad you understood!")
    else:
        st.warning("Please enter text first.")








