import time
import streamlit as st
from repositories.worker import get_health_data, get_all_health_data ,get_health_reports, get_all_health_reports, create_health_report, delete_health_report

if "flag" not in st.session_state:
    st.session_state.flag = None
if "flag1" not in st.session_state:
    st.session_state.flag1 = None
if "liable_id" not in st.session_state:
    st.session_state.liable_id = None
if "first_name" not in st.session_state:
    st.session_state.first_name = None
if "last_name" not in st.session_state:
    st.session_state.last_name = None
if "report_id" not in st.session_state:
    st.session_state.report_id = None
if "flag2" not in st.session_state:
    st.session_state.flag2 = None

st.session_state.flag1 = st.selectbox(
    "Что хотите сделать?",
    ("Создать заключение о годности к службе", "Удалить заключение о годности к службе"),
    index=None,
    placeholder="Выберите действие...",
)

if st.session_state.flag1 == "Создать заключение о годности к службе":
    st.session_state.flag2 = st.selectbox(
        "Как искать военнообязанного?",
        ("Поиск военнобязанного по ФИО", "Показать всех военнобязанных"),
        index=None,
        placeholder="Выберите действие...",
    )
if st.session_state.flag2 == "Поиск военнобязанного по ФИО":
    st.session_state.first_name = st.text_input("Имя")
    st.session_state.last_name = st.text_input("Фамилия")
    if st.button("Подтвердить ФИО военнобязанного"):
        st.session_state.flag = "Выбрать счастливчика"
if (st.session_state.flag == "Выбрать счастливчика" or st.session_state.flag2 == "Показать всех военнобязанных") and (st.session_state.flag1 == "Создать заключение о годности к службе"):
    if st.session_state.first_name == None:
        liables = get_all_health_data(st.session_state.military_office_id)
    else:
        liables = get_health_data(st.session_state.military_office_id, st.session_state.first_name, st.session_state.last_name)
        st.session_state.first_name = None;
        st.session_state.last_name = None;
    if not liables:
        st.write("Не найдены военнообязанные")
    else:
        for user_id, first_name, last_name, birth_date, description in liables:
            st.write("Имя: " , first_name)
            st.write("Фамилия: ",last_name)
            st.write("Дата рождения: ",birth_date)
            st.write("Описание: ",description)
            if st.button("Выбрать военнобязанного", key = user_id):
                st.session_state.liable_id = user_id
                st.session_state.flag = "Форма для создания заключени"
if st.session_state.flag == "Форма для создания заключени" and st.session_state.flag1 == "Создать заключение о годности к службе" and (st.session_state.flag2 in ("Поиск военнобязанного по ФИО", "Показать всех военнобязанных")):
    level = st.text_input("Уровень годности")
    description = st.text_input("Описание")
    if st.button("Подтвердить создание заключения о годности к службе"):
        create_health_report(st.session_state.liable_id, st.session_state.user_id, level, description)
        st.success("Создан")
        time.sleep(2)
        st.session_state.flag1 = None
        st.session_state.flag2 = None
        st.session_state.flag = None
        st.session_state.liable_id = None
        st.rerun()

if st.session_state.flag1 == "Удалить заключение о годности к службе":
    st.session_state.flag2 = st.selectbox(
        "Как искать заключение?",
        ("Поиск заключения по ФИО", "Показать все заключения о годности к службе"),
        index=None,
        placeholder="Выберите действие...",
    )
   
if st.session_state.flag2 == "Поиск заключения по ФИО":
    st.session_state.first_name = st.text_input("Имя")
    st.session_state.last_name = st.text_input("Фамилия")
    if st.button("Подтвердить ФИО для заключения о годности к службе"):
        st.session_state.flag = "Выбрать заключение"
if (st.session_state.flag == "Выбрать заключение" or st.session_state.flag2 == "Показать все заключения о годности к службе") and st.session_state.flag1 == "Удалить заключение о годности к службе":
    if st.session_state.first_name == None:
        reports = get_all_health_reports(st.session_state.military_office_id)
    else:
        reports = get_health_reports(st.session_state.military_office_id, st.session_state.first_name, st.session_state.last_name)
        st.session_state.first_name = None;
        st.session_state.last_name = None;
    if not reports:
        st.write("Не найдены заключения о годности к службе")
    for report_id, health_level, description, first_name, last_name, birth_date in reports:
        st.write("Уровень годности: ",health_level)
        st.write("Описание: ",description)
        st.write("Имя ",first_name)
        st.write("Фамилия: " ,last_name)
        st.write("Дата рождения: ",birth_date)
        if st.button("Выбрать заключение о годности к службе для удаления", key = report_id):
            st.session_state.report_id = report_id
            st.session_state.flag = "Подтвердить удаление"
if st.session_state.flag == "Подтвердить удаление" and st.session_state.flag1 == "Удалить заключение о годности к службе" and (st.session_state.flag2 in ("Поиск заключения по ФИО", "Показать все заключения о годности к службе")):
    delete_health_report(st.session_state.report_id)
    st.success("Удален")
    time.sleep(2)
    st.session_state.flag1 = None
    st.session_state.flag2 = None
    st.session_state.flag = None
    st.session_state.report_id = None
    st.rerun()
