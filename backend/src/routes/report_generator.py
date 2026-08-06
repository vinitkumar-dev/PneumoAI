import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from config import REPORT_FOLDER

def generate_report(prediction_id, data):
    """
    Creates a clean, hospital-style AI patient report PDF matching the frontend structure.
    """
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    file_path = os.path.join(
        REPORT_FOLDER,
        f"report_{prediction_id}.pdf"
    )

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # =====================================
    # HEADER ACCENT BLOCK
    # =====================================
    c.setFillColorRGB(0.058, 0.298, 0.505) # Institutional Blue (#0F4C81)
    c.rect(0, height - 60, width, 60, fill=True, stroke=False)
    
    c.setFillColorRGB(1, 1, 1) # Text White
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 38, "PneumoAI Medical Report")
    
    # Header Subtitle
    c.setFont("Helvetica", 9)
    c.drawString(50, height - 52, "AI Powered Pneumonia Detection & Verification Pipeline")

    # =====================================
    # CASE METADATA TERMINAL
    # =====================================
    c.setFillColorRGB(0, 0, 0) # Text Reset
    c.setFont("Helvetica-Bold", 10)
    c.drawString(420, height - 85, "Institutional Tracking:")
    
    c.setFont("Helvetica", 9)
    c.drawString(420, height - 100, f"Case Record ID: #{prediction_id}")
    
    # Handle Date Generation Formatting safely
    raw_date = data.get("created_at")
    if raw_date:
        try:
            formatted_date = datetime.fromisoformat(raw_date.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            formatted_date = str(raw_date)
    else:
        formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    c.drawString(420, height - 115, f"Evaluation Date: {formatted_date}")

    # =====================================
    # PATIENT PROFILE DEMOGRAPHICS
    # =====================================
    y = height - 90
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Patient Profile & Session Demographics")
    
    # Horizontal Rule separator line
    c.setStrokeColorRGB(0.88, 0.91, 0.94)
    c.setLineWidth(1)
    c.line(50, y - 6, width - 50, y - 6)
    
    y -= 24
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Patient Name:  {data.get('patient_name') or 'Anonymous Data Record'}")
    y -= 18
    c.drawString(50, y, f"Age / Gender:   {data.get('patient_age') or 'N/A'} Yrs / {data.get('patient_gender') or 'N/A'}")
    
    # =====================================
    # DIAGNOSIS TELEMETRY SUMMARY
    # =====================================
    y -= 35
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "AI Diagnosis Telemetry Summary")
    c.line(50, y - 6, width - 50, y - 6)
    
    y -= 24
    prediction_state = str(data.get('prediction', '-')).upper()
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Assigned Prediction State: ")
    
    # Conditional Alerts for Diagnostics Outcome Text
    if "PNEUMONIA" in prediction_state:
        c.setFillColorRGB(0.86, 0.20, 0.27) # High-alert Medical Crimson
    else:
        c.setFillColorRGB(0.15, 0.65, 0.27) # Safe Emerald Green
        
    c.setFont("Helvetica-Bold", 10)
    c.drawString(180, y, prediction_state)
    
    c.setFillColorRGB(0, 0, 0) # Reset color channel
    c.setFont("Helvetica", 10)
    y -= 18
    c.drawString(50, y, f"Confidence Matrix Score: {data.get('confidence', '-')}%")
    
    # =====================================
    # PATIENT CLINICAL INTAKE NOTES
    # =====================================
    clinical_notes = data.get("clinical_notes")
    if clinical_notes:
        y -= 35
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Patient Intake Presenting Manifestations")
        c.line(50, y - 6, width - 50, y - 6)
        
        y -= 24
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColorRGB(0.27, 0.33, 0.41) # Soft charcoal text for notes
        
        # Simple bounds line text wrapper protection snippet
        if len(clinical_notes) > 95:
            c.drawString(50, y, f'"{clinical_notes[:95]}..."')
        else:
            c.drawString(50, y, f'"{clinical_notes}"')
            
        c.setFillColorRGB(0, 0, 0)

    # =====================================
    # MEDICAL DISCLOSURE SHIELD (FOOTER)
    # =====================================
    # Bottom Boundary Line Accent
    c.setStrokeColorRGB(0.88, 0.91, 0.94)
    c.line(50, 75, width - 50, 75)
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColorRGB(0.058, 0.298, 0.505)
    c.drawString(50, 60, "Regulatory Decision Support Disclaimer:")
    
    c.setFont("Helvetica", 7.5)
    c.setFillColorRGB(0.27, 0.33, 0.41)
    c.drawString(50, 48, "This payload represents an automated inference file computed from deep artificial intelligence layers. This artifact functions strictly")
    c.drawString(50, 38, "as an assistive workspace tool. It is not approved as an independent legal or diagnostic instrument. Direct diagnostic agency remains")
    c.drawString(50, 28, "solely under the execution boundaries of a certified human practitioner.")

    # Page tracking index marker stamp
    c.setFont("Helvetica-Bold", 8)
    c.setFillColorRGB(0.58, 0.64, 0.72)
    c.drawString(50, 14, "AUTOMATED DIAGNOSTIC RECORD // PNEUMOAI CORE")
    c.drawRightString(width - 50, 14, "Page 1 of 1")

    c.save()
    return file_path