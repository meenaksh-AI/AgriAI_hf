import streamlit as st
import requests

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI — Smart Agriculture Assistant")

HF_TOKEN = st.secrets.get("HF_API_TOKEN")
if not HF_TOKEN:
    st.warning("🚨 Add HF token in Streamlit Secrets.")
else:
    MODEL_ID = "facebook/opt-6.7b-instruct"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    user_input = st.text_input("📝 Ask AgriAI:")
    if user_input:
        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(API_URL, headers=headers, json={"inputs": user_input})
                if response.status_code == 200:
                    text = response.json()[0].get("generated_text")
                    st.success(text or "No response received.")
                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Network error: {e}")
