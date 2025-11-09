import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# ---------- Legal Awareness Data ----------
legal_data = {
    "harassed": {
        "section": "Section 354D, IPC",
        "law": "Stalking or harassment of a woman by any means, including online harassment, is punishable under Section 354D of IPC.",
        "punishment": "Up to 3 years imprisonment for the first conviction, and up to 5 years for repeat offences.",
        "rule": "Protects individuals, especially women, from unwanted contact or following either physically or online.",
        "tamil": "ஒரு பெண்ணை துரத்துதல் அல்லது தொந்தரவு செய்வது குற்றமாகும். இது இந்திய தண்டனைச் சட்டம் பிரிவு 354D இன் கீழ் தண்டனைக்குரியது."
    },
    "money": {
        "section": "Section 420, IPC",
        "law": "Cheating and dishonestly inducing delivery of property is punishable under Section 420 of IPC.",
        "punishment": "Up to 7 years imprisonment and fine.",
        "rule": "Covers cheating related to money, property, or online transactions.",
        "tamil": "பணம் அல்லது சொத்து தொடர்பான ஏமாற்றுதல் குற்றமாகும். இது பிரிவு 420 இன் கீழ் 7 ஆண்டுகள் சிறைத் தண்டனையுடன் வருகிறது."
    },
    "bank": {
        "section": "Section 66D, IT Act",
        "law": "Cheating by personation using computer resources is punishable under Section 66D of the IT Act.",
        "punishment": "Up to 3 years imprisonment and fine up to ₹1 lakh.",
        "rule": "Covers fake bank calls, online scams, and phishing.",
        "tamil": "வங்கிக் கணக்கு அல்லது ஆன்லைன் ஏமாற்றம் செய்வது தகவல் தொழில்நுட்பச் சட்டம் பிரிவு 66D இன் கீழ் தண்டனைக்குரியது."
    },
    "cyber": {
        "section": "Section 66, IT Act",
        "law": "Hacking or unauthorized access to a computer system is punishable under Section 66 of IT Act.",
        "punishment": "Up to 3 years imprisonment or fine up to ₹5 lakh or both.",
        "rule": "Protects systems from unauthorized access or data theft.",
        "tamil": "அங்கீகாரம் இல்லாமல் கணினி அமைப்பில் நுழைவு குற்றமாகும் (பிரிவு 66)."
    },
    "threat": {
        "section": "Section 503, IPC",
        "law": "Criminal intimidation by threatening another person is punishable under Section 503 of IPC.",
        "punishment": "Up to 2 years imprisonment, or fine, or both.",
        "rule": "Protects individuals from verbal or written threats.",
        "tamil": "மிரட்டல் அல்லது அச்சுறுத்தல் செயல் குற்றமாகும் (பிரிவு 503)."
    }
}

# ---------- Streamlit UI ----------
st.title("🛡️ Rural Legal Awareness Chatbot (English ➜ Tamil)")
st.markdown("### Type your message below (in English):")

user_input = st.text_area("Enter your text in English:")

if st.button("Submit"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        # ---------- Step 1: Translate English → Tamil ----------
        tamil_translation = GoogleTranslator(source='en', target='ta').translate(user_input)
        st.subheader("🈯 Tamil Translation:")
        st.write(tamil_translation)

        # ---------- Step 2: Tamil Voice (using gTTS) ----------
        tts = gTTS(tamil_translation, lang='ta')
        tts.save("tamil_voice.mp3")
        audio_file = open("tamil_voice.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        audio_file.close()
        os.remove("tamil_voice.mp3")

        # ---------- Step 3: Legal Awareness ----------
        found_section = None
        for key, value in legal_data.items():
            if key in user_input.lower():
                found_section = value
                break

        st.subheader("⚖️ Legal Awareness:")
        if found_section:
            lang_option = st.radio("Select Language:", ("Tamil", "English"))
            if lang_option == "Tamil":
                st.markdown(f"**பிரிவு:** {found_section['section']}")
                st.markdown(f"**சட்டம்:** {found_section['tamil']}")
                st.markdown(f"**தண்டனை:** {found_section['punishment']}")
            else:
                st.markdown(f"**Section:** {found_section['section']}")
                st.markdown(f"**Law:** {found_section['law']}")
                st.markdown(f"**Punishment:** {found_section['punishment']}")
                st.markdown(f"**Rule:** {found_section['rule']}")
        else:
            st.info("No specific law found for this sentence.")

        # ---------- Step 4: User Feedback ----------
        st.subheader("🗣️ User Feedback")
        feedback = st.radio("Do you understand the information?", ["Understand", "Not Understand"])
        if feedback == "Not Understand":
            reason = st.radio("Which part you didn’t understand?", ["Voice", "Text", "Both"])
            st.success(f"✅ Feedback saved: You didn't understand the {reason.lower()}. Future improvements will address this.")









