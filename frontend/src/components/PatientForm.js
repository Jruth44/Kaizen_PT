import React, { useState } from "react";
import { createPatient } from "../services/api";

function PatientForm() {
  const [form, setForm] = useState({
    name: "",
    age: 0,
    injury_location: "",
    pain_level: 5,
    mobility_status: "",
    medical_history: "",
    activity_level: "Sedentary",
    goals: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await createPatient(form);
      alert("Patient created successfully!");
      setForm({
        name: "",
        age: 0,
        injury_location: "",
        pain_level: 5,
        mobility_status: "",
        medical_history: "",
        activity_level: "Sedentary",
        goals: "",
      });
    } catch (err) {
      alert("Error creating patient. Check console for details.");
      console.error(err);
    }
  }

  return (
    <div>
      <h3>Create New Patient</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input name="name" value={form.name} onChange={handleChange} />
        </div>
        <div>
          <label>Age:</label>
          <input
            type="number"
            name="age"
            value={form.age}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Injury Location:</label>
          <input
            name="injury_location"
            value={form.injury_location}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Pain Level (0-10):</label>
          <input
            type="number"
            name="pain_level"
            min="0"
            max="10"
            value={form.pain_level}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Mobility Status:</label>
          <input
            name="mobility_status"
            value={form.mobility_status}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Medical History:</label>
          <textarea
            name="medical_history"
            value={form.medical_history}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Activity Level:</label>
          <select
            name="activity_level"
            value={form.activity_level}
            onChange={handleChange}
          >
            <option>Sedentary</option>
            <option>Light</option>
            <option>Moderate</option>
            <option>Active</option>
            <option>Very Active</option>
          </select>
        </div>
        <div>
          <label>Goals:</label>
          <textarea name="goals" value={form.goals} onChange={handleChange} />
        </div>
        <button type="submit">Create Patient</button>
      </form>
    </div>
  );
}

export default PatientForm;
