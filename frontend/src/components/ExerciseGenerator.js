import React, { useState } from "react";
import { generateExercises } from "../services/api";

function ExerciseGenerator({ selectedPatient }) {
  const [numExercises, setNumExercises] = useState(4);
  const [exercises, setExercises] = useState(null);

  async function handleGenerate() {
    if (!selectedPatient) {
      alert("Please select a patient first!");
      return;
    }
    try {
      const result = await generateExercises(selectedPatient, numExercises);
      setExercises(result);
    } catch (err) {
      console.error(err);
      alert("Error generating exercises.");
    }
  }

  return (
    <div>
      <h3>Generate Exercises</h3>
      {selectedPatient ? (
        <div>
          <p>Generate an exercise plan for {selectedPatient}.</p>
          <div>
            <label>Number of Exercises:</label>
            <input
              type="number"
              value={numExercises}
              min={1}
              max={10}
              onChange={(e) => setNumExercises(parseInt(e.target.value, 10))}
            />
            <button onClick={handleGenerate}>Generate Plan</button>
          </div>
        </div>
      ) : (
        <p>Please select a patient in the sidebar.</p>
      )}

      {exercises && (
        <div style={{ marginTop: "1rem" }}>
          <h4>Generated Exercises</h4>
          <pre>{JSON.stringify(exercises, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ExerciseGenerator;
