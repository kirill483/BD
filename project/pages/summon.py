import time
import streamlit as st
from repositories.worker import get_liables, get_all_liables ,get_summons, get_all_summons, create_summon, delete_summon

if "flag" not in st.session_state:
    st.session_state.flag = None
if "flag1" not in st.session_state:
    st.session_state.flag1 = None
if "flag2" not in st.session_state:
    st.session_state.flag2 = None
if "liable_id" not in st.session_state:
    st.session_state.liable_id = None
if "first_name" not in st.session_state:
    st.session_state.first_name = None
if "last_name" not in st.session_state:
    st.session_state.last_name = None
if "summon_id" not in st.session_state:
    st.session_state.summon_id = None

st.session_state.flag1 = st.selectbox(
    "Что хотите сделать?",
    ("Создать повестку", "Удалить повестку"),
    index=None,
    placeholder="Выберите действие...",
)

if st.session_state.flag1 == "Создать повестку":
    st.session_state.flag2 = st.selectbox(
        "Как выбрать военнобязанного?",
        ("Поиск военнобязанного по ФИО", "Показать всех военнобязанных"),
        index=None,
        placeholder="Выберите действие...",
    )
if st.session_state.flag2 == "Поиск военнобязанного по ФИО":
    st.session_state.first_name = st.text_input("Имя")
    st.session_state.last_name = st.text_input("Фамилия")
    if st.button("Подтвердить ФИО военнобязанного"):
        st.session_state.flag = "Выбрать счастливчика"
if st.session_state.flag == "Выбрать счастливчика" or st.session_state.flag2 == "Показать всех военнобязанных":
    if st.session_state.first_name == None:
        liables = get_all_liables(st.session_state.military_office_id)
    else:
        liables = get_liables(st.session_state.military_office_id, st.session_state.first_name, st.session_state.last_name)
        st.session_state.first_name = None;
        st.session_state.last_name = None;
    if not liables:
        st.write("Не найдено военнобязанных")
    else:
        for user_id, first_name, last_name, birth_date, health_level, health_description in liables:
            st.write("Имя: ",first_name)
            st.write("Фамилия : ",last_name)
            st.write("Дата рождения: ",birth_date)
            st.write("Уровень годности: ",health_level)
            st.write("Описание: ",health_description)
            if st.button("Выбрать военнобязанного", key = user_id):
                st.session_state.liable_id = user_id
                st.session_state.flag = "Подтвердить создание повестки"
if st.session_state.flag == "Подтвердить создание повестки":
    appearance_time = st.text_input("Время к которому нужно прибыть")
    description = st.text_input("Описание")
    if st.button("Подтвердить создание повестки"):
        create_summon(st.session_state.liable_id, appearance_time, description, st.session_state.user_id, st.session_state.military_office_id)
        st.success("Создана")
        time.sleep(2)
        st.session_state.flag1 = None
        st.session_state.flag2 = None
        st.session_state.flag = None
        st.session_state.liable_id = None
        st.rerun()

if st.session_state.flag1 == "Удалить повестку":
    st.session_state.flag2 = st.selectbox(
        "Как выбрать повестку?",
        ("Поиск повестки по ФИО", "Показать все повестки"),
        index=None,
        placeholder="Выберите действие...",
    )
if st.session_state.flag2 == "Поиск повестки по ФИО":
    st.session_state.first_name = st.text_input("Имя")
    st.session_state.last_name = st.text_input("Фамилия")
    if st.button("Подтвердить ФИО для повестки"):
        st.session_state.flag = "Выбрать повестку"
if st.session_state.flag == "Выбрать повестку"  or st.session_state.flag2 == "Показать все повестки":
    if st.session_state.first_name == None:
        summons = get_all_summons(st.session_state.military_office_id)
    else:
        summons = get_summons(st.session_state.military_office_id, st.session_state.first_name, st.session_state.last_name)
        st.session_state.first_name = None;
        st.session_state.last_name = None;
    if not summons:
        st.write("Не найдено повесток")
    for summon_id, creation_date, appearance_date, description, first_name, last_name, birth_date in summons:
        st.write("Дата создания повестки: ",creation_date)
        st.write("Дата прибытия: ",appearance_date)
        st.write("Описание: ",description)
        st.write("Имя: ",first_name)
        st.write("Фамилия: ",last_name)
        st.write("Дата рождения: ",birth_date)
        if st.button("Выбрать повестку для удаления", key = summon_id):
            st.session_state.summon_id = summon_id
            st.session_state.flag = "Подтвердить удаление"
if st.session_state.flag == "Подтвердить удаление":
    delete_summon(st.session_state.summon_id)
    st.success("Удален")
    time.sleep(2)
    st.session_state.flag1 = None
    st.session_state.flag2 = None
    st.session_state.flag = None
    st.session_state.summon_id = None
    st.rerun()
