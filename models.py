import anthropic
import json
from typing import Dict, List

class PTExercisePlanner:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key="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"
        )

    def generate_exercises(self, patient_data: Dict, num_exercises: int) -> Dict:
        """Generate exercise recommendations based on patient data."""
        try:
            message = self.client.beta.prompt_caching.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0,
                system=[
                    {
                        "type": "text",
                        "text": f"""You are an expert physical therapy assistant specialized in creating evidence-based exercise recommendations. Your role is to analyze patient data and suggest appropriate exercises based on their condition. Your recommendations must be formatted as structured data for easy integration into a PT planning system.

Each exercise recommendation must be evidence-based and include:
1. Clear name and brief description
2. Specific parameters (sets/reps/frequency)
3. Clear progression criteria
4. Scientific rationale

Generate exactly {num_exercises} exercises.

Format all responses as a JSON object. Be precise and concise, avoiding unnecessary explanations or disclaimers.""",
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
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

            # Handle possible list response
            if isinstance(message.content, list):
                content = message.content[0].text
            else:
                content = message.content

            return json.loads(content)

        except Exception as e:
            print(f"Error generating exercises: {str(e)}")
            return None