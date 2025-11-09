import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# ---------- Expanded Legal Awareness Data (Detailed Tamil Info) ----------
legal_data = {
    "harassed": {
        "section": "பிரிவு 354D, இந்திய தண்டனைச் சட்டம் (IPC)",
        "law": "ஒரு பெண்ணை துரத்துதல், மீண்டும் மீண்டும் தொடர்பு கொள்ளுதல், அல்லது ஆன்லைனில் தொந்தரவு செய்தல் குற்றமாகும். இதில் சமூக ஊடகம், மெசேஜ்கள், அழைப்புகள் மூலம் தொந்தரவு செய்தலும் அடங்கும்.",
        "punishment": "முதல் குற்றத்துக்கு 3 ஆண்டுகள் வரை சிறைத் தண்டனை; மீண்டும் குற்றம் செய்தால் 5 ஆண்டுகள் வரை சிறை மற்றும் அபராதம்.",
        "extra": "இது பெண்களை ஆன்லைன் மற்றும் நேரடி துரத்தலிலிருந்து பாதுகாக்கும் பிரிவு ஆகும். மேலும் இதற்கு இணையான பிரிவுகள் 354A (அவமதிப்பு), 509 (பெண்களுக்கு எதிரான வார்த்தை அவமதிப்பு) ஆகியவையும் சேர்க்கலாம்."
    },
    "money": {
        "section": "பிரிவு 420, இந்திய தண்டனைச் சட்டம் (IPC)",
        "law": "ஏமாற்றி அல்லது பொய்யான நம்பிக்கையால் பணம் அல்லது சொத்தைப் பெறுவது குற்றமாகும். இது ஆன்லைன் பண மோசடி, போலி முதலீட்டு சதி, வங்கி மோசடி போன்றவற்றையும் உள்ளடக்கியது.",
        "punishment": "7 ஆண்டுகள் வரை சிறைத் தண்டனை மற்றும் அபராதம்.",
        "extra": "மேலும் பிரிவு 406 (நம்பிக்கையை மீறுதல்), 417 (ஏமாற்றுதல்) ஆகியவை இதற்குச் சம்பந்தமானவை. ஆன்லைன் வங்கிகள் அல்லது UPI மூலம் ஏமாற்றங்கள் நடந்தால் இது பொருந்தும்."
    },
    "bank": {
        "section": "பிரிவு 66D, தகவல் தொழில்நுட்பச் சட்டம் (IT Act)",
        "law": "தகவல் தொழில்நுட்பம் மூலம் ஒருவரைப் போல நடித்து மோசடி செய்வது (போலி வங்கி இணையதளம், OTP கேட்கும் அழைப்புகள் போன்றவை) குற்றமாகும்.",
        "punishment": "3 ஆண்டுகள் வரை சிறைத் தண்டனை மற்றும் ₹1,00,000 வரை அபராதம்.",
        "extra": "இது வங்கிக் கணக்கு மோசடிகள், க்ளோன் கார்டு, ஃபிஷிங் (phishing), சைபர் மோசடிகள் அனைத்துக்கும் பொருந்தும். 66C (அடையாள திருட்டு) மற்றும் 419 (போலி அடையாளம்) ஆகிய பிரிவுகளும் தொடர்புடையவை."
    },
    "cyber": {
        "section": "பிரிவு 66, தகவல் தொழில்நுட்பச் சட்டம் (IT Act)",
        "law": "அங்கீகாரம் இல்லாமல் கணினி அல்லது இணைய அமைப்பில் நுழைவு, ஹாக்கிங் அல்லது தரவு திருட்டு செய்வது குற்றமாகும்.",
        "punishment": "3 ஆண்டுகள் வரை சிறைத் தண்டனை அல்லது ₹5,00,000 வரை அபராதம் அல்லது இரண்டும்.",
        "extra": "இதில் மால்வேர், வைரஸ், போட்நெட், மற்றும் தனிநபர் தரவு திருட்டு போன்றவை அடங்கும். CERT-In வழியாக புகார் அளிக்கலாம்."
    },
    "threat": {
        "section": "பிரிவு 503, இந்திய தண்டனைச் சட்டம் (IPC)",
        "law": "ஒருவரை மிரட்டுவது, அச்சுறுத்துவது, அல்லது சேதப்படுத்துவேன் என்று கூறுவது குற்றமாகும்.",
        "punishment": "2 ஆண்டுகள் வரை சிறைத் தண்டனை அல்லது அபராதம் அல்லது இரண்டும்.",
        "extra": "இது மிரட்டல் மெசேஜ்கள், ஆன்லைன் ட்ரோலிங், அல்லது புகைப்படங்களை தவறாகப் பகிர்வேன் என்ற மிரட்டல் ஆகியவற்றுக்கும் பொருந்தும்."
    }
}

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Tamil Legal Awareness App", page_icon="⚖️")
st.title("🛡️ கிராம சட்ட விழிப்புணர்வு பயன்பாடு (Rural Legal Awareness App)")
st.markdown("### 👉 கீழே உங்கள் செய்தியை (English) வடிவில் இடுங்கள்:")

user_input = st.text_area("Enter your text in English:")

if st.button("Submit"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        # ---------- Step 1: English → Tamil Translation ----------
        tamil_translation = GoogleTranslator(source='en', target='ta').translate(user_input)
        st.subheader("🈯 தமிழில் மொழிபெயர்ப்பு:")
        st.write(tamil_translation)

        # ---------- Step 2: Tamil Voice ----------
        tts = gTTS(tamil_translation, lang='ta')
        tts.save("tamil_voice.mp3")
        with open("tamil_voice.mp3", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
        os.remove("tamil_voice.mp3")

        # ---------- Step 3: Legal Awareness ----------
        st.subheader("⚖️ சட்ட விழிப்புணர்வு (Legal Awareness):")
        found = None
        for key, details in legal_data.items():
            if key in user_input.lower():
                found = details
                break

        if found:
            st.markdown(f"**🔸 பிரிவு:** {found['section']}")
            st.markdown(f"**📘 சட்ட விளக்கம்:** {found['law']}")
            st.markdown(f"**⚖️ தண்டனை:** {found['punishment']}")
            st.markdown(f"**📖 கூடுதல் தகவல்:** {found['extra']}")
        else:
            st.info("இந்த வாக்கியத்தில் எந்தவொரு சட்ட பிரிவும் அடையாளம் காணப்படவில்லை.")

        # ---------- Step 4: User Feedback ----------
        st.subheader("🗣️ பயனர் கருத்து (User Feedback)")
        feedback = st.radio("நீங்கள் இதை புரிந்துகொண்டீர்களா?", ["✅ புரிந்துகொண்டேன்", "❌ புரியவில்லை"])

        if feedback == "❌ புரியவில்லை":
            st.markdown("### 😕 எது புரியவில்லை?")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔊 Voice"):
                    st.success("✅ Feedback Saved: Voice not understood.")
            with col2:
                if st.button("📝 Text"):
                    st.success("✅ Feedback Saved: Text not understood.")
            with col3:
                if st.button("🔊📝 Both"):
                    st.success("✅ Feedback Saved: Both not understood.")










