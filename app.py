import streamlit as st
import requests

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI — Smart Agriculture Assistant")

HF_TOKEN = st.secrets.get("HF_API_TOKEN")

# Backup Q&A logic for known questions
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

if not HF_TOKEN:
    st.warning("🚨 Please add your Hugging Face token in Streamlit Secrets as 'HF_API_TOKEN'.")

user_input = st.text_input("📝 Ask AgriAI:")

if user_input:
    with st.spinner("🤖 Thinking..."):
        if HF_TOKEN:
            try:
                response = requests.post(
                    "https://api-inference.huggingface.co/models/google/flan-t5-large",
                    headers={
                        "Authorization": f"Bearer {HF_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json={"inputs": f"Answer this agricultural question: {user_input}"}
                )

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, dict) and "error" not in result:
                        generated = result[0].get("generated_text", "").strip()
                        if generated:
                            st.success(generated)
                            st.info("✅ Answered by Hugging Face model")
                            st.stop()
                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Network Error: {str(e)}")

        # Fallback only if model fails
        st.success(get_backup_answer(user_input))
        st.info("✅ Answered by local backup logic")
