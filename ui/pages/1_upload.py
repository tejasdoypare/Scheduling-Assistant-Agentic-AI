"""
Page 1: Upload Calendars
Upload and parse calendar files for meeting participants.
"""

import streamlit as st
import json
import sys
from pathlib import Path
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app_logging import get_logger
from ui.components.theme import apply_theme, theme_toggle_sidebar

# Page config
st.set_page_config(page_title="Upload Calendars", page_icon="📤", layout="wide")

# Apply theme
apply_theme()

# Sidebar with theme toggle
with st.sidebar:
    theme_toggle_sidebar()

logger = get_logger()
logger.log_app("Upload page accessed", level="INFO")

# Initialize session state
if 'uploaded_calendars' not in st.session_state:
    st.session_state.uploaded_calendars = {}

st.title("📤 Upload Calendars")
st.markdown("Upload calendar files for all meeting participants.")

st.divider()

# Upload section
st.markdown("### Upload Calendar Files")
st.markdown("Supported formats: JSON, CSV, iCalendar (.ics)")

uploaded_files = st.file_uploader(
    "Choose calendar files",
    type=['json', 'csv', 'ics'],
    accept_multiple_files=True,
    help="Upload one calendar file per participant"
)

if uploaded_files:
    st.success(f"✓ {len(uploaded_files)} file(s) uploaded")
    
    # Process each uploaded file
    for uploaded_file in uploaded_files:
        participant_name = uploaded_file.name.split('.')[0]
        
        with st.expander(f"📄 {uploaded_file.name}", expanded=False):
            try:
                if uploaded_file.name.endswith('.json'):
                    content = json.load(uploaded_file)
                    st.json(content)
                    st.session_state.uploaded_calendars[participant_name] = {
                        'filename': uploaded_file.name,
                        'format': 'json',
                        'content': content
                    }
                    logger.log_app(f"Loaded JSON calendar for {participant_name}", level="INFO")
                    
                elif uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                    st.dataframe(df, use_container_width=True)
                    st.session_state.uploaded_calendars[participant_name] = {
                        'filename': uploaded_file.name,
                        'format': 'csv',
                        'content': df.to_dict('records')
                    }
                    logger.log_app(f"Loaded CSV calendar for {participant_name}", level="INFO")
                    
                elif uploaded_file.name.endswith('.ics'):
                    content = uploaded_file.read().decode('utf-8')
                    st.code(content[:500] + "..." if len(content) > 500 else content)
                    st.session_state.uploaded_calendars[participant_name] = {
                        'filename': uploaded_file.name,
                        'format': 'ics',
                        'content': content
                    }
                    logger.log_app(f"Loaded iCalendar for {participant_name}", level="INFO")
                    
                st.success(f"✓ Parsed successfully")
                
            except Exception as e:
                st.error(f"Error parsing file: {str(e)}")
                logger.log_error(e, context={'file': uploaded_file.name})

st.divider()

# Display loaded calendars
if st.session_state.uploaded_calendars:
    st.markdown("### 📋 Loaded Calendars")
    
    cols = st.columns(3)
    for idx, (name, data) in enumerate(st.session_state.uploaded_calendars.items()):
        with cols[idx % 3]:
            st.info(f"**{name}**\n\nFormat: {data['format']}\n\nFile: {data['filename']}")
    
    st.divider()
    
    # Clear button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.uploaded_calendars = {}
            logger.log_user_action("Cleared all calendars")
            st.rerun()
    
    st.divider()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button("Next: Create Meeting ➡️", use_container_width=True):
            logger.log_user_action("Navigate to Meeting page from Upload")
            st.switch_page("pages/2_meeting.py")

else:
    st.info("👆 Upload calendar files to get started")
    
    # Sample data option
    st.divider()
    st.markdown("### 📦 Or Use Sample Data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load Scenario 1 (2 participants)", use_container_width=True):
            # Load from data/scenarios/scenario_001
            try:
                scenario_path = project_root / "data" / "scenarios" / "scenario_001"
                for json_file in scenario_path.glob("*.json"):
                    if json_file.name != "request.json":
                        with open(json_file, 'r') as f:
                            content = json.load(f)
                            participant_name = json_file.stem
                            st.session_state.uploaded_calendars[participant_name] = {
                                'filename': json_file.name,
                                'format': 'json',
                                'content': content
                            }
                logger.log_app("Loaded Scenario 1 sample data", level="INFO")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
                logger.log_error(e, context={'scenario': 'scenario_001'})
    
    with col2:
        if st.button("Load Scenario 2 (3 participants)", use_container_width=True):
            try:
                scenario_path = project_root / "data" / "scenarios" / "scenario_002"
                for json_file in scenario_path.glob("*.json"):
                    if json_file.name != "request.json":
                        with open(json_file, 'r') as f:
                            content = json.load(f)
                            participant_name = json_file.stem
                            st.session_state.uploaded_calendars[participant_name] = {
                                'filename': json_file.name,
                                'format': 'json',
                                'content': content
                            }
                logger.log_app("Loaded Scenario 2 sample data", level="INFO")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
                logger.log_error(e, context={'scenario': 'scenario_002'})

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <p style="color: #888; margin-bottom: 1rem;">💡 Tip: Calendar files should contain availability, working hours, and timezone information</p>
</div>
""", unsafe_allow_html=True)

# Sample data format examples
with st.expander("📋 See Sample Calendar Format Examples", expanded=False):
    st.markdown("### Example Calendar Data Format")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Person A - CSV Format**")
        st.code("""name,email,timezone,working_hours_start,working_hours_end,available_dates,priority
Alice,alice@company.com,America/New_York,09:00,17:00,"2026-01-20,2026-01-21,2026-01-22",high""", language="csv")
        
        st.markdown("**Person A - JSON Format**")
        st.code("""{
  "name": "Alice",
  "email": "alice@company.com",
  "timezone": "America/New_York",
  "working_hours": {
    "start": "09:00",
    "end": "17:00"
  },
  "available_dates": [
    "2026-01-20",
    "2026-01-21",
    "2026-01-22"
  ],
  "busy_slots": [
    {
      "date": "2026-01-20",
      "start": "10:00",
      "end": "11:00"
    }
  ],
  "priority": "high"
}""", language="json")
    
    with col2:
        st.markdown("**Person B - CSV Format**")
        st.code("""name,email,timezone,working_hours_start,working_hours_end,available_dates,priority
Bob,bob@company.com,Asia/Tokyo,08:00,16:00,"2026-01-20,2026-01-21,2026-01-23",medium""", language="csv")
        
        st.markdown("**Person B - JSON Format**")
        st.code("""{
  "name": "Bob",
  "email": "bob@company.com",
  "timezone": "Asia/Tokyo",
  "working_hours": {
    "start": "08:00",
    "end": "16:00"
  },
  "available_dates": [
    "2026-01-20",
    "2026-01-21",
    "2026-01-23"
  ],
  "busy_slots": [
    {
      "date": "2026-01-21",
      "start": "13:00",
      "end": "14:00"
    }
  ],
  "priority": "medium"
}""", language="json")
    
    st.info("📝 **Required Fields**: name, email, timezone, working_hours, available_dates")
    st.success("✨ **Optional Fields**: busy_slots, priority, preferences")

