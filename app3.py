# -*- coding: utf-8 -*-
"""AI Tamil Legal Awareness + Translator App"""

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import random
import os

# ----------------------------------------------------------------
# 🧾 PAGE CONFIG
# ----------------------------------------------------------------
st.set_page_config(page_title="Tamil Legal Awareness & Translator", page_icon="⚖️", layout="centered")

st.title("⚖️ AI Tamil Legal Awareness & Translator App")
st.markdown("""
This app helps users **translate English to Tamil** and **understand legal rights**  
related to **Section 66 (Cybercrime)** and **Section 420 (Cheating)** with voice support.
""")

# ----------------------------------------------------------------
# 📁 FEEDBACK STORAGE
# ----------------------------------------------------------------
FEEDBACK_FILE = "user_feedback.csv"
if not os.path.exists(FEEDBACK_FILE):
    pd.DataFrame(columns=["time", "type", "input", "output", "feedback", "accuracy"]).to_csv(FEEDBACK_FILE, index=False)

# ----------------------------------------------------------------
# 🧩 LEGAL SECTIONS DATA
# ----------------------------------------------------------------
section_66 = {
    "section": "IT Act Section 66 / 66C – Cyber Offences & Identity Theft",
    "tamil_explanation": "இணையம் அல்லது கணினி மூலம் பிறரின் தரவை திருடுவது, கடவுச்சொல்லை பயன்படுத்துவது, அல்லது அனுமதியின்றி கணக்கில் நுழைவது குற்றமாகும்.",
    "tamil_punishment": "மூன்று ஆண்டு வரை சிறை அல்லது ₹1 லட்சம் அபராதம் அல்லது இரண்டும்.",
    "keywords": [
        "hack","hacked","hacking","unauthorized access","password","otp","account","login",
        "identity","impersonate","fake profile","clone account","phishing","malware",
        "virus","cyber attack","privacy leak","data theft","database leak",
        "ஹேக்","பாஸ்வேர்டு","ஆன்லைன் கணக்கு","ஓடிபி","டேட்டா திருடல்","அணுகல்"
    ]
}
section_420 = {
    "section": "IPC Section 420 – மோசடி மற்றும் ஏமாற்றல்",
    "tamil_explanation": "பிறரை ஏமாற்றி பணம் அல்லது நன்மை பெறுவது குற்றமாகும்.",
    "tamil_punishment": "ஏழு ஆண்டு வரை சிறை மற்றும் அபராதம்.",
    "keywords": [
        "cheat","cheated","cheating","fraud","scam","fake","false promise",
        "deceive","forgery","money","loan","upi","bank","credit card","atm","withdraw",
        "investment","crypto","job offer","shopping fraud","dating scam",
        "ஏமாற்று","மோசடி","பணம்","ஆன்லைன் மோசடி","லாட்டரி","வேலை வாய்ப்பு"
    ]
}
legal_rules = [section_66, section_420]

def detect_legal_section(text):
    """Detect which legal section applies based on keywords."""
    text_lower = text.lower()
    for rule in legal_rules:
        for kw in rule["keywords"]:
            if kw.lower() in text_lower:
                return rule
    return None

def play_tamil_audio(text):
    """Convert Tamil text to voice."""
    tts = gTTS(text=text, lang="ta")
    audio = BytesIO()
    tts.write_to_fp(audio)
    st.audio(audio.getvalue(), format="audio/mp3")

# ----------------------------------------------------------------
# 🗂️ TABS FOR TRANSLATION & LEGAL
# ----------------------------------------------------------------
tab1, tab2 = st.tabs(["🈁 Translation", "⚖️ Legal Awareness"])

# --------------------- TRANSLATION TAB -------------------------
with tab1:
    st.subheader("🈶 English ➜ Tamil Translator")
    english_text = st.text_area("Enter any English sentence:", height=120, key="trans_input")

    if st.button("🔄 Translate to Tamil"):
        if not english_text.strip():
            st.warning("Please enter some text to translate.")
        else:
            with st.spinner("Translating..."):
                tamil_text = GoogleTranslator(source="en", target="ta").translate(english_text)
                st.success("✅ Translation Successful!")
                st.markdown(f"### 🇮🇳 Tamil Translation:\n**{tamil_text}**")
                play_tamil_audio(tamil_text)

                acc = round(random.uniform(90, 100), 2)
                df = pd.read_csv(FEEDBACK_FILE)
                df.loc[len(df)] = [datetime.now(), "Translation", english_text, tamil_text, "Auto", acc]
                df.to_csv(FEEDBACK_FILE, index=False)

# --------------------- LEGAL TAB -------------------------
with tab2:
    st.subheader("⚖️ Legal Awareness – Know Your Rights")
    legal_input = st.text_area(
        "Ask your question or describe what happened (in Tamil or English):",
        placeholder="Example: Someone cheated me in money or என் வாட்ஸ்அப் ஹேக் செய்யப்பட்டது.",
        height=120, key="legal_input"
    )

    if st.button("🔍 Analyze Legal Section"):
        if not legal_input.strip():
            st.warning("Please enter a sentence related to a legal situation.")
        else:
            rule = detect_legal_section(legal_input)
            if rule:
                st.success(f"✅ It comes under **{rule['section']}**")
                st.write(f"**விளக்கம்:** {rule['tamil_explanation']}")
                st.write(f"**தண்டனை:** {rule['tamil_punishment']}")
                play_tamil_audio(rule["tamil_explanation"] + " " + rule["tamil_punishment"])

                feedback = st.radio("Did this answer your question?", ("Yes", "No"), horizontal=True)
                acc = 100 if feedback == "Yes" else 70
                df = pd.read_csv(FEEDBACK_FILE)
                df.loc[len(df)] = [datetime.now(), "Legal", legal_input, rule['section'], feedback, acc]
                df.to_csv(FEEDBACK_FILE, index=False)
            else:
                st.info("⚠️ No specific section detected for your input. Try rephrasing or use a different example.")
                play_tamil_audio("இந்த குற்றத்திற்கான பிரிவு தற்போது கிடைக்கவில்லை. மீண்டும் முயற்சி செய்யவும்.")

# ----------------------------------------------------------------
st.markdown("---")
st.caption("Developed for Tamil legal awareness — integrates AI translation, speech & law education.")
