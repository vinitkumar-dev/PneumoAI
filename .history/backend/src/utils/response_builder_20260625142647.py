import os

CLASSIFICATION_INFO = {
    "model": "EfficientNet-B0",
    "accuracy": 90.54,
    "auc_roc": 96.80,
    "f1_score": 90.34,
    "precision": 90.93,
    "recall": 90.54,
}

DETECTION_INFO = {
    "model": "YOLOv8"
}


def build_response(prediction_result, filename, base_url):

    # -----------------------------
    # Original Image
    # -----------------------------
    original_image = f"{base_url}/uploads/{filename}"

    # -----------------------------
    # GradCAM URL
    # -----------------------------
    gradcam_image = None

    if prediction_result.get("heatmap"):

        gradcam_path = (
            prediction_result["heatmap"]
            .replace("\\", "/")
        )

        gradcam_image = (
            f"{base_url}/{gradcam_path}"
        )

    # -----------------------------
    # YOLO URL
    # -----------------------------
    yolo_image = None

    if prediction_result.get("yolo"):

        yolo_path = (
            prediction_result["yolo"]
            .replace("\\", "/")
        )

        yolo_image = (
            f"{base_url}/{yolo_path}"
        )

    # -----------------------------
    # Detection List
    # -----------------------------
    detections = []

    for det in prediction_result.get("detections", []):

        if isinstance(det, dict):
            detections.append(det)

        elif len(det) >= 6:

            detections.append({

                "class": "Pneumonia",

                "confidence": round(det[4] * 100, 2),

                "x1": int(det[0]),
                "y1": int(det[1]),
                "x2": int(det[2]),
                "y2": int(det[3]),

            })

    # -----------------------------
    # Explanation
    # -----------------------------
    explanation = (
        f"The EfficientNet-B0 model classified this Chest X-ray as "
        f"{prediction_result['prediction']} with "
        f"{round(prediction_result['confidence']*100,2)}% confidence. "
        f"YOLOv8 detected {len(detections)} suspicious region(s)."
    )


    
    # -----------------------------
    # Final JSON
    # -----------------------------
    return {

        "status": "success",

        "prediction": prediction_result["prediction"],

        "confidence": round(
            prediction_result["confidence"] * 100,
            2
        ),

        "normal_probability": round(
            prediction_result["normal_probability"] * 100,
            2
        ),

        "pneumonia_probability": round(
            prediction_result["pneumonia_probability"] * 100,
            2
        ),

        "original_image": original_image,

        "gradcam_image": gradcam_image,

        "yolo_image": yolo_image,

        "classification": CLASSIFICATION_INFO,

        "detection": {

            "model": DETECTION_INFO["model"],

            "detections": detections,

            "num_detections": len(detections),

            "average_confidence": round(
                prediction_result.get("avg_conf", 0) * 100,
                2
            )

        },

        "processing_time": prediction_result.get(
            "time",
            0
        ),

        "inference_time": prediction_result.get(
            "inference_time",
            0
        ),

        "timestamp": prediction_result.get(
            "timestamp"
        ),

        "explanation": explanation,
    }