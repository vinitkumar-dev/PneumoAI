// Features.jsx
import "./Features.css";

const FEATURES = [
  {
    id: 1,
    icon: "🧠",
    title: "EfficientNet-B0 Classification",
    description:
      "Detects pneumonia from chest X-rays with high accuracy using a deep convolutional neural network.",
  },
  {
    id: 2,
    icon: "🎯",
    title: "YOLO Detection",
    description:
      "Localizes suspicious lung regions using object detection with bounding boxes.",
  },
  {
    id: 3,
    icon: "🔥",
    title: "Grad-CAM Explainability",
    description:
      "Visualizes the regions of the X-ray that influenced the AI prediction.",
  },
  {
    id: 4,
    icon: "📊",
    title: "Performance Metrics",
    description:
      "View confidence, accuracy, precision, recall, F1-score, and inference time.",
  },
  {
    id: 5,
    icon: "📄",
    title: "Medical PDF Report",
    description:
      "Download a professional report containing AI results, Grad-CAM, YOLO output, and metrics.",
  },
  {
    id: 6,
    icon: "🤖",
    title: "AI Medical Assistant",
    description:
      "Ask follow-up questions about the diagnosis using an AI-powered chatbot.",
  },
];

function Features() {
  return (
    <section className="features" aria-labelledby="features-heading">
      <div className="features-blur-overlay" aria-hidden="true">
        <div className="features-orb features-orb-1"></div>
        <div className="features-orb features-orb-2"></div>
      </div>

      <div className="features-container">
        <div className="features-header">
          <span className="section-badge" role="status">
            <span className="badge-pulse-dot" aria-hidden="true"></span>
            Platform Features
          </span>
          <h2 id="features-heading">
            Everything Needed for Explainable AI Diagnosis
          </h2>
          <p>
            A complete workflow from image upload to explainable AI prediction,
            visualization, reporting, and intelligent assistance.
          </p>
        </div>

        <div className="features-grid">
          {FEATURES.map((feature) => (
            <article key={feature.id} className="feature-card">
              <div className="feature-card-glow" aria-hidden="true"></div>
              <div className="feature-icon-wrapper">
                <span
                  className="feature-icon"
                  role="img"
                  aria-label={`${feature.title} icon`}
                >
                  {feature.icon}
                </span>
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Features;
