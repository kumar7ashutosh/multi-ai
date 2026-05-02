import sys
import os

# 🔥 fix import path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import requests
import uuid

from app.config.settings import settings

st.set_page_config(page_title="Multi AI Agent", layout="centered")
st.title("Multi AI Agent using LangGraph + Tavily + Memory")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

system_prompt = st.text_area("Define your AI Agent", height=70)
selected_model = st.selectbox("Select your AI model", settings.ALLOWED_MODEL_NAMES)
allow_web_search = st.checkbox("Allow web search")

user_query = st.text_area("Enter your query", height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [
            {"role": "user", "content": user_query}
        ],
        "allow_search": allow_web_search,
        "session_id": st.session_state.session_id
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=30)

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            st.subheader("Agent Response")
            st.markdown(agent_response)

        else:
            st.error(f"Backend Error {response.status_code}: {response.text}")

    except Exception as e:
        st.error(f"Exception: {str(e)}")