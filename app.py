import streamlit as st
import requests

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI - Smart Farming Assistant")

HF_TOKEN = st.secrets.get("HF_API_TOKEN")

if not HF_TOKEN:
    st.warning("🚨 Hugging Face API token not found. Please add it in Streamlit Cloud → Settings → Secrets.")
else:
    MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.1"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    st.markdown("👨‍🌾 Ask your agriculture-related question below (e.g., crops, soil, pests, irrigation).")

    user_input = st.text_input("📝 Your question:")

    if user_input:
        with st.spinner("🤖 Thinking..."):
            try:
                prompt = f"### Instruction:\nAnswer the following farming-related question:\n{user_input}\n\n### Response:\n"
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={"inputs": prompt}
                )
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result[0]["generated_text"]
                    st.success(generated_text.strip())
                else:
                    st.error(f"❌ API Error: {response.status_code}\nDetails: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Network error: {e}")
