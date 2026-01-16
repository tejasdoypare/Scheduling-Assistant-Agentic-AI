"""
Scheduling Assistant - Main Streamlit Application
Multi-agent scheduling system with calendar parsing, negotiation, and message generation.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app_logging import get_logger, init_logger

# Page configuration
st.set_page_config(
    page_title="Scheduling Assistant",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize logging
logger = init_logger()
logger.log_app("Application started", level="INFO")

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #145a8c;
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header">📅 Scheduling Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Multi-Agent Meeting Scheduler</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
### Welcome to the Scheduling Assistant!

This intelligent system helps you find the perfect meeting time by:
- Parsing calendars from multiple participants
- Understanding preferences, timezones, and constraints
- Running multi-agent negotiations to find optimal slots
- Generating professional communication messages
""")

st.divider()

# Features Overview
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>📤 Upload Calendars</h3>
        <p>Support for JSON, CSV, and iCalendar formats. Easy drag-and-drop interface.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 AI Negotiation</h3>
        <p>Multi-agent system finds optimal meeting times respecting all constraints.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>✉️ Smart Messages</h3>
        <p>Automatically generates professional emails for all participants.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Quick Start Guide
st.markdown("### 🚀 Quick Start")

with st.expander("How to use this application", expanded=True):
    st.markdown("""
    1. **Upload Calendars**: Go to the Upload page and add calendar files for all participants
    2. **Create Meeting Request**: Define meeting requirements (duration, participants, constraints)
    3. **Run Negotiation**: Let the AI agents find the optimal meeting time
    4. **View Messages**: See generated emails and communication for all participants
    5. **Export Results**: Download meeting details and logs
    """)

st.divider()

# System Status
st.markdown("### 🔧 System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Calendar Parser", value="Ready", delta="✓")

with col2:
    st.metric(label="AI Agents", value="3 Active", delta="✓")

with col3:
    st.metric(label="Logging", value="Enabled", delta="✓")

# Navigation Buttons
st.divider()
st.markdown("### 📍 Navigate to:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📤 Upload Calendars", use_container_width=True):
        logger.log_user_action("Navigate to Upload page")
        st.switch_page("pages/1_upload.py")

with col2:
    if st.button("📝 Create Meeting", use_container_width=True):
        logger.log_user_action("Navigate to Meeting page")
        st.switch_page("pages/2_meeting.py")

with col3:
    if st.button("🤝 Run Negotiation", use_container_width=True):
        logger.log_user_action("Navigate to Negotiation page")
        st.switch_page("pages/3_negotiate.py")

with col4:
    if st.button("✉️ View Messages", use_container_width=True):
        logger.log_user_action("Navigate to Messages page")
        st.switch_page("pages/4_messages.py")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>Powered by Google Gemini AI • Built with Streamlit</p>
    <p>Phase 7: UI + Logging Complete</p>
</div>
""", unsafe_allow_html=True)

# Log application ready
logger.log_app("Home page rendered successfully", level="INFO")
