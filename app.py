# app.py

import streamlit as st
from summarizer import summarize_text
import re

# --- Text Cleaner Function ---
def clean_text(text):
    # Remove repeated phone numbers, noise, and excessive whitespace
    text = re.sub(r'\b(\d{3}-\d{3}-\d{4})\b(?:\s+\1\b)+', r'\1', text)  # deduplicate phone-like strings
    text = re.sub(r'\d{3}-\d{3}-\d{4}', '', text)  # remove phone-like numbers
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
    return text.strip()

# --- Streamlit UI ---
st.set_page_config(page_title="Pegasus Summarizer", layout="wide")
st.title("📄 Pegasus-XSum Text Summarizer")
st.markdown("Enter an article or news report below, and get an accurate summary using the Pegasus model.")

# Input Text Area
user_input = st.text_area("Enter your text here:", height=300)

# Summarize Button
if st.button("Summarize"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some text to summarize.")
    else:
        st.info("⏳ Cleaning and summarizing your text...")
        cleaned_input = clean_text(user_input)

        try:
            summary = summarize_text(cleaned_input)
            st.success("✅ Summary generated successfully!")
            st.subheader("📝 Summary")
            st.write(summary)
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
