from flask import Blueprint, send_file, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

import os

from models.prediction import Prediction


report_bp = Blueprint("report", __name__)


# ==========================================================
# PDF REPORT
# ==========================================================
@report_bp.route("/report/<int:prediction_id>", methods=["GET"])
@jwt_required()
def generate_report(prediction_id):

    try:

        user_id = int(get_jwt_identity())

        prediction = Prediction.query.filter_by(
            id=prediction_id,
            user_id=user_id
        ).first()

        if prediction is None:
            return jsonify({
                "status": "error",
                "message": "Prediction not found."
            }), 404

        os.makedirs("artifacts", exist_ok=True)

        file_path = os.path.join(
            "artifacts",
            f"report_{prediction.id}.pdf"
        )

        doc = SimpleDocTemplate(file_path)

        styles = getSampleStyleSheet()

        elements = []

        # ==========================================================
        # TITLE
        # ==========================================================
        elements.append(
            Paragraph(
                "AI PNEUMONIA DETECTION REPORT",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        # ==========================================================
        # PATIENT INFORMATION
        # ==========================================================
        elements.append(
            Paragraph("Patient Information", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                f"<b>Name:</b> {prediction.patient_name or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Age:</b> {prediction.patient_age or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Gender:</b> {prediction.patient_gender or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Clinical Notes:</b> {prediction.clinical_notes or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 20))

        # ==========================================================
        # PREDICTION
        # ==========================================================
        elements.append(
            Paragraph("Prediction Summary", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                f"<b>Prediction:</b> {prediction.prediction}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Confidence:</b> {prediction.confidence:.2f} %",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Model:</b> {prediction.model or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Inference Time:</b> {prediction.inference_time or 0:.3f} sec",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 20))

        # ==========================================================
        # METRICS
        # ==========================================================
        elements.append(
            Paragraph("Performance Metrics", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                f"<b>Accuracy:</b> {prediction.accuracy or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Precision:</b> {prediction.precision or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Recall:</b> {prediction.recall or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>F1 Score:</b> {prediction.f1_score or 'N/A'}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 20))

        # ==========================================================
        # AI EXPLANATION
        # ==========================================================
        elements.append(
            Paragraph("AI Explanation", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                prediction.explanation or "No explanation available.",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 20))

        # ==========================================================
        # FOOTER
        # ==========================================================
        elements.append(
            Paragraph(
                f"<b>Created:</b> {prediction.created_at.strftime('%d %B %Y %H:%M:%S')}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                "This report is generated by ChestVision AI. "
                "It is intended to assist clinicians and should not "
                "replace professional medical diagnosis.",
                styles["Italic"]
            )
        )

        doc.build(elements)

        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"Prediction_Report_{prediction.id}.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500