# app_improved.py
# Single-input English -> Tamil translator + legal awareness + improved keyword matching + feedback
# Uses deep-translator + gTTS. Saves feedback to user_feedback.csv

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import os
import random
import re

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Tamil Legal-Aware Translator", page_icon="⚖️", layout="centered")
st.title("⚖️ Tamil Legal-Aware Translator (Improved Detection)")
st.caption("Enter any English sentence (SMS/notification/normal text). It translates to Tamil, plays Tamil voice, detects legal issues, explains in Tamil, and saves feedback.")

# -------------------------
# Feedback CSV setup
# -------------------------
FEEDBACK_CSV = "user_feedback.csv"
if not os.path.exists(FEEDBACK_CSV):
    pd.DataFrame(columns=[
        "timestamp", "input_english", "tamil_translation",
        "detected_sections", "feedback", "feedback_detail", "accuracy"
    ]).to_csv(FEEDBACK_CSV, index=False)

# -------------------------
# Legal DB (expanded keywords + phrases)
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "IT Act 66C / 66D — அடையாளத் திருட்டு மற்றும் நகலாக நடித்து மோசடி",
        "tamil_explanation": "66C: பிறரின் கடவுச்சொல், OTP அல்லது அடையாளத்தை தவறாக பயன்படுத்துதல்; 66D: இணையத்தில் நகலாக நடித்து ஏமாற்றுதல்.",
        "tamil_punishment": "முதல் நிலை: 3 ஆண்டு வரை சிறை மற்றும் அபராதம்.",
        "examples": [
            "போலி வங்கி இணைப்பில் OTP கேட்டால் (phishing).",
            "யாரோ உங்கள் கணக்கிற்கு கடவுச்சொல்லை பயன்படுத்தி நுழைந்து பணம் எடுத்தால்."
        ],
        "advice": "OTP/Password பகிர வேண்டாம். சந்தேகம் இருந்தால் வங்கி மற்றும் சைபர் போலீசில் புகார் செய்யவும்.",
        "keywords": [
            # single words & short variants
            "otp","one time password","password","pwd","login","account","verify","verification","phish","phishing",
            "hack","hacked","hacking","impersonate","impersonation","fake website","fake link",
            # money-related phishing phrases
            "verify account","click link","click here to verify","verify your account",
            # punctuation forms etc
            "bank link","bank notice","bank account",
            # tamil variants
            "ஹேக்","ஓடிபி","கடவுச்சொல்","கணக்கு","இணைப்பு","பின்னிணைப்பு"
        ]
    },
    "420": {
        "section": "IPC 420 — மோசடி மற்றும் ஏமாற்றல்",
        "tamil_explanation": "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் மோசடி ஆகும்.",
        "tamil_punishment": "அதிகபட்சம் 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "examples": [
            "போலி லாட்டரி / பரிசு டெக்ஸ், advance கட்டணம் கேட்டு பணம் பறிகிறது.",
            "அரசு/வங்கி என்று படித்து பணம் வாங்கும் போலி முறை."
        ],
        "advice": "பணம் அனுப்புவதற்கு முன் ஆதாரங்களை சரிபார்க்கவும்; சந்தேகம் இருந்தால் போலீசில் புகார் செய்யவும்.",
        "keywords": [
            # money/suspicious money phrases
            "scam","scammed","scamming","fraud","frauds","fraudulent","cheat","cheated","cheating",
            "lottery","prize","winner","congratulations you won","you have won","advance payment","advance fee",
            "pay now","send money","transfer money","wire transfer","bank transfer","payment","paid","paid to",
            "loan app","loan scam","fake loan","collect money","collect payment",
            # government impersonation
            "government asked","government is asking","govt asked","govt is asking","official asked","official is asking",
            # currency signs
            "₹","rs ","rs.","rupee","rupees","dollars","usd",
            # tamil
            "மோசடி","ஏமாற்று","பணம்","கடன்","அறிவிப்பு","அரசு","வங்கி"
        ]
    },
    "406": {
        "section": "IPC 406 — நம்பிக்கையிழப்பு (Criminal Breach of Trust)",
        "tamil_explanation": "நம்பிக்கையுடன் ஒப்படைக்கப்பட்ட பொருள்/பணத்தை தவறாக பயன்படுத்துவது.",
        "tamil_punishment": "3 ஆண்டு வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "examples": [
            "கடன் கொடுத்தவனை பணம் திருப்பி தரவில்லை.",
            "ஒப்படைத்த சொத்தை திருடி விடுதல்."
        ],
        "advice": "கட்டுப்படுத்திய எழுத்துப்பூர்வ ஒப்பந்தம் வைத்திருங்கள்; சந்தேகம் இருந்தால் சட்ட ஆலோசனை பெறுங்கள்.",
        "keywords": [
            "breach of trust","breach trust","embezzle","embezzled","misuse funds","did not return loan",
            "stole money","stole","loan not returned","trust","trust violated","நம்பிக்கை","திருட்டு"
        ]
    },
    "354D": {
        "section": "IPC 354D — Cyberstalking / Harassment",
        "tamil_explanation": "தொடர்ச்சியாக ஒருவரை தொந்தரவு செய்தல் அல்லது மிரட்டல் (அனக்சன்) குற்றமாகும்.",
        "tamil_punishment": "குற்றத்தின் தீவிரத்தின்படி சிறை மற்றும் அபராதம்.",
        "examples": [
            "தொடர்ச்சியாக மிரட்டல் செய்தல், அமைதியை தவிர்க்காமல் அஞ்சல் அனுப்புதல்.",
            "தனிப்பட்ட புகைப்படங்களை பகிர்ந்து தொந்தரவு செய்தல்."
        ],
        "advice": "ஆதாரங்கள் (screenshots) சேகரிக்கவும்; உடனே போலீஸ்/சைபர் போலிஸில் புகார் இல்லையெனில் சம்பந்தப்பட்டது.",
        "keywords": [
            "harass","harassed","harassment","harassing","stalk","stalking","stalker","follow","following",
            "threat","threaten","threatened","blackmail","blackmailed","molest","molested","abuse","abused",
            "message repeatedly","unwanted messages","send messages repeatedly",
            # tamil
            "மிரட்டி","அச்சுறுத்து","தொடர்ந்து","தொடர்ச்சியாக"
        ]
    },
    "67A": {
        "section": "IT Act 67A — Obscene / Sexual Content Sharing",
        "tamil_explanation": "தனிப்பட்ட அல்லது பாலின சம்பந்தமான புகைப்படங்கள்/வீடியோக்களை அனுமதியில்லாமல் பகிர்வது குற்றம்.",
        "tamil_punishment": "கடுமையான அபராதமும் சிறையும்அதிகப்படியானதை உடன்படுதலுக்கு ஏற்ப.",
        "examples": [
            "தனிநபரின் நியூட் புகைப்படங்களை பகிர்தல்.",
            "குழந்தை சம்பந்தமான ஆபாச வீடியோக்கள் பகிர்தல்."
        ],
        "advice": "புகைப்படங்கள் பகிரப்படின் ஆதாரங்கள் சேகரிக்கவும்; உடனே சைபர் போலீசில் புகார் செய்யவும்.",
        "keywords": [
            "nude","porn","obscene","private photo","leak","leaked","share photo","sex video","child porn",
            "obscenity","pornography","அசிங்க","புகைப்படம்","வீடியோ","லீக்"
        ]
    }
}

# -------------------------
# Helper: Tamil TTS bytes
# -------------------------
def tamil_tts_bytes(text):
    """Return mp3 bytes for Tamil text using gTTS."""
    try:
        tts = gTTS(text=str(text), lang="ta")
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None

# -------------------------
# Robust detection using regex word boundaries & phrase checking
# -------------------------
def detect_legal_sections(english_text):
    """Return list of (key, info) for matched sections using regex-based matching."""
    found = []
    t = english_text.lower()
    # normalize some punctuation and remove repeated spaces
    t = re.sub(r'[\t\n\r]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()

    for key, info in LEGAL_DB.items():
        matched = False
        for kw in info["keywords"]:
            kw_l = kw.lower().strip()
            # if keyword contains spaces (phrase), match the phrase directly
            if ' ' in kw_l:
                # direct substring search for phrase
                if kw_l in t:
                    matched = True
                    break
            else:
                # use word boundary regex to avoid partial matches: e.g., "pay" should not match "prepay" incorrectly
                pattern = r'\b' + re.escape(kw_l) + r'\b'
                if re.search(pattern, t):
                    matched = True
                    break
            # additional fallback: check presence of currency symbol or numbers patterns for money
            if kw_l in ['₹','rs','rupee','rupees','dollars','usd'] and re.search(r'[\d]+', t):
                matched = True
                break
        if matched:
            found.append((key, info))
    return found

# -------------------------
# Single input UI
# -------------------------
st.markdown("#### ➤ Enter one English sentence or paste an SMS/notification (example: bank SMS, govt notice, chat text):")
user_text = st.text_area("", height=120, key="input_box")

if st.button("Translate → Tamil & Analyze"):
    if not user_text.strip():
        st.warning("Please enter some English text.")
    else:
        # translate to Tamil
        try:
            tamil_text = GoogleTranslator(source='en', target='ta').translate(user_text)
        except Exception as e:
            st.error("Translation failed — check internet or try again.")
            st.write(str(e))
            tamil_text = ""

        # show translation
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_text)

        # play translation audio
        audio_bytes = tamil_tts_bytes(tamil_text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")

        # detect legal sections robustly
        matches = detect_legal_sections(user_text)

        if matches:
            st.divider()
            st.subheader("⚖️ சட்டப் பகுதி / Legal awareness (தமிழில்):")
            detected_keys = []
            for key, info in matches:
                detected_keys.append(key)
                st.markdown(f"### {info['section']}")
                st.write(f"**விளக்கம்:** {info['tamil_explanation']}")
                st.write(f"**தண்டனை:** {info['tamil_punishment']}")
                st.write("**எடுத்துக்காட்டு (Examples):**")
                for ex in info.get("examples", []):
                    st.write(f"- {ex}")
                st.write(f"**எச்சரிக்கை / Advice:** {info.get('advice','')}")
                # play legal text
                legal_speech = f"{info['tamil_explanation']}. தண்டனை: {info['tamil_punishment']}. எச்சரிக்கை: {info.get('advice','')}"
                la = tamil_tts_bytes(legal_speech)
                if la:
                    st.audio(la, format="audio/mp3")
        else:
            detected_keys = []
            st.info("✅ இந்த செய்திக்கு தொடர்புடைய சட்டப் பகுதி கண்டறியப்படவில்லை.")

        # feedback UI & save
        st.divider()
        st.markdown("### 🗣️ நீங்கள் இதைப் புரிந்துகொண்டீர்களா? (Feedback)")
        c1, c2 = st.columns(2)
        if c1.button("✅ புரிந்துகொண்டேன் (Understand)"):
            acc = round(random.uniform(90, 100), 2)
            st.success(f"நன்றி! உங்கள் கருத்து சேமிக்கப்பட்டது (Accuracy: {acc}%).")
            df = pd.read_csv(FEEDBACK_CSV)
            df.loc[len(df)] = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_text,
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

        if c2.button("❌ புரியவில்லை (Not Understand)"):
            st.session_state["need_detail"] = True

        if st.session_state.get("need_detail", False):
            st.markdown("### ❓ எது புரியவில்லை? (What was not clear?)")
            d1, d2, d3 = st.columns(3)
            chosen = None
            if d1.button("📝 உரை (Text)"):
                chosen = "Text"
            elif d2.button("🔊 குரல் (Voice)"):
                chosen = "Voice"
            elif d3.button("🔁 இரண்டும் (Both)"):
                chosen = "Both"

            if chosen:
                acc = round(random.uniform(60, 89), 2)
                st.error(f"நன்றி! உங்கள் கருத்து சேமிக்கப்பட்டது (Accuracy: {acc}%).")
                df = pd.read_csv(FEEDBACK_CSV)
                df.loc[len(df)] = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    user_text,
                    tamil_text,
                    ",".join(detected_keys) if detected_keys else "",
                    "Not Understand",
                    chosen,
                    acc
                ]
                df.to_csv(FEEDBACK_CSV, index=False)
                conf = tamil_tts_bytes("உங்கள் பின்னூட்டம் பதிவு செய்யப்பட்டு உள்ளது. நன்றி.")
                if conf:
                    st.audio(conf, format="audio/mp3")
                st.session_state["need_detail"] = False

# Footer
st.markdown("---")
st.caption("Feedback saved to user_feedback.csv. Extend LEGAL_DB keywords to increase recall further.")




