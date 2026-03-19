import requests
import streamlit as st
from frontend_settings import API_URL
from register import register


def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{API_URL}/api/token/",
            json={"username": username, "password": password},
        )

        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data["access"]
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Go to Register", key="go_register"):
        st.session_state.page = "register"
        st.rerun()
