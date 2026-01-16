"""
Page 3: Run Negotiation
Execute multi-agent negotiation to find optimal meeting time.
"""

import streamlit as st
import sys
from pathlib import Path
import time
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app_logging import get_logger
from agents.negotiation_orchestrator import NegotiationOrchestrator
from agents.participant_agent import ParticipantAgent
from ui.components.visualizations import (
    create_negotiation_timeline,
    create_participant_responses,
    create_confidence_evolution,
    create_slot_comparison
)

# Page config
st.set_page_config(page_title="Run Negotiation", page_icon="🤝", layout="wide")

logger = get_logger()
logger.log_app("Negotiation page accessed", level="INFO")

# Initialize session state
if 'uploaded_calendars' not in st.session_state:
    st.session_state.uploaded_calendars = {}

if 'meeting_request' not in st.session_state:
    st.session_state.meeting_request = None

if 'negotiation_result' not in st.session_state:
    st.session_state.negotiation_result = None

st.title("🤝 Run Negotiation")
st.markdown("Let AI agents negotiate the best meeting time.")

st.divider()

# Check prerequisites
if not st.session_state.uploaded_calendars:
    st.warning("⚠️ No calendars uploaded. Please upload calendars first.")
    if st.button("Go to Upload Page"):
        st.switch_page("pages/1_upload.py")
elif not st.session_state.meeting_request:
    st.warning("⚠️ No meeting request created. Please create a meeting request first.")
    if st.button("Go to Meeting Page"):
        st.switch_page("pages/2_meeting.py")
else:
    # Display meeting info
    st.markdown("### 📋 Meeting Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Meeting Title", st.session_state.meeting_request['title'])
    
    with col2:
        st.metric("Participants", len(st.session_state.meeting_request['participants']))
    
    with col3:
        st.metric("Duration", f"{st.session_state.meeting_request['duration_minutes']} min")
    
    st.divider()
    
    # Run negotiation button
    if st.button("🚀 Start Negotiation", type="primary", use_container_width=True):
        logger.log_app("Starting negotiation process", level="INFO")
        
        # Progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Initialize agents
            status_text.text("Step 1/4: Initializing participant agents...")
            progress_bar.progress(25)
            time.sleep(0.5)
            
            participants = []
            for name, calendar_data in st.session_state.uploaded_calendars.items():
                # Extract participant info from calendar
                content = calendar_data['content']
                
                # Create profile dict for ParticipantAgent
                profile = {
                    'timezone': content.get('timezone', 'UTC'),
                    'working_hours': content.get('working_hours', {'start': '09:00', 'end': '17:00'}),
                    'flexibility_score': content.get('flexibility_score', 0.5),
                    'priorities': content.get('priorities', ['minimize_disruption'])
                }
                
                # Get API key from environment or config
                import os
                api_key = os.getenv('GOOGLE_API_KEY', '')
                
                agent = ParticipantAgent(
                    name=name,
                    profile=profile,
                    api_key=api_key
                )
                participants.append(agent)
                
                logger.log_agent(name, "Agent initialized", {
                    'timezone': agent.timezone,
                    'flexibility': agent.flexibility_score
                })
            
            st.success(f"✓ Initialized {len(participants)} agents")
            
            # Step 2: Prepare calendars
            status_text.text("Step 2/4: Processing calendars...")
            progress_bar.progress(50)
            time.sleep(0.5)
            
            calendars = {}
            for name, calendar_data in st.session_state.uploaded_calendars.items():
                calendars[name] = calendar_data['content']
            
            st.success(f"✓ Processed {len(calendars)} calendars")
            
            # Step 3: Run negotiation
            status_text.text("Step 3/4: Running multi-agent negotiation...")
            progress_bar.progress(75)
            
            orchestrator = NegotiationOrchestrator(participants=participants)
            
            meeting_request = st.session_state.meeting_request
            
            result = orchestrator.run_negotiation(
                calendars=calendars,
                meeting_duration_minutes=meeting_request['duration_minutes'],
                max_rounds=meeting_request['max_negotiation_rounds']
            )
            
            st.session_state.negotiation_result = result
            
            logger.log_negotiation(
                round_num=result.get('rounds_completed', 0),
                event="Negotiation completed",
                details={
                    'success': result.get('success', False),
                    'final_slot': result.get('final_slot')
                }
            )
            
            st.success(f"✓ Completed {result.get('rounds_completed', 0)} negotiation rounds")
            
            # Step 4: Finalize
            status_text.text("Step 4/4: Finalizing results...")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            status_text.empty()
            progress_bar.empty()
            
            st.success("🎉 Negotiation completed successfully!")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error during negotiation: {str(e)}")
            logger.log_error(e, context={'page': 'negotiation'})
            status_text.empty()
            progress_bar.empty()
    
    st.divider()
    
    # Display results
    if st.session_state.negotiation_result:
        result = st.session_state.negotiation_result
        
        st.markdown("### 📊 Negotiation Results")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Status",
                "✓ Success" if result.get('success') else "✗ Failed"
            )
        
        with col2:
            st.metric(
                "Rounds",
                result.get('rounds_completed', 0)
            )
        
        with col3:
            st.metric(
                "Confidence",
                f"{result.get('confidence_score', 0):.0%}"
            )
        
        with col4:
            st.metric(
                "Consensus",
                "Yes" if result.get('consensus_reached') else "No"
            )
        
        st.divider()
        
        # Visualizations
        st.markdown("### 📊 Negotiation Visualizations")
        
        # Timeline and responses
        col1, col2 = st.columns(2)
        
        with col1:
            if 'history' in result:
                fig_timeline = create_negotiation_timeline(result['history'])
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        with col2:
            fig_responses = create_participant_responses(result)
            st.plotly_chart(fig_responses, use_container_width=True)
        
        # Confidence evolution and slot comparison
        col1, col2 = st.columns(2)
        
        with col1:
            if 'history' in result:
                fig_confidence = create_confidence_evolution(result['history'])
                st.plotly_chart(fig_confidence, use_container_width=True)
        
        with col2:
            if 'history' in result and result['history']:
                # Get proposals from last round
                last_round = result['history'][-1]
                if 'proposals' in last_round:
                    fig_slots = create_slot_comparison(last_round['proposals'])
                    st.plotly_chart(fig_slots, use_container_width=True)
        
        st.divider()
        
        # Final slot
        if result.get('final_slot'):
            st.markdown("### 🎯 Recommended Meeting Time")
            
            final_slot = result['final_slot']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"""
                **Start Time**: {final_slot.get('start', 'N/A')}
                
                **End Time**: {final_slot.get('end', 'N/A')}
                
                **Confidence**: {final_slot.get('confidence_score', 0):.0%}
                """)
            
            with col2:
                st.info(f"""
                **Reasoning**: {final_slot.get('reasoning', 'N/A')}
                
                **Rank**: #{final_slot.get('rank', 'N/A')}
                """)
        
        st.divider()
        
        # Negotiation history
        with st.expander("📜 View Negotiation History", expanded=False):
            if 'history' in result:
                for idx, round_data in enumerate(result['history'], 1):
                    st.markdown(f"#### Round {idx}")
                    st.json(round_data)
            else:
                st.info("No history available")
        
        # Full result data
        with st.expander("🔍 View Full Result Data", expanded=False):
            st.json(result)
        
        st.divider()
        
        # Export button
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            result_json = json.dumps(result, indent=2)
            st.download_button(
                label="📥 Download Results (JSON)",
                data=result_json,
                file_name=f"negotiation_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    st.divider()
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Back to Meeting", use_container_width=True):
            st.switch_page("pages/2_meeting.py")
    
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    
    with col3:
        if st.session_state.negotiation_result:
            if st.button("Next: View Messages ➡️", use_container_width=True):
                logger.log_user_action("Navigate to Messages page from Negotiation")
                st.switch_page("pages/4_messages.py")
        else:
            st.button("Next: View Messages ➡️", disabled=True, use_container_width=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>Tip: The AI agents consider timezones, working hours, and preferences during negotiation</p>
</div>
""", unsafe_allow_html=True)
