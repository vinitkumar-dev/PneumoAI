from sqlalchemy import or_
from models.prediction import Prediction


def get_history(user_id, page, limit, search, prediction_filter):

    query = Prediction.query.filter_by(user_id=user_id)

    # =====================================
    # Search
    # =====================================
    if search:
        search = search.strip()

        query = query.filter(
            or_(
                Prediction.patient_name.ilike(f"%{search}%"),
                Prediction.patient_gender.ilike(f"%{search}%"),
                Prediction.prediction.ilike(f"%{search}%"),
                Prediction.model.ilike(f"%{search}%"),
                Prediction.clinical_notes.ilike(f"%{search}%"),
            )
        )

    # =====================================
    # Prediction Filter
    # =====================================
    if prediction_filter:
        query = query.filter(
            Prediction.prediction == prediction_filter.upper()
        )

    # =====================================
    # Latest First
    # =====================================
    query = query.order_by(
        Prediction.created_at.desc()
    )

    results = query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )

    return {
        "items": [
            {
                # ======================================
                # Core
                # ======================================
                "id": p.id,
                "created_at": (
                    p.created_at.isoformat()
                    if p.created_at
                    else None
                ),

                # ======================================
                # Patient Information
                # ======================================
                "patient_name": p.patient_name,
                "patient_age": p.patient_age,
                "patient_gender": p.patient_gender,
                "clinical_notes": p.clinical_notes,

                # ======================================
                # Prediction
                # ======================================
                "prediction": p.prediction,
                "confidence": float(p.confidence or 0),
                "model": p.model,

                # ======================================
                # Images
                # ======================================
                "image_path": p.image_path,
                "gradcam_path": p.gradcam_path,
                "yolo_path": p.yolo_path,

                # ======================================
                # Metrics
                # ======================================
                "accuracy": p.accuracy,
                "precision": p.precision,
                "recall": p.recall,
                "f1_score": p.f1_score,
                "inference_time": p.inference_time,
                "explanation": p.explanation,
            }
            for p in results.items
        ],

        "page": results.page,
        "totalPages": results.pages,
        "total": results.total,
        "hasNext": results.has_next,
        "hasPrev": results.has_prev,
    }