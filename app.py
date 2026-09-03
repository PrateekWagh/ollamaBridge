import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()


API_BASE_URL = os.environ["LOCAL_HOST"]  # change if your FastAPI runs elsewhere

st.set_page_config(page_title="OllamaBridge", page_icon="🦙")
st.title("🦙 OllamaBridge")

# ---- Session state ----
if "token" not in st.session_state:
    st.session_state.token = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- Auth: Login / Signup ----
if not st.session_state.token:
    st.subheader("Login")

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            try:
                # OAuth2PasswordRequestForm expects form-encoded data, field name is "username"
                resp = requests.post(
                    f"{API_BASE_URL}/login",
                    data={"username": email, "password": password},
                )
                if resp.status_code == 200:
                    st.session_state.token = resp.json().get("access_token")
                    st.rerun()
                else:
                    st.error(f"Login failed: {resp.json().get('detail', resp.text)}")
            except requests.exceptions.ConnectionError:
                st.error("Could not reach the API. Is your FastAPI server running?")

    with tab_signup:
        su_email = st.text_input("Email", key="signup_email")
        su_password = st.text_input("Password", type="password", key="signup_password")
        su_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if st.button("Sign Up"):
            try:
                resp = requests.post(
                    f"{API_BASE_URL}/signUp",
                    json={
                        "email": su_email,
                        "password": su_password,
                        "confirm_password": su_confirm,
                    },
                )
                if resp.status_code == 200:
                    st.success("Signup successful! You can log in now.")
                else:
                    st.error(f"Signup failed: {resp.json().get('detail', resp.text)}")
            except requests.exceptions.ConnectionError:
                st.error("Could not reach the API. Is your FastAPI server running?")

# ---- Chat UI (only shown once logged in) ----
else:
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.messages = []
            st.rerun()

    # Render past messages (this session only — full history lives in your DB)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Message OllamaBridge...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        try:
            resp = requests.post(
                f"{API_BASE_URL}/chat",
                json={"prompt": prompt},
                headers=headers,
            )
            if resp.status_code == 200:
                reply = resp.json().get("reply", "")
            elif resp.status_code == 429:
                reply = "⏳ Rate limit hit — try again in a bit."
            elif resp.status_code == 401:
                reply = "🔒 Session expired — please log out and log back in."
            else:
                reply = f"⚠️ Error: {resp.json().get('detail', resp.text)}"
        except requests.exceptions.ConnectionError:
            reply = "⚠️ Could not reach the API. Is your FastAPI server running?"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)