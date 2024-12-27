import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from models import PTExercisePlanner
from utils import save_patients, create_weekly_schedule
import pandas as pd
from typing import Dict
from datetime import datetime

def display_patient_management_page(patients):
    st.header("Patient Management")

    # Select existing patient or create new
    patient_list = list(patients.keys())
    patient_list.insert(0, "Add New Patient")
    selected_patient = st.selectbox("Select Patient", patient_list)

    if selected_patient == "Add New Patient":
        # Form for adding a new patient
        with st.form("new_patient_form"):
            patient_name = st.text_input("Patient Name")
            age = st.number_input("Age", min_value=0, max_value=120)
            injury_location = st.text_input("Injury Location")
            pain_level = st.slider("Pain Level", 0, 10, 5)
            mobility_status = st.text_input("Mobility Status")
            medical_history = st.text_area("Medical History")
            activity_level = st.selectbox(
                "Activity Level",
                ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
            )
            goals = st.text_area("Treatment Goals")
            submit_new_patient = st.form_submit_button("Add Patient")

            if submit_new_patient:
                patients[patient_name] = {
                    "age": age,
                    "injury_location": injury_location,
                    "pain_level": pain_level,
                    "mobility_status": mobility_status,
                    "medical_history": medical_history,
                    "activity_level": activity_level,
                    "goals": goals,
                    "weekly_schedule": create_weekly_schedule()
                }
                save_patients(patients)
                st.success(f"Patient {patient_name} added successfully!")
                st.rerun()
    else:
        # Display and edit selected patient's information
        patient_data = patients[selected_patient]
        st.subheader(f"Edit Patient: {selected_patient}")
        with st.form("edit_patient_form"):
            new_patient_name = st.text_input("Patient Name", selected_patient)
            age = st.number_input("Age", min_value=0, max_value=120, value=patient_data["age"])
            injury_location = st.text_input("Injury Location", patient_data["injury_location"])
            pain_level = st.slider("Pain Level", 0, 10, value=patient_data["pain_level"])
            mobility_status = st.text_input("Mobility Status", patient_data["mobility_status"])
            medical_history = st.text_area("Medical History", patient_data["medical_history"])
            activity_level = st.selectbox(
                "Activity Level",
                ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                index=["Sedentary", "Light", "Moderate", "Active", "Very Active"].index(patient_data["activity_level"])
            )
            goals = st.text_area("Treatment Goals", patient_data["goals"])
            submit_changes = st.form_submit_button("Save Changes")

            if submit_changes:
                # Update patient data
                if new_patient_name != selected_patient:
                    del patients[selected_patient]
                patients[new_patient_name] = {
                    "age": age,
                    "injury_location": injury_location,
                    "pain_level": pain_level,
                    "mobility_status": mobility_status,
                    "medical_history": medical_history,
                    "activity_level": activity_level,
                    "goals": goals,
                    "weekly_schedule": patient_data["weekly_schedule"]
                }
                save_patients(patients)
                st.success(f"Patient {new_patient_name} updated successfully!")
                st.rerun()

def display_treatment_plan_page(patients):
    st.header("Patient Treatment Plan")

    # Select patient
    patient_list = list(patients.keys())
    if not patient_list:
        st.warning("Please add a patient first.")
        return

    selected_patient = st.selectbox("Select Patient", patient_list)
    patient_data = patients[selected_patient]

    # Generate or use existing schedule
    if "weekly_schedule" not in patient_data:
        patient_data["weekly_schedule"] = create_weekly_schedule()

    # Number of exercises to generate
    num_exercises = st.number_input("Number of Exercises to Generate", min_value=1, max_value=10, value=4)

    # Button to generate exercise plan
    if st.button("Generate Exercise Plan"):
        planner = PTExercisePlanner()
        with st.spinner("Generating exercise recommendations..."):
            recommendations = planner.generate_exercises(patient_data, num_exercises)
            if recommendations:
                patient_data["recommendations"] = recommendations  # Store in patient_data
                save_patients(patients)  # Save updated patient data
                st.session_state.recommendations = recommendations
                st.success("Exercise recommendations generated!")

    # Display generated exercises (only if they exist for the patient)
    if "recommendations" in patient_data:
        st.subheader("Generated Exercises")
        for exercise in patient_data["recommendations"]["exercises"]:
            with st.expander(exercise["name"]):
                st.write(f"**Description:** {exercise['description']}")
                st.write(f"**Parameters:** {exercise['parameters']}")
                st.write(f"**Progression Criteria:** {exercise['progressionCriteria']}")
                st.write(f"**Rationale:** {exercise['rationale']}")

                # Add exercise to the selected day of the weekly schedule
                selected_day = st.selectbox("Select Day", list(patient_data["weekly_schedule"].keys()), key=f"day_{exercise['id']}")
                if st.button(f"Add to {selected_day}", key=f"add_{exercise['id']}"):
                    patient_data["weekly_schedule"][selected_day].append(exercise)
                    save_patients(patients)
                    st.success(f"Added {exercise['name']} to {selected_day}")

    # Display the weekly schedule using a table
    st.subheader(f"{selected_patient}'s Weekly Schedule")
    display_weekly_schedule_table(patient_data["weekly_schedule"], patients, selected_patient)

    # Export treatment plan
    if st.button("Export Treatment Plan"):
        export_plan(patient_data, patient_data["weekly_schedule"])

def display_pt_schedule_page(patients):
    from utils import generate_pt_weekly_schedule

    st.header("PT Weekly Schedule")
    pt_weekly_schedule = generate_pt_weekly_schedule(patients)
    display_weekly_schedule_table(pt_weekly_schedule, patients)

def display_weekly_schedule_table(schedule_data, patients, selected_patient=None):
    """Displays the weekly schedule using Ag-Grid."""

    # If a patient is selected, show their schedule, otherwise show the PT's overall schedule
    if selected_patient:
        data = []
        for day, exercises in schedule_data.items():
            for exercise in exercises:
                data.append({"Day": day, "Exercise": exercise["name"], "Details": exercise["parameters"]})
        df = pd.DataFrame(data)
    else:
        data = []
        for day, entries in schedule_data.items():
            for entry in entries:
                data.append({"Day": day, "Appointment": entry})
        df = pd.DataFrame(data)

    if not df.empty:
        # Ensure 'Day' column exists and has the correct order
        if 'Day' not in df.columns:
            df['Day'] = ""

        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        df['Day'] = pd.Categorical(df['Day'], categories=days_order, ordered=True)
        df = df.sort_values('Day')

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, autoHeight=True, wrapText=True)
        gb.configure_grid_options(domLayout='normal')

        # Make cells editable if it's a patient's schedule
        if selected_patient:
            gb.configure_selection("multiple", use_checkbox=False)
            gb.configure_column("Day", editable=False, cellEditor='agSelectCellEditor', cellEditorParams={'values': days_order})
            gb.configure_column("Exercise", editable=True)
            gb.configure_column("Details", editable=True)

        gridOptions = gb.build()

        grid_response = AgGrid(
            df,
            gridOptions=gridOptions,
            data_return_mode=DataReturnMode.AS_INPUT,
            update_mode=GridUpdateMode.MODEL_CHANGED if selected_patient else GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=False,
            height=350,
            width='100%',
            reload_data=False
        )

        # Handle data updates if it's a patient's schedule
        if selected_patient:
            updated_df = pd.DataFrame(grid_response['data'])
            if not updated_df.equals(df):
                updated_schedule = create_weekly_schedule()
                for index, row in updated_df.iterrows():
                    # Find the exercise in recommendations based on its name
                    exercise_details = next((ex for ex in st.session_state.recommendations["exercises"] if ex["name"] == row["Exercise"]), None)

                    if exercise_details:
                        updated_schedule[row["Day"]].append(exercise_details)

                # Update the patient's weekly schedule and save
                if selected_patient in patients:
                    patients[selected_patient]["weekly_schedule"] = updated_schedule
                    save_patients(patients)
                    st.success("Patient's weekly schedule updated!")

def export_plan(patient_data: Dict, weekly_schedule: Dict):
    """Export the treatment plan as a formatted document"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"treatment_plan_{timestamp}.txt"

    content = []
    content.append("PHYSICAL THERAPY TREATMENT PLAN")
    content.append("=" * 30 + "\n")
    content.append("PATIENT INFORMATION")
    content.append("-" * 20)
    content.append(f"Name: {patient_data.get('name', 'N/A')}")
    content.append(f"Age: {patient_data.get('age', 'N/A')}")
    content.append(f"Injury Location: {patient_data.get('injury_location', 'N/A')}")
    content.append(f"Pain Level: {patient_data.get('pain_level', 'N/A')}/10")
    content.append(f"Activity Level: {patient_data.get('activity_level', 'N/A')}")
    content.append(f"\nTreatment Goals:")
    content.append(f"{patient_data.get('goals', 'N/A')}\n")
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

    export_content = "\n".join(content)

    # Using pandas to create a DataFrame (optional for formatting)
    df = pd.DataFrame({
        'Patient Information': [
            f"Name: {patient_data.get('name', 'N/A')}",
            f"Age: {patient_data.get('age', 'N/A')}",
            f"Injury Location: {patient_data.get('injury_location', 'N/A')}",
            f"Pain Level: {patient_data.get('pain_level', 'N/A')}/10",
            f"Activity Level: {patient_data.get('activity_level', 'N/A')}",
            f"Treatment Goals: {patient_data.get('goals', 'N/A')}"
        ],
        'Weekly Exercise Schedule': [""]  # Placeholder for schedule
    })

    # Create a formatted string for the schedule
    schedule_str = ""
    for day, exercises in weekly_schedule.items():
        schedule_str += f"\n{day}:\n"
        if not exercises:
            schedule_str += "Rest day / No exercises scheduled\n"
        else:
            for exercise in exercises:
                schedule_str += f"  • {exercise['name']}\n"
                schedule_str += f"    Parameters: {exercise['parameters']}\n"
                schedule_str += f"    Description: {exercise['description']}\n"
                schedule_str += f"    Progression Criteria: {exercise['progressionCriteria']}\n"

    # Concatenate patient info and schedule
    export_content = df.to_string(index=False) + "\n" + schedule_str

    # Create download button in Streamlit
    st.download_button(
        label="Download Treatment Plan",
        data=export_content,
        file_name=filename,
        mime="text/plain"
    )

    with st.expander("Preview Treatment Plan"):
        st.text(export_content)