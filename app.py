import streamlit as st
import requests
from googletrans import Translator

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI — Smart Agriculture Assistant")

HF_TOKEN = st.secrets.get("HF_API_TOKEN")
MODEL_ID = "google/flan-t5-base"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

translator = Translator()

# Local backup answers
backup_answers = {
    "best fertilizer for sugarcane": (
        "For sugarcane, a balanced NPK fertilizer like 20-20-20 is commonly recommended, "
        "along with compost for better soil health."
    ),
    "best fertilizer for rice": (
        "Rice crops benefit from Urea (nitrogen), DAP (phosphorus), and MOP (potassium). "
        "Apply at planting and mid-tillering stages."
    ),
    "how do i prevent pest attacks in tomato": (
        "Use neem oil spray early in the morning, maintain plant spacing, and introduce beneficial predators like ladybugs."
    )
}

def get_backup_answer(question: str) -> str:
    q = question.strip().lower()
    for key, ans in backup_answers.items():
        if key in q:
            return ans
    return "I'm still learning that one — please ask another question!"

user_input = st.text_input("📝 Ask AgriAI in any language:")

if user_input:
    with st.spinner("🤖 Thinking..."):
        try:
            # Translate user input to English
            detected_lang = translator.detect(user_input).lang
            translated_input = translator.translate(user_input, dest="en").text
            st.write("🌐 Translated to English:", translated_input)

            # Hugging Face API call
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            payload = {"inputs": f"Answer this agricultural question: {translated_input}"}
            response = requests.post(API_URL, headers=headers, json=payload)

            st.write("📦 API Status Code:", response.status_code)
            st.write("📦 Raw Response:", response.text)

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and "generated_text" in result[0]:
                    english_answer = result[0]["generated_text"].strip()
                    translated_answer = translator.translate(english_answer, dest=detected_lang).text
                    st.success(translated_answer)
                    st.info("✅ Answered by Hugging Face model")
                else:
                    st.warning("⚠️ Unexpected response format. Showing local answer.")
                    st.success(get_backup_answer(translated_input))
                    st.info("✅ Answered by local backup logic")
            else:
                st.warning(f"❌ API Error {response.status_code}. Using backup.")
                st.success(get_backup_answer(translated_input))
                st.info("✅ Answered by local backup logic")

        except Exception as e:
            st.error(f"🚨 Error: {e}")
            st.success(get_backup_answer(user_input))
            st.info("✅ Answered by local backup logic")
