from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json
import os

def run_scheduler_agent(input_payload: dict, prompt_text: str):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    prompt = PromptTemplate(
        template=prompt_text + "\n\nINPUT:\n{input}\nOUTPUT:",
        input_variables=["input"]
    )

    response = llm.invoke(
        prompt.format(input=json.dumps(input_payload, indent=2))
    )

    # Extract content from the response
    response_content = response.content if hasattr(response, 'content') else str(response)
    
    # Handle JSON wrapped in markdown code blocks
    if "```json" in response_content:
        # Extract JSON from markdown code block
        start_idx = response_content.find("```json") + 7
        end_idx = response_content.find("```", start_idx)
        if end_idx != -1:
            response_content = response_content[start_idx:end_idx].strip()
    elif "```" in response_content:
        # Handle generic code blocks
        start_idx = response_content.find("```") + 3
        end_idx = response_content.find("```", start_idx)
        if end_idx != -1:
            response_content = response_content[start_idx:end_idx].strip()
    
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        # If JSON parsing fails, return the raw response
        return {"response": response_content, "error": "Failed to parse JSON response"}
