import streamlit as st
from repositories.liable import get_military_offices, add_liable, get_all_military_offices

if "flag" not in st.session_state:
    st.session_state.flag = None
if "military_office_address" not in st.session_state:
    st.session_state.military_office_address = ""

first_name = st.text_input("Имя")
last_name = st.text_input("Фамилия")
email = st.text_input("Email")
birth_date = st.text_input("Дата рождения")
password = st.text_input("Пароль")

if st.button("Найти военкомат по адресу"):
    st.session_state.flag = "Найти военкомат по адресу"

if st.button("Показать все военкоматы"):
    st.session_state.flag = "Показать все военкоматы"

if st.session_state.flag == "Найти военкомат по адресу":
    military_office_address = st.text_input("Адрес")
    military_offices = get_military_offices(military_office_address)
    for office_id, address in military_offices:
        st.write(address)
        if st.button("Выбрать", key = office_id):
            st.session_state.military_office_id = office_id
            st.session_state.flag = "Зарегистрироваться"
if st.session_state.flag == "Показать все военкоматы":
    military_offices = get_all_military_offices()
    for office_id, address in military_offices:
        st.write(address)
        if st.button("Выбрать", key = office_id):
            st.session_state.military_office_id = office_id
            st.session_state.flag = "Зарегистрироваться"

if st.session_state.flag == "Зарегистрироваться":
    if(first_name == None):
        st.write("error")
    st.session_state.user_id = add_liable(first_name, last_name, email, birth_date, password, st.session_state.military_office_id)
    st.session_state.role = "liable"
    st.rerun()
