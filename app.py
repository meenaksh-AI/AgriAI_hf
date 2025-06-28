import streamlit as st
import requests

st.set_page_config(page_title="AgriAI", page_icon="🌾")

st.title("🌾 AgriAI - Your Smart Agriculture Assistant")
st.markdown("Ask me anything about crops, farming, soil, weather, or pests!")

# Hugging Face API token from Streamlit secrets
HF_TOKEN = st.secrets["HF_API_TOKEN"]
API_URL = "https://api.huggingface.co/chat/conversations"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Input from user
user_input = st.text_input("👨‍🌾 Enter your question:")

if user_input:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                url=API_URL,
                headers=headers,
                json={
                    "inputs": {"text": user_input},
                    "assistant_id": "68600892cedee33d63776db4"
                }
            )
            if response.status_code == 200:
                answer = response.json()["generated_responses"][0]
                st.success(answer)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException:
            st.error("⚠️ Network error. Please check your connection or try on Streamlit Cloud.")
