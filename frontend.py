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

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.run(prompt)

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# Sidebar
with st.sidebar:
    st.header("Options")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()