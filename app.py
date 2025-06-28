import streamlit as st
import requests

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI - Smart Farming Assistant")

HF_TOKEN = st.secrets.get("HF_API_TOKEN")

if not HF_TOKEN:
    st.warning("🚨 Hugging Face API token not found. Please add it in Streamlit Cloud → Settings → Secrets.")
else:
    MODEL_ID = "bigscience/bloomz-560m"  # ✅ Fully public and stable
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    st.markdown("👋 Ask me about farming, crops, seasons, soil, irrigation, or pest control!")

    user_input = st.text_input("📝 Your farming question:")

    if user_input:
        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={"inputs": f"Answer this farming question: {user_input}"}
                )
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list):
                        st.success(result[0]["generated_text"])
                    else:
                        st.error("⚠️ Unexpected response format.")
                else:
                    st.error(f"❌ API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Network error: {e}")
