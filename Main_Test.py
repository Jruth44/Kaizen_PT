import streamlit as st
import anthropic
import json
from typing import Dict, List
import os

class PTExercisePlanner:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key="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"
        )
        
    def generate_exercises(self, patient_data: Dict) -> Dict:
        """Generate exercise recommendations based on patient data."""
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            system="You are an expert physical therapy assistant specialized in creating evidence-based exercise recommendations. Your role is to analyze patient data and suggest appropriate exercises based on their condition. Your recommendations must be formatted as structured data for easy integration into a PT planning system.\n\nEach exercise recommendation must be evidence-based and include:\n1. Clear name and brief description\n2. Specific parameters (sets/reps/frequency)\n3. Clear progression criteria\n4. Scientific rationale\n\nFormat all responses as a JSON object. Be precise and concise, avoiding unnecessary explanations or disclaimers.",
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
            
            # Debug: Print raw message content
            st.write("Debug - Raw message content:", message.content)
            
            # Handle possible list response
            if isinstance(message.content, list):
                content = message.content[0].text
            else:
                content = message.content
                
            # Debug: Print processed content
            st.write("Debug - Processed content:", content)
            
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                st.error(f"JSON parsing error: {str(e)}")
                st.write("Content that failed to parse:", content)
                return None
                
        except Exception as e:
            st.error(f"Error generating exercises: {str(e)}")
            st.write("Full error:", str(e))
            return None

def main():
    st.title("PT Exercise Planner")
    
    # Initialize session state for selected exercises
    if 'selected_exercises' not in st.session_state:
        st.session_state.selected_exercises = []
    if 'current_recommendations' not in st.session_state:
        st.session_state.current_recommendations = None
        
    # Patient Information Form
    st.header("Patient Information")
    with st.form("patient_info"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120)
            injury_location = st.text_input("Injury Location")
            pain_level = st.slider("Pain Level", 0, 10, 5)
            mobility_status = st.text_input("Mobility Status")
            
        with col2:
            medical_history = st.text_area("Medical History")
            activity_level = st.selectbox(
                "Activity Level",
                ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
            )
            goals = st.text_area("Treatment Goals")
            
        submitted = st.form_submit_button("Generate Exercise Plan")
        
        if submitted:
            planner = PTExercisePlanner()
            patient_data = {
                "age": age,
                "injury_location": injury_location,
                "pain_level": pain_level,
                "mobility_status": mobility_status,
                "medical_history": medical_history,
                "activity_level": activity_level,
                "goals": goals
            }
            
            with st.spinner("Generating exercise recommendations..."):
                recommendations = planner.generate_exercises(patient_data)
                if recommendations:
                    st.session_state.current_recommendations = recommendations
                
    # Display Exercise Recommendations
    if st.session_state.current_recommendations:
        st.header("Recommended Exercises")
        recommendations = st.session_state.current_recommendations
        
        # Display notes
        st.info(recommendations["notes"])
        
        # Exercise Selection
        st.subheader("Select Exercises for Plan")
        for exercise in recommendations["exercises"]:
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                selected = st.checkbox(
                    "", 
                    key=f"select_{exercise['id']}",
                    value=exercise['id'] in [ex['id'] for ex in st.session_state.selected_exercises]
                )
            with col2:
                with st.expander(f"{exercise['name']}"):
                    st.write(f"**Description:** {exercise['description']}")
                    st.write(f"**Parameters:** {exercise['parameters']}")
                    st.write(f"**Progression Criteria:** {exercise['progressionCriteria']}")
                    st.write(f"**Rationale:** {exercise['rationale']}")
            
            if selected and exercise['id'] not in [ex['id'] for ex in st.session_state.selected_exercises]:
                st.session_state.selected_exercises.append(exercise)
            elif not selected and exercise['id'] in [ex['id'] for ex in st.session_state.selected_exercises]:
                st.session_state.selected_exercises = [ex for ex in st.session_state.selected_exercises if ex['id'] != exercise['id']]
        
        # Display Selected Exercises
        if st.session_state.selected_exercises:
            st.header("Selected Exercises")
            for exercise in st.session_state.selected_exercises:
                st.markdown(f"""
                ### {exercise['name']}
                - **Description:** {exercise['description']}
                - **Parameters:** {exercise['parameters']}
                - **Progression Criteria:** {exercise['progressionCriteria']}
                """)
                
            # Add buttons for plan actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Generate New Exercises"):
                    st.session_state.current_recommendations = None
                    st.session_state.selected_exercises = []
                    st.rerun()
            with col2:
                if st.button("Clear Selection"):
                    st.session_state.selected_exercises = []
                    st.rerun()
            with col3:
                if st.button("Export Plan"):
                    # In a real application, you would implement export functionality here
                    st.info("Export functionality would go here")

if __name__ == "__main__":
    main()