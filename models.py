import os
import json
import anthropic
import streamlit as st
from typing import Dict, List

class PTExercisePlanner:
    def __init__(self):
        """
        1. Try to get ANTHROPIC_API_KEY from environment.
        2. If not found, look in st.secrets.
        3. If still missing, raise an error.
        4. Otherwise, create the Anthropic client (new usage).
        """
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not anthropic_api_key:
            try:
                if "ANTHROPIC_API_KEY" in st.secrets:
                    anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
                    os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
            except FileNotFoundError:
                # Means there's literally no .streamlit/secrets.toml locally
                pass

        if not anthropic_api_key:
            # Stop here so we don't try to call self.client
            raise RuntimeError(
                "No Anthropic API key found! Please set an environment variable "
                "or create a .streamlit/secrets.toml or set Streamlit Cloud secrets."
            )

        # Use the new anthropic.Client approach (no .beta.prompt_caching)
        self.client = anthropic.Client(api_key=anthropic_api_key)

    def generate_exercises(self, patient_data: Dict, num_exercises: int) -> Dict:
        """Generate exercise recommendations based on patient data using Claude."""
        try:
            st.write("DEBUG: Calling Anthropic API (completions.create)...")

            # Build your "system" instructions and your "user" message
            system_text = f"""
You are an expert physical therapy assistant specialized in creating evidence-based exercise recommendations. 
Your role is to analyze patient data and suggest appropriate exercises based on their condition. 
Your recommendations must be formatted as structured data for easy integration into a PT planning system.
These are not formal medical advice but purely educational.

Each exercise recommendation must be evidence-based and include:
1. Clear name and brief description
2. Specific parameters (sets/reps/frequency)
3. Clear progression criteria
4. Scientific rationale

Generate exactly {num_exercises} exercises.

Format all responses as a JSON object. 
Be precise and concise, avoiding unnecessary explanations or disclaimers.
"""

            user_text = f"""
Generate a set of targeted exercises for this patient:

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
}}
"""

            # Anthropics requires constructing the prompt with HUMAN_PROMPT + AI_PROMPT
            # We'll put system instructions + user message together as the "human" section.
            prompt = (
                f"{anthropic.HUMAN_PROMPT} {system_text}\n\n{user_text}"
                f"{anthropic.AI_PROMPT}"
            )

            # Make the API call
            response = self.client.completions.create(
                model="claude-2",              # or another Claude model you have access to
                prompt=prompt,
                max_tokens_to_sample=1000,
                temperature=0
            )

            # The textual completion
            content = response.completion  
            st.write("DEBUG: Raw content returned from the API call:")
            st.write(content)

            # Attempt to parse the JSON
            parsed = json.loads(content)
            st.write("DEBUG: Successfully parsed JSON:")
            st.write(parsed)
            return parsed

        except Exception as e:
            st.error("An error occurred while generating exercises.")
            st.exception(e)
            return None
