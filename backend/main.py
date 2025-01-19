# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from OldStreamlit.models import PatientCreate, PatientUpdate, ExerciseRecommendationsRequest
from OldStreamlit.utils import load_patients, save_patients, create_weekly_schedule
from services import generate_exercises

app = FastAPI(title="PT Exercise Planner API")

# In-memory (or JSON file) data structure for patients
patients_db = load_patients()

@app.get("/patients", response_model=List[str])
def list_patients():
    """
    Returns a list of patient names (keys).
    """
    return list(patients_db.keys())


@app.get("/patients/{patient_name}")
def get_patient(patient_name: str):
    """
    Returns the patient's data.
    """
    if patient_name not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients_db[patient_name]


@app.post("/patients", status_code=201)
def create_patient(payload: PatientCreate):
    """
    Creates a new patient entry.
    """
    if payload.name in patients_db:
        raise HTTPException(status_code=400, detail="Patient already exists")

    new_data = {
        "age": payload.age,
        "injury_location": payload.injury_location,
        "pain_level": payload.pain_level,
        "mobility_status": payload.mobility_status,
        "medical_history": payload.medical_history,
        "activity_level": payload.activity_level,
        "goals": payload.goals,
        "weekly_schedule": create_weekly_schedule(),
        "recommendations": {}
    }
    patients_db[payload.name] = new_data
    save_patients(patients_db)
    return {"message": f"Patient '{payload.name}' created successfully"}


@app.put("/patients/{patient_name}")
def update_patient(patient_name: str, payload: PatientUpdate):
    """
    Updates an existing patient’s data.
    """
    if patient_name not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_data = patients_db[patient_name]

    # Update fields if provided
    if payload.new_name:
        # handle renaming logic
        if payload.new_name != patient_name and payload.new_name in patients_db:
            raise HTTPException(status_code=400, detail="New name conflicts with existing patient name")
        # move data in the dictionary
        patients_db[payload.new_name] = existing_data
        del patients_db[patient_name]
        patient_name = payload.new_name

    if payload.age is not None:
        patients_db[patient_name]["age"] = payload.age
    if payload.injury_location is not None:
        patients_db[patient_name]["injury_location"] = payload.injury_location
    if payload.pain_level is not None:
        patients_db[patient_name]["pain_level"] = payload.pain_level
    if payload.mobility_status is not None:
        patients_db[patient_name]["mobility_status"] = payload.mobility_status
    if payload.medical_history is not None:
        patients_db[patient_name]["medical_history"] = payload.medical_history
    if payload.activity_level is not None:
        patients_db[patient_name]["activity_level"] = payload.activity_level
    if payload.goals is not None:
        patients_db[patient_name]["goals"] = payload.goals

    save_patients(patients_db)
    return {"message": f"Patient '{patient_name}' updated successfully"}


@app.delete("/patients/{patient_name}")
def delete_patient(patient_name: str):
    """
    Deletes a patient entry.
    """
    if patient_name not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    del patients_db[patient_name]
    save_patients(patients_db)
    return {"message": f"Patient '{patient_name}' has been deleted."}


@app.post("/generate_exercises")
def generate_patient_exercises(request: ExerciseRecommendationsRequest):
    """
    Calls the Anthropic-based exercise generation using a patient's data.
    """
    patient_name = request.patient_name
    num_exercises = request.num_exercises

    if patient_name not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_data = patients_db[patient_name]
    recommendations = generate_exercises(patient_data, num_exercises)
    if not recommendations:
        raise HTTPException(status_code=500, detail="Failed to generate exercises")

    patients_db[patient_name]["recommendations"] = recommendations
    save_patients(patients_db)
    return recommendations


@app.get("/weekly_schedule/{patient_name}")
def get_weekly_schedule(patient_name: str):
    """
    Returns the weekly schedule for a given patient.
    """
    if patient_name not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients_db[patient_name]["weekly_schedule"]


@app.post("/weekly_schedule/{patient_name}/{day}")
def add_exercise_to_day(patient_name: str, day: str, exercise: Dict):
    """
    Add an exercise to a particular day of the patient's weekly schedule.
    """
    if patient_name not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    if day not in patients_db[patient_name]["weekly_schedule"]:
        raise HTTPException(status_code=400, detail="Invalid day provided")

    patients_db[patient_name]["weekly_schedule"][day].append(exercise)
    save_patients(patients_db)
    return {"message": f"Exercise added to {day} for {patient_name}"}


@app.get("/pt_schedule")
def get_overall_pt_schedule():
    """
    Returns the PT's overall schedule (combines all patients).
    """
    from OldStreamlit.utils import generate_pt_weekly_schedule
    schedule = generate_pt_weekly_schedule(patients_db)
    return schedule


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
