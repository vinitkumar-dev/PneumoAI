// Report.jsx
import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";
import "./Report.css";

function Report({ result }) {
  const downloadReport = () => {
    if (!result) return;

    // Instantiate A4 Canvas
    const pdf = new jsPDF("p", "mm", "a4");
    const PAGE_WIDTH = pdf.internal.pageSize.getWidth();
    const PAGE_HEIGHT = pdf.internal.pageSize.getHeight();

    let y = 35; // Safe vertical padding anchor

    // =====================================
    // Dynamic Section Header System
    // =====================================
    const generateSectionTitle = (title) => {
      if (y > 250) {
        pdf.addPage();
        y = 25;
      }

      pdf.setFillColor(15, 76, 129);
      pdf.roundedRect(12, y - 5, 186, 9, 1.5, 1.5, "F");

      pdf.setFont("helvetica", "bold");
      pdf.setTextColor(255, 255, 255);
      pdf.setFontSize(11);
      pdf.text(title, 16, y + 1);

      pdf.setTextColor(0, 0, 0); // Reset colors
      y += 12;
    };

    // =====================================
    // Main Document Banner
    // =====================================
    pdf.setFillColor(15, 76, 129);
    pdf.rect(0, 0, PAGE_WIDTH, 26, "F");

    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(18);
    pdf.setTextColor(255, 255, 255);
    pdf.text("PneumoAI Medical Report", PAGE_WIDTH / 2, 14, {
      align: "center",
    });

    pdf.setFontSize(9);
    pdf.setFont("helvetica", "normal");
    pdf.text("Clinical Screening & AI Analysis Summary", PAGE_WIDTH / 2, 20, {
      align: "center",
    });

    pdf.setTextColor(0, 0, 0);

    // =====================================
    // Section 1: Patient Information
    // =====================================
    generateSectionTitle("Patient Information");

    autoTable(pdf, {
      startY: y,
      theme: "grid",
      styles: { fontSize: 9, cellPadding: 2.5 },
      headStyles: { fillColor: [15, 76, 129] },
      body: [
        ["Patient Name", result.patient_name || "Anonymous Record"],
        [
          "Age / Gender",
          `${result.patient_age || "N/A"} Yrs / ${result.patient_gender || "N/A"}`,
        ],
        [
          "Analysis Date",
          result.created_at
            ? new Date(result.created_at).toLocaleString()
            : new Date().toLocaleString(),
        ],
        ["Case Reference ID", `#${result.id || "N/A"}`],
      ],
    });

    y = pdf.lastAutoTable.finalY + 8;

    // =====================================
    // Section 2: Diagnostic Results
    // =====================================
    generateSectionTitle("AI Diagnostic Results");

    const isPneumonia = result.prediction?.toUpperCase() === "PNEUMONIA";
    const statusColor = isPneumonia ? [220, 53, 69] : [40, 167, 69]; // Red alert vs Green normal

    autoTable(pdf, {
      startY: y,
      theme: "grid",
      styles: { fontSize: 9, cellPadding: 2.5 },
      headStyles: { fillColor: statusColor },
      body: [
        ["Finding State", result.prediction || "-"],
        [
          "Confidence Level",
          result.confidence != null ? `${result.confidence}%` : "-",
        ],
        [
          "Inference Latency",
          result.inference_time != null ? `${result.inference_time} ms` : "-",
        ],
      ],
    });

    y = pdf.lastAutoTable.finalY + 8;

    // =====================================
    // Section 3: AI Analysis Findings
    // =====================================
    generateSectionTitle("AI Analysis Findings");

    const explanation =
      result.explanation || "No automated clinical remarks generated.";
    const explanationLines = pdf.splitTextToSize(explanation, 180);

    if (y + explanationLines.length * 4.5 > PAGE_HEIGHT - 35) {
      pdf.addPage();
      y = 25;
      generateSectionTitle("AI Analysis Findings");
    }

    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(10);
    pdf.text(explanationLines, 14, y);

    y += explanationLines.length * 4.5 + 8;

    // =====================================
    // Section 4: Clinical Notes
    // =====================================
    if (result.clinical_notes) {
      if (y > 230) {
        pdf.addPage();
        y = 25;
      }
      generateSectionTitle("Patient Clinical Notes");
      const noteLines = pdf.splitTextToSize(`"${result.clinical_notes}"`, 180);
      pdf.setFont("helvetica", "italic");
      pdf.setFontSize(10);
      pdf.text(noteLines, 14, y);
      y += noteLines.length * 4.5 + 8;
    }

    // =====================================
    // Section 5: Recommendations
    // =====================================
    if (y > 230) {
      pdf.addPage();
      y = 25;
    }

    generateSectionTitle("Clinical Recommendations");

    const recommendation = isPneumonia
      ? "AI analysis indicates findings consistent with Pneumonia. Immediate clinical correlation and review by a radiologist or attending physician is strongly recommended. Do not use this tool as the sole basis for therapeutics."
      : "AI analysis indicates normal lung structures with no clear evidence of pneumonia. If patient symptoms persist, continue tracking through regular diagnostic screening pathways.";

    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(10);
    pdf.text(pdf.splitTextToSize(recommendation, 180), 14, y);

    y += 20;

    // =====================================
    // Section 6: Medical Disclaimer Box
    // =====================================
    if (y > 240) {
      pdf.addPage();
      y = 25;
    }

    pdf.setFillColor(248, 250, 252);
    pdf.setDrawColor(226, 232, 240);
    pdf.roundedRect(12, y, 186, 20, 2, 2, "FD");

    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(9);
    pdf.setTextColor(15, 76, 129);
    pdf.text("Medical Disclaimer", 16, y + 5);

    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(8);
    pdf.setTextColor(71, 85, 105);
    pdf.text(
      pdf.splitTextToSize(
        "This document is generated by an automated AI diagnostic assistance framework to assist medical workflows. It is not an independent diagnostic tool. Final diagnostic authority and patient care path design remain under the strict supervision of qualified human practitioners.",
        178,
      ),
      16,
      y + 10,
    );

    // =====================================
    // Running Page Numbers & Footers
    // =====================================
    const totalPages = pdf.internal.getNumberOfPages();

    for (let i = 1; i <= totalPages; i++) {
      pdf.setPage(i);
      pdf.setDrawColor(226, 232, 240);
      pdf.line(12, PAGE_HEIGHT - 12, PAGE_WIDTH - 12, PAGE_HEIGHT - 12);

      pdf.setFontSize(8);
      pdf.setFont("helvetica", "bold");
      pdf.setTextColor(148, 163, 184);
      pdf.text(
        "CLINICAL DIAGNOSTIC RECORD // PNEUMOAI PLATFORM",
        14,
        PAGE_HEIGHT - 6,
      );

      pdf.setFont("helvetica", "normal");
      pdf.text(`Page ${i} of ${totalPages}`, PAGE_WIDTH - 14, PAGE_HEIGHT - 6, {
        align: "right",
      });
    }

    // Export PDF file out to device storage
    pdf.save(`PneumoAI_Clinical_Record_${Date.now()}.pdf`);
  };

  return (
    <div className="report-container-block">
      <div className="report-info">
        <div className="report-icon-box" aria-hidden="true">
          <svg
            width="22"
            height="22"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
            <polyline points="10 9 9 9 8 9" />
          </svg>
        </div>

        <div className="report-text-block">
          <h2>Medical Report</h2>
          <p>
            Export a formal, structured clinical validation summary generated
            from full pipeline outputs.
          </p>
        </div>
      </div>

      <button
        className="download-action-btn"
        onClick={downloadReport}
        disabled={!result}
        type="button"
        aria-label="Export diagnostic findings summary to local disk storage as a PDF document"
      >
        Download Document
      </button>
    </div>
  );
}

export default Report;
