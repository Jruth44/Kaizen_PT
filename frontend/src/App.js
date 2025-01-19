import React, { useState } from "react";
import PatientList from "./components/PatientList";
import PatientForm from "./components/PatientForm";
import WeeklySchedule from "./components/WeeklySchedule";
import ExerciseGenerator from "./components/ExerciseGenerator";

function App() {
  const [selectedPage, setSelectedPage] = useState("Patients");
  const [selectedPatient, setSelectedPatient] = useState("");

  const handleMenuClick = (page) => {
    setSelectedPage(page);
  };

  return (
    <div style={{ display: "flex" }}>
      {/* Sidebar */}
      <div style={{ width: "200px", background: "#f0f0f0", padding: "1rem" }}>
        <h2>PT Planner</h2>
        <div style={{ marginBottom: "1rem" }}>
          <button onClick={() => handleMenuClick("Patients")}>Patients</button>
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <button onClick={() => handleMenuClick("CreatePatient")}>Add Patient</button>
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <button onClick={() => handleMenuClick("Schedule")}>Weekly Schedule</button>
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <button onClick={() => handleMenuClick("Exercises")}>Generate Exercises</button>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, padding: "1rem" }}>
        {selectedPage === "Patients" && (
          <PatientList onSelectPatient={(p) => setSelectedPatient(p)} />
        )}
        {selectedPage === "CreatePatient" && <PatientForm />}
        {selectedPage === "Schedule" && (
          <WeeklySchedule selectedPatient={selectedPatient} />
        )}
        {selectedPage === "Exercises" && (
          <ExerciseGenerator selectedPatient={selectedPatient} />
        )}
      </div>
    </div>
  );
}

export default App;
