import streamlit as st

if st.button("Выйти"):
    st.session_state.role = None
    st.rerun()
