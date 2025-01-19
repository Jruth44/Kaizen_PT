# services.py
import json
import os
import anthropic
from typing import Dict

def generate_exercises(patient_data: Dict, num_exercises: int) -> Dict:
    """
    Calls Anthropic’s API to generate exercise recommendations 
    based on patient data.
    """
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return {}

    client = anthropic.Anthropic(api_key=anthropic_api_key)
    try:
        message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10000,
            system=f"""You are an expert physical therapy assistant specialized in creating evidence-based exercise recommendations. Your role is to analyze patient data and suggest appropriate exercises based on their condition. Your recommendations must be formatted as structured data for easy integration into a PT planning system.

Each exercise recommendation must be evidence-based and include:
1. Clear name and brief description
2. Specific parameters (sets/reps/frequency)
3. Clear progression criteria
4. Scientific rationale

Generate exactly {num_exercises} exercises.

Format all responses as a JSON object. Be precise and concise, avoiding unnecessary explanations or disclaimers.""",
            messages=[
                {
                    "role": "user",
                    "content": f"""Generate a set of targeted exercises for this patient:
<patient_data>
Age: {patient_data['age']}
Injury Location: {patient_data['injury_location']}
Pain Level: {patient_data['pain_level']}/10
Mobility Status: {patient_data['mobility_status']}
Medical History: {patient_data['medical_history']}
Activity Level: {patient_data['activity_level']}
Goals: {patient_data['goals']}
</patient_data>

Provide output in this exact JSON structure:
{{
  "exercises": [
    {{
      "id": "string",
      "name": "string",
      "description": "string",
      "parameters": "string",
      "progressionCriteria": "string",
      "rationale": "string"
    }}
  ],
  "notes": "string"
}}"""
                }
            ]
        )

        if isinstance(message.content, list):
            content = message.content[0].text
        else:
            content = message.content

        parsed = json.loads(content)
        return parsed

    except Exception as e:
        print(f"Anthropic API error: {e}")
        return {}