import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd
import time

# ------------------------------------------
# Title
# ------------------------------------------
st.set_page_config(page_title="Rural Act - Translator", page_icon="🌾", layout="centered")
st.title("🌾 Rural Act - Multilingual Translator")
st.write("Translate English text into your local language easily.")

# ------------------------------------------
# Language Options
# ------------------------------------------
languages = {
    "Tamil": "ta",
    "Telugu": "te",
    "Hindi": "hi",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Urdu": "ur"
}

# ------------------------------------------
# User Input
# ------------------------------------------
text_input = st.text_area("📝 Enter English text here:")
target_lang = st.selectbox("🌐 Choose target language:", list(languages.keys()))

# ------------------------------------------
# Translate Button
# ------------------------------------------
if st.button("🔄 Translate"):
    if text_input.strip() == "":
        st.warning("⚠️ Please enter some text to translate.")
    else:
        with st.spinner("Translating... please wait ⏳"):
            try:
                translated_text = GoogleTranslator(source='en', target=languages[target_lang]).translate(text_input)
                st.success(f"✅ Translated ({target_lang}):")
                st.write(translated_text)
            except Exception as e:
                st.error(f"❌ Error during translation: {e}")

# ------------------------------------------
# Optional: Save translations (for reference)
# ------------------------------------------
if st.checkbox("📁 Save translation to file"):
    if text_input.strip():
        df = pd.DataFrame([[text_input, translated_text, target_lang]],
                          columns=["Original Text", "Translated Text", "Language"])
        df.to_csv("translations.csv", mode="a", index=False, header=False)
        st.success("💾 Translation saved successfully to translations.csv")
    else:
        st.warning("⚠️ Please translate something before saving.")

# ------------------------------------------
# Footer
# ------------------------------------------
st.markdown("---")
st.caption("🌿 Developed with ❤️ using Streamlit and Deep Translator")

