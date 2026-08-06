// PredictionDetails.jsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Loader from "../../components/Loader/Loader";
import PredictionCard from "../../components/PredictionCard/PredictionCard";
import ConfidenceBar from "../../components/ConfidenceBar/ConfidenceBar";
import GradCAMViewer from "../../components/GradCAMViewer/GradCAMViewer";
import YOLOViewer from "../../components/YOLOViewer/YOLOViewer";
import Metrics from "../../components/Metrics/Metrics";
import Report from "../../components/Report/Report";
import Chatbot from "../../components/Chatbot/Chatbot";

import { getPrediction } from "../../services/predictionDetailsService";

import "./PredictionDetails.css";

function PredictionDetails() {
  const { id } = useParams();

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadPrediction() {
      try {
        setLoading(true);
        setError("");

        const data = await getPrediction(id);

        setPrediction(data);
      } catch (err) {
        console.error(err);

        setError("Unable to load prediction details.");
      } finally {
        setLoading(false);
      }
    }

    loadPrediction();
  }, [id]);

  if (loading) {
    return <Loader text="Loading patient prediction details..." />;
  }

  if (error || !prediction) {
    return (
      <main className="details-page">
        <div className="details-error">{error || "Prediction not found."}</div>
      </main>
    );
  }
  // console.log(prediction);

  return (
    <main className="details-page">
      {/* Header */}

      <header className="details-header">
        <h1>Prediction Details</h1>

        <p>Case ID #{prediction.id}</p>
      </header>

      {/* Patient Information */}

      <section className="patient-card">
        <h2>Patient Information</h2>

        <div className="patient-grid">
          <div className="patient-item">
            <span>Name</span>
            <strong>{prediction.patient_name || "N/A"}</strong>
          </div>

          <div className="patient-item">
            <span>Age</span>
            <strong>{prediction.patient_age || "N/A"}</strong>
          </div>

          <div className="patient-item">
            <span>Gender</span>
            <strong>{prediction.patient_gender || "N/A"}</strong>
          </div>

          <div className="patient-item">
            <span>Date</span>
            <strong>
              {prediction.created_at
                ? new Date(prediction.created_at).toLocaleString()
                : "N/A"}
            </strong>
          </div>
        </div>

        <div className="patient-notes">
          <h3>Clinical Notes</h3>

          <p>{prediction.clinical_notes || "No clinical notes available."}</p>
        </div>
      </section>

      {/* Original Image */}

      <section className="original-image-card">
        <h2>Uploaded Chest X-Ray</h2>

        <img
          src={prediction.original_image}
          alt="Original X-Ray"
          className="original-image"
        />
      </section>

      {/* Prediction */}

      <section className="prediction-summary">
        <PredictionCard predictionData={prediction} />

        <ConfidenceBar confidence={prediction.confidence} />
      </section>

      {/* Heatmaps */}

      <section className="heatmap-grid">
        <GradCAMViewer image={prediction.gradcam_image} />

        <YOLOViewer image={prediction.yolo_image} />
      </section>

      {/* Metrics */}

      <section>
        <Metrics metrics={prediction} />
      </section>

      {/* Explanation */}

      {prediction.explanation && (
        <section className="explanation-card">
          <h2>AI Explanation</h2>

          <p>{prediction.explanation}</p>
        </section>
      )}

      {/* Footer */}

      <section className="details-footer">
        <Report result={prediction} />
        {/* console.log(result); console.log(result.id); */}
        <Chatbot predictionId={prediction.id} />
      </section>
    </main>
  );
}

export default PredictionDetails;
