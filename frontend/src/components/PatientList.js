import React, { useEffect, useState } from "react";
import { listPatients, getPatient, deletePatient } from "../services/api";

function PatientList({ onSelectPatient }) {
  const [patients, setPatients] = useState([]);
  const [selectedInfo, setSelectedInfo] = useState(null);

  useEffect(() => {
    fetchPatients();
  }, []);

  async function fetchPatients() {
    const data = await listPatients();
    setPatients(data);
  }

  async function handleSelect(name) {
    const data = await getPatient(name);
    setSelectedInfo(data);
    onSelectPatient(name);
  }

  async function handleDelete(name) {
    await deletePatient(name);
    fetchPatients();
    setSelectedInfo(null);
  }

  return (
    <div>
      <h3>Patients</h3>
      <ul>
        {patients.map((p) => (
          <li key={p}>
            <button onClick={() => handleSelect(p)}>{p}</button>
            <button onClick={() => handleDelete(p)} style={{ marginLeft: 8 }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
      {selectedInfo && (
        <div style={{ marginTop: "1rem" }}>
          <h4>Details for selected patient:</h4>
          <pre>{JSON.stringify(selectedInfo, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default PatientList;
