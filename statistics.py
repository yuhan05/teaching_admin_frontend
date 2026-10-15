import streamlit as st
import pandas as pd
import plotly.express as px
import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import api_request

if 'summary' not in st.session_state:
    response = api_request("GET", "/students/me/summary")
    if response:
        st.session_state['summary'] = response

if 'assignments' not in st.session_state:
    response = api_request("GET", "/assignments")
    if response:
        st.session_state['assignments'] = response

if 'grades' not in st.session_state:
    response = api_request("GET", "/grades")
    if response:
        st.session_state['grades'] = response

st.title("成绩统计与可视化")

summary = st.session_state.get('summary')
grades = st.session_state.get('grades')

if summary:
    st.subheader("学习进度")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        submitted = summary.get('submitted_count', 0)
        total = summary.get('assignment_count', 0)
        fig = px.pie(values=[submitted, total - submitted], 
                     names=['已提交', '未提交'],
                     title=f'提交率: {submitted}/{total}')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        on_time = summary.get('on_time_count', 0)
        late = summary.get('late_count', 0)
        unsubmitted = summary.get('unsubmitted_count', 0)
        fig = px.pie(values=[on_time, late, unsubmitted],
                     names=['按时提交', '迟交', '未提交'],
                     title='提交情况分布')
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        graded = summary.get('graded_count', 0)
        ungraded = summary.get('submitted_count', 0) - graded
        fig = px.pie(values=[graded, ungraded],
                     names=['已评分', '未评分'],
                     title='评分进度')
        st.plotly_chart(fig, use_container_width=True)

assignments = st.session_state.get('assignments') or []
if assignments:
    st.subheader("成绩分析")
    
    grades_dict = {}
    for grade in (grades or []):
        assignment_id = grade.get('assignment_id')
        if assignment_id:
            grades_dict[assignment_id] = grade
    
    rows = []
    for assignment in assignments:
        assignment_id = assignment['id']
        grade = grades_dict.get(assignment_id)
        title = grade.get('title', assignment.get('title', '')) if grade else assignment.get('title', '')
        max_score = grade.get('max_score', assignment.get('max_score', 0)) if grade else assignment.get('max_score', 0)
        
        if grade and grade.get('score') is not None:
            score = grade['score']
        else:
            score = 0
        
        percentage = round(score / max_score * 100, 2) if max_score > 0 else 0
        
        short_title = re.search(r'【K\d+】', title)
        short_title = short_title.group() if short_title else title
        
        rows.append({
            'assignment_title': short_title,
            'score': score,
            'max_score': max_score,
            'percentage': percentage,
            'status': '已评分' if grade and grade.get('score') is not None else '未评分'
        })
    
    df = pd.DataFrame(rows)
    
    graded_df = df[df['status'] == '已评分']
    if not graded_df.empty:
        avg_score = graded_df['score'].mean()
        avg_max = graded_df['max_score'].mean()
        avg_percentage = graded_df['percentage'].mean()
    else:
        avg_score = 0
        avg_max = df['max_score'].mean() if not df.empty else 0
        avg_percentage = 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("平均得分", f"{avg_score:.2f}")
    with col2:
        st.metric("平均得分率", f"{avg_percentage:.2f}%")

    fig = px.bar(df, x='assignment_title', y='score',
                 title='各作业得分',
                 labels={'assignment_title': '作业名称', 'score': '得分'},
                 height=400)
    fig.update_layout(showlegend=False)
    fig.update_traces(width=0.3)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(df, x='assignment_title', y='percentage',
                  title='得分率趋势',
                  labels={'assignment_title': '作业名称', 'percentage': '得分率(%)'},
                  markers=True,
                  color='assignment_title',
                  height=400)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

if not summary and not grades and not assignments:
    st.info("暂无统计数据")