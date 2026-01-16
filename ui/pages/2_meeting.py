"""
Page 2: Create Meeting Request
Define meeting requirements and constraints.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app_logging import get_logger
from ui.components.theme import apply_theme, theme_toggle_sidebar

# Page config
st.set_page_config(page_title="Create Meeting", page_icon="📝", layout="wide")

# Apply theme
apply_theme()

# Sidebar with theme toggle
with st.sidebar:
    theme_toggle_sidebar()

logger = get_logger()
logger.log_app("Meeting page accessed", level="INFO")

# Initialize session state
if 'uploaded_calendars' not in st.session_state:
    st.session_state.uploaded_calendars = {}

if 'meeting_request' not in st.session_state:
    st.session_state.meeting_request = None

st.title("📝 Create Meeting Request")
st.markdown("Define your meeting requirements and preferences.")

st.divider()

# Check if calendars are uploaded
if not st.session_state.uploaded_calendars:
    st.warning("⚠️ No calendars uploaded yet. Please upload calendars first.")
    if st.button("Go to Upload Page"):
        st.switch_page("pages/1_upload.py")
else:
    # Display participants
    st.markdown("### 👥 Participants")
    participants = list(st.session_state.uploaded_calendars.keys())
    st.info(f"**{len(participants)} participant(s)**: {', '.join(participants)}")
    
    st.divider()
    
    # Meeting details form
    st.markdown("### 📋 Meeting Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        meeting_title = st.text_input(
            "Meeting Title",
            value="Team Sync Meeting",
            help="Name for this meeting"
        )
        
        duration_minutes = st.number_input(
            "Duration (minutes)",
            min_value=15,
            max_value=480,
            value=60,
            step=15,
            help="How long should the meeting last?"
        )
        
        priority = st.selectbox(
            "Priority Level",
            options=["High", "Medium", "Low"],
            index=1,
            help="Meeting importance"
        )
    
    with col2:
        # Date range
        today = datetime.now().date()
        start_date = st.date_input(
            "Search Start Date",
            value=today,
            help="Start looking for available slots from this date"
        )
        
        end_date = st.date_input(
            "Search End Date",
            value=today + timedelta(days=14),
            help="Stop looking for slots after this date"
        )
        
        max_slots = st.number_input(
            "Max Slot Suggestions",
            min_value=1,
            max_value=20,
            value=5,
            help="How many time slot options to find?"
        )
    
    st.divider()
    
    # Constraints
    st.markdown("### ⚙️ Constraints & Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        respect_working_hours = st.checkbox(
            "Respect Working Hours",
            value=True,
            help="Only suggest times during participants' working hours"
        )
        
        timezone_fairness = st.checkbox(
            "Timezone Fairness",
            value=True,
            help="Try to find times fair to all timezones"
        )
        
        avoid_back_to_back = st.checkbox(
            "Avoid Back-to-Back Meetings",
            value=True,
            help="Leave buffer time between meetings"
        )
    
    with col2:
        preferred_time_of_day = st.selectbox(
            "Preferred Time of Day",
            options=["Any", "Morning (8AM-12PM)", "Afternoon (12PM-5PM)", "Evening (5PM-8PM)"],
            index=0,
            help="When do you prefer to schedule?"
        )
        
        max_negotiation_rounds = st.number_input(
            "Max Negotiation Rounds",
            min_value=1,
            max_value=5,
            value=3,
            help="How many rounds of negotiation between agents?"
        )
    
    st.divider()
    
    # Additional notes
    st.markdown("### 📝 Additional Notes (Optional)")
    additional_notes = st.text_area(
        "Meeting Description or Special Requirements",
        placeholder="E.g., This is a critical planning session. We need everyone's full attention.",
        height=100
    )
    
    st.divider()
    
    # Create meeting button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("✨ Create Meeting Request", use_container_width=True, type="primary"):
            # Validate dates
            if end_date <= start_date:
                st.error("End date must be after start date!")
            else:
                # Create meeting request object
                meeting_request = {
                    'title': meeting_title,
                    'participants': participants,
                    'duration_minutes': duration_minutes,
                    'priority': priority,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'max_slots': max_slots,
                    'constraints': {
                        'respect_working_hours': respect_working_hours,
                        'timezone_fairness': timezone_fairness,
                        'avoid_back_to_back': avoid_back_to_back,
                        'preferred_time_of_day': preferred_time_of_day
                    },
                    'max_negotiation_rounds': max_negotiation_rounds,
                    'additional_notes': additional_notes,
                    'created_at': datetime.now().isoformat()
                }
                
                st.session_state.meeting_request = meeting_request
                
                logger.log_app(
                    f"Meeting request created: {meeting_title}",
                    level="INFO",
                    participants=len(participants),
                    duration=duration_minutes
                )
                
                st.success("✓ Meeting request created successfully!")
                st.balloons()
    
    # Show created request
    if st.session_state.meeting_request:
        st.divider()
        st.markdown("### ✓ Current Meeting Request")
        
        with st.expander("View Details", expanded=True):
            st.json(st.session_state.meeting_request)
    
    st.divider()
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Back to Upload", use_container_width=True):
            st.switch_page("pages/1_upload.py")
    
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    
    with col3:
        if st.session_state.meeting_request:
            if st.button("Next: Run Negotiation ➡️", use_container_width=True):
                logger.log_user_action("Navigate to Negotiation page from Meeting")
                st.switch_page("pages/3_negotiate.py")
        else:
            st.button("Next: Run Negotiation ➡️", disabled=True, use_container_width=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>Tip: Be flexible with constraints for better meeting slot options</p>
</div>
""", unsafe_allow_html=True)
