import streamlit as st
import requests

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI — Smart Agriculture Assistant")

HF_TOKEN = st.secrets.get("HF_API_TOKEN")
MODEL_ID = "tiiuae/falcon-7b-instruct"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

# Local backup for fallback
backup_answers = {
    "best fertilizer for sugarcane": (
        "For sugarcane, a balanced N-P-K fertilizer like 20-20-20 is commonly recommended, "
        "along with organic composted manure to enhance soil structure."
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

user_input = st.text_input("📝 Ask AgriAI:")

if user_input:
    with st.spinner("🤖 Thinking..."):
        if not HF_TOKEN:
            st.warning("🚨 Hugging Face token missing in secrets.")
        else:
            try:
                response = requests.post(
                    API_URL,
                    headers={
                        "Authorization": f"Bearer {HF_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json={"inputs": f"Agricultural question: {user_input}"}
                )
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and "generated_text" in result[0]:
                        st.success(result[0]["generated_text"].strip())
                        st.info("✅ Answered by Hugging Face model")
                    else:
                        st.warning("⚠️ Hugging Face model did not return expected output.")
                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")
                    st.success(get_backup_answer(user_input))
                    st.info("✅ Answered by local backup logic")
            except Exception as e:
                st.error(f"❌ Network Error: {e}")
                st.success(get_backup_answer(user_input))
                st.info("✅ Answered by local backup logic")
