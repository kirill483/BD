import streamlit as st
from repositories.liable import get_data, get_health_reports

if "flag1" not in st.session_state:
    st.session_state.flag1 = None

st.session_state.flag1 = st.selectbox(
    "Что хотите сделать?",
    ("Посмотреть заключения о годности к службе", "Прочая информация"),
    index=None,
    placeholder="Выберите действие...",
)

if st.session_state.flag1 == "Посмотреть заключения о годности к службе":
    reports = get_health_reports(st.session_state.user_id)
    if not reports:
        st.write("Заключения о годности к службе не найдены")
    for health_level, description, first_name, last_name in reports:
        st.write("Уровень годности: ",health_level)
        st.write("Заключение создал: ", first_name, " ", last_name)
        st.write("Описание: ", description)
    st.session_state.flag1 = None

if st.session_state.flag1 == "Прочая информация":
    data = get_data(st.session_state.user_id)
    for first_name, last_name, birth_date, email, address in data:
        st.write("Вы: ", first_name, " ",last_name)
        st.write("родились: ", birth_date)
        st.write("почта: ", email)
        st.write( "адрес военкомата: ", address)
    st.session_state.flag1 = None
