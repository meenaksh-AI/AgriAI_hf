import streamlit as st
import requests

st.set_page_config(page_title="AgriAI", page_icon="🌾")
st.title("🌾 AgriAI — Smart Agriculture Assistant")

HF_TOKEN = st.secrets.get("HF_API_TOKEN")

# Backup Q&A logic for key questions
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
    st.warning("🚨 Add HF token in Streamlit Secrets for advanced answers.")
    
user_input = st.text_input("📝 Ask AgriAI:")

if user_input:
    with st.spinner("🤖 Thinking..."):
        # Try HF API if token is present
        if HF_TOKEN:
            try:
                response = requests.post(
                    f"https://api-inference.huggingface.co/models/facebook/opt-6.7b-instruct",
                    headers={"Authorization": f"Bearer {HF_TOKEN}"},
                    json={"inputs": user_input}
                )
                if response.status_code == 200:
                    text = response.json()[0].get("generated_text", "").strip()
                    if text:
                        st.success(text)
                        st.info("✅ Answer by Hugging Face model")
                    return
                # Fall back if any non-200 or empty
            except Exception:
                pass  # ignore and fall back

        # Local backup fallback
        st.success(get_backup_answer(user_input))
        st.info("✅ Answer from local backup logic")
