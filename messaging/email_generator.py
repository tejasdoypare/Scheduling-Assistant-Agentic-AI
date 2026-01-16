from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class EmailGenerator:
    """
    Generates polite, context-aware professional messages for meeting scheduling.
    Handles confirmation, reschedule requests, apologies, and alternatives.
    """
    
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)  # Higher temp for natural language
        
    def generate_message(self, 
                        message_type: str, 
                        context: Dict,
                        recipient_name: str,
                        tone: str = "professional") -> Dict[str, str]:
        """
        Generate a message based on type and context.
        
        Args:
            message_type: "confirmation", "reschedule", "apology", "counter_proposal", "decline"
            context: Dictionary with meeting details, times, reasoning, etc.
            recipient_name: Name of the message recipient
            tone: "professional", "casual", "formal", "friendly"
            
        Returns:
            Dictionary with subject and body text
        """
        
        # Select appropriate template based on message type
        template_map = {
            "confirmation": self._get_confirmation_template(),
            "reschedule": self._get_reschedule_template(),
            "apology": self._get_apology_template(),
            "counter_proposal": self._get_counter_proposal_template(),
            "decline": self._get_decline_template()
        }
        
        if message_type not in template_map:
            raise ValueError(f"Unknown message type: {message_type}. Supported: {list(template_map.keys())}")
        
        template = template_map[message_type]
        
        # Format the prompt
        formatted_prompt = template.format(
            recipient_name=recipient_name,
            tone=tone,
            context=json.dumps(context, indent=2)
        )
        
        # Generate response
        response = self.llm.invoke(formatted_prompt)
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Parse JSON response
        return self._parse_message_response(response_content)
    
    def _get_confirmation_template(self) -> PromptTemplate:
        """Template for meeting confirmation messages"""
        template = """
You are a professional assistant composing a meeting confirmation email.

Recipient: {recipient_name}
Tone: {tone}
Context: {context}

Generate a polite confirmation email with subject and body.
The email should:
- Confirm the agreed meeting time
- Include meeting details (title, duration, participants)
- Show appreciation for scheduling flexibility
- Include any relevant meeting preparation or logistics
- Match the specified tone

Respond with JSON:
{{
  "subject": "Meeting confirmation subject line",
  "body": "Email body with appropriate greeting, confirmation details, and professional closing"
}}
        """
        return PromptTemplate(template=template, input_variables=["recipient_name", "tone", "context"])
    
    def _get_reschedule_template(self) -> PromptTemplate:
        """Template for rescheduling request messages"""
        template = """
You are a professional assistant composing a meeting reschedule request.

Recipient: {recipient_name}
Tone: {tone}
Context: {context}

Generate a polite reschedule request email with subject and body.
The email should:
- Explain the need to reschedule (if reason provided)
- Propose alternative times or ask for availability
- Apologize for any inconvenience
- Show flexibility and willingness to accommodate
- Match the specified tone

Respond with JSON:
{{
  "subject": "Reschedule request subject line", 
  "body": "Email body with polite reschedule request and alternatives"
}}
        """
        return PromptTemplate(template=template, input_variables=["recipient_name", "tone", "context"])
    
    def _get_apology_template(self) -> PromptTemplate:
        """Template for apology + alternative messages"""
        template = """
You are a professional assistant composing an apology email with alternatives.

Recipient: {recipient_name}
Tone: {tone}
Context: {context}

Generate an apologetic email with subject and body.
The email should:
- Sincerely apologize for scheduling conflicts/issues
- Explain the situation professionally
- Offer concrete alternative solutions
- Show commitment to finding a workable solution
- Match the specified tone

Respond with JSON:
{{
  "subject": "Apology and alternative solutions subject line",
  "body": "Email body with sincere apology and alternative proposals"
}}
        """
        return PromptTemplate(template=template, input_variables=["recipient_name", "tone", "context"])
    
    def _get_counter_proposal_template(self) -> PromptTemplate:
        """Template for counter-proposal messages"""
        template = """
You are a professional assistant composing a counter-proposal email.

Recipient: {recipient_name}
Tone: {tone}
Context: {context}

Generate a diplomatic counter-proposal email with subject and body.
The email should:
- Acknowledge the original proposal
- Explain constraints that necessitate the counter-proposal
- Present alternative options clearly
- Remain positive and solution-focused
- Match the specified tone

Respond with JSON:
{{
  "subject": "Meeting time counter-proposal subject line",
  "body": "Email body with diplomatic counter-proposal and reasoning"
}}
        """
        return PromptTemplate(template=template, input_variables=["recipient_name", "tone", "context"])
    
    def _get_decline_template(self) -> PromptTemplate:
        """Template for meeting decline messages"""
        template = """
You are a professional assistant composing a meeting decline email.

Recipient: {recipient_name}
Tone: {tone}
Context: {context}

Generate a polite decline email with subject and body.
The email should:
- Politely decline the meeting request
- Provide clear but brief reasoning
- Suggest alternatives if possible (different format, delegate, etc.)
- Maintain positive relationship tone
- Match the specified tone

Respond with JSON:
{{
  "subject": "Meeting decline subject line",
  "body": "Email body with polite decline and potential alternatives"
}}
        """
        return PromptTemplate(template=template, input_variables=["recipient_name", "tone", "context"])
    
    def _parse_message_response(self, response_content: str) -> Dict[str, str]:
        """Parse the LLM response and extract subject/body"""
        
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
            parsed = json.loads(response_content)
            return {
                "subject": parsed.get("subject", "Meeting Update"),
                "body": parsed.get("body", response_content)
            }
        except json.JSONDecodeError:
            # Fallback: try to extract subject and body manually
            lines = response_content.split('\n')
            subject = "Meeting Update"
            body = response_content
            
            for line in lines:
                if line.lower().startswith('subject:'):
                    subject = line.split(':', 1)[1].strip()
                    break
            
            return {
                "subject": subject,
                "body": body
            }
    
    def generate_negotiation_summary(self, 
                                   negotiation_history: List[Dict],
                                   final_outcome: Dict,
                                   participants: List[str]) -> Dict[str, str]:
        """
        Generate a summary email of the entire negotiation process.
        Useful for keeping all parties informed of the final decision.
        """
        
        context = {
            "negotiation_rounds": len(negotiation_history),
            "participants": participants,
            "final_outcome": final_outcome,
            "key_interactions": negotiation_history[-3:] if len(negotiation_history) > 3 else negotiation_history
        }
        
        template = """
You are composing a negotiation summary email for meeting scheduling.

Context: {context}

Generate a professional summary email that:
- Summarizes the negotiation process briefly
- Announces the final meeting time/decision
- Thanks participants for their flexibility
- Includes clear next steps or calendar details
- Maintains a positive, collaborative tone

Respond with JSON:
{{
  "subject": "Meeting scheduling summary and confirmation",
  "body": "Professional summary of negotiation outcome and next steps"
}}
        """
        
        prompt = PromptTemplate(template=template, input_variables=["context"])
        formatted_prompt = prompt.format(context=json.dumps(context, indent=2))
        
        response = self.llm.invoke(formatted_prompt)
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        return self._parse_message_response(response_content)


def demo_message_generation():
    """
    Demonstrate the message generation capabilities
    """
    print("PHASE 6: Polite Message Generation Demo")
    print("=" * 50)
    
    # Initialize generator
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found in environment variables")
        return
    
    generator = EmailGenerator(api_key)
    
    # Test different message types
    test_scenarios = [
        {
            "type": "confirmation",
            "context": {
                "meeting_title": "Product Strategy Review",
                "final_time": "2026-01-17T14:00:00Z",
                "duration_minutes": 90,
                "participants": ["Alice", "Bob", "Charlie"],
                "negotiation_rounds": 2
            },
            "recipient": "Alice",
            "tone": "professional"
        },
        {
            "type": "apology",
            "context": {
                "meeting_title": "Team Standup",
                "original_time": "2026-01-16T22:00:00Z",
                "issue": "timezone_conflict",
                "affected_participant": "Alice",
                "alternative_times": ["2026-01-17T09:00:00Z", "2026-01-17T15:00:00Z"]
            },
            "recipient": "Team",
            "tone": "friendly"
        },
        {
            "type": "counter_proposal",
            "context": {
                "meeting_title": "Client Presentation",
                "proposed_time": "2026-01-16T08:00:00Z",
                "constraint": "outside_working_hours",
                "counter_times": ["2026-01-16T10:00:00Z", "2026-01-16T14:00:00Z"],
                "reasoning": "Original time conflicts with team working hours"
            },
            "recipient": "Project Manager",
            "tone": "professional"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. Testing {scenario['type'].upper()} message:")
        print("-" * 30)
        
        try:
            message = generator.generate_message(
                message_type=scenario["type"],
                context=scenario["context"],
                recipient_name=scenario["recipient"],
                tone=scenario["tone"]
            )
            
            print(f"Subject: {message['subject']}")
            print(f"Body Preview: {message['body'][:200]}...")
            print("Message generated successfully!")
            
        except Exception as e:
            print(f"Error generating {scenario['type']} message: {e}")
    
    print(f"\nPhase 6 Message Generation system implemented successfully!")
    return generator