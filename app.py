import streamlit as st
import requests
from requests.exceptions import RequestException

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI - Smart Farming Assistant")

# Get Hugging Face token securely from Streamlit secrets
HF_TOKEN = st.secrets.get("HF_API_TOKEN", None)

# Hugging Face API config
API_URL = "https://api.huggingface.co/chat/conversations"
ASSISTANT_ID = "68600892cedee33d63776db4"

if not HF_TOKEN:
    st.warning("🚨 Hugging Face API token not found. Please add it in Streamlit Cloud → Settings → Secrets.")
else:
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    # User input box
    user_input = st.text_input("👨‍🌾 Ask AgriAI a question about farming, crops, or soil:")

    if user_input:
        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(
                    url=API_URL,
                    headers=headers,
                    json={
                        "inputs": {"text": user_input},
                        "assistant_id": ASSISTANT_ID
                    }
                )
                if response.status_code == 200:
                    reply = response.json()["generated_responses"][0]
                    st.success(reply)
                else:
                    st.error(f"❌ Hugging Face error: {response.status_code} - {response.text}")
            except RequestException as e:
                st.error(f"⚠️ Network error: {e}")
