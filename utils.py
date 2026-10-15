import streamlit as st
import requests

from config import BASE_URL

def apply_theme():
    st.markdown("""
    <style>
    :root {
        --primary: #1677ff;
        --primary-hover: #0958d9;
        --bg-main: #f5f7fa;
        --bg-card: #ffffff;
        --text-title: #1a1a2e;
        --text-body: #4a4a6a;
        --text-muted: #8a8aa0;
        --success: #52c41a;
        --warning: #faad14;
        --danger: #ff4d4f;
        --border: #e8ecf1;
        --sidebar-bg: #001529;
        --sidebar-text: rgba(255,255,255,0.65);
        --shadow-card: 0 1px 3px rgba(0,0,0,0.06);
        --radius: 10px;
    }

    .stApp {
        background-color: var(--bg-main);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-title) !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }
    h1 { font-size: 36px !important; }
    h2 { font-size: 28px !important; }
    h3 { font-size: 18px !important; }
    .stMarkdown, .stText, p, li {
        color: var(--text-body);
        font-size: 14px;
    }
    [data-testid="stMetric"] label,
    .stCaption, .stMarkdown small {
        font-size: 12px !important;
        color: var(--text-muted) !important;
    }

    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: var(--sidebar-text) !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] [data-testid="stPageLink"] {
        border-radius: 6px;
        margin: 2px 8px;
        transition: background-color 0.2s ease;
    }
    section[data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
        background-color: rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
        color: var(--sidebar-text) !important;
    }

    .stMainBlockContainer {
        padding: 24px 32px !important;
        max-width: 1200px;
    }

    .stCard {
        background-color: var(--bg-card);
        border-radius: var(--radius);
        box-shadow: var(--shadow-card);
        padding: 20px 24px;
        margin-bottom: 16px;
        border: 1px solid var(--border);
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--bg-card);
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow-card);
        padding: 20px 24px !important;
        margin-bottom: 16px;
    }

    .stButton > button, div.stButton > button {
        background-color: var(--primary) !important;
        color: #ffffff !important;
        border: 1px solid var(--primary) !important;
        border-radius: 6px !important;
        height: 36px !important;
        padding: 0 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    .stButton > button:hover, div.stButton > button:hover {
        background-color: var(--primary-hover) !important;
        border-color: var(--primary-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(22,119,255,0.25) !important;
    }
    .stButton > button:active, div.stButton > button:active {
        transform: scale(0.98);
    }
    .stButton > button[kind="secondary"], div.stButton > button[data-testid="stBaseButton-secondary"] {
        background-color: #ffffff !important;
        color: var(--text-body) !important;
        border: 1px solid #d9d9d9 !important;
    }
    .stButton > button[kind="secondary"]:hover, div.stButton > button[data-testid="stBaseButton-secondary"]:hover {
        border-color: var(--primary) !important;
        color: var(--primary) !important;
        background-color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255,255,255,0.08) !important;
        color: rgba(255,255,255,0.85) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255,255,255,0.15) !important;
        border-color: rgba(255,255,255,0.3) !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stButton > button:active {
        transform: scale(0.98);
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        height: 36px !important;
        border-radius: 6px !important;
        border-color: #d9d9d9 !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(22,119,255,0.1) !important;
    }

    .stDataFrame {
        border-radius: var(--radius);
        overflow: hidden;
        box-shadow: var(--shadow-card);
    }
    .stDataFrame [data-testid="stDataFrameResizable"] {
        border: 1px solid var(--border);
        border-radius: var(--radius);
    }
    .stDataFrame thead tr th {
        background-color: #fafafa !important;
        color: var(--text-title) !important;
        font-weight: 600 !important;
        border-bottom: 1px solid var(--border) !important;
    }
    .stDataFrame tbody tr:hover {
        background-color: var(--bg-main) !important;
    }

    [data-testid="stMetric"] {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 16px 20px !important;
        box-shadow: var(--shadow-card);
    }
    [data-testid="stMetric"] label {
        color: var(--text-muted) !important;
        font-size: 13px !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text-title) !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    .stExpander {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        background-color: var(--bg-card) !important;
        box-shadow: var(--shadow-card) !important;
        margin-bottom: 12px;
    }
    .stExpander > details > summary {
        padding: 12px 16px !important;
        font-weight: 500 !important;
        color: var(--text-title) !important;
    }
    .stExpander > details > summary span {
        color: var(--text-title) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 8px 16px !important;
        font-size: 14px !important;
        color: var(--text-muted) !important;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom: 2px solid var(--primary) !important;
    }

    .stAlert {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
    }

    hr {
        border-color: var(--border) !important;
        margin: 16px 0 !important;
    }

    .stPlotlyChart {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 12px;
        box-shadow: var(--shadow-card);
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def api_request(method, endpoint, **kwargs):
    headers = kwargs.get('headers', {})
    if 'access_token' in st.session_state:
        headers['Authorization'] = f"Bearer {st.session_state['access_token']}"
    kwargs['headers'] = headers
    
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            error_info = error_data.get("error", {})
            st.error(f"HTTP错误 [{e.response.status_code}]: {error_info.get('message', str(e))}")
        except:
            st.error(f"HTTP错误: {str(e)}")
        return None
    except Exception as e:
        st.error(f"请求错误: {str(e)}")
        return None

def login(identifier, secret):
    data = {"identifier": identifier, "secret": secret}
    response = api_request("POST", "/auth/login", json=data)
    if response:
        st.session_state['access_token'] = response['access_token']
        st.session_state['user'] = response['user']
        return True
    return False

def logout():
    for key in ['access_token', 'user', 'student_info', 'assignments', 'grades', 'summary']:
        if key in st.session_state:
            del st.session_state[key]

def submit_assignment(assignment_id, text, file_upload, llm_log_upload):
    data = {"text": text}
    files = {}
    
    if file_upload:
        files["file"] = (file_upload.name, file_upload.getvalue(), file_upload.type)
    
    if llm_log_upload:
        files["LLM_chat_log"] = (llm_log_upload.name, llm_log_upload.getvalue(), "text/markdown")
    
    if not text and not files:
        st.error("作业文本内容和作业文件至少提供一个")
        return None
    
    response = api_request(
        "POST", 
        f"/assignments/{assignment_id}/submissions",
        data=data,
        files=files if files else None
    )
    if response:
        st.session_state.pop('assignments', None)
        st.success("作业提交成功！")
    return response

def download_file(file_url):
    headers = {}
    if 'access_token' in st.session_state:
        headers['Authorization'] = f"Bearer {st.session_state['access_token']}"
    
    if not file_url.startswith('http://') and not file_url.startswith('https://'):
        if file_url.startswith('/api/v1'):
            file_url = f"{BASE_URL.rsplit('/api/v1', 1)[0]}{file_url}"
        elif file_url.startswith('/'):
            file_url = f"{BASE_URL}{file_url}"
        else:
            file_url = f"{BASE_URL}/{file_url}"
    
    try:
        response = requests.get(file_url, headers=headers)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.error(f"下载失败: {str(e)}")
        return None