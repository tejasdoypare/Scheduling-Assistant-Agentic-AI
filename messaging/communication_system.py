from agents.negotiation_orchestrator import NegotiationOrchestrator
from messaging.email_generator import EmailGenerator
import json
import os
from datetime import datetime

class SchedulingCommunicationSystem:
    """
    Integrates multi-agent negotiation with polite message generation.
    Orchestrates the complete scheduling process from negotiation to final communication.
    """
    
    def __init__(self, api_key: str):
        self.orchestrator = NegotiationOrchestrator(api_key)
        self.message_generator = EmailGenerator(api_key)
        
    def run_full_scheduling_process(self, 
                                  meeting_request: dict, 
                                  candidate_slots: list,
                                  participants: dict,
                                  communication_preferences: dict = None):
        """
        Run the complete scheduling process:
        1. Multi-agent negotiation
        2. Generate appropriate messages based on outcome
        3. Return both scheduling result and messages
        
        Args:
            meeting_request: Meeting details
            candidate_slots: Available time slots
            participants: Dict of participant profiles
            communication_preferences: Tone, format preferences per participant
        """
        
        print("Starting Complete Scheduling Process")
        print("=" * 50)
        
        # Step 1: Add participants to orchestrator
        for name, profile in participants.items():
            self.orchestrator.add_participant(name, profile)
        
        # Step 2: Run negotiation
        print("Step 1: Running multi-agent negotiation...")
        negotiation_result = self.orchestrator.run_negotiation(meeting_request, candidate_slots)
        
        print(f"Negotiation Status: {negotiation_result.get('status')}")
        
        # Step 3: Generate appropriate messages based on outcome
        print("\nStep 2: Generating communication messages...")
        messages = self._generate_outcome_messages(
            negotiation_result, 
            meeting_request, 
            participants,
            communication_preferences or {}
        )
        
        # Step 4: Compile final result
        return {
            "scheduling_result": negotiation_result,
            "generated_messages": messages,
            "participants": list(participants.keys()),
            "process_summary": {
                "total_rounds": negotiation_result.get("rounds", 0),
                "interactions": len(negotiation_result.get("negotiation_history", [])),
                "final_status": negotiation_result.get("status"),
                "messages_generated": len(messages)
            }
        }
    
    def _generate_outcome_messages(self, 
                                 negotiation_result: dict, 
                                 meeting_request: dict,
                                 participants: dict,
                                 communication_preferences: dict):
        """
        Generate appropriate messages based on negotiation outcome
        """
        
        messages = {}
        status = negotiation_result.get("status")
        
        if status == "success":
            # Generate confirmation messages for all participants
            for participant_name in participants.keys():
                tone = communication_preferences.get(participant_name, {}).get("tone", "professional")
                
                context = {
                    "meeting_title": meeting_request.get("title"),
                    "final_time": negotiation_result["final_slot"]["start_utc"],
                    "duration_minutes": meeting_request.get("duration_minutes"),
                    "participants": list(participants.keys()),
                    "negotiation_rounds": negotiation_result.get("rounds", 0)
                }
                
                message = self.message_generator.generate_message(
                    message_type="confirmation",
                    context=context,
                    recipient_name=participant_name,
                    tone=tone
                )
                
                messages[participant_name] = {
                    "type": "confirmation",
                    "subject": message["subject"],
                    "body": message["body"]
                }
        
        elif status == "failed":
            # Generate apology messages
            reason = negotiation_result.get("reason", "scheduling_conflicts")
            
            for participant_name in participants.keys():
                tone = communication_preferences.get(participant_name, {}).get("tone", "professional")
                
                context = {
                    "meeting_title": meeting_request.get("title"),
                    "failure_reason": reason,
                    "negotiation_rounds": negotiation_result.get("rounds", 0),
                    "alternative_suggestion": "Please suggest alternative times or meeting formats"
                }
                
                message = self.message_generator.generate_message(
                    message_type="apology",
                    context=context,
                    recipient_name=participant_name,
                    tone=tone
                )
                
                messages[participant_name] = {
                    "type": "apology",
                    "subject": message["subject"],
                    "body": message["body"]
                }
        
        elif status == "alternatives_suggested":
            # Generate messages about suggested alternatives
            alternatives = negotiation_result.get("all_alternatives", [])
            
            for participant_name in participants.keys():
                tone = communication_preferences.get(participant_name, {}).get("tone", "professional")
                
                context = {
                    "meeting_title": meeting_request.get("title"),
                    "alternative_slots": alternatives[:3],  # Top 3 alternatives
                    "next_steps": "Please review and confirm your preferred option"
                }
                
                message = self.message_generator.generate_message(
                    message_type="counter_proposal",
                    context=context,
                    recipient_name=participant_name,
                    tone=tone
                )
                
                messages[participant_name] = {
                    "type": "counter_proposal", 
                    "subject": message["subject"],
                    "body": message["body"]
                }
        
        # Generate summary message for organizer/admin
        if negotiation_result.get("negotiation_history"):
            summary_message = self.message_generator.generate_negotiation_summary(
                negotiation_history=negotiation_result["negotiation_history"],
                final_outcome=negotiation_result,
                participants=list(participants.keys())
            )
            
            messages["_summary"] = {
                "type": "summary",
                "subject": summary_message["subject"],
                "body": summary_message["body"]
            }
        
        return messages
    
    def generate_individual_response_message(self, 
                                           participant_name: str,
                                           participant_response: dict,
                                           meeting_context: dict,
                                           tone: str = "professional"):
        """
        Generate a message based on individual participant response during negotiation
        """
        
        decision = participant_response.get("decision")
        
        if decision == "counter_propose":
            message_type = "counter_proposal"
            context = {
                "meeting_title": meeting_context.get("title"),
                "original_proposal": meeting_context.get("proposed_time"),
                "counter_proposals": participant_response.get("alternative_slots", []),
                "reasoning": participant_response.get("reasoning")
            }
        
        elif decision == "decline":
            message_type = "decline"
            context = {
                "meeting_title": meeting_context.get("title"),
                "proposed_time": meeting_context.get("proposed_time"),
                "decline_reason": participant_response.get("reasoning"),
                "flexibility": participant_response.get("flexibility", 0.5)
            }
        
        else:  # accept
            message_type = "confirmation"
            context = {
                "meeting_title": meeting_context.get("title"),
                "accepted_time": meeting_context.get("proposed_time"),
                "enthusiasm_level": "high" if participant_response.get("flexibility", 0.5) > 0.7 else "moderate"
            }
        
        return self.message_generator.generate_message(
            message_type=message_type,
            context=context,
            recipient_name="Meeting Organizer",
            tone=tone
        )


def demo_full_scheduling_communication():
    """
    Demonstrate the complete scheduling + communication system
    """
    print("PHASE 6: Complete Scheduling Communication Demo")
    print("=" * 60)
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found in environment variables")
        return
    
    # Initialize the complete system
    system = SchedulingCommunicationSystem(api_key)
    
    # Test scenario
    meeting_request = {
        "title": "Q1 Planning Session",
        "duration_minutes": 120,
        "priority": "high",
        "description": "Strategic planning for first quarter goals"
    }
    
    participants = {
        "Alice": {
            "flexibility_score": 0.8,
            "priorities": ["client_meetings", "project_deadlines"],
            "working_hours": {"start": "09:00", "end": "17:00"},
            "timezone": "Asia/Kolkata",
            "personality": "accommodating"
        },
        "Bob": {
            "flexibility_score": 0.4,
            "priorities": ["deep_work", "no_late_meetings"],
            "working_hours": {"start": "08:00", "end": "16:00"},
            "timezone": "US/Pacific",
            "personality": "structured"
        }
    }
    
    candidate_slots = [
        {
            "start_utc": "2026-01-17T14:00:00Z",  # Reasonable for both
            "end_utc": "2026-01-17T16:00:00Z",
            "participants": ["Alice", "Bob"],
            "confidence": 0.8
        }
    ]
    
    communication_preferences = {
        "Alice": {"tone": "friendly"},
        "Bob": {"tone": "professional"}
    }
    
    print(f"Meeting: {meeting_request['title']}")
    print(f"Participants: {list(participants.keys())}")
    print(f"Available slots: {len(candidate_slots)}")
    
    # Run complete process
    result = system.run_full_scheduling_process(
        meeting_request=meeting_request,
        candidate_slots=candidate_slots,
        participants=participants,
        communication_preferences=communication_preferences
    )
    
    print(f"\nPROCESS COMPLETE")
    print("=" * 30)
    print(f"Final Status: {result['process_summary']['final_status']}")
    print(f"Negotiation Rounds: {result['process_summary']['total_rounds']}")
    print(f"Messages Generated: {result['process_summary']['messages_generated']}")
    
    # Show sample messages
    print(f"\nSAMPLE GENERATED MESSAGES:")
    print("-" * 30)
    
    for recipient, message_data in result['generated_messages'].items():
        if not recipient.startswith('_'):  # Skip summary messages
            print(f"\n{recipient} ({message_data['type']}):")
            print(f"Subject: {message_data['subject']}")
            print(f"Body: {message_data['body'][:150]}...")
    
    return result