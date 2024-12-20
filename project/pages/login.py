import streamlit as st
from repositories.login import get_user, get_military_office_id
from passlib.hash import bcrypt

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "military_office_id" not in st.session_state:
    st.session_state.military_office_id = None

email = st.text_input("Email")
password = st.text_input("Пароль")

if st.button("Войти"):
    result = get_user(email)
    if result and bcrypt.verify(password, result[2]):
        st.session_state.user_id = result[0]
        st.session_state.role = result[3]
        st.session_state.military_office_id = get_military_office_id(result[0], result[3])
        st.rerun()
    else:
        st.error("Неверный email или пароль")

