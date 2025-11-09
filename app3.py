# Cyber Law Awareness Streamlit App (English / Tamil)
# Run this file in Streamlit:  streamlit run app.py

import streamlit as st

# ----------------------- App Title -----------------------
st.title("🛡️ Cyber Law Awareness Assistant")
st.write("Stay safe online! Know your rights under Indian Cyber Laws 🇮🇳")

# ----------------------- Language Selection -----------------------
language = st.radio("Choose Language / மொழி தேர்வு செய்யவும்", ["English", "தமிழ்"])

# ----------------------- Keyword-Law Mapping -----------------------
keywords_to_laws = {
    "money": ["Section 66D", "Section 420 IPC"],
    "bank": ["Section 66C", "Section 66D"],
    "account": ["Section 66C", "Section 66D"],
    "password": ["Section 66C"],
    "otp": ["Section 66D"],
    "government": ["Section 66D"],
    "harassed": ["Section 67", "Section 67A", "Section 354 IPC"],
    "photo": ["Section 66E", "Section 67"],
    "video": ["Section 67", "Section 67A"],
    "image": ["Section 66E"],
    "cheated": ["Section 66D", "Section 420 IPC"],
    "fraud": ["Section 66D"],
    "threat": ["Section 503 IPC"],
    "blackmail": ["Section 503 IPC", "Section 67A"],
    "abuse": ["Section 509 IPC", "Section 67"],
    "fake": ["Section 66D"],
}

# ----------------------- Legal Details (English + Tamil) -----------------------
legal_details = {
    "Section 66C": {
        "en": "Section 66C – Identity Theft: Using someone else's password, signature, or digital identity is a crime.\nPunishment: Up to 3 years imprisonment and/or ₹1 lakh fine.",
        "ta": "பிரிவு 66C – அடையாள திருட்டு: பிறரின் கடவுச்சொல், கையொப்பம் அல்லது டிஜிட்டல் அடையாளத்தை தவறாக பயன்படுத்துவது குற்றம்.\nதண்டனை: 3 ஆண்டுகள் சிறைத்தண்டனை அல்லது ரூ.1,00,000 அபராதம்."
    },
    "Section 66D": {
        "en": "Section 66D – Cheating by Personation: Fraud using computer resources like fake calls, SMS, or emails.\nPunishment: Up to 3 years imprisonment and/or ₹1 lakh fine.",
        "ta": "பிரிவு 66D – போலி அடையாளத்தின் மூலம் மோசடி: போலியான அழைப்புகள், SMS, மின்னஞ்சல்கள் மூலம் ஏமாற்றுவது.\nதண்டனை: 3 ஆண்டுகள் சிறைத்தண்டனை அல்லது ரூ.1,00,000 அபராதம்."
    },
    "Section 66E": {
        "en": "Section 66E – Privacy Violation: Capturing or sharing private images without consent.\nPunishment: Up to 3 years imprisonment or ₹2 lakh fine.",
        "ta": "பிரிவு 66E – தனியுரிமை மீறல்: அனுமதி இல்லாமல் தனிப்பட்ட புகைப்படங்களை எடுப்பது அல்லது பகிர்வது.\nதண்டனை: 3 ஆண்டுகள் சிறைத்தண்டனை அல்லது ரூ.2,00,000 அபராதம்."
    },
    "Section 67": {
        "en": "Section 67 – Publishing or Transmitting Obscene Material in Electronic Form.\nPunishment: First conviction – up to 3 years and ₹5 lakh fine. Second conviction – up to 5 years and ₹10 lakh fine.",
        "ta": "பிரிவு 67 – அசிங்கமான அல்லது தவறான உள்ளடக்கத்தை இணையத்தில் பகிர்வது.\nதண்டனை: முதல் முறையாக 3 ஆண்டுகள் சிறைத்தண்டனை மற்றும் ரூ.5,00,000 அபராதம்; மீண்டும் செய்தால் 5 ஆண்டுகள் மற்றும் ரூ.10,00,000 அபராதம்."
    },
    "Section 67A": {
        "en": "Section 67A – Publishing or Transmitting Sexually Explicit Material.\nPunishment: Up to 5 years imprisonment and ₹10 lakh fine.",
        "ta": "பிரிவு 67A – பாலியல் சார்ந்த வீடியோக்கள் அல்லது படங்களை பகிர்வது.\nதண்டனை: 5 ஆண்டுகள் சிறைத்தண்டனை மற்றும் ரூ.10,00,000 அபராதம்."
    },
    "Section 354 IPC": {
        "en": "Section 354 IPC – Outraging the Modesty of a Woman.\nPunishment: 1–5 years imprisonment and fine.",
        "ta": "பிரிவு 354 (IPC) – பெண்களின் மரியாதையை அவமதிப்பது.\nதண்டனை: 1 முதல் 5 ஆண்டுகள் சிறைத்தண்டனை மற்றும் அபராதம்."
    },
    "Section 420 IPC": {
        "en": "Section 420 IPC – Cheating and Dishonest Inducement to Deliver Property.\nPunishment: Up to 7 years imprisonment and fine.",
        "ta": "பிரிவு 420 (IPC) – மோசடி அல்லது பணம்/சொத்தை ஏமாற்றி பெறுதல்.\nதண்டனை: 7 ஆண்டுகள் சிறைத்தண்டனை மற்றும் அபராதம்."
    },
    "Section 503 IPC": {
        "en": "Section 503 IPC – Criminal Intimidation or Threat.\nPunishment: Up to 2 years imprisonment, or fine, or both.",
        "ta": "பிரிவு 503 (IPC) – மிரட்டல் அல்லது அச்சுறுத்தல்.\nதண்டனை: 2 ஆண்டுகள் சிறைத்தண்டனை அல்லது அபராதம் அல்லது இரண்டும்."
    },
    "Section 509 IPC": {
        "en": "Section 509 IPC – Word, Gesture, or Act Intended to Insult the Modesty of a Woman.\nPunishment: 3 years imprisonment and fine.",
        "ta": "பிரிவு 509 (IPC) – பெண்களின் மரியாதையை அவமதிக்கும் வார்த்தைகள் அல்லது செயல்கள்.\nதண்டனை: 3 ஆண்டுகள் சிறைத்தண்டனை மற்றும் அபராதம்."
    }
}

# ----------------------- User Input -----------------------
user_input = st.text_area("✉️ Paste your message or SMS content here:")

if st.button("Analyze Message"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        found_sections = set()

        # Detect keywords
        for keyword, sections in keywords_to_laws.items():
            if keyword.lower() in user_input.lower():
                for sec in sections:
                    found_sections.add(sec)

        if found_sections:
            st.success("✅ Potential Cyber Laws Applicable:")
            for sec in found_sections:
                if sec in legal_details:
                    if language == "English":
                        st.markdown(f"**{sec}:** {legal_details[sec]['en']}")
                    else:
                        st.markdown(f"**{sec}:** {legal_details[sec]['ta']}")
        else:
            st.info("ℹ️ No specific cyber law matched your message. However, stay alert and avoid sharing personal or financial information online.")

# ----------------------- Footer -----------------------
st.markdown("---")
st.caption("🧩 Developed as part of Cyber Law Awareness Project | CERT-In & IT Act (India)")




