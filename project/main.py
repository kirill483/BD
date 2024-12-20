import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

exit_page = st.Page("pages/exit.py", title = "выход")
login_page = st.Page("pages/login.py", title = "вход")
register_page = st.Page("pages/register.py", title ="регистрация")


summon_page = st.Page("pages/summon.py", title = "повестки")
health_page = st.Page("pages/health.py", title = "здоровье")

check_summon_page = st.Page("pages/check_summon.py", title = "проверить есть ли повестка")
check_mydata_page = st.Page("pages/check_mydata.py", title = "посмотреть мои данные")
add_health_data = st.Page("pages/add_health_data.py", title = "добавить информацию о здоровье")

worker_main_page = [summon_page, health_page]
liable_main_page = [check_summon_page, check_mydata_page, add_health_data]
start_page = [login_page, register_page]
st.title("Онлайн-военкомат")

page_dict = []
if st.session_state.role == "liable":
    page_dict = liable_main_page
if st.session_state.role == "worker":
    page_dict = worker_main_page
if len(page_dict) > 0:
    pg = st.navigation(page_dict + [exit_page])
else:
    pg = st.navigation(start_page)
pg.run()







