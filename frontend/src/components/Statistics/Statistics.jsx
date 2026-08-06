import { useEffect, useState } from "react";
import api from "../../services/api"; // <-- adjust path if needed
import "./Statistics.css";

const DEFAULT_STATS = [
  {
    id: 1,
    title: "Total Predictions",
    value: 0,
    suffix: "+",
    iconType: "xray",
  },
  {
    id: 2,
    title: "Validation Accuracy",
    value: 0,
    suffix: "%",
    iconType: "target",
  },
  {
    id: 3,
    title: "Mean Inference Latency",
    value: 0,
    suffix: " sec",
    iconType: "flash",
  },
  {
    id: 4,
    title: "Active AI Engines",
    value: 0,
    suffix: "",
    iconType: "brain",
  },
  {
    id: 5,
    title: "Registered Practitioners",
    value: 0,
    suffix: "+",
    iconType: "doctor",
  },
];

function Statistics() {
  const [stats, setStats] = useState(DEFAULT_STATS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    const loadStatistics = async () => {
      try {
        const { data } = await api.get("/statistics");

        if (!mounted) return;

        setStats([
          {
            id: 1,
            title: "Total Predictions",
            value: data.total_predictions ?? 0,
            suffix: "+",
            iconType: "xray",
          },
          {
            id: 2,
            title: "Validation Accuracy",
            value: data.accuracy ?? 0,
            suffix: "%",
            iconType: "target",
          },
          {
            id: 3,
            title: "Mean Inference Latency",
            value: data.average_inference ?? 0,
            suffix: " sec",
            iconType: "flash",
          },
          {
            id: 4,
            title: "Active AI Engines",
            value: data.models ?? 0,
            suffix: "",
            iconType: "brain",
          },
          {
            id: 5,
            title: "Registered Practitioners",
            value: data.users ?? 0,
            suffix: "+",
            iconType: "doctor",
          },
        ]);
      } catch (err) {
        console.error("Statistics Error:", err);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadStatistics();

    return () => {
      mounted = false;
    };
  }, []);

  const renderVectorIcon = (type) => {
    const baseAttrs = {
      width: "20",
      height: "20",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth: "2.5",
      strokeLinecap: "round",
      strokeLinejoin: "round",
      "aria-hidden": "true",
    };

    switch (type) {
      case "xray":
        return (
          <svg {...baseAttrs}>
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <path d="M12 3v18M3 12h18M7 7l10 10M17 7L7 17" />
          </svg>
        );

      case "target":
        return (
          <svg {...baseAttrs}>
            <circle cx="12" cy="12" r="10" />
            <circle cx="12" cy="12" r="6" />
            <circle cx="12" cy="12" r="2" />
          </svg>
        );

      case "flash":
        return (
          <svg {...baseAttrs}>
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
          </svg>
        );

      case "brain":
        return (
          <svg {...baseAttrs}>
            <path d="M9.5 2A2.5 2.5 0 0112 4.5v15a2.5 2.5 0 01-4.96-.44 2.5 2.5 0 010-3.12 3 3 0 010-4.88 2.5 2.5 0 010-3.12A2.5 2.5 0 019.5 2zM14.5 2A2.5 2.5 0 0012 4.5v15a2.5 2.5 0 004.96-.44 2.5 2.5 0 000-3.12 3 3 0 000-4.88 2.5 2.5 0 000-3.12A2.5 2.5 0 0014.5 2z" />
          </svg>
        );

      case "doctor":
        return (
          <svg {...baseAttrs}>
            <path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
            <circle cx="8.5" cy="7" r="4" />
            <line x1="19" y1="11" x2="19" y2="17" />
            <line x1="16" y1="14" x2="22" y2="14" />
          </svg>
        );

      default:
        return null;
    }
  };

  return (
    <section className="st-metrics-flow">
      <div className="st-panel-header">
        <h2>Platform Operational Statistics</h2>
        <p>
          Live framework runtime telemetries, throughput and verified neural
          pipeline metrics.
        </p>
      </div>

      <div className="st-metrics-grid">
        {stats.map((item) => (
          <article
            key={item.id}
            className={`st-metrics-card ${loading ? "is-loading" : ""}`}
          >
            <div className="st-icon-housing">
              {renderVectorIcon(item.iconType)}
            </div>

            <div className="st-card-content">
              <p className="st-metric-value">
                {loading ? (
                  "--"
                ) : (
                  <>
                    {item.value}
                    <span className="st-metric-suffix">{item.suffix}</span>
                  </>
                )}
              </p>

              <h3 className="st-metric-title">{item.title}</h3>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default Statistics;
