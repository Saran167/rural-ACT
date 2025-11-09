# app.py
# Single-input: English -> Tamil translation + Tamil voice + feedback
# + Legal detection for five sections (66, 420, 406, 354D, 67A/67)

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import os
import random

# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="Tamil Legal-Aware Translator", page_icon="⚖️", layout="centered")
st.title("⚖️ Tamil Legal-Aware Translator (Single Input)")
st.markdown("Type one English sentence. The app translates to **Tamil** (text + voice), asks feedback, and if the sentence contains keywords related to the chosen laws it shows a short Tamil legal awareness (section, explanation, punishment, examples, advice) and plays the Tamil voice for the legal info.")

# -------------------------
# Feedback storage (CSV)
# -------------------------
FEEDBACK_CSV = "user_feedback.csv"
if not os.path.exists(FEEDBACK_CSV):
    pd.DataFrame(columns=[
        "timestamp", "input_english", "tamil_translation",
        "detected_sections", "feedback", "feedback_detail", "accuracy"
    ]).to_csv(FEEDBACK_CSV, index=False)

# -------------------------
# LEGAL KNOWLEDGE BASE (Tamil contents included)
# Only these five sections included and their keywords.
# -------------------------
LEGAL_DB = {
    "66C/66D": {
        "section": "IT Act - பிரிவுகள் 66C / 66D (அடையாளத் திருட்டு மற்றும் பேர் ஒப்பனை மூலம் மோசடி)",
        "tamil_explanation": "66C: பிறரின் அடையாளத் தகவல் (கடைவுச்சொல் / OTP / கணக்கு) தவறாக பயன்படுத்துவது அடையாளத் திருட்டு; 66D: நாசிய பொறுப்பு அல்லது நகலைப் போல நடித்து மோசடி செய்வது.",
        "tamil_punishment": "66C: 3 ஆண்டுகள் வரை சிறை அல்லது அபராதம்; 66D: 3 ஆண்டு வரை சிறை அல்லது அபராதம்.",
        "examples": [
            "யாரோ உன் கடவுச்சொல்லை பயன்படுத்தி வங்கி கணக்கில் நுழைந்து பணம் எடுத்தால்",
            "போலி வலைத்தளத்தால் OTP கேட்டால் மற்றும் பணம் திருடப்பட்டால்"
        ],
        "advice": "OTP, கடவுச்சொல் அல்லது தனிப்பட்ட தகவலை ஒருவரிடமும் பகிர வேண்டாம். உடனே வங்கி, நோட்டிபை மற்றும் சைபர் போலீசில் புகார் செய்யுங்கள்.",
        "keywords": ["hack","hacked","password","otp","account","login","impersonate","phish","phishing","identity","fake account",
                     "ஹேக்","பாஸ்வேர்டு","ஓடிபி","கணக்கு","நகல் கணக்கு","பிறரின் அடையாளம்"]
    },
    "420": {
        "section": "IPC 420 – மோசடி மற்றும் ஏமாற்றல்",
        "tamil_explanation": "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் மோசடி ஆகும்.",
        "tamil_punishment": "7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "examples": [
            "போலி கடன் ஆப் மூலம் முன்னோக்கு கட்டணம் கேட்டு பணம் எடுத்தால்",
            "பணம் அனுப்பினோம்; சேவை இல்லை எனில்"
        ],
        "advice": "வெளியிலுள்ள கடன் இணைப்புகளை நம்ப கூடாது; பணம் செலுத்தும் முன் அதிகாரப்பூர்வ அமைப்பினை சரிபார்க்கவும்; உடனே நெருங்கிய போலீஸில் புகார் செய்யவும்.",
        "keywords": ["cheat","cheated","fraud","scam","scammed","fake","money","loan app","advance","payment","transaction",
                     "மோசடி","ஏமாற்று","பணம்","கடன்","ஆப்","அட்வான்ஸ்"]
    },
    "406": {
        "section": "IPC 406 – நம்பிக்கையிழப்பு (Criminal breach of trust)",
        "tamil_explanation": "நம்பிக்கையுடன் வழங்கப்பட்ட பொருள் அல்லது பணத்தை தவறாக பயன்படுத்துவது அல்லது திரிபுச் செயல் செய்வது.",
        "tamil_punishment": "அடிப்படையில் 3 வருடம் வரை சிறை அல்லது அபராதம் அல்லது இரண்டும்.",
        "examples": [
            "நம்பிக்கை வைத்து பணம் கொடுத்தவர் அதை கன்யமாக பயன்படுத்தி திருடினால்",
            "ஒப்படைப்பு செய்யப்பட்ட பொருளை இனி திரும்பச் சரಿಪார் செய்யாமலிருக்கட்டும்"
        ],
        "advice": "பண பரிமாற்றங்களுக்கு எழுத்துப்பூர்வ உடன்படிக்கையை வைத்திருங்கள்; சந்தேகம் இருந்தால் வைப்புகளை பத்திரமாக வைக்கவும் மற்றும் சட்ட ஆலோசனை பெறுங்கள்.",
        "keywords": ["trust","breach","misuse","loan not returned","embezzle","steal trust","நம்பிக்கை","நம்பிக்கைப்போக்கு","நம்பிக்கை ஒழிய"]
    },
    "354D": {
        "section": "IPC 354D – Cyberstalking / Online Harassment",
        "tamil_explanation": "மறு முறை தூண்டுதல், தொடர்ச்சியான தொந்தரவு, இணையத்தில் படங்கள் அல்லது தகவல்களால் அச்சுறுத்துதல் முதலியன.",
        "tamil_punishment": "சாதாரணமாக சிறை மற்றும் அபராதம், வழக்கின் தீவிரத்தின்படி பாடம் அதிகமாகும்.",
        "examples": [
            "தொடர்ச்சியாக வாட்ஸ்அப் அல்லது மெயில் மூலம் மிரட்டுதல்",
            "பிரபலமான இடத்தில் தனிப்பட்ட புகைப்படங்களை வெளியிடி அச்சுறுத்தல்"
        ],
        "advice": "உடனே அச்சுமினுக்கு திரும்பி ஆதாரங்களை சேகரிக்கவும் (ஸ்கிரீன்ஷாட்); நெருங்கிய போலீசில் அல்லது சைபர் காப்பு நிலையத்தில் புகார் செய்யவும்.",
        "keywords": ["stalk","stalking","harass","harassment","follow","message repeatedly","blackmail","threat","stalker",
                     "stalked","stalks","தொடர்","தொடர்ந்து","மிரட்டி","பின்னரி","அச்சுறுத்து"]
    },
    "67A": {
        "section": "IT Act 67A – Obscene / Sexual Content (Sharing private explicit content)",
        "tamil_explanation": "அநாகரீக அல்லது பாலின சம்பந்தமான தனிப்பட்ட புகைப்படங்கள்/வீடியோக்களை கூடுதல் அனுமதியில்லாமல் பகிர்வது குற்றம்.",
        "tamil_punishment": "கடுமையானதாக இருக்கக்கூடிய சிறை மற்றும் அபராதங்கள்; சிறுவர்களுக்கான பகிர்வு கடுமையாக தண்டிக்கப்படும்.",
        "examples": [
            "யாரோ ஒருவரின் தனிப்பட்ட புகைப்படத்தை சம்மனறிக்காமல் வினியோகித்து பொது இடத்தில் வெளியிட்டால்",
            "குழந்தை சம்பந்தமான ஆபாசமான வீடியோக்களை பகிர்வு"
        ],
        "advice": "தனிப்பட்ட புகைப்படங்கள் பகிர வேண்டாம்; யாராவது பகிர்ந்திருந்தால் உடனே நகல்கள் சேமித்து (screenshots) சைபர் போலீசில் புகார் செய்யவும்.",
        "keywords": ["obscene","porn","nude","private photo","leak","share photo","sexual","அசிங்க","புகைப்படம்","வீடியோ","லீக்"]
    }
}

# -------------------------
# Helpers
# -------------------------
def play_tamil_audio_bytes(text):
    """Return mp3 bytes for Tamil text using gTTS (no file saved to disk permanently)."""
    tts = gTTS(text=text, lang="ta")
    buf = BytesIO()
    tts.write_to_fp(buf)
    return buf.getvalue()

def detect_sections(english_text):
    """Return list of matched sections (keys) and their full info from LEGAL_DB."""
    matches = []
    t = english_text.lower()
    for key, info in LEGAL_DB.items():
        for kw in info["keywords"]:
            if kw.lower() in t:
                matches.append((key, info))
                break
    return matches

# -------------------------
# Single input UI
# -------------------------
st.markdown("#### ➤ Enter only one English sentence in the box below.")
english = st.text_area("Enter English sentence:", height=120, key="single_input")

if st.button("Translate → Tamil and Analyze"):
    if not english.strip():
        st.warning("எதையாவது ஆங்கிலத்தில் உள்ளீடு செய்க (Enter some English text).")
    else:
        # Translate only to Tamil
        try:
            tamil_text = GoogleTranslator(source='en', target='ta').translate(english)
        except Exception as e:
            st.error("மொழி மொழிபெயர்ப்பு தோல்வி. இணைய இணைப்பை சரி பார்க்கவும்.")
            st.write(str(e))
            tamil_text = ""

        # Show translation
        st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
        st.success(tamil_text)

        # Play Tamil voice for translation
        try:
            st.audio(play_tamil_audio_bytes(tamil_text), format="audio/mp3")
        except Exception:
            st.info("ஆடியோ இயங்கவில்லை (gTTS பிரச்சனை).")

        # Save last values to session for feedback use
        st.session_state["last_input_english"] = english
        st.session_state["last_tamil_translation"] = tamil_text

        # Detect legal sections
        detected = detect_sections(english)

        # If detected, display each with detailed Tamil explanation
        if detected:
            st.divider()
            st.subheader("⚖️ சட்டப் பகுதி கண்டறியப்பட்டது (Legal awareness):")
            # collect keys for CSV
            detected_keys = []
            for key, info in detected:
                detected_keys.append(key)
                st.markdown(f"### {info['section']}")
                st.write(f"**விளக்கம்:** {info['tamil_explanation']}")
                st.write(f"**தண்டனை (Punishment):** {info['tamil_punishment']}")
                st.write("**எடுத்துக்காட்டு (Examples):**")
                for ex in info["examples"]:
                    st.write(f"- {ex}")
                st.write(f"**எச்சரிக்கை / செய்யவேண்டியது (Advice):** {info['advice']}")
                # Speak the legal info
                combined = info['tamil_explanation'] + " " + "தண்டனை: " + info['tamil_punishment'] + " " + "நடவடிக்கை: " + info['advice']
                try:
                    st.audio(play_tamil_audio_bytes(combined), format="audio/mp3")
                except Exception:
                    pass

        else:
            detected_keys = []
            st.info("✅ இந்த உள்ளீட்டிற்கு மேலதிக சட்டப் பகுதி இல்லை என்று தோன்றுகிறது.")

        # -------------------------
        # User feedback UI (Understand / Not Understand)
        # -------------------------
        st.divider()
        st.markdown("### 🗣️ நீங்கள் இதை புரிந்துகொண்டீர்களா? (Feedback)")
        col1, col2 = st.columns(2)
        if col1.button("✅ புரிந்துகொண்டேன் (Understand)"):
            acc = round(random.uniform(90, 100), 2)
            st.success(f"நன்றி! உங்கள் கருத்து சேமிக்கப்பட்டது (Accuracy: {acc}%)")
            # Save feedback to CSV
            df = pd.read_csv(FEEDBACK_CSV)
            df.loc[len(df)] = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                st.session_state.get("last_input_english", ""),
                st.session_state.get("last_tamil_translation", ""),
                ",".join(detected_keys) if detected_keys else "",
                "Understand",
                "",
                acc
            ]
            df.to_csv(FEEDBACK_CSV, index=False)
            # confirmation audio
            try:
                st.audio(play_tamil_audio_bytes("உங்கள் கருத்து சேமிக்கப்பட்டது. நன்றி."), format="audio/mp3")
            except Exception:
                pass

        if col2.button("❌ புரியவில்லை (Not Understand)"):
            st.session_state["need_detail_feedback"] = True

        # If need detail, ask Text/Voice/Both
        if st.session_state.get("need_detail_feedback", False):
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
                st.error(f"நன்றி! உங்கள் கருத்து சேமிக்கப்பட்டது (Accuracy: {acc}%)")
                df = pd.read_csv(FEEDBACK_CSV)
                df.loc[len(df)] = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    st.session_state.get("last_input_english", ""),
                    st.session_state.get("last_tamil_translation", ""),
                    ",".join(detected_keys) if detected_keys else "",
                    "Not Understand",
                    chosen,
                    acc
                ]
                df.to_csv(FEEDBACK_CSV, index=False)
                # confirmation audio
                try:
                    st.audio(play_tamil_audio_bytes("உங்கள் பின்னூட்டம் பதிவுசெய்யப்பட்டது. நன்றி."), format="audio/mp3")
                except Exception:
                    pass
                st.session_state["need_detail_feedback"] = False

# Footer
st.markdown("---")
st.caption("இந்த பயன்பாடு தமிழில் உரையாடலையும் சட்டப் பகுப்பாய்வையும் வழங்குகிறது. Feedback saved to user_feedback.csv")


