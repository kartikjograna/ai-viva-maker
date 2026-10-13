import streamlit as st
import os
from dotenv import load_dotenv, set_key

def show():
    st.title("⚙️ Settings")
    st.markdown("Configure your AI API keys and provider settings.")

    # Load current env
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "")

    with st.form("settings_form"):
        new_key = st.text_input("Google Gemini API Key", value=api_key, type="password")
        save = st.form_submit_button("Save Settings")

    if save:
        # Save to .env file
        set_key(".env", "GEMINI_API_KEY", new_key)
        st.success("API Key saved successfully! Please restart the app for changes to take effect.")
        st.info("Note: In a production app, this would be stored in a secure database or secret manager.")
