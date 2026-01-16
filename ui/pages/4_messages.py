"""
Page 4: View Messages
Display generated communication messages for all participants.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app_logging import get_logger
from messaging.email_generator import EmailGenerator

# Page config
st.set_page_config(page_title="View Messages", page_icon="✉️", layout="wide")

logger = get_logger()
logger.log_app("Messages page accessed", level="INFO")

# Initialize session state
if 'meeting_request' not in st.session_state:
    st.session_state.meeting_request = None

if 'negotiation_result' not in st.session_state:
    st.session_state.negotiation_result = None

if 'generated_messages' not in st.session_state:
    st.session_state.generated_messages = None

st.title("✉️ View Messages")
st.markdown("Professional communication for all participants.")

st.divider()

# Check prerequisites
if not st.session_state.meeting_request:
    st.warning("⚠️ No meeting request found. Please create a meeting first.")
    if st.button("Go to Meeting Page"):
        st.switch_page("pages/2_meeting.py")
elif not st.session_state.negotiation_result:
    st.warning("⚠️ No negotiation results found. Please run negotiation first.")
    if st.button("Go to Negotiation Page"):
        st.switch_page("pages/3_negotiate.py")
else:
    # Generate messages button
    if not st.session_state.generated_messages:
        st.markdown("### 📧 Generate Messages")
        
        st.info("Generate professional emails to send to all participants based on the negotiation outcome.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("✨ Generate Messages", type="primary", use_container_width=True):
                with st.spinner("Generating messages..."):
                    try:
                        email_generator = EmailGenerator()
                        
                        result = st.session_state.negotiation_result
                        meeting = st.session_state.meeting_request
                        
                        # Determine message type based on result
                        if result.get('success') and result.get('final_slot'):
                            message_type = "confirmation"
                            context = {
                                'meeting_title': meeting['title'],
                                'participants': meeting['participants'],
                                'proposed_time': result['final_slot'].get('start'),
                                'duration': meeting['duration_minutes'],
                                'reasoning': result['final_slot'].get('reasoning', '')
                            }
                        else:
                            message_type = "apology"
                            context = {
                                'meeting_title': meeting['title'],
                                'participants': meeting['participants'],
                                'reason': 'Unable to find a suitable time slot after negotiation'
                            }
                        
                        # Generate message
                        message = email_generator.generate_message(
                            message_type=message_type,
                            context=context,
                            tone="professional"
                        )
                        
                        st.session_state.generated_messages = {
                            'type': message_type,
                            'message': message,
                            'context': context,
                            'generated_at': datetime.now().isoformat()
                        }
                        
                        logger.log_app(
                            f"Generated {message_type} message",
                            level="INFO",
                            recipients=len(meeting['participants'])
                        )
                        
                        st.success("✓ Messages generated successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error generating messages: {str(e)}")
                        logger.log_error(e, context={'page': 'messages'})
    
    # Display generated messages
    if st.session_state.generated_messages:
        messages_data = st.session_state.generated_messages
        message = messages_data['message']
        
        st.markdown("### 📬 Generated Messages")
        
        # Message type indicator
        message_type = messages_data['type'].replace('_', ' ').title()
        st.info(f"**Message Type**: {message_type}")
        
        st.divider()
        
        # Email preview
        st.markdown("### 📧 Email Preview")
        
        # Subject
        st.markdown("#### Subject")
        st.code(message.get('subject', 'N/A'), language=None)
        
        # Body
        st.markdown("#### Body")
        st.text_area(
            "Email Body",
            value=message.get('body', 'N/A'),
            height=300,
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Recipients
        st.markdown("### 👥 Recipients")
        
        participants = st.session_state.meeting_request['participants']
        
        cols = st.columns(min(len(participants), 3))
        for idx, participant in enumerate(participants):
            with cols[idx % 3]:
                st.success(f"✓ {participant}")
        
        st.divider()
        
        # Additional actions
        st.markdown("### 🛠️ Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Copy to clipboard
            if st.button("📋 Copy Message", use_container_width=True):
                full_message = f"Subject: {message.get('subject', '')}\n\n{message.get('body', '')}"
                st.code(full_message, language=None)
                st.info("Copy the message above to your clipboard")
        
        with col2:
            # Download as text
            full_message = f"Subject: {message.get('subject', '')}\n\n{message.get('body', '')}"
            st.download_button(
                label="💾 Download Text",
                data=full_message,
                file_name=f"message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            # Download as JSON
            message_json = json.dumps(messages_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=message_json,
                file_name=f"message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.divider()
        
        # Regenerate with different tone
        st.markdown("### 🎨 Change Tone")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_tone = st.selectbox(
                "Select Tone",
                options=["professional", "casual", "formal", "friendly"],
                index=0
            )
        
        with col2:
            if st.button("🔄 Regenerate with New Tone", use_container_width=True):
                with st.spinner("Regenerating message..."):
                    try:
                        email_generator = EmailGenerator()
                        
                        new_message = email_generator.generate_message(
                            message_type=messages_data['type'],
                            context=messages_data['context'],
                            tone=new_tone
                        )
                        
                        st.session_state.generated_messages['message'] = new_message
                        
                        logger.log_app(
                            f"Regenerated message with {new_tone} tone",
                            level="INFO"
                        )
                        
                        st.success(f"✓ Regenerated with {new_tone} tone!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error regenerating: {str(e)}")
                        logger.log_error(e, context={'tone': new_tone})
        
        st.divider()
        
        # View full data
        with st.expander("🔍 View Full Message Data", expanded=False):
            st.json(messages_data)
    
    st.divider()
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Back to Negotiation", use_container_width=True):
            st.switch_page("pages/3_negotiate.py")
    
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    
    with col3:
        if st.button("🔄 Start New Meeting", use_container_width=True):
            # Clear session state
            st.session_state.meeting_request = None
            st.session_state.negotiation_result = None
            st.session_state.generated_messages = None
            logger.log_user_action("Started new meeting workflow")
            st.switch_page("pages/1_upload.py")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>Tip: Use the copy or download buttons to share messages with participants</p>
</div>
""", unsafe_allow_html=True)
