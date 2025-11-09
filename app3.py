# --- INSTALL (run once in Colab or local terminal) ---
# !pip install streamlit googletrans==4.0.0-rc1 gtts pyngrok > /dev/null

import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os

# Initialize Translator
translator = Translator()

# ---------------- LEGAL KNOWLEDGE BASE ----------------
legal_sections = {
    "420": {
        "law": "IPC Section 420 - Cheating and Fraud",
        "tamil": "இந்திய தண்டனைச் சட்டம் பிரிவு 420 - மோசடி மற்றும் ஏமாற்றல்",
        "desc": "மற்றவரை ஏமாற்றி சொத்து அல்லது பணம் பெறுவது குற்றமாகும்.",
        "punishment": "7 ஆண்டுகள் வரை சிறைத்தண்டனை மற்றும் அபராதம்."
    },
    "406": {
        "law": "IPC Section 406 - Criminal Breach of Trust",
        "tamil": "இந்திய தண்டனைச் சட்டம் பிரிவு 406 - நம்பிக்கையிழப்பு குற்றம்",
        "desc": "நம்பிக்கையுடன் கொடுக்கப்பட்ட பொருளை தவறாக பயன்படுத்துவது குற்றம்.",
        "punishment": "3 ஆண்டுகள் வரை சிறைத்தண்டனை அல்லது அபராதம் அல்லது இரண்டும்."
    },
    "66": {
        "law": "IT Act Section 66 - Cybercrime & Hacking",
        "tamil": "தகவல் தொழில்நுட்ப சட்டம் பிரிவு 66 - இணைய குற்றம் மற்றும் ஹாக்கிங்",
        "desc": "மற்றவரின் கணினி அல்லது தரவை அனுமதியின்றி அணுகுவது குற்றமாகும்.",
        "punishment": "3 ஆண்டுகள் வரை சிறைத்தண்டனை அல்லது ₹5 லட்சம் அபராதம் அல்லது இரண்டும்."
    },
    "67": {
        "law": "IT Act Section 67 - Publishing Obscene Material Online",
        "tamil": "தகவல் தொழில்நுட்ப சட்டம் பிரிவு 67 - அசிங்கமான உள்ளடக்கங்களை இணையத்தில் வெளியிடுதல்",
        "desc": "அசிங்கமான அல்லது அநாகரீகமான உள்ளடக்கங்களை இணையத்தில் பகிர்வது குற்றமாகும்.",
        "punishment": "5 ஆண்டுகள் வரை சிறைத்தண்டனை மற்றும் ₹10 லட்சம் அபராதம்."
    },
    "498A": {
        "law": "IPC Section 498A - Cruelty by Husband or Relatives",
        "tamil": "இந்திய தண்டனைச் சட்டம் பிரிவு 498A - கணவன் அல்லது உறவினரின் கொடுமை",
        "desc": "பெண்ணுக்கு உடல் அல்லது மனவலிமை கொடுமை செய்வது குற்றமாகும்.",
        "punishment": "3 ஆண்டுகள் வரை சிறைத்தண்டனை மற்றும் அபராதம்."
    },
    "354": {
        "law": "IPC Section 354 - Assault or Criminal Force to Woman",
        "tamil": "இந்திய தண்டனைச் சட்டம் பிரிவு 354 - பெண்ணைத் தாக்குதல் அல்லது அவமதித்தல்",
        "desc": "பெண்ணை அவமதிக்கும் வகையில் தாக்குதல் அல்லது தொடுதல் குற்றமாகும்.",
        "punishment": "2 ஆண்டுகள் முதல் 5 ஆண்டுகள் வரை சிறைத்தண்டனை மற்றும் அபராதம்."
    }
}

# ---------------- STREAMLIT APP UI ----------------
st.set_page_config(page_title="AI Legal-Aware Translator", page_icon="⚖️", layout="centered")
st.title("⚖️ AI Legal-Aware Translator")
st.write("### 💬 Type any English sentence — get Tamil translation, voice, and legal awareness instantly!")

# ---------------- USER INPUT ----------------
user_input = st.text_area("Enter your English sentence:")

if st.button("Translate & Analyze"):
    if user_input.strip():
        # 1️⃣ TRANSLATION
        translation = translator.translate(user_input, src='en', dest='ta').text
        st.subheader("🈶 Tamil Translation:")
        st.success(translation)

        # 2️⃣ VOICE OUTPUT
        tts = gTTS(translation, lang='ta')
        tts.save("tamil_voice.mp3")
        st.audio("tamil_voice.mp3")

        # 3️⃣ USER FEEDBACK
        st.write("#### 📢 Feedback:")
        feedback = st.radio(
            "Did you understand the translation?",
            ["✅ Yes, I understood", "❌ No, I didn't understand"]
        )

        if feedback == "❌ No, I didn't understand":
            reason = st.radio(
                "Select the reason:",
                ["Text not clear", "Voice not clear", "Both not clear"]
            )
            st.info(f"📝 Feedback noted: {reason}")

        # 4️⃣ LEGAL AWARENESS CHECK
        matched_sections = []
        for section, info in legal_sections.items():
            keywords = {
                "420": ["cheat", "fraud", "scam", "fake", "duplicate", "money", "trick", "con", "swindle"],
                "406": ["trust", "property", "misuse", "breach"],
                "66": ["hack", "cyber", "data", "computer", "account", "phish", "virus"],
                "67": ["obscene", "vulgar", "photo", "image", "video", "sexual", "post"],
                "498A": ["husband", "wife", "torture", "dowry", "violence", "family"],
                "354": ["touch", "harass", "molest", "girl", "woman", "abuse"]
            }
            for kw in keywords.get(section, []):
                if kw.lower() in user_input.lower():
                    matched_sections.append((section, info))
                    break

        if matched_sections:
            st.subheader("⚖️ Legal Awareness Found:")
            for section, info in matched_sections:
                st.markdown(f"**{info['law']}**")
                st.markdown(f"📘 *{info['tamil']}*")
                st.write(f"📝 விளக்கம்: {info['desc']}")
                st.write(f"🚫 தண்டனை: {info['punishment']}")

                # Tamil voice for legal info
                voice_text = f"{info['tamil']}. {info['desc']}. தண்டனை: {info['punishment']}"
                tts_legal = gTTS(voice_text, lang='ta')
                tts_legal.save("legal_tamil.mp3")
                st.audio("legal_tamil.mp3")

        else:
            st.info("✅ No legal issue detected in your input.")
    else:
        st.warning("⚠️ Please enter some text to translate and analyze.")

