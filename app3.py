import streamlit as st
from gtts import gTTS
import os

# ---------------------------
# 💬 Offline English → Tamil mini translator
# ---------------------------
translation_dict = {
    "hello": "வணக்கம்",
    "how are you": "நீங்கள் எப்படி இருக்கிறீர்கள்",
    "money": "பணம்",
    "bank": "வங்கி",
    "friend": "நண்பர்",
    "government": "அரசு",
    "hacked": "கணக்கு ஹேக் செய்யப்பட்டது",
    "harassed": "துன்புறுத்தப்பட்டது",
    "cheated": "ஏமாற்றப்பட்டது",
    "cyber": "இணைய பாதுகாப்பு",
    "security": "பாதுகாப்பு",
    "account": "கணக்கு",
}

def translate_to_tamil(text):
    text = text.lower()
    tamil_words = []
    for word in text.split():
        tamil_words.append(translation_dict.get(word, word))
    return " ".join(tamil_words)

def play_tamil_audio(tamil_text):
    tts = gTTS(tamil_text, lang='ta')
    tts.save("temp.mp3")
    st.audio("temp.mp3", format="audio/mp3")
    os.remove("temp.mp3")

# ---------------------------
# ⚖️ Legal Awareness Data
# ---------------------------
legal_sections = {
    "66": {
        "keywords": ["hacked", "cyber", "security", "account", "malware", "virus", "data theft"],
        "english": """Section 66 – Computer-related offences.
Covers unauthorized access, hacking, data theft, and misuse of information.
Punishment: Imprisonment up to 3 years or fine up to ₹5 lakhs or both.""",
        "tamil": """பிரிவு 66 – கணினி தொடர்பான குற்றங்கள்.
அனுமதியின்றி கணினி அணுகல், ஹேக்கிங், தரவு திருட்டு மற்றும் தவறான தகவல் பயன்பாடு.
தண்டனை: 3 ஆண்டுகள் சிறை அல்லது ₹5 லட்சம் அபராதம் அல்லது இரண்டும்."""
    },
    "66D": {
        "keywords": ["cheated", "fraud", "money", "otp", "bank", "loan", "account"],
        "english": """Section 66D – Cheating by personation using computer resources.
Covers online frauds, fake calls, and bank scams.
Punishment: Imprisonment up to 3 years and fine up to ₹1 lakh.""",
        "tamil": """பிரிவு 66D – கணினி மூலம் போலிவேடம் பூண்டு ஏமாற்றுதல்.
ஆன்லைன் மோசடி, போலி அழைப்புகள் மற்றும் வங்கி மோசடிகள்.
தண்டனை: 3 ஆண்டுகள் சிறை மற்றும் ₹1 லட்சம் அபராதம்."""
    },
    "354A": {
        "keywords": ["harassed", "molest", "sexual", "touch", "girl", "woman"],
        "english": """Section 354A – Sexual harassment of women.
Covers physical or verbal sexual harassment.
Punishment: Up to 3 years imprisonment or fine or both.""",
        "tamil": """பிரிவு 354A – பெண்களை பாலியல் துன்புறுத்தல்.
உடல் அல்லது வாய்வழி பாலியல் தொந்தரவு.
தண்டனை: அதிகபட்சம் 3 ஆண்டுகள் சிறை அல்லது அபராதம் அல்லது இரண்டும்."""
    },
    "420": {
        "keywords": ["money", "cheated", "fraud", "loan", "property", "fake document"],
        "english": """Section 420 – Cheating and dishonestly inducing delivery of property.
Covers fraud, fake documents, or dishonest transactions.
Punishment: Up to 7 years imprisonment and fine.""",
        "tamil": """பிரிவு 420 – ஏமாற்றம் மற்றும் சொத்தை தவறாக பெறுதல்.
மோசடி, போலி ஆவணங்கள் அல்லது ஏமாற்றமான பரிவர்த்தனைகள்.
தண்டனை: அதிகபட்சம் 7 ஆண்டுகள் சிறை மற்றும் அபராதம்."""
    },
    "67": {
        "keywords": ["photo", "video", "nude", "share", "internet", "post"],
        "english": """Section 67 – Publishing or transmitting obscene material in electronic form.
Punishment: Up to 5 years imprisonment and fine up to ₹10 lakhs.""",
        "tamil": """பிரிவு 67 – இணையத்தில் அசிங்கமான உள்ளடக்கங்களை பகிர்வு.
தண்டனை: அதிகபட்சம் 5 ஆண்டுகள் சிறை மற்றும் ₹10 லட்சம் அபராதம்."""
    },
}

# ---------------------------
# 🧠 App Layout
# ---------------------------
st.set_page_config(page_title="Legal Awareness Translator", layout="centered")
st.title("🛡️ Legal Awareness Translator – English ➜ Tamil")

# User Input
user_input = st.text_area("Enter text in English:", placeholder="Type your message here...")

if st.button("Translate & Analyze"):
    if user_input.strip():
        # Tamil translation
        tamil_text = translate_to_tamil(user_input)
        st.subheader("🈶 Tamil Translation:")
        st.write(tamil_text)

        # Tamil Voice
        play_tamil_audio(tamil_text)

        # Legal Awareness
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
                # Language Switch
                lang_choice = st.radio(f"View Section {sec} Details In:", ["Tamil", "English"], key=sec)
                if lang_choice == "Tamil":
                    st.info(f"{info['tamil']}")
                else:
                    st.info(f"{info['english']}")
        else:
            st.warning("No specific law detected for this sentence.")

        # Feedback
        st.subheader("🗣️ User Feedback:")
        fb = st.radio("Did you understand the translation?", ["Understand", "Not Understand"], horizontal=True)
        if fb == "Not Understand":
            fb_type = st.radio("Which part was not clear?", ["Voice", "Text", "Both"], horizontal=True)
            st.success(f"✅ Feedback saved: Not understood - {fb_type}")
        else:
            st.success("✅ Glad you understood!")
    else:
        st.warning("Please enter some text first.")







