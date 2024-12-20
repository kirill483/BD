import streamlit as st
from repositories.liable import create_health_data

description = st.text_input("Описание")
if st.button("Добавить"):
    res = create_health_data(st.session_state.user_id, description)
    if res:
        st.success("Информация отправлена")
