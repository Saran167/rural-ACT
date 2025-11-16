import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Tamil Legal Awareness Translator", layout="centered")

st.title("🛡️ Tamil Legal Awareness Translator")

# -------------------- Translation Function --------------------
def translate_to_tamil(text):
    try:
        return GoogleTranslator(source='en', target='ta').translate(text)
    except:
        return None

# -------------------- Voice Function (Memory-Based Audio) --------------------
def generate_tamil_audio(tamil_text):
    try:
        tts = gTTS(tamil_text, lang="ta")
        audio_bytes = tts.stream()
        return audio_bytes
    except:
        return None

# -------------------- Legal Awareness Function --------------------
def get_legal_awareness(text):

    text_lower = text.lower()

    # IPC 354D – Harassment / Stalking
    if any(word in text_lower for word in ["harass", "harassed", "stalk", "threat", "blackmail"]):
        return (
            "IPC பிரிவு 354D - துரத்தல் / தொந்தரவு (Stalking / Harassment)\n"
            "ஒருவரை தொடர்ந்து பின்தொடர்தல், தொந்தரவு செய்தல், இணைய வழி மிரட்டல் குற்றமாகும்.\n"
            "எடுத்துக்காட்டு: ‘நீ என்னுடன் பேசாவிட்டால் உன் படங்களை வெளியிடுவேன்’ போன்ற மிரட்டல் செய்திகள் அனுப்புதல்.\n"
            "செய்ய வேண்டியது: அனைத்து ஆதாரங்களையும் (screenshots, chat logs) சேமிக்கவும்; சைபர் போலீசில் உடனடியாக புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930 - Tamil Nadu Cyber Helpline\n"
            "📚 எடுத்துக்காட்டு: 2024ல் Chennaiயில் cyberstalking செய்த நபர் கைது.\n"
            "தண்டனை: 3 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்."
        )

    # OTP / Fraud – IT ACT 66C / 66D
    if any(word in text_lower for word in ["otp", "bank", "fraud", "scam", "lottery"]):
        return (
            "IT Act 66C / 66D - அடையாள திருட்டு & ஆன்லைன் மோசடி\n"
            "OTP, password, bank account விவரங்களை கேட்டு ஏமாற்றுதல் குற்றம்.\n"
            "எடுத்துக்காட்டு: ‘உங்கள் கணக்கு தற்காலிகமாக தடுக்கப்பட்டுள்ளது – OTP பகிரவும்’.\n"
            "செய்ய வேண்டியது: OTP பகிர வேண்டாம்; உடனே 1930 எண்ணில் புகார் செய்யவும்.\n"
            "📞 உதவி எண்: 1930\n"
            "📚 எடுத்துக்காட்டு: 2023ல் OTP மோசடி மூலம் 1.5 லட்சம் இழந்த நபர்.\n"
            "தண்டனை: 3 ஆண்டுகள் சிறை + அபராதம்."
        )

    # Loan scam / Money cheating – IPC 420
    if any(word in text_lower for word in ["loan", "money", "payment", "send", "amount"]):
        return (
            "IPC பிரிவு 420 - மோசடி மற்றும் ஏமாற்றுதல்\n"
            "பிறரை ஏமாற்றி பணம் அல்லது சொத்தைப் பெறுதல் குற்றம்.\n"
            "இதில் advance fee scams, fake loan apps, lottery scams அடங்கும்.\n"
            "எடுத்துக்காட்டு: ‘நீங்கள் வெற்றி பெற்றீர்கள் — பரிசுக்காக 5000 அனுப்பவும்’.\n"
            "📞 உதவி எண்: 1930\n"
            "தண்டனை: 7 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்."
        )

    return "சட்டத்திற்கான எந்த முரண்பாடும் உங்கள் செய்தியில் கண்டறியப்படவில்லை."

# -------------------- Feedback Saving --------------------
def save_feedback(input_text, tamil_text, legal_info, fb_main, fb_detail):

    data = {
        "English_Text": input_text,
        "Tamil_Translation": tamil_text,
        "Legal_Section": legal_info,
        "Feedback": fb_main,
        "Feedback_Detail": fb_detail,
        "Timestamp": datetime.now()
    }

    df = pd.DataFrame([data])

    try:
        df_existing = pd.read_csv("user_feedback.csv")
        df = pd.concat([df_existing, df], ignore_index=True)
    except:
        pass  

    df.to_csv("user_feedback.csv", index=False)


# -------------------- UI --------------------
st.write("Enter English → Get Tamil Translation + Voice + Legal Awareness + Feedback")
user_input = st.text_area("➤ Enter English sentence:")

if st.button("Translate & Analyze"):

    if not user_input.strip():
        st.error("Please enter some text.")
        st.stop()

    # ---- TRANSLATION ----
    tamil_text = translate_to_tamil(user_input)

    st.subheader("🈶 தமிழில் மொழிபெயர்ப்பு:")
    if tamil_text:
        st.success(tamil_text)
    else:
        st.error("⚠️ Translation temporarily unavailable.")

    # ---- VOICE ----
    st.subheader("🔊 Tamil Voice:")
    if tamil_text:
        audio_data = generate_tamil_audio(tamil_text)
        if audio_data:
            st.audio(audio_data, format="audio/mp3")
        else:
            st.error("⚠️ Tamil voice could not be generated.")
    else:
        st.warning("Voice available only after successful translation.")

    # ---- LEGAL AWARENESS ----
    st.subheader("⚖️ சட்ட விழிப்புணர்வு (தமிழில்):")
    legal_output = get_legal_awareness(user_input)
    st.info(legal_output)

    # ---- FEEDBACK ----
    st.subheader("📝 User Feedback")

    fb = st.radio("Did you understand the explanation?", ["Understand", "Not Understand"])

    fb_detail = ""

    if fb == "Not Understand":
        fb_detail = st.radio("How do you want it explained?", ["Text", "Voice", "Both"])

    if st.button("Submit Feedback"):
        save_feedback(user_input, tamil_text, legal_output, fb, fb_detail)
        st.success("Feedback saved successfully ✔️")

























