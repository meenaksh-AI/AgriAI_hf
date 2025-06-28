import streamlit as st
import requests

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI - Smart Farming Assistant")

HF_TOKEN = st.secrets.get("HF_API_TOKEN")

if not HF_TOKEN:
    st.warning("🚨 Hugging Face API token not found. Please add it in Streamlit Cloud → Settings → Secrets.")
else:
    MODEL_ID = "microsoft/DialoGPT-medium"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    st.markdown("👨‍🌾 Ask anything about agriculture: crops, soil, irrigation, pests.")

    user_input = st.text_input("📝 Your question:")

    if user_input:
        with st.spinner("🤖 Thinking..."):
            try:
                payload = {
                    "inputs": {
                        "text": user_input
                    }
                }

                response = requests.post(API_URL, headers=headers, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("generated_text", "🤔 No response generated.")
                    st.success(generated_text.strip())
                else:
                    st.error(f"❌ API Error: {response.status_code}\nDetails: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Network error: {e}")
