# models.py
from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    name: str
    age: int
    injury_location: str
    pain_level: int
    mobility_status: str
    medical_history: str
    activity_level: str
    goals: str

class PatientUpdate(BaseModel):
    new_name: Optional[str] = None
    age: Optional[int] = None
    injury_location: Optional[str] = None
    pain_level: Optional[int] = None
    mobility_status: Optional[str] = None
    medical_history: Optional[str] = None
    activity_level: Optional[str] = None
    goals: Optional[str] = None

class ExerciseRecommendationsRequest(BaseModel):
    patient_name: str
    num_exercises: int
