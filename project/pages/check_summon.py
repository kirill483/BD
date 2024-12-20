from repositories.liable import get_summons
import streamlit as st

if "flag" not in st.session_state:
    st.session_state.flag = None

if st.button("Проверить"):
    st.session_state.flag = "Проверить"

if st.session_state.flag == "Проверить":
    summons = get_summons(st.session_state.user_id)
    if not summons:
        st.write("У вас нет повесток")
    for creation_date, appearance_date, description, address, last_name, first_name in summons:
        st.write("Повестка была создана: ",creation_date)
        st.write( "Нужно прийти в военкомат: " , appearance_date)
        st.write( "Адрес военкомата: ", address)
        st.write( "Сотрудник создавший повестку: ", first_name ," ", last_name )
        st.write("Описание: ",description)
    st.session_state.flag = None
