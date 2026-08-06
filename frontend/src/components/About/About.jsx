// About.jsx
import "./About.css";

const PIPELINE = [
  {
    id: 1,
    icon: "📤",
    title: "Upload X-ray",
    description: "Upload a chest X-ray image securely for AI analysis.",
  },
  {
    id: 2,
    icon: "🧠",
    title: "EfficientNet-B0",
    description: "The deep learning model predicts Normal or Pneumonia.",
  },
  {
    id: 3,
    icon: "🔥",
    title: "Grad-CAM",
    description: "Highlights image regions that influenced the prediction.",
  },
  {
    id: 4,
    icon: "🎯",
    title: "YOLO Detection",
    description: "Localizes suspicious lung regions with bounding boxes.",
  },
  {
    id: 5,
    icon: "📊",
    title: "Performance Metrics",
    description:
      "Displays confidence, precision, recall, F1-score, and inference time.",
  },
  {
    id: 6,
    icon: "📄",
    title: "Medical Report",
    description:
      "Generate and download a professional AI-generated PDF report.",
  },
  {
    id: 7,
    icon: "🤖",
    title: "AI Assistant",
    description: "Ask follow-up medical questions about the prediction.",
  },
];

function About() {
  return (
    <section className="ab-viewport-flow" aria-labelledby="ab-panel-heading">
      <div className="ab-background-blur" aria-hidden="true">
        <div className="blur-shape blur-shape-1"></div>
        <div className="blur-shape blur-shape-2"></div>
      </div>

      <div className="ab-content-container">
        <div className="ab-panel-header">
          <span className="ab-section-badge" role="status">
            <span className="ab-badge-pulse" aria-hidden="true"></span>
            Operational Mechanics
          </span>

          <h2 id="ab-panel-heading">Explainable AI Pipeline</h2>

          <p>
            Our system combines deep learning architectures, spatial
            explainability layers, object localization grids, and conversational
            intelligence matrices to back down diagnostic metrics.
          </p>
        </div>

        <div className="ab-pipeline-layout">
          <div className="ab-pipeline-grid">
            {PIPELINE.map((step, index) => (
              <div className="ab-card-wrapper" key={step.id}>
                <article className="ab-pipeline-card">
                  <div className="ab-card-inner">
                    <div className="ab-icon-harness">
                      <div
                        className="ab-step-icon"
                        role="img"
                        aria-label={`${step.title} matrix node indicator`}
                      >
                        {step.icon}
                      </div>
                      <div className="ab-step-index" aria-hidden="true">
                        {String(index + 1).padStart(2, "0")}
                      </div>
                    </div>

                    <h3>{step.title}</h3>
                    <p>{step.description}</p>
                  </div>
                </article>

                {index < PIPELINE.length - 1 && (
                  <div className="ab-pipeline-arrow" aria-hidden="true">
                    <svg
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2.5"
                    >
                      <path
                        d="M5 12H19M19 12L13 6M19 12L13 18"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export default About;
