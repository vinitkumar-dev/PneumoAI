from datetime import datetime, timezone
from database.db import db
# from datetime import datetime
from zoneinfo import ZoneInfo


class Prediction(db.Model):
    __tablename__ = "predictions"

    # Primary Tracking Identification Columns
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Inbound Patient Demographics Matrix Tracks
    patient_name = db.Column(
        db.String(255),
        nullable=True
    )

    patient_age = db.Column(
        db.Integer,
        nullable=True
    )

    patient_gender = db.Column(
        db.String(50),
        nullable=True
    )

    clinical_notes = db.Column(
        db.Text,
        nullable=True
    )


    # File System Pipeline Artifact Asset Paths
    image_path = db.Column(
        db.String(500),
        nullable=False
    )

    gradcam_path = db.Column(
        db.String(500),
        nullable=True
    )

    yolo_path = db.Column(
        db.String(500),
        nullable=True
    )


    # Model Classifications & Deep Telemetry Metrics
    prediction = db.Column(
        db.String(50),
        nullable=False
    )

    confidence = db.Column(
        db.Float,
        nullable=False
    )

    accuracy = db.Column(
        db.Float,
        nullable=True
    )

    precision = db.Column(
        db.Float,
        nullable=True
    )

    recall = db.Column(
        db.Float,
        nullable=True
    )

    f1_score = db.Column(
        db.Float,
        nullable=True
    )

    model = db.Column(
        db.String(100),
        nullable=True
    )

    inference_time = db.Column(
        db.Float,
        nullable=True
    )

    explanation = db.Column(
        db.Text,
        nullable=True
    )


    # Audit Lifecycle Tracking (Timezone-aware UTC)
    created_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))


    # Relational Bidirectional Mapping Backlinks
    user = db.relationship(
        "User",
        back_populates="predictions"
    )