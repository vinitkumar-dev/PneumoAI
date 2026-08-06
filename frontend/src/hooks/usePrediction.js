// usePrediction.js
import { useState } from "react";
import { predictPneumonia } from "../services/predictionService";

export default function usePrediction() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  /**
   * Triggers the AI inference pipeline execution step.
   * @param {Object} payload - An object containing the binary file and metadata
   * @param {File} payload.image - The chest X-ray image file object
   * @param {Object} payload.patientData - Structured dictionary of patient info
   */
  async function predict({ image, patientData }) {
    try {
      setLoading(true);
      setError("");

      // Assemble multi-part form boundary fields for streaming to the API gateway
      const formData = new FormData();
      formData.append("image", image);
      formData.append("patient_name", patientData.name);
      formData.append("patient_age", patientData.age);
      formData.append("patient_gender", patientData.gender);
      formData.append("clinical_notes", patientData.clinicalNotes);

      // Hand over the full multipart envelope to the network service handler
      const response = await predictPneumonia(formData);

      setResult(response);
      return response;
    } catch (err) {
      setError(
        err.response?.data?.message ||
          "An error occurred while executing the deep layer inference run.",
      );
      throw err;
    } finally {
      setLoading(false);
    }
  }

  return {
    loading,
    result,
    error,
    predict,
  };
}
