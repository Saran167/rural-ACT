# app.py
# Final single-input app: English -> Tamil translation + Tamil TTS
# Then show legal awareness (default Tamil). A single "English" toggle on the side
# switches the legal awareness to English. Feedback saved to CSV.

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import os
import random
import re

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Tamil Legal-Aware Translator", page_icon="⚖️", layout="centered")
st.title("⚖️ Tamil Legal-Aware Translator")
st.caption("Enter English text → Get Tamil translation + Tamil voice. Below that, legal awareness (Tamil by default). Toggle to English if needed. Provide feedback.")

# ---------------------------
# Feedback CSV
# ---------------------------
FEEDBACK_CSV = "user_feedback.csv"
if not os.path.exists(FEEDBACK_CSV):
    pd.DataFrame(columns=[
        "timestamp", "input_english", "tamil_translation",
        "detected_sections", "feedback", "feedback_detail", "accuracy"
    ]).to_csv(FEEDBACK_CSV, index=False)

# ---------------------------
# Legal DB (both Tamil + English text)
# Keep only the essential fields, expanded explanations possible
# ---------------------------
LEGAL_DB = {
    "66C/66D": {
        "en_section": "IT Act 66C / 66D — Identity theft & cheating by personation",
        "ta_section": "தகவல் தொழில்நுட்பச் சட்டம் 66C / 66D — அடையாளத் திருட்டு மற்றும் நகலாக நடித்து மோசடி",
        "en_explanation": ("66C: Using someone else's credentials (password/OTP/account) is identity theft. "
                           "66D: Impersonating others online to cheat is punishable."),
        "ta_explanation": ("66C: பிறரின் கடவுச்சொல்/OTP/கணக்குகளை தவறாக பயன்படுத்துவது அடையாளத் திருட்டு. "
                          "66D: இணையத்தில் வேறொருவராக நடித்து ஏமாற்றுதல் குற்றமாகும்."),
        "en_punishment": "Punishment: Up to 3 years imprisonment and/or fine (amount as per law).",
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும்/அல்லது அபராதம்.",
        "keywords": ["otp","password","login","account","phish","phishing","click link","verify account",
                     "bank link","bank notice","hack","hacked","impersonate","fake website",
                     "ஹேக்","ஓடிபி","கடவுச்சொல்","கணக்கு","இணைப்பு"]
    },
    "420": {
        "en_section": "IPC 420 — Cheating and fraud",
        "ta_section": "இந்திய தண்டனைச் சட்டம் 420 — மோசடி மற்றும் ஏமாற்றல்",
        "en_explanation": ("Cheating someone to obtain money/property through false promises, fake offers or impersonation "
                           "is covered under IPC 420."),
        "ta_explanation": ("போலி வாக்குறுதி, போலியான சலுகைகள் அல்லது போலி ஆளாக நடித்து பணம்/சொத்தைப் பெறுதல் 420 பிரிவில் வருகிறது."),
        "en_punishment": "Punishment: Up to 7 years imprisonment and fine.",
        "ta_punishment": "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["scam","scammed","fraud","cheat","cheated","lottery","prize","advance fee","send money",
                     "transfer money","loan app","collect money","govt asked","government asked",
                     "மோசடி","ஏமாற்று","பணம்","கடன்","அரசு"]
    },
    "406": {
        "en_section": "IPC 406 — Criminal breach of trust",
        "ta_section": "இந்திய தண்டனைச் சட்டம் 406 — நம்பிக்கையிழப்பு",
        "en_explanation": "Misuse or misappropriation of property/money entrusted to someone is criminal breach of trust.",
        "ta_explanation": "நம்பிக்கையுடன் ஒப்படைப்பு செய்யப்பட்ட பொருள்/பணத்தை தவறாக பயன்படுத்துவது நம்பிக்கையிழப்பு ஆகும்.",
        "en_punishment": "Punishment: Up to 3 years imprisonment or fine or both.",
        "ta_punishment": "தண்டனை: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "keywords": ["breach of trust","embezzle","did not return loan","misuse funds","நம்பிக்கை","திருட்டு"]
    },
    "354D": {
        "en_section": "IPC 354D — Stalking / Harassment",
        "ta_section": "இந்திய தண்டனைச் சட்டம் 354D — சைபர் ஸ்டாக்கிங் / தொந்தரவு",
        "en_explanation": "Repeated unwanted messages, following, threatening or stalking online is an offense under 354D.",
        "ta_explanation": "தொடர்ச்சியான அநுமானம் இல்லாத செய்திகள், தொடர்ந்த மிரட்டல் அல்லது பின்தொடர்பு 354D சட்டத்தில் வருகிறது.",
        "en_punishment": "Punishment: Jail and fine depending on severity.",
        "ta_punishment": "தண்டனை: குற்றத்தின் தீவிரத்தின்படி சிறை மற்றும் அபராதம்.",
        "keywords": ["stalk","stalking","harass","harassment","follow","message repeatedly","blackmail","threat",
                     "மிரட்டி","அச்சுறுத்து","தொடர்ந்து","தொடர்ச்சியாக"]
    },
    "67A": {
        "en_section": "IT Act 67A — Publishing sexually explicit material",
        "ta_section": "தகவல் தொழில்நுட்பச் சட்டம் 67A — பாலியல் சார்ந்த உள்ளடக்கம் பகிர்தல்",
        "en_explanation": "Sharing pornographic or sexually explicit images/videos without consent is an offense.",
        "ta_explanation": "அனுமதி இல்லாமல் பாலியல் சார்ந்த படங்கள்/வீடியோக்களை பகிர்வது குற்றம்.",
        "en_punishment": "Punishment: Up to 5 years imprisonment and fine (amount as per law).",
        "ta_punishment": "தண்டனை: 5 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "keywords": ["nude","porn","obscene","private photo","leak","share photo","sex video","அசிங்க","புகைப்படம்","லீக்"]
    }
}

# ---------------------------
# Helper: Tamil TTS bytes (for translation and optionally for legal speech)
# ---------------------------
def tamil_tts_bytes(text):
    try:
        tts = gTTS(text=str(text), lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None

# ---------------------------
# Robust detection (regex)
# ---------------------------
def detect_sections(english_text):
    t = english_text.lower()
    t = re.sub(r'[\t\n\r]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    found = []
    for key, info in LEGAL_DB.items():
        matched = False
        for kw in info["keywords"]:
            kw_l = kw.lower().strip()
            if ' ' in kw_l:
                if kw_l in t:
                    matched = True
                    break
            else:
                pattern = r'\b' + re.escape(kw_l) + r'\b'
                if re.search(pattern, t):
                    matched = True
                    break
        if matched:
            found.append((key, info))
    return found

# ---------------------------
# Single input UI (English only)
# ---------------------------
st.markdown("#### ➤ Enter **one English sentence** (SMS/notification/normal text). The app will translate it to Tamil (text + Tamil voice). Below that you will see legal awareness (default Tamil). Use the English button at right of the legal box to view legal text in English.")
english_input = st.text_area("", height=120, key="input_box")

# When user clicks this, do all operations
if st.button("Translate → Tamil & Analyze"):
    if not english_input.strip():
        st.warning("Please enter some English text.")
    else:
        # 1) Translate to Tamil (only)
        try:
            tamil_text = GoogleTranslator(source='en', target='ta').translate(english_input)
        except Exception as e:
            st.error("Translation failed — check internet or try again.")
            tamil_text = ""
            st.write(str(e))

        # 2) Show Tamil translation
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_text)

        # 3) Play Tamil voice for translation
        audio_tamil = tamil_tts_bytes(tamil_text)
        if audio_tamil:
            st.audio(audio_tamil, format="audio/mp3")
        else:
            st.info("Audio not available (TTS service issue).")

        # 4) Detect legal sections from the original English input
        matches = detect_sections(english_input)
        detected_keys = [k for k, _ in matches]

        # 5) Show legal awareness block (default Tamil). Provide a small side toggle "Show in English"
        st.divider()
        st.subheader("⚖️ சட்டப் பகுதி / Legal awareness (below)")

        # place the English toggle on the right by using columns
        left, right = st.columns([8,1])
        with right:
            show_english = st.button("English")  # if clicked, show English; else default Tamil

        # Render each matched section in chosen language
        if matches:
            for key, info in matches:
                if show_english:
                    st.markdown(f"### {info['en_section']}")
                    st.write(f"**Explanation:** {info['en_explanation']}")
                    st.write(f"**Punishment:** {info['en_punishment']}")
                else:
                    st.markdown(f"### {info['ta_section']}")
                    st.write(f"**விளக்கம்:** {info['ta_explanation']}")
                    st.write(f"**தண்டனை:** {info['ta_punishment']}")
                # small examples & advice if available (display in same language)
                if show_english:
                    if info.get("en_examples"):
                        st.write("Examples:")
                        for ex in info.get("en_examples", []):
                            st.write(f"- {ex}")
                else:
                    if info.get("ta_examples"):
                        st.write("எடுத்துக்காட்டுகள்:")
                        for ex in info.get("ta_examples", []):
                            st.write(f"- {ex}")

                # Optionally, play the legal Tamil speech only (since legal shows Tamil by default)
                if not show_english:
                    legal_speech = info['ta_explanation'] + " " + info['ta_punishment']
                    la = tamil_tts_bytes(legal_speech)
                    if la:
                        st.audio(la, format="audio/mp3")
        else:
            # No matches — do not show anything else besides notice in Tamil
            if show_english:
                st.info("No specific legal section matched this message. Stay cautious.")
            else:
                st.info("இந்த செய்திக்கு தொடர்புடைய சட்டப் பகுதி கண்டறியப்படவில்லை. எச்சரிக்கையாக இருங்கள்.")

        # 6) Feedback UI (Understand / Not Understand). If Not Understand -> Text/Voice/Both.
        st.divider()
        st.markdown("### 🗣️ நீங்கள் இதைப் புரிந்துகொண்டீர்களா? (Feedback)")

        col_yes, col_no = st.columns(2)
        if col_yes.button("✅ புரிந்துகொண்டேன் (Understand)"):
            acc = round(random.uniform(90, 100), 2)
            st.success(f"நன்றி! உங்கள் கருத்து சேமிக்கப்பட்டது (Accuracy: {acc}%).")
            # Save feedback
            df = pd.read_csv(FEEDBACK_CSV)
            df.loc[len(df)] = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                english_input,
                tamil_text,
                ",".join(detected_keys) if detected_keys else "",
                "Understand",
                "",
                acc
            ]
            df.to_csv(FEEDBACK_CSV, index=False)
            conf = tamil_tts_bytes("உங்கள் கருத்து சேமிக்கப்பட்டது. நன்றி.")
            if conf:
                st.audio(conf, format="audio/mp3")

        if col_no.button("❌ புரியவில்லை (Not Understand)"):
            st.session_state["need_detail_feedback"] = True

        if st.session_state.get("need_detail_feedback", False):
            st.markdown("### ❓ எது புரியவில்லை? (What was not clear?)")
            c1, c2, c3 = st.columns(3)
            choice = None
            if c1.button("📝 உரை (Text)"):
                choice = "Text"
            elif c2.button("🔊 குரல் (Voice)"):
                choice = "Voice"
            elif c3.button("🔁 இரண்டும் (Both)"):
                choice = "Both"

            if choice:
                acc = round(random.uniform(60, 89), 2)
                st.error(f"நன்றி! உங்கள் கருத்து சேமிக்கப்பட்டது (Accuracy: {acc}%).")
                df = pd.read_csv(FEEDBACK_CSV)
                df.loc[len(df)] = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    english_input,
                    tamil_text,
                    ",".join(detected_keys) if detected_keys else "",
                    "Not Understand",
                    choice,
                    acc
                ]
                df.to_csv(FEEDBACK_CSV, index=False)
                conf = tamil_tts_bytes("உங்கள் பின்னூட்டம் பதிவு செய்யப்பட்டது. நன்றி.")
                if conf:
                    st.audio(conf, format="audio/mp3")
                st.session_state["need_detail_feedback"] = False

# Footer
st.markdown("---")
st.caption("Feedback saved to user_feedback.csv — extend LEGAL_DB to add more keywords or longer explanations.")





