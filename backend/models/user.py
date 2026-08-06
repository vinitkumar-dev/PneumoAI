from datetime import datetime
from database.db import db


class User(db.Model):
    __tablename__ = "users"

    # ==========================
    # Primary Key
    # ==========================
    id = db.Column(db.Integer, primary_key=True)

    # ==========================
    # User Information
    # ==========================
    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    # ==========================
    # Audit Fields
    # ==========================
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ==========================
    # Relationships
    # ==========================
    predictions = db.relationship(
        "Prediction",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )