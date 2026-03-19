import requests
import streamlit as st
from frontend_settings import API_URL


def register():
    st.title("Register")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):
        res = requests.post(
            f"{API_URL}/users/api/register/",
            json={"username": username, "password": password},
        )

        if res.status_code == 200:
            st.success("Account created! Please login.")
        else:
            st.error(res.json().get("error", "Something went wrong"))
