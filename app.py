import streamlit as st
from transformers import pipeline

# Load the model once (offline + stable settings)
@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-base"
    )

generator = load_model()

# Setup page
st.set_page_config(page_title="🌾 AgriAI (Final)", page_icon="🌱", layout="centered")
st.title("🌾 AgriAI - Offline Agriculture Chat Assistant")
st.markdown("💬 Ask anything about soil, crops, irrigation, or farming (Fully Offline & Stable)")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
user_input = st.chat_input("Ask your agriculture-related question...")

if user_input:
    st.session_state.chat_history.append(("🧑 You", user_input))

    # Clean prompt
    prompt = f"Answer clearly: {user_input}"
    
    # Generate stable output (no junk)
    response = generator(
        prompt,
        max_length=100,
        do_sample=False,         # ⛔ No randomness
        temperature=0.0          # 🔒 Deterministic output
    )[0]["generated_text"]

    # Clean junk characters
    clean_answer = (
        response.replace("�", "")
                .replace("(i)", "")
                .replace("(ii)", "")
                .replace("(iii)", "")
                .replace("(iv)", "")
                .strip()
    )

    st.session_state.chat_history.append(("🤖 AgriAI", clean_answer))

# Display chat
for speaker, message in st.session_state.chat_history:
    with st.chat_message(speaker):
        st.markdown(message)
