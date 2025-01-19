import axios from "axios";

// Adjust this if your backend is on a different URL/port
const API_BASE = "http://localhost:8000";

export async function listPatients() {
  const res = await axios.get(`${API_BASE}/patients`);
  return res.data; // array of patient names
}

export async function getPatient(name) {
  const res = await axios.get(`${API_BASE}/patients/${name}`);
  return res.data; // patient details
}

export async function createPatient(data) {
  // data includes { name, age, injury_location, ... }
  const res = await axios.post(`${API_BASE}/patients`, data);
  return res.data;
}

export async function updatePatient(patientName, data) {
  // data is partial update
  const res = await axios.put(`${API_BASE}/patients/${patientName}`, data);
  return res.data;
}

export async function deletePatient(name) {
  const res = await axios.delete(`${API_BASE}/patients/${name}`);
  return res.data;
}

export async function generateExercises(patientName, numExercises) {
  const res = await axios.post(`${API_BASE}/generate_exercises`, {
    patient_name: patientName,
    num_exercises: numExercises,
  });
  return res.data; // the recommendations JSON
}

export async function getWeeklySchedule(patientName) {
  const res = await axios.get(`${API_BASE}/weekly_schedule/${patientName}`);
  return res.data;
}

export async function addExerciseToDay(patientName, day, exercise) {
  const res = await axios.post(
    `${API_BASE}/weekly_schedule/${patientName}/${day}`,
    exercise
  );
  return res.data;
}

export async function getOverallPTSchedule() {
  const res = await axios.get(`${API_BASE}/pt_schedule`);
  return res.data;
}
