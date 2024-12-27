# main.py
import streamlit as st
from ui import display_patient_management_page, display_treatment_plan_page, display_pt_schedule_page
from utils import load_patients, save_patients, generate_pt_weekly_schedule

def main():
    st.title("PT Exercise Planner")

    # Load patient data (consider doing this once at the start)
    patients = load_patients()

    # Sidebar navigation
    page = st.sidebar.selectbox("Select Page", ["Patient Management", "Patient Treatment Plan", "PT Weekly Schedule"])

    # Display the selected page
    if page == "Patient Management":
        display_patient_management_page(patients)
    elif page == "Patient Treatment Plan":
        display_treatment_plan_page(patients)
    elif page == "PT Weekly Schedule":
        display_pt_schedule_page(patients)

if __name__ == "__main__":
    main()