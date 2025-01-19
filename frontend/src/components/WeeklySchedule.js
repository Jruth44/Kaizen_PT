import React, { useEffect, useState } from "react";
import { getWeeklySchedule, addExerciseToDay } from "../services/api";

function WeeklySchedule({ selectedPatient }) {
  const [schedule, setSchedule] = useState(null);
  const [exerciseInput, setExerciseInput] = useState({ name: "", parameters: "" });
  const [selectedDay, setSelectedDay] = useState("Monday");

  useEffect(() => {
    if (selectedPatient) {
      fetchSchedule(selectedPatient);
    }
  }, [selectedPatient]);

  async function fetchSchedule(patientName) {
    const data = await getWeeklySchedule(patientName);
    setSchedule(data);
  }

  async function handleAddExercise(e) {
    e.preventDefault();
    if (!selectedPatient) return;
    // Minimal example: we just add { name, parameters } as the exercise object
    const exerciseData = {
      id: Date.now().toString(),
      name: exerciseInput.name,
      description: "",
      parameters: exerciseInput.parameters,
      progressionCriteria: "",
      rationale: ""
    };
    await addExerciseToDay(selectedPatient, selectedDay, exerciseData);
    setExerciseInput({ name: "", parameters: "" });
    fetchSchedule(selectedPatient);
  }

  if (!selectedPatient) {
    return <div>Please select a patient first.</div>;
  }

  if (!schedule) {
    return <div>Loading schedule...</div>;
  }

  return (
    <div>
      <h3>Weekly Schedule for {selectedPatient}</h3>
      {Object.keys(schedule).map((day) => (
        <div key={day} style={{ marginBottom: "1rem" }}>
          <strong>{day}:</strong>
          <ul>
            {schedule[day].map((ex, idx) => (
              <li key={idx}>{ex.name || ex}</li>
            ))}
          </ul>
        </div>
      ))}

      <form onSubmit={handleAddExercise}>
        <h4>Add Exercise</h4>
        <label>Day: </label>
        <select
          value={selectedDay}
          onChange={(e) => setSelectedDay(e.target.value)}
        >
          {Object.keys(schedule).map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
        <br />
        <label>Exercise Name: </label>
        <input
          value={exerciseInput.name}
          onChange={(e) =>
            setExerciseInput({ ...exerciseInput, name: e.target.value })
          }
        />
        <br />
        <label>Parameters (e.g. sets/reps): </label>
        <input
          value={exerciseInput.parameters}
          onChange={(e) =>
            setExerciseInput({ ...exerciseInput, parameters: e.target.value })
          }
        />
        <br />
        <button type="submit">Add to Schedule</button>
      </form>
    </div>
  );
}

export default WeeklySchedule;
