import json
from datetime import datetime
import pandas as pd
from typing import Dict

def create_weekly_schedule():
    """Create a weekly schedule template"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return {day: [] for day in days}

def load_patients():
    """Loads patient data from a JSON file, or initializes an empty dictionary."""
    try:
        with open("patients.json", "r") as f:
            patients = json.load(f)
    except FileNotFoundError:
        patients = {}
    return patients

def save_patients(patients):
    """Saves patient data to a JSON file."""
    with open("patients.json", "w") as f:
        json.dump(patients, f, indent=4)

def generate_pt_weekly_schedule(patients):
    """Generates the overall weekly schedule for the PT."""
    pt_schedule = create_weekly_schedule()
    for patient_name, patient_data in patients.items():
        for day, exercises in patient_data["weekly_schedule"].items():
            for exercise in exercises:
                pt_schedule[day].append(f"{patient_name}: {exercise['name']}")
    return pt_schedule