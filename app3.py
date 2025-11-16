import streamlit as st
from deep_translator import LibreTranslator
from gtts import gTTS
import pandas as pd
import re
from datetime import datetime
import os

st.set_page_config(page_title="Tamil Legal Awareness Translator", layout="centered")

# ======================
# 1. TRANSLATION FUNCTION
# ======================
def translate_to_tamil(text):
    try:
        translated = LibreTranslator(source='en', target='ta').translate(text)
        return translated
    except Exception as e:
        print("Translation Error:", e)
        return None


# ======================
# 2. TEXT TO SPEECH (TAMIL)
# ======================
def generate_audio(tamil_text):
    try:
        file_path = "tamil_voice.mp3"
        tts = gTTS(text=tamil_text, lang="ta")
        tts.save(file_path)
        return file_path
    except Exception as e:
        print("TTS Error:", e)
        return None


# ======================
# 3. LEGAL KEYWORD–TO–SECTION MAPPING
# ======================
def get_legal_section(text):

    text_low = text.lower()

    rules = {
        r"(otp|bank|verify|account|money|fraud|transaction)": {
            "section": "IT Act 66C / 66D – OTP Fraud / Cheating",
            "explanation": "வங்கிக் கணக்கு, OTP, அல்லது பணம் தொடர்பான மோசடி செய்தல் குற்றமாகும்.",
            "action": "OTP-ஐ யாருக்கும் சொல்லாதீர்கள். 1930 உதவி எண்ணில் புகார் செய்யவும்.",
            "punishment": "3 ஆண்டுகள் சிறை + அபராதம்."
        },
        r"(harass|torture|follow|stalk|trouble)": {
            "section": "IPC 354D – Stalking / Harassment",
            "explanation": "பெண்களைத் தொடர்ந்து துரத்துதல், தொந்தரவு செய்தல், ஆன்லைன் மிரட்டல் குற்றம்.",
            "action": "அனைத்து screenshots-ஐ சேமிக்கவும்; சைபர் போலீசில் புகார் செய்யவும்.",
            "punishment": "3 ஆண்டுகள் சிறை + அபராதம்."
        },
        r"(cheat|loan|offer|gift|free|credit|upi)": {
            "section": "IPC 420 – Cheating & Fraud",
            "explanation": "பணம் அல்லது பரிசு வழங்குவதாக கூறி ஏமாற்றுவது குற்றம்.",
            "action": "அந்த link-ஐ திறக்காதீர்கள்; 1930-ல் புகார் செய்யவும்.",
            "punishment": "7 ஆண்டுகள் சிறை."
        },
        r"(abuse|threat|kill|murder|warn)": {
            "section": "IPC 506 – Criminal Intimidation",
            "explanation": "யாரையும் மிரட்டுவது குற்றமாகும்.",
            "action": "மிரட்டல் செய்திகளை சேமித்து போலீசில் புகார் செய்யவும்.",
            "punishment": "2 ஆண்டுகள் சிறை."
        },
        r"(photo|video|blackmail|nude)": {
            "section": "IT Act 67 – Sending Obscene Content",
            "explanation": "அசிங்கமான புகைப்படம்/வீடியோ அனுப்புதல் குற்றம்.",
            "action": "உடனடியாக cybercrime.gov.in-ல் புகார் செய்யவும்.",
            "punishment": "5 ஆண்டுகள் சிறை."
        }
    }

    for pattern, info in rules.items():
        if re.search(pattern, text_low):
            return info

    return {
        "section": "No Legal Issue Detected",
        "explanation": "இச் செய்தியில் சட்ட பிரச்சனை கண்டறியப்படவில்லை.",
        "action": "கவனமாக இருந்து தகவலை சரிபார்க்கவும்.",
        "punishment": "-"
    }


# ======================
# 4. FEEDBACK SAVE FUNCTION
# ======================
def save_feedback(eng, tamil, law, fb_type, fb_detail):

    file_name = "user_feedback.csv"

    row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "English Text": eng,
        "Tamil Translation": tamil,
        "Legal Section": law,
        "Feedback": fb_type,
        "Feedback Detail": fb_detail
    }

    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(file_name, index=False)


# ======================
# 5. STREAMLIT UI
# ======================
st.title("🌾 **Tamil Legal Awareness Translator – Rural ACT**")
st.write("Enter English → Get Tamil Translation + Voice + Legal Awareness + Feedback")

user_text = st.text_area("➤ Enter English sentence:")

if st.button("Translate & Analyze"):

    if user_text.strip() == "":
        st.warning("Please enter a valid English message.")
    else:
        tamil_output = translate_to_tamil(user_text)

        if tamil_output:
            st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
            st.success(tamil_output)
        else:
            st.error("⚠️ Translation temporarily unavailable.")
            tamil_output = ""

        # Tamil Voice
        if tamil_output != "":
            audio_file = generate_audio(tamil_output)
            if audio_file:
                st.audio(audio_file)
            else:
                st.error("⚠️ Tamil voice could not be generated.")

        # Legal Awareness
        info = get_legal_section(user_text)

        st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")
        st.info(f"""
**{info['section']}**

{info['explanation']}

**செய்ய வேண்டியது:** {info['action']}

**தண்டனை:** {info['punishment']}
        """)

        # Feedback section
        st.subheader("📝 Feedback")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Understand"):
                save_feedback(user_text, tamil_output, info['section'], "Understand", "All Good")
                st.success("Thanks for your feedback!")

        with col2:
            if st.button("👎 Not Understand"):
                detail = st.radio(
                    "Which part is unclear?",
                    ["Tamil Text", "Tamil Voice", "Legal Explanation", "All"]
                )
                save_feedback(user_text, tamil_output, info['section'], "Not Understand", detail)
                st.success("Feedback saved. We will improve it.")
























