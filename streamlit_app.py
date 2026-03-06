import cohere
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title= "Toyota Car Assistant",
    page_icon=  "🚗🤖",
    layout= "centered",
)

st.title("Toyota Car Assitant")
st.caption("Welcome to Toyota!! How can I assist you today??")

@st.cache_resource
def get_client():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        st.error("Missing Cohere API key")
        st.stop()
    return cohere.Client(st.secrets["general"]["COHERE_API_KEY"])

co = get_client()

SYSTEM_MESSAGE = (
    "You are helpful Toyota Car Assistant. "
    "Recommend Toyota cars to user's specifications. "
    "Respond in a friendly and informative manner. "
    "Keep the conversations short and concise. "
    "Don't answer questions that are not related to Toyota cars. "
    "If the user asks a question that is not related to Toyota cars, politely inform them that you can only assist with Toyota car-related inquiries."
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_MESSAGE}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

prompt = st.chat_input("Ask about Toyota models, specs, or comparisons...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response_text = ""

        stream = co.chat_stream(
            model="command-a-03-2025",
            messages=st.session_state.messages,
            temperature=0.25,
            max_tokens=500
        )

        placeholder = st.empty()

        for event in stream:
            if event.type == "content-delta":
                response_text += event.delta.message.content.text
                placeholder.markdown(response_text + "▌")

        placeholder.markdown(response_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )