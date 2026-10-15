import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import api_request

if 'assignments' not in st.session_state:
    response = api_request("GET", "/assignments")
    if response:
        st.session_state['assignments'] = response

if 'grades' not in st.session_state:
    response = api_request("GET", "/grades")
    if response:
        st.session_state['grades'] = response

st.title("成绩查询")

grades = st.session_state.get('grades') or []
assignments = st.session_state.get('assignments') or []

if assignments:
    grade_dict = {}
    for grade in grades:
        assignment_id = grade.get('assignment_id')
        if assignment_id:
            grade_dict[assignment_id] = grade

    rows = []
    for assignment in assignments:
        assignment_id = assignment['id']
        grade = grade_dict.get(assignment_id)
        
        if grade:
            title = grade.get('title', assignment.get('title', ''))
            rows.append({
                'assignment_title': title,
                'max_score': grade.get('max_score', assignment.get('max_score', 0)),
                'score': grade.get('score', 'NA'),
                'feedback': grade.get('feedback', 'NA'),
                'published_at': str(grade.get('published_at', ''))[:10] if grade.get('published_at') else 'NA'
            })
        else:
            rows.append({
                'assignment_title': assignment.get('title', ''),
                'max_score': assignment.get('max_score', 0),
                'score': 'NA',
                'feedback': 'NA',
                'published_at': 'NA'
            })

    df = pd.DataFrame(rows)

    df['score'] = df['score'].fillna('NA')
    df['feedback'] = df['feedback'].fillna('NA')
    df['published_at'] = df['published_at'].apply(
        lambda x: x if x and x != 'None' else 'NA'
    )

    st.dataframe(df[['assignment_title', 'max_score', 'score', 'feedback', 'published_at']],
                    column_config={
                    'assignment_title': '作业名称',
                    'max_score': '满分',
                    'score': '得分',
                    'feedback': st.column_config.TextColumn('评语', width='medium'),                     'published_at': '发布时间'
                    },
                hide_index=True,
                use_container_width=True)
else:
    st.info("暂无作业信息")