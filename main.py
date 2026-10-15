import streamlit as st
from utils import apply_theme, api_request, login, logout, submit_assignment, download_file

def handle_login():
    identifier = st.session_state.get('identifier_input', '')
    secret = st.session_state.get('secret_input', '')
    if identifier and secret:
        if login(identifier, secret):
            st.session_state['_login_success'] = True
        else:
            st.session_state['_login_error'] = True
    else:
        st.session_state['_login_error'] = True

if __name__ == '__main__':
    if 'access_token' not in st.session_state:
        st.set_page_config(page_title="教学管理系统", page_icon="📚", layout='centered')
        apply_theme()
        st.title("教学管理系统")
        st.subheader("用户登录")

        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            with st.container(border=True):
                identifier = st.text_input("学号或用户名", key='identifier_input')
                secret = st.text_input("密钥", type="password", key='secret_input', on_change=handle_login)
                st.write("")
                if st.button("登录", use_container_width=True):
                    if identifier and secret:
                        if login(identifier, secret):
                            st.success("登录成功！")
                            st.rerun()
                        else:
                            st.error("登录失败，请检查学号和密钥")
                    else:
                        st.warning("请输入学号和密钥")
                
                if st.session_state.get('_login_success'):
                    st.success("登录成功！")
                    st.session_state.pop('_login_success', None)
                    st.rerun()
                if st.session_state.get('_login_error'):
                    identifier_val = st.session_state.get('identifier_input', '')
                    secret_val = st.session_state.get('secret_input', '')
                    if not identifier_val or not secret_val:
                        st.warning("请输入学号和密钥")
                    else:
                        st.error("登录失败，请检查学号和密钥")
                    st.session_state.pop('_login_error', None)
    else:
        st.set_page_config(page_title="教学管理系统", page_icon="📚", layout='centered')
        apply_theme()

        with st.sidebar:
            st.write(f"欢迎, {st.session_state['user'].get('name', '')}")
            st.write(f"角色: {st.session_state['user'].get('role', '')}")
            st.divider()

            if st.button("退出登录"):
                logout()
                st.switch_page("main.py")
        
        pages = [
            st.Page("pages/dashboard.py", title="首页", icon="🏠"),
            st.Page("pages/assignments.py", title="作业管理", icon="📝"),
            st.Page("pages/grades.py", title="成绩查询", icon="📊"),
            st.Page("pages/statistics.py", title="统计分析", icon="📈"),
        ]
        
        pg = st.navigation(pages)
        pg.run()