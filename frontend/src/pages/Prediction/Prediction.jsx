// Prediction.jsx
import { useState } from "react";
import Upload from "../../components/Upload/Upload";
import Loader from "../../components/Loader/Loader";
import PredictionCard from "../../components/PredictionCard/PredictionCard";
import ConfidenceBar from "../../components/ConfidenceBar/ConfidenceBar";
import GradCAMViewer from "../../components/GradCAMViewer/GradCAMViewer";
import YOLOViewer from "../../components/YOLOViewer/YOLOViewer";
import Metrics from "../../components/Metrics/Metrics";
import Report from "../../components/Report/Report";
import Chatbot from "../../components/Chatbot/Chatbot";
import usePrediction from "../../hooks/usePrediction";
import "./Prediction.css";

function Prediction() {
  const [image, setImage] = useState(null);

  // Core Structured Form State Map
  const [patientInfo, setPatientInfo] = useState({
    name: "",
    age: "",
    gender: "",
    clinicalNotes: "",
  });

  const { loading, result, error, predict } = usePrediction();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPatientInfo((prev) => ({ ...prev, [name]: value }));
  };

  const handlePredict = async (e) => {
    e.preventDefault(); // Intercept and cancel native page refreshes
    if (!image) return;

    // Pass the matching structured envelope to your hook pipeline
    await predict({ image, patientData: patientInfo });
  };

  // console.log(result);

  return (
    <main className="predict-viewport-flow">
      <header className="predict-header-panel">
        <h1>AI Pneumonia Detection Engine</h1>
        <p>
          Deploy specialized vision pipelines mapped with localized patient
          demographics.
        </p>
      </header>

      {/* Structured Ingestion Layout Track */}
      <form onSubmit={handlePredict} className="predict-ingestion-layout-grid">
        {/* Patient Registration Details Card */}
        <section className="predict-patient-form-card">
          <h2>Patient Demographics</h2>
          <div className="form-fields-matrix">
            <div className="input-group">
              <label htmlFor="patient-name">Full Name</label>
              <input
                id="patient-name"
                type="text"
                name="name"
                value={patientInfo.name}
                onChange={handleInputChange}
                placeholder="e.g., John Doe"
                required
              />
            </div>

            <div className="input-row-split">
              <div className="input-group">
                <label htmlFor="patient-age">Age</label>
                <input
                  id="patient-age"
                  type="number"
                  name="age"
                  value={patientInfo.age}
                  onChange={handleInputChange}
                  placeholder="Years"
                  required
                />
              </div>

              <div className="input-group">
                <label htmlFor="patient-gender">Gender</label>
                <select
                  id="patient-gender"
                  name="gender"
                  value={patientInfo.gender}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select...</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div className="input-group">
              <label htmlFor="clinical-notes">
                Clinical Notes / Presenting Symptoms
              </label>
              <textarea
                id="clinical-notes"
                name="clinicalNotes"
                value={patientInfo.clinicalNotes}
                onChange={handleInputChange}
                placeholder="Persistent cough, high fever, dyspnea..."
                rows="3"
              />
            </div>
          </div>
        </section>

        {/* Radiograph Dropzone Frame */}
        <section
          className="predict-ingestion-card"
          aria-label="Radiograph File Ingestion Dropzone"
        >
          <h2>Radiograph Matrix Input</h2>
          <Upload selectedFile={image} onFileSelect={setImage} />

          <button
            disabled={!image || loading}
            className="predict-execute-action"
            type="submit"
          >
            {loading ? (
              <div className="button-spinner-housing">
                <div className="action-inline-spinner"></div>
                <span>Executing Inference Pipeline...</span>
              </div>
            ) : (
              "Analyze Matrix"
            )}
          </button>
        </section>
      </form>

      {/* Async Suspense Processing Spinner Overlays */}
      {loading && <Loader text="Executing Deep Layer Inference Matrices..." />}

      {error && (
        <div className="predict-exception-toast" role="alert">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <span>{error}</span>
        </div>
      )}

      {/* Model Result Output Display Arrays */}
      {result && (
        <section
          className="predict-telemetry-dashboard"
          aria-label="Pipeline Trace Telemetry Metrics"
        >
          <div className="telemetry-primary-split">
            <PredictionCard predictionData={result} />
            <ConfidenceBar confidence={result.confidence} />
          </div>

          <div className="telemetry-vision-grids">
            <GradCAMViewer image={result.gradcam_image} />
            <YOLOViewer image={result.yolo_image} />
          </div>

          <div className="telemetry-metrics-block">
            <Metrics metrics={result} />
          </div>

          <footer className="telemetry-interactive-footer">
            <Report result={result} />
            {/* console.log(result); console.log(result.id); */}
            <Chatbot predictionId={result.id} />
          </footer>
        </section>
      )}
    </main>
  );
}

export default Prediction;
