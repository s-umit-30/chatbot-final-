import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from db import register_user, verify_user, get_user_id, save_message, get_chat_history

# Load environment variables
load_dotenv()

# Initialize Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# System prompt for the chatbot
system_prompt = "You are a friendly cybersecurity teacher bot. Guide users on processes and requirements in cybersecurity. Be helpful, patient, and encouraging. Explain concepts clearly and provide examples when possible."

# Initialize the model with system instruction
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

st.title("Cybersecurity Teacher Chatbot")

# Session state for user
if "user" not in st.session_state:
    st.session_state.user = None
if "chat" not in st.session_state:
    st.session_state.chat = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def login_page():
    st.header("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if verify_user(username, password):
                st.session_state.user = username
                st.session_state.user_id = get_user_id(username)
                load_chat()
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def register_page():
    st.header("Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match")
            elif register_user(username, password):
                st.success("Registered successfully! Please login.")
            else:
                st.error("Username already exists")

def load_chat():
    if st.session_state.user:
        history = get_chat_history(st.session_state.user_id)
        st.session_state.messages = history
        # Initialize chat with history
        st.session_state.chat = model.start_chat(history=[{"role": msg["role"], "parts": [msg["content"]]} for msg in history])

def generate_response(user_input):
    if not st.session_state.chat:
        st.session_state.chat = model.start_chat(history=[])
    response = st.session_state.chat.send_message(user_input)
    return response.text

def chat_page():
    st.header(f"Welcome, {st.session_state.user}!")
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.chat = None
        st.session_state.messages = []
        st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("You:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message(st.session_state.user_id, "user", prompt)
        response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        save_message(st.session_state.user_id, "assistant", response)
        st.rerun()

def main():
    if st.session_state.user:
        chat_page()
    else:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login_page()
        with tab2:
            register_page()

if __name__ == "__main__":
    main()
