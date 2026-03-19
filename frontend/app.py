import streamlit as st
from login import login
from register import register

st.title("Hello Streamlit 👋")


if "page" not in st.session_state:
    st.session_state.page = "login"


if st.session_state.page == "login":
    login()
else:
    register()
