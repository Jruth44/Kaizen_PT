# main.py
import streamlit as st
from OldStreamlit.ui import display_patient_management_page, display_treatment_plan_page, display_pt_schedule_page
from OldStreamlit.utils import load_patients, save_patients

def main():
    st.title("PT Exercise Planner")

    # Load patient data 
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