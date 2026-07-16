import os
import streamlit as st
from agent import Agent

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Agent")

# Create agent only once
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
prompt = st.chat_input("Type your message...")

if prompt:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response (guard errors to avoid full app crash)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.run(prompt)
            except RuntimeError as e:
                # Show a friendly error message (do not reveal secrets)
                st.error(str(e))
                response = None

        if response:
            st.markdown(response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

# Sidebar
with st.sidebar:
    st.header("Options")

    # Diagnostics (non-sensitive): whether an OPENAI_API_KEY is present
    st.subheader("Diagnostics")
    env_key = bool(os.getenv("OPENAI_API_KEY"))
    secret_key = False
    try:
        secret_key = bool(st.secrets.get("OPENAI_API_KEY"))
    except Exception:
        secret_key = False

    st.write("OPENAI_API_KEY in environment:", "Yes" if env_key else "No")
    st.write("OPENAI_API_KEY in Streamlit secrets:", "Yes" if secret_key else "No")
    st.write("BASE_URL:", st.secrets.get("BASE_URL") if st.secrets.get("BASE_URL") else (os.getenv("BASE_URL") or "<not set>"))

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()