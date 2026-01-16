"""
Shared theme component for all pages.
Provides consistent theming across the entire application.
"""

import streamlit as st


def init_theme():
    """Initialize theme in session state if not exists."""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'


def apply_theme():
    """Apply the current theme CSS to the page."""
    init_theme()
    
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
            /* Dark theme */
            .stApp {
                background-color: #1a1a2e !important;
                color: #eaeaea !important;
            }
            
            /* Main content area */
            .main .block-container {
                background-color: #1a1a2e !important;
                color: #eaeaea !important;
            }
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #4CAF50 !important;
            }
            
            .main-header {
                font-size: 3rem;
                font-weight: bold;
                color: #4CAF50 !important;
                text-align: center;
                margin-bottom: 1rem;
            }
            
            .sub-header {
                font-size: 1.2rem;
                color: #b0b0b0 !important;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            /* Feature boxes */
            .feature-box {
                background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%) !important;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                color: white !important;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
                border: 1px solid #4CAF50;
            }
            
            .feature-box h3 {
                color: #81C784 !important;
                margin-top: 0;
            }
            
            .feature-box p {
                color: #e0e0e0 !important;
            }
            
            /* Buttons */
            .stButton > button {
                background-color: #4CAF50 !important;
                color: white !important;
                font-weight: bold;
                border-radius: 5px;
                border: none !important;
            }
            
            .stButton > button:hover {
                background-color: #45a049 !important;
                border: none !important;
            }
            
            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: #16213e !important;
            }
            
            section[data-testid="stSidebar"] .stMarkdown {
                color: #eaeaea !important;
            }
            
            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3 {
                color: #4CAF50 !important;
            }
            
            /* Text inputs */
            .stTextInput > div > div > input {
                background-color: #2d3748 !important;
                color: white !important;
                border: 1px solid #4a5568 !important;
            }
            
            .stTextArea > div > div > textarea {
                background-color: #2d3748 !important;
                color: white !important;
                border: 1px solid #4a5568 !important;
            }
            
            /* Select boxes */
            .stSelectbox > div > div {
                background-color: #2d3748 !important;
                color: white !important;
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                color: #4CAF50 !important;
            }
            
            [data-testid="stMetricLabel"] {
                color: #b0b0b0 !important;
            }
            
            /* Info/Warning/Error boxes */
            .stAlert {
                background-color: #2d3748 !important;
                color: #eaeaea !important;
            }
            
            /* Expanders */
            .streamlit-expanderHeader {
                background-color: #2d3748 !important;
                color: #eaeaea !important;
            }
            
            .streamlit-expanderContent {
                background-color: #1a1a2e !important;
                color: #eaeaea !important;
            }
            
            /* Tables */
            .stDataFrame {
                background-color: #2d3748 !important;
            }
            
            /* JSON display */
            pre {
                background-color: #2d3748 !important;
                color: #e0e0e0 !important;
            }
            
            /* Dividers */
            hr {
                border-color: #4a5568 !important;
            }
            
            /* Labels and captions */
            .stCaption, label {
                color: #b0b0b0 !important;
            }
            
            /* Markdown text */
            .stMarkdown p, .stMarkdown li {
                color: #e0e0e0 !important;
            }
            
            /* File uploader */
            .stFileUploader {
                background-color: #2d3748 !important;
            }
            
            [data-testid="stFileUploader"] {
                background-color: #2d3748 !important;
            }
            
            /* Progress bar */
            .stProgress > div > div {
                background-color: #4CAF50 !important;
            }
            
            /* Number input */
            .stNumberInput > div > div > input {
                background-color: #2d3748 !important;
                color: white !important;
            }
            
            /* Date input */
            .stDateInput > div > div > input {
                background-color: #2d3748 !important;
                color: white !important;
            }
            
            /* Checkbox */
            .stCheckbox label {
                color: #e0e0e0 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            /* Light theme */
            .stApp {
                background-color: #ffffff !important;
                color: #1a1a1a !important;
            }
            
            .main-header {
                font-size: 3rem;
                font-weight: bold;
                color: #1f77b4 !important;
                text-align: center;
                margin-bottom: 1rem;
            }
            
            .sub-header {
                font-size: 1.2rem;
                color: #666666 !important;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            /* Feature boxes */
            .feature-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                color: white !important;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .feature-box h3 {
                color: white !important;
                margin-top: 0;
            }
            
            .feature-box p {
                color: rgba(255, 255, 255, 0.95) !important;
            }
            
            /* Buttons */
            .stButton > button {
                background-color: #1f77b4 !important;
                color: white !important;
                font-weight: bold;
                border-radius: 5px;
                border: none !important;
            }
            
            .stButton > button:hover {
                background-color: #145a8c !important;
            }
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #1f77b4 !important;
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                color: #1f77b4 !important;
            }
            
            /* Markdown text */
            .stMarkdown p, .stMarkdown li {
                color: #333333 !important;
            }
        </style>
        """, unsafe_allow_html=True)


def theme_toggle_sidebar():
    """Add theme toggle to sidebar."""
    init_theme()
    
    st.markdown("### 🎨 Theme")
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("☀️ Light", use_container_width=True, 
                     type="primary" if st.session_state.theme == 'light' else "secondary"):
            st.session_state.theme = 'light'
            st.rerun()
    with theme_col2:
        if st.button("🌙 Dark", use_container_width=True,
                     type="primary" if st.session_state.theme == 'dark' else "secondary"):
            st.session_state.theme = 'dark'
            st.rerun()
    st.divider()
