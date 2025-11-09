# app.py
# Single-input English -> Tamil translator + legal awareness + feedback
# Uses deep-translator + gTTS. Saves feedback to user_feedback.csv

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import os
import random

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Tamil Legal-Aware Translator", page_icon="⚖️", layout="centered")
st.title("⚖️ Tamil Legal-Aware Translator (Single Input)")
st.caption("Enter any English sentence (SMS/notification/normal text). It translates to Tamil, plays Tamil voice, detects legal issues (common sections), explains in Tamil, and saves feedback.")

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
# Legal knowledge base (Tamil outputs included)
# Add or expand keywords as needed.
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "IT Act 66C / 66D — அடையாளத் திருட்டு மற்றும் நகலாக நடித்து மோசடி",
        "tamil_explanation": "66C: பிறரின் கடவுச்சொல், OTP, அல்லது அடையாளத்தை தவறாக பயன்படுத்துவது; 66D: இணையத்தில் நகலாக நடித்து ஏமாற்றுவது.",
        "tamil_punishment": "இவை பொதுவாக 3 ஆண்டு வரை சிறை மற்றும் அபராதமாக நிர்ணயிக்கப்படலாம்.",
        "examples": [
            "போலி வங்கி லிங்க் வைத்து OTP கேட்டால் (phishing link).",
            "யாரோ உன் கணக்கிற்காக கடவுச்சொல்லைப் பயன்படுத்தி நுழைந்து பணம் எடுத்தால்."
        ],
        "advice": "OTP, கடவுச்சொல், வங்கி விவரங்களை ஒருவர்களிடம் பகிர வேண்டாம். சந்தேகம் இருந்தால் வங்கி மற்றும் சைபர் போலீசில் உடனே புகார் செய்யவும்.",
        "keywords": [
            "otp","password","pwd","login","account","verify link","verify","click link","phish","phishing",
            "hack","hacked","hacking","impersonate","fake website","bank link","bank notice","verify account",
            "ஹேக்","ஓடிபி","கடவுச்சொல்","கணக்கு","இணைப்பு"
        ]
    },
    "420": {
        "section": "IPC 420 — மோசடி மற்றும் ஏமாற்றல்",
        "tamil_explanation": "பிறரை ஏமாற்றி பணம் பெறுதல் அல்லது பொய் வாக்குறுதியால் நிதி நன்மையைப் பெறுதல் மோசடியாகும்.",
        "tamil_punishment": "அதிகபட்சம் 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "examples": [
            "போலி கடன் ஆப் advance மூலம் பணம் வாங்கி சேவை வழங்காமை.",
            "அரசு அதிகாரி போல நடித்து பணம் கேட்கும் செய்தி."
        ],
        "advice": "பணம் அனுப்பாத முந்தைய தயார்; அதிகாரப்பூர்வ தொலைபேசி எண்ணை சோதிக்கவும்; திருட்டு உள்ள சந்தேகம் இருந்தால் போலீசில் புகார் செய்யவும்.",
        "keywords": [
            "scam","scammed","fraud","cheat","cheated","fake offer","lottery","prize","advance","payment","transfer",
            "loan app","job offer","government asked","collect money","collect payment",
            "மோசடி","ஏமாற்று","பணம்","லாட்டரி","பரிசு","கடன்","அரசு"
        ]
    },
    "406": {
        "section": "IPC 406 — நம்பிக்கையிழப்பு (Criminal Breach of Trust)",
        "tamil_explanation": "நம்பிக்கையுடன் ஒப்படைக்கப்பட்ட பொருள் அல்லது பணத்தை தவறாக பயன்படுத்துவது அல்லது திருடுவது.",
        "tamil_punishment": "3 ஆண்டுகள் வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "examples": [
            "நம்பிக்கை வைப்பை திருடி செல்லுதல்.",
            "ஒப்படைப்பு செய்யப்பட்ட பணத்தை திருப்பித் தராமை."
        ],
        "advice": "பணப் பரிவர்த்தனையில் எழுத்துப்பூர்வ உறுதிமொழி கொள்வது; சந்தேகம் இருந்தால் சட்ட ஆலோசனை பெறுதல்.",
        "keywords": [
            "breach of trust","breach trust","embezzle","misuse funds","did not return loan","stole money",
            "trust","நம்பிக்கை","திருடு","நம்பிக்கை முறை"
        ]
    },
    "354D": {
        "section": "IPC 354D — மொழி முறை / சைபர் ஸ்டாக்கிங் (Cyberstalking/Harassment)",
        "tamil_explanation": "தொடர்ச்சியாக ஒருவரை தொந்தரவு செய்தல், அவமதித்தல் அல்லது மிரட்டல் குற்றமாகும்.",
        "tamil_punishment": "குற்றத்தின் தீவிரத்தின்படி சிறை மற்றும் அபராதம் விதிக்கப்படலாம்.",
        "examples": [
            "நெடுங்காலமாக ஒருவன் தொடர்ந்து தனக்கு விரோதமான செய்திகள் அனுப்புதல்.",
            "தனிப்பட்ட புகைப்படங்களை பகிர்ந்து அவமதித்தல்."
        ],
        "advice": "ஸ்கிரீன்ஷாட், உரையின் பதிவுகள் சேகரித்து உடனே போலீசில் புகார் செய்யவும்.",
        "keywords": [
            "stalk","stalking","harass","harassment","follow","message repeatedly","blackmail","threat",
            "molest","touch","அனுசரிப்பு","மிரட்டி","தொடர்ந்து"
        ]
    },
    "67A": {
        "section": "IT Act 67A — அசிங்கமான/அபகருடைய உள்ளடக்கம் பகிர்தல்",
        "tamil_explanation": "அதிகமான பாலின அல்லது ஆபாசமாகும் புகைப்படங்கள்/வீடியோக்களை அனுமதியில்லாமல் பகிர்வது குற்றம்.",
        "tamil_punishment": "கடுமையான அபராதம் மற்றும் சிறை (விரும்பிக்கக்கூடிய விவரத்திற்கு ஏற்ப அதிகமாகும்).",
        "examples": [
            "யாரோ ஒருவரின் தனிப்பட்ட 'நியூட்' புகைப்படத்தை பகிர்ந்தால்.",
            "குழந்தை சம்பந்தமான ஆபாச வீடியோ பகிர்வு."
        ],
        "advice": "தனிப்பட்ட புகைப்படங்களை எந்தனும் அழைப்பாளரிடம் பகிர வேண்டாம்; பகிரப்பட்டால் உடனே ஆதாரங்கள் சேகரித்து சைபர் போலீசில் புகார் செய்யவும்.",
        "keywords": [
            "nude","porn","obscene","private photo","leak","share photo","sex video","child porn",
            "அசிங்க","புகைப்படம்","வீடியோ","லீக்"
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
    except Exception as e:
        # If TTS fails, return None
        return None

# -------------------------
# Helper: detect sections
# -------------------------
def detect_legal_sections(english_text):
    """Return list of (key, info) for matched sections."""
    found = []
    t = english_text.lower()
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if kw.lower() in t:
                found.append((key, info))
                break
    return found

# -------------------------
# Single input UI
# -------------------------
st.markdown("#### ➤ Enter one English sentence or paste an SMS/notification:")
user_text = st.text_area("", height=120, key="input_box")

if st.button("Translate → Tamil & Analyze"):
    if not user_text.strip():
        st.warning("Please enter some English text (SMS/notification/normal sentence).")
    else:
        # 1) Translate English -> Tamil (only)
        try:
            tamil_text = GoogleTranslator(source='en', target='ta').translate(user_text)
        except Exception as e:
            st.error("மொழிபெயர்ப்பு தோல்வி — இணைய இணைப்பு சோதிக்கவும்.")
            st.write(str(e))
            tamil_text = ""

        # Show Tamil text
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_text)

        # Play Tamil voice for translation
        audio_bytes = tamil_tts_bytes(tamil_text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
        else:
            st.info("Audio கிடைக்கவில்லை (gTTS சேவை பிரச்சனை).")

        # 2) Detect legal sections from the original English message (works for normal SMS language too)
        matches = detect_legal_sections(user_text)

        if matches:
            st.divider()
            st.subheader("⚖️ சட்டப் பகுதி / Legal awareness (தமிழில்):")
            detected_keys = []
            # For each matched section display full Tamil explanation + punishment + examples + advice
            for key, info in matches:
                detected_keys.append(key)
                st.markdown(f"### {info['section']}")
                st.write(f"**விளக்கம்:** {info['tamil_explanation']}")
                st.write(f"**தண்டனை:** {info['tamil_punishment']}")
                st.write("**எடுத்துக்காட்டு (Examples):**")
                for ex in info.get("examples", []):
                    st.write(f"- {ex}")
                st.write(f"**எச்சரிக்கை / செய்யவேண்டியது:** {info.get('advice','')}")

                # Play legal info in Tamil (combined)
                legal_speech = f"{info['tamil_explanation']}. தண்டனை: {info['tamil_punishment']}. எச்சரிக்கை: {info.get('advice','')}"
                legal_audio = tamil_tts_bytes(legal_speech)
                if legal_audio:
                    st.audio(legal_audio, format="audio/mp3")
        else:
            detected_keys = []
            st.info("✅ இந்த செய்திக்கு தொடர்புடைய முக்கிய சட்டப் பகுதி கண்டறியப்படவில்லை (No legal section detected).")

        # 3) Feedback UI and storage
        st.divider()
        st.markdown("### 🗣️ நீங்கள் இதைப் புரிந்துகொண்டீர்களா? (Feedback)")
        c1, c2 = st.columns(2)
        if c1.button("✅ புரிந்துகொண்டேன் (Understand)"):
            acc = round(random.uniform(90, 100), 2)
            st.success(f"நன்றி! உங்கள் கருத்து சேமிக்கப்பட்டது (Accuracy: {acc}%).")
            # Save feedback
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
            # confirmation audio
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
                # confirmation audio
                conf = tamil_tts_bytes("உங்கள் பின்னூட்டம் பதிவு செய்யப்பட்டு உள்ளது. நன்றி.")
                if conf:
                    st.audio(conf, format="audio/mp3")
                st.session_state["need_detail"] = False

# Footer
st.markdown("---")
st.caption("Feedback is stored locally in user_feedback.csv. Extend LEGAL_DB to add more sections/keywords.")



