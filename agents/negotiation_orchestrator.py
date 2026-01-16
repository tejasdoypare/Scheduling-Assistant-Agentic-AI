from agents.scheduler_agent import run_scheduler_agent
from agents.participant_agent import ParticipantAgent, create_participant_profiles
import json
import os
from datetime import datetime

class NegotiationOrchestrator:
    """
    Manages multi-agent negotiation between scheduler and participants.
    Demonstrates agentic behavior through iterative proposal and response cycles.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.participants = {}
        self.negotiation_history = []
        self.max_rounds = 3  # Limit negotiation rounds
        
    def add_participant(self, name: str, profile: dict):
        """Add a participant agent to the negotiation"""
        self.participants[name] = ParticipantAgent(name, profile, self.api_key)
        
    def run_negotiation(self, meeting_request: dict, candidate_slots: list):
        """
        Run the multi-agent negotiation process.
        
        Flow:
        1. Scheduler proposes initial time
        2. Participants respond (accept/counter/decline) 
        3. Scheduler adapts based on responses
        4. Repeat until consensus or max rounds reached
        """
        
        print(f"Starting negotiation for: {meeting_request['title']}")
        print(f"Participants: {list(self.participants.keys())}")
        print("=" * 50)
        
        # Round 0: Initial scheduler proposal
        scheduler_input = {
            "meeting_request": meeting_request,
            "candidate_slots": candidate_slots,
            "participants": list(self.participants.keys())
        }
        
        try:
            with open("prompts/scheduler.txt", "r") as f:
                scheduler_prompt = f.read()
        except FileNotFoundError:
            scheduler_prompt = """
You are a scheduling agent. Given meeting requirements and candidate slots, choose the best option.

Consider:
- Participant time zones
- Working hours
- Meeting priority
- Minimize disruption

Respond with JSON:
{
  "decision": "confirm_time|propose_new_time|negotiate_or_reschedule",
  "selected_slot_id": "slot_id or null",
  "reasoning": "explanation",
  "confidence": 0.0-1.0
}
            """
        
        initial_decision = run_scheduler_agent(scheduler_input, scheduler_prompt, self.api_key)
        print(f"Scheduler Initial Proposal:")
        print(f"   Decision: {initial_decision.get('decision')}")
        print(f"   Reasoning: {initial_decision.get('reasoning')}")
        
        self.negotiation_history.append({
            "round": 0,
            "agent": "scheduler",
            "action": "initial_proposal",
            "content": initial_decision
        })
        
        # If no good slots available, scheduler suggests negotiation
        if initial_decision.get("decision") == "negotiate_or_reschedule":
            return self._handle_no_initial_slots(meeting_request)
        
        # Extract proposed slot for participant feedback
        if initial_decision.get("selected_slot_id") is not None:
            try:
                slot_id = initial_decision["selected_slot_id"]
                proposed_slot = candidate_slots[slot_id] if isinstance(slot_id, int) else candidate_slots[0]
            except (IndexError, KeyError):
                proposed_slot = candidate_slots[0] if candidate_slots else {
                    "start": "2026-01-16T10:00:00Z",
                    "end": "2026-01-16T11:00:00Z",
                    "confidence_score": 0.5
                }
        else:
            proposed_slot = candidate_slots[0] if candidate_slots else {
                "start": "2026-01-16T10:00:00Z", 
                "end": "2026-01-16T11:00:00Z",
                "confidence_score": 0.5
            }
        
        # Normalize slot keys (convert start_utc -> start, end_utc -> end if needed)
        if "start_utc" in proposed_slot and "start" not in proposed_slot:
            proposed_slot["start"] = proposed_slot["start_utc"]
        if "end_utc" in proposed_slot and "end" not in proposed_slot:
            proposed_slot["end"] = proposed_slot["end_utc"]
        if "confidence_score" not in proposed_slot:
            proposed_slot["confidence_score"] = proposed_slot.get("confidence", 0.7)
        if "reasoning" not in proposed_slot:
            proposed_slot["reasoning"] = initial_decision.get("reasoning", "Best available slot based on participant availability")
        if "rank" not in proposed_slot:
            proposed_slot["rank"] = 1
        
        # Negotiation rounds
        current_slot = proposed_slot
        
        for round_num in range(1, self.max_rounds + 1):
            print(f"\nNegotiation Round {round_num}")
            print("-" * 30)
            
            # Collect participant responses
            participant_responses = {}
            all_accepted = True
            counter_proposals = []
            
            for name, agent in self.participants.items():
                print(f"{name} responding...")
                
                response = agent.respond_to_proposal(
                    meeting_request,
                    current_slot,
                    {"round": round_num, "history": self.negotiation_history[-3:]}  # Last 3 rounds context
                )
                
                participant_responses[name] = response
                
                print(f"   {name}: {response.get('decision')} - {response.get('reasoning', 'No reasoning provided')}")
                
                # Track negotiation history
                self.negotiation_history.append({
                    "round": round_num,
                    "agent": name,
                    "action": "respond",
                    "content": response
                })
                
                if response.get("decision") != "accept":
                    all_accepted = False
                    if response.get("decision") == "counter_propose" and response.get("alternative_slots"):
                        counter_proposals.extend(response["alternative_slots"])
            
            # Check if consensus reached
            if all_accepted:
                print(f"\nConsensus reached! Meeting scheduled.")
                return {
                    "success": True,
                    "status": "success",
                    "final_slot": current_slot,
                    "rounds_completed": round_num,
                    "confidence_score": current_slot.get("confidence_score", 0.8),
                    "consensus_reached": True,
                    "participant_responses": participant_responses,
                    "negotiation_history": self.negotiation_history,
                    "history": self.negotiation_history
                }
            
            # If we're at max rounds, declare negotiation failed
            if round_num >= self.max_rounds:
                print(f"\nNegotiation failed after {self.max_rounds} rounds")
                return {
                    "success": False,
                    "status": "failed",
                    "reason": "max_rounds_exceeded",
                    "rounds_completed": round_num,
                    "confidence_score": 0.0,
                    "consensus_reached": False,
                    "participant_responses": participant_responses,
                    "negotiation_history": self.negotiation_history,
                    "history": self.negotiation_history
                }
            
            # Scheduler adapts based on participant feedback
            print(f"\nScheduler adapting based on feedback...")
            adaptation_result = self._scheduler_adaptation(
                meeting_request, 
                current_slot, 
                participant_responses, 
                counter_proposals
            )
            
            if adaptation_result.get("decision") == "abort":
                print("Scheduler decided to abort negotiation")
                return {
                    "success": False,
                    "status": "aborted",
                    "reason": adaptation_result.get("reasoning"),
                    "rounds_completed": round_num,
                    "confidence_score": 0.0,
                    "consensus_reached": False,
                    "negotiation_history": self.negotiation_history,
                    "history": self.negotiation_history
                }
            
            # Update current slot for next round
            if adaptation_result.get("new_slot"):
                current_slot = adaptation_result["new_slot"]
                print(f"New proposed time: {current_slot}")
        
        return {
            "success": False,
            "status": "incomplete",
            "rounds_completed": self.max_rounds,
            "confidence_score": 0.0,
            "consensus_reached": False,
            "negotiation_history": self.negotiation_history,
            "history": self.negotiation_history
        }
    
    def _handle_no_initial_slots(self, meeting_request: dict):
        """Handle case where scheduler has no good initial slots"""
        print("\nNo ideal slots available - gathering participant availability...")
        
        all_alternatives = []
        for name, agent in self.participants.items():
            print(f"{name} suggesting alternatives...")
            alternatives = agent.propose_alternatives(
                meeting_request, 
                {"reason": "no_initial_slots"}
            )
            
            if alternatives.get("alternative_slots"):
                for slot in alternatives["alternative_slots"]:
                    slot["proposed_by"] = name
                    all_alternatives.append(slot)
                    
                print(f"   {name} suggested {len(alternatives['alternative_slots'])} alternatives")
        
        if not all_alternatives:
            return {
                "success": False,
                "status": "failed",
                "reason": "no_alternatives_suggested",
                "rounds_completed": 0,
                "confidence_score": 0.0,
                "consensus_reached": False,
                "negotiation_history": self.negotiation_history,
                "history": self.negotiation_history
            }
        
        # Scheduler evaluates alternatives
        print(f"\nScheduler evaluating {len(all_alternatives)} alternative slots...")
        
        # Use the best alternative as new proposal
        best_alternative = all_alternatives[0]  # Simplified selection
        
        print(f"Scheduler selected: {best_alternative}")
        
        # Continue with normal negotiation flow
        return {
            "success": True,
            "status": "alternatives_suggested",
            "selected_alternative": best_alternative,
            "all_alternatives": all_alternatives,
            "rounds_completed": 0,
            "confidence_score": best_alternative.get("confidence_score", 0.5),
            "consensus_reached": False,
            "negotiation_history": self.negotiation_history,
            "history": self.negotiation_history
        }
    
    def _scheduler_adaptation(self, meeting_request: dict, current_slot: dict, 
                            participant_responses: dict, counter_proposals: list):
        """Scheduler adapts based on participant feedback"""
        
        # Count responses
        accepts = sum(1 for r in participant_responses.values() if r.get("decision") == "accept")
        declines = sum(1 for r in participant_responses.values() if r.get("decision") == "decline") 
        counters = sum(1 for r in participant_responses.values() if r.get("decision") == "counter_propose")
        
        print(f"   Feedback: {accepts} accepts, {counters} counters, {declines} declines")
        
        # Simple adaptation logic
        if declines > len(participant_responses) // 2:
            return {
                "decision": "abort",
                "reasoning": "Too many participants declined"
            }
        
        if counter_proposals:
            # Select first counter-proposal for simplicity
            new_slot = {
                "start_utc": counter_proposals[0]["start"],
                "end_utc": counter_proposals[0]["end"]
            }
            return {
                "decision": "adapt",
                "new_slot": new_slot,
                "reasoning": f"Adopting counter-proposal: {counter_proposals[0].get('reason', 'participant suggestion')}"
            }
        
        return {
            "decision": "continue",
            "reasoning": "Continuing with current slot"
        }


# Demo function for testing
def demo_negotiation():
    """
    Demonstrate the multi-agent negotiation process
    """
    print("PHASE 5: Multi-Agent Negotiation Demo")
    print("=" * 60)
    
    # Setup
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found in environment variables")
        return
    
    orchestrator = NegotiationOrchestrator(api_key)
    
    # Add participants with different personalities
    profiles = create_participant_profiles()
    for name, profile in profiles.items():
        orchestrator.add_participant(name, profile)
        print(f"Added {name}: flexibility={profile['flexibility_score']}, personality={profile['personality']}")
    
    # Meeting request
    meeting_request = {
        "title": "Product Strategy Review",
        "duration_minutes": 90,
        "priority": "high",
        "participants": list(profiles.keys())
    }
    
    # Sample candidate slots (normally from calendar analysis)
    candidate_slots = [
        {
            "start_utc": "2026-01-16T14:00:00Z",  # 2 PM UTC
            "end_utc": "2026-01-16T15:30:00Z",
            "participants": list(profiles.keys()),
            "confidence": 0.7
        },
        {
            "start_utc": "2026-01-17T09:00:00Z",  # 9 AM UTC  
            "end_utc": "2026-01-17T10:30:00Z",
            "participants": list(profiles.keys()),
            "confidence": 0.6
        }
    ]
    
    print(f"\nMeeting: {meeting_request['title']} ({meeting_request['duration_minutes']} min)")
    print(f"Available slots: {len(candidate_slots)}")
    
    # Run negotiation
    result = orchestrator.run_negotiation(meeting_request, candidate_slots)
    
    print("\n" + "="*60)
    print("NEGOTIATION RESULT")
    print("="*60)
    print(f"Status: {result['status']}")
    
    if result.get('final_slot'):
        print(f"Final time: {result['final_slot']}")
        print(f"Rounds needed: {result.get('rounds', 'N/A')}")
    
    if result.get('reason'):
        print(f"Reason: {result['reason']}")
    
    print(f"\nNegotiation involved {len(result.get('negotiation_history', []))} interactions")
    
    return result