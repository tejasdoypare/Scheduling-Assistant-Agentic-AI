from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json
import random
from datetime import datetime, timedelta

class ParticipantAgent:
    """
    Represents a meeting participant with preferences and negotiation capabilities.
    Each agent has distinct personality traits that influence their responses.
    """
    
    def __init__(self, name: str, profile: dict, api_key: str):
        self.name = name
        self.profile = profile
        self.api_key = api_key
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.3,
            google_api_key=api_key
        )
        
        # Extract key personality traits
        self.flexibility_score = profile.get("flexibility_score", 0.5)  # 0-1 scale
        self.priorities = profile.get("priorities", [])
        self.working_hours = profile.get("working_hours", {"start": "09:00", "end": "17:00"})
        self.timezone = profile.get("timezone", "UTC")
        
    def respond_to_proposal(self, meeting_request: dict, proposed_slot: dict, context: dict = None):
        """
        Agent responds to a meeting proposal from the scheduler.
        Returns: accept, counter_propose, or decline
        """
        
        prompt_template = """
You are {name}, a professional with specific scheduling preferences and constraints.

Your Profile:
- Flexibility Score: {flexibility_score}/1.0 (how willing you are to accommodate others)
- Working Hours: {working_hours}
- Timezone: {timezone}
- Priorities: {priorities}

Meeting Request:
{meeting_request}

Proposed Time Slot:
{proposed_slot}

Context (previous negotiations):
{context}

Based on your personality and constraints, respond to this meeting proposal.

Response Options:
1. "accept" - if the slot works well for you
2. "counter_propose" - if you want to suggest alternatives
3. "decline" - if absolutely unable to meet

Provide your response as JSON:
{{
  "decision": "accept|counter_propose|decline",
  "reasoning": "Brief explanation of your decision",
  "alternative_slots": [{{ "start": "...", "end": "..." }}] (only if counter_propose),
  "flexibility": 0.1-1.0,
  "priority_concerns": ["concern1", "concern2"]
}}

Be realistic and consider:
- Your working hours and timezone
- Meeting importance vs your flexibility score
- Whether the time conflicts with your priorities

Response:
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["name", "flexibility_score", "working_hours", "timezone", 
                           "priorities", "meeting_request", "proposed_slot", "context"]
        )
        
        formatted_prompt = prompt.format(
            name=self.name,
            flexibility_score=self.flexibility_score,
            working_hours=json.dumps(self.working_hours),
            timezone=self.timezone,
            priorities=json.dumps(self.priorities),
            meeting_request=json.dumps(meeting_request, indent=2),
            proposed_slot=json.dumps(proposed_slot, indent=2),
            context=json.dumps(context or {}, indent=2)
        )
        
        response = self.llm.invoke(formatted_prompt)
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Handle JSON wrapped in markdown code blocks
        if "```json" in response_content:
            start_idx = response_content.find("```json") + 7
            end_idx = response_content.find("```", start_idx)
            if end_idx != -1:
                response_content = response_content[start_idx:end_idx].strip()
        elif "```" in response_content:
            start_idx = response_content.find("```") + 3
            end_idx = response_content.find("```", start_idx)
            if end_idx != -1:
                response_content = response_content[start_idx:end_idx].strip()
        
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            # Fallback response
            return {
                "decision": "counter_propose" if self.flexibility_score > 0.7 else "accept",
                "reasoning": "Unable to parse detailed response, using fallback based on flexibility",
                "flexibility": self.flexibility_score,
                "response_content": response_content
            }
    
    def propose_alternatives(self, meeting_request: dict, rejected_slot: dict):
        """
        Agent proactively suggests alternative meeting times
        """
        prompt_template = """
You are {name}. The proposed meeting time didn't work.

Your Profile:
- Flexibility Score: {flexibility_score}/1.0
- Working Hours: {working_hours}  
- Timezone: {timezone}
- Priorities: {priorities}

Meeting Request:
{meeting_request}

Rejected Slot:
{rejected_slot}

Suggest 2-3 alternative time slots that would work better for you.
Consider your working hours, timezone, and typical availability patterns.

Response as JSON:
{{
  "alternative_slots": [
    {{"start": "2026-01-16T10:00:00", "end": "2026-01-16T11:00:00", "reason": "preferred morning slot"}},
    {{"start": "2026-01-17T14:00:00", "end": "2026-01-17T15:00:00", "reason": "afternoon alternative"}}
  ],
  "preference_explanation": "Why these times work better for you"
}}
        """
        
        formatted_prompt = prompt_template.format(
            name=self.name,
            flexibility_score=self.flexibility_score,
            working_hours=json.dumps(self.working_hours),
            timezone=self.timezone,
            priorities=json.dumps(self.priorities),
            meeting_request=json.dumps(meeting_request, indent=2),
            rejected_slot=json.dumps(rejected_slot, indent=2)
        )
        
        response = self.llm.invoke(formatted_prompt)
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Handle JSON parsing similar to above
        if "```json" in response_content:
            start_idx = response_content.find("```json") + 7
            end_idx = response_content.find("```", start_idx)
            if end_idx != -1:
                response_content = response_content[start_idx:end_idx].strip()
                
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            # Fallback with reasonable alternatives
            return {
                "alternative_slots": [
                    {"start": "2026-01-16T10:00:00", "end": "2026-01-16T11:00:00", "reason": "morning preference"},
                    {"start": "2026-01-17T14:00:00", "end": "2026-01-17T15:00:00", "reason": "afternoon option"}
                ],
                "preference_explanation": f"As {self.name} with flexibility {self.flexibility_score}, these slots align with my working hours",
                "response_content": response_content
            }


def create_participant_profiles():
    """
    Create diverse participant profiles for testing negotiation
    """
    profiles = {
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
        },
        "Charlie": {
            "flexibility_score": 0.9,
            "priorities": ["collaboration", "team_alignment"],
            "working_hours": {"start": "10:00", "end": "18:00"},
            "timezone": "Europe/London",
            "personality": "flexible"
        }
    }
    return profiles