import streamlit as st
import anthropic
import json
from typing import Dict, List
import os
from datetime import datetime, timedelta
import pandas as pd

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
            st.error(f"Error generating exercises: {str(e)}")
            return None

def create_weekly_schedule():
    """Create a weekly schedule template"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return {day: [] for day in days}

def main():
    st.title("PT Exercise Planner")
    
    # Initialize session state
    if 'selected_exercises' not in st.session_state:
        st.session_state.selected_exercises = []
    if 'current_recommendations' not in st.session_state:
        st.session_state.current_recommendations = None
    if 'weekly_schedule' not in st.session_state:
        st.session_state.weekly_schedule = create_weekly_schedule()
    if 'patient_data' not in st.session_state:
        st.session_state.patient_data = {}
        
    # Patient Information Form
    st.header("Patient Information")
    with st.form("pt_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120)
            injury_location = st.text_input("Injury Location")
            pain_level = st.slider("Pain Level", 0, 10, 5)
            mobility_status = st.text_input("Mobility Status")
            num_exercises = st.number_input("Number of Exercises to Generate", min_value=1, max_value=10, value=4)
            
        with col2:
            medical_history = st.text_area("Medical History")
            activity_level = st.selectbox(
                "Activity Level",
                ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
            )
            goals = st.text_area("Treatment Goals")
            patient_name = st.text_input("Patient Name")
            
        submitted = st.form_submit_button("Generate Exercise Plan")
        
        if submitted:
            # Store patient data in session state
            st.session_state.patient_data = {
                "name": patient_name,
                "age": age,
                "injury_location": injury_location,
                "pain_level": pain_level,
                "mobility_status": mobility_status,
                "medical_history": medical_history,
                "activity_level": activity_level,
                "goals": goals
            }
            
            planner = PTExercisePlanner()
            with st.spinner("Generating exercise recommendations..."):
                recommendations = planner.generate_exercises(st.session_state.patient_data, num_exercises)
                if recommendations:
                    st.session_state.current_recommendations = recommendations
                    st.rerun()
                
    # Display Exercise Recommendations and Weekly Planner
    if st.session_state.current_recommendations:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.header("Exercise Library")
            recommendations = st.session_state.current_recommendations
            
            # Display notes
            st.info(recommendations["notes"])
            
            # Exercise Selection
            for exercise in recommendations["exercises"]:
                with st.expander(f"{exercise['name']}"):
                    st.write(f"**Description:** {exercise['description']}")
                    st.write(f"**Parameters:** {exercise['parameters']}")
                    st.write(f"**Progression Criteria:** {exercise['progressionCriteria']}")
                    st.write(f"**Rationale:** {exercise['rationale']}")
                    
                    # Add to schedule button
                    cols = st.columns(2)
                    with cols[0]:
                        day = st.selectbox(f"Day for {exercise['name']}", 
                                         ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                                         key=f"day_{exercise['id']}")
                    with cols[1]:
                        if st.button("Add to Schedule", key=f"add_{exercise['id']}"):
                            if exercise not in st.session_state.weekly_schedule[day]:
                                st.session_state.weekly_schedule[day].append(exercise)
                                st.success(f"Added {exercise['name']} to {day}")
        
        with col2:
            st.header("Weekly Schedule")
            
            # Display and edit weekly schedule
            for day, exercises in st.session_state.weekly_schedule.items():
                with st.expander(day, expanded=True):
                    if not exercises:
                        st.write("No exercises scheduled")
                    else:
                        for idx, exercise in enumerate(exercises):
                            st.write(f"**{exercise['name']}**")
                            st.write(f"Parameters: {exercise['parameters']}")
                            if st.button("Remove", key=f"remove_{day}_{idx}"):
                                st.session_state.weekly_schedule[day].remove(exercise)
                                st.rerun()
            
            # Export functionality
            if st.button("Export Treatment Plan"):
                export_plan(st.session_state.patient_data, st.session_state.weekly_schedule)

def export_plan(patient_data: Dict, weekly_schedule: Dict):
    """Export the treatment plan as a formatted document"""
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"treatment_plan_{timestamp}.txt"
    
    # Generate the content
    content = []
    content.append("PHYSICAL THERAPY TREATMENT PLAN")
    content.append("=" * 30 + "\n")
    
    # Patient Information
    content.append("PATIENT INFORMATION")
    content.append("-" * 20)
    content.append(f"Name: {patient_data.get('name', 'N/A')}")
    content.append(f"Age: {patient_data.get('age', 'N/A')}")
    content.append(f"Injury Location: {patient_data.get('injury_location', 'N/A')}")
    content.append(f"Pain Level: {patient_data.get('pain_level', 'N/A')}/10")
    content.append(f"Activity Level: {patient_data.get('activity_level', 'N/A')}")
    content.append(f"\nTreatment Goals:")
    content.append(f"{patient_data.get('goals', 'N/A')}\n")
    
    # Weekly Schedule
    content.append("WEEKLY EXERCISE SCHEDULE")
    content.append("-" * 20)
    for day, exercises in weekly_schedule.items():
        content.append(f"\n{day}:")
        if not exercises:
            content.append("Rest day / No exercises scheduled")
        else:
            for exercise in exercises:
                content.append(f"\n  • {exercise['name']}")
                content.append(f"    Parameters: {exercise['parameters']}")
                content.append(f"    Description: {exercise['description']}")
                content.append(f"    Progression Criteria: {exercise['progressionCriteria']}")
    
    # Create the export
    export_content = "\n".join(content)
    
    # Create download button
    st.download_button(
        label="Download Treatment Plan",
        data=export_content,
        file_name=filename,
        mime="text/plain"
    )
    
    # Also display in the app
    with st.expander("Preview Treatment Plan"):
        st.text(export_content)

if __name__ == "__main__":
    main()