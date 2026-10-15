import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import api_request

if 'student_info' not in st.session_state:
    response = api_request("GET", "/students/me")
    if response:
        st.session_state['student_info'] = response

if 'summary' not in st.session_state:
    response = api_request("GET", "/students/me/summary")
    if response:
        st.session_state['summary'] = response

if 'assignments' not in st.session_state:
    response = api_request("GET", "/assignments")
    if response:
        st.session_state['assignments'] = response

st.title("首页")

user = st.session_state['user']
student_info = st.session_state.get('student_info')

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.subheader("个人信息")
        if student_info:
            st.write(f"**学号:** {student_info.get('student_id', '')}")
            st.write(f"**姓名:** {student_info.get('name', '')}")
            st.write(f"**角色:** {user.get('role', '')}")
            if student_info.get('extra'):
                st.write("**扩展信息:**")
                for key, value in student_info['extra'].items():
                    st.write(f"  - {key}: {value}")

with col2:
    with st.container(border=True):
        st.subheader("快捷操作")
        if st.button("查看作业", key="btn_assignments"):
            st.switch_page("pages/assignments.py")
        if st.button("查看成绩", key="btn_grades"):
            st.switch_page("pages/grades.py")
        if st.button("成绩统计", key="btn_statistics"):
            st.switch_page("pages/statistics.py")
        if st.button("退出登录", key="btn_logout"):
            for key in ['access_token', 'user', 'student_info', 'assignments', 'grades', 'summary']:
                if key in st.session_state:
                    del st.session_state[key]
            st.switch_page("main.py")

summary = st.session_state.get('summary')
if summary:
    with st.container(border=True):
        st.subheader("学习概览")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("作业总数", summary.get('assignment_count', 0))
        with col2:
            st.metric("已提交", summary.get('submitted_count', 0))
        with col3:
            st.metric("已评分", summary.get('graded_count', 0))
        with col4:
            avg = summary.get('average_percentage', 0)
            st.metric("平均得分率", f"{avg}%" if avg else "-")
