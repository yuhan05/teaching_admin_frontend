import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import api_request, submit_assignment, download_file

if 'assignments' not in st.session_state:
    response = api_request("GET", "/assignments")
    if response:
        st.session_state['assignments'] = response

if 'grades' not in st.session_state:
    response = api_request("GET", "/grades")
    if response:
        st.session_state['grades'] = response

st.title("作业管理")

assignments = st.session_state.get('assignments')

if assignments:
    tab1, tab2 = st.tabs(["作业列表", "提交作业"])

    with tab1:
        for assignment in assignments:
            with st.expander(f"{assignment['title']}"):
                detail_tab, history_tab = st.tabs(["查看作业详情", "查看提交历史"])
                
                with detail_tab:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**截止时间:** {assignment['deadline']}")
                        st.write(f"**满分:** {assignment['max_score']}")
                    with col2:
                        st.write(f"**状态:** {assignment['status']}")
                        st.write(f"**允许迟交:** {'是' if assignment['allow_late'] else '否'}")
                    with col3:
                        submission_status = assignment.get('submission_status', {})
                        grade_status = assignment.get('grade_status', {})
                        st.write(f"**已提交:** {'是' if submission_status.get('submitted') else '否'}")
                        if grade_status.get('published'):
                            st.write(f"**成绩:** {grade_status.get('score')}/{assignment['max_score']}")
                        else:
                            st.write("**成绩:** 未发布")
                    
                    st.write(f"**作业说明:**")
                    st.write(assignment['description'])
                
                with history_tab:
                    submissions = api_request("GET", f"/assignments/{assignment['id']}/submissions")
                    if submissions:
                        for sub in submissions:
                            with st.expander(f"版本 {sub['version']} - {sub['submitted_at']}"):
                                if sub.get('text'):
                                    st.write(f"**文本内容:**")
                                    st.write(sub['text'])
                                if sub.get('file'):
                                    file_info = sub['file']
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.write(f"**附件:** {file_info['original_name']} ({file_info['size']} bytes)")
                                    with col2:
                                        file_content = download_file(file_info.get('download_url', ''))
                                        if file_content:
                                            st.download_button(
                                                label="下载",
                                                data=file_content,
                                                file_name=file_info['original_name'],
                                                key=f"download_file_{sub['id']}",
                                                type="primary"
                                            )
                                if sub.get('LLM_chat_log'):
                                    llm_info = sub['LLM_chat_log']
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.write(f"**LLM聊天记录:** {llm_info['original_name']}")
                                    with col2:
                                        llm_content = download_file(llm_info.get('download_url', ''))
                                        if llm_content:
                                            st.download_button(
                                                label="下载",
                                                data=llm_content,
                                                file_name=llm_info['original_name'],
                                                key=f"download_llm_{sub['id']}",
                                                type="primary"
                                            )
                                st.write(f"**是否迟交:** {'是' if sub.get('is_late') else '否'}")
                    else:
                        st.info("暂无提交记录")

    with tab2:
        assignment_options = {a['title']: a['id'] for a in assignments}
        selected_title = st.selectbox("选择作业", list(assignment_options.keys()))
        
        if selected_title:
            assignment_id = assignment_options[selected_title]
            text = st.text_area("作业文本内容")
            file_upload = st.file_uploader("作业文件", type=['txt', 'py', 'ipynb', 'pdf', 'zip'])
            llm_log_upload = st.file_uploader("LLM聊天记录 (.md)", type=['md'])
            
            if st.button("提交作业"):
                submit_assignment(assignment_id, text, file_upload, llm_log_upload)
else:
    st.info("暂无作业信息")