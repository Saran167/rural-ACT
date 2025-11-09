import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os

st.set_page_config(page_title="Legal Awareness Chat", layout="centered")

translator = Translator()

# Header
st.markdown("<h1 style='text-align:center;color:#004080;'>🛡️ Legal Awareness Chat Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align:center;'>Understand your rights and Indian laws in Tamil</h5>", unsafe_allow_html=True)

# User Input
user_input = st.text_input("Enter your problem or issue (in English):", "")

# Legal database (expanded and more descriptive)
legal_db = {
    "harassment": {
        "section": "Section 354, IPC & Section 509 IPC",
        "details": (
            "Section 354 IPC: Assault or use of criminal force to a woman with intent to outrage her modesty. "
            "Punishment: Imprisonment up to 5 years and fine.\n\n"
            "Section 509 IPC: Word, gesture, or act intended to insult the modesty of a woman. "
            "Punishment: Imprisonment up to 3 years and fine.\n\n"
            "Additionally, Section 66E of the IT Act covers violation of privacy through online harassment or sharing private content."
        )
    },
    "cyberbullying": {
        "section": "Section 66A, 67 IT Act & 509 IPC",
        "details": (
            "Section 66A IT Act: Sending offensive messages through communication service. "
            "Punishment: Up to 3 years imprisonment.\n\n"
            "Section 67 IT Act: Publishing or transmitting obscene material electronically.\n\n"
            "Section 509 IPC: Using words or gestures intended to insult the modesty of a woman."
        )
    },
    "theft": {
        "section": "Section 378 IPC",
        "details": (
            "Whoever dishonestly takes any movable property out of someone’s possession without consent is said to commit theft. "
            "Punishment: Imprisonment up to 3 years or fine or both."
        )
    },
    "domestic violence": {
        "section": "Protection of Women from Domestic Violence Act, 2005",
        "details": (
            "Covers physical, emotional, sexual, verbal, and economic abuse. "
            "Women can approach Protection Officers, NGOs, or the nearest police station for immediate help."
        )
    },
    "online fraud": {
        "section": "Section 66D IT Act & Section 420 IPC",
        "details": (
            "Section 66D IT Act: Punishment for cheating by personation using computer resources. "
            "Punishment: Up to 3 years imprisonment and fine up to ₹1 lakh.\n\n"
            "Section 420 IPC: Cheating and dishonestly inducing delivery of property. "
            "Punishment: Up to 7 years imprisonment and fine."
        )
    }
}

if user_input:
    found = False
    for keyword, law in legal_db.items():
        if keyword.lower() in user_input.lower():
            found = True

            st.subheader("📘 Legal Awareness (in Tamil):")
            tamil_text = translator.translate(law["details"], src="en", dest="ta").text
            st.write(tamil_text)

            tts = gTTS(text=tamil_text, lang='ta')
            tts.save("law.mp3")
            st.audio("law.mp3")

            st.markdown("**English Reference:**")
            st.info(f"{law['section']}\n\n{law['details']}")
            break

    if not found:
        st.warning("⚠️ No specific law found for your query. Please try a different description.")

# Feedback Section
st.markdown("---")
st.subheader("🗣️ Feedback")
feedback = st.radio("Did you understand the legal information?", ["Yes", "Not Understand"], index=None)

if feedback == "Yes":
    st.success("✅ Feedback saved successfully. Glad you understood!")

elif feedback == "Not Understand":
    st.markdown("### Choose how you want to receive help:")
    feedback_type = st.radio(
        "Select one option:",
        ["📝 Text", "🔊 Voice", "🎧 Both"],
        index=None
    )

    if feedback_type:
        st.success("✅ Feedback saved successfully.")

        if feedback_type == "📝 Text":
            st.info("We'll provide a simpler text explanation soon.")

        elif feedback_type == "🔊 Voice":
            st.info("We'll send you the explanation in Tamil voice shortly.")

        elif feedback_type == "🎧 Both":
            st.info("We'll send both Tamil text and voice explanation shortly.")

st.markdown("<hr><center>© 2025 Rural ACT - Legal Awareness Platform</center>", unsafe_allow_html=True)











