import sys
from datetime import datetime

from src.pipeline.predict_pipeline import PredictionPipeline
from src.components.gradcam_generator import GradCAMGenerator
from src.exception import CustomException
from src.logger import logging




class ExplainPipeline:

    def __init__(self):

        self.predictor = PredictionPipeline()

        self.gradcam = GradCAMGenerator()

        logging.info(
            "ExplainPipeline Initialized"
        )

    def explain(self, image_path):

        try:
            prediction_result = self.predictor.predict(image_path)

            prediction = prediction_result["prediction"]
            confidence = prediction_result["confidence"]
            inference_time = prediction_result['inference_time']

            detections = prediction_result.get("detections", [])
            avg_conf = prediction_result.get("avg_conf", 0)

            heatmap_path = None

            if prediction == "PNEUMONIA":
                heatmap_path = self.gradcam.generate_heatmap(image_path)

            result = {
                "status": "success",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "prediction": prediction,
                "confidence": confidence,

                "heatmap": heatmap_path,

                "yolo": prediction_result.get("yolo_image"),  # IMPORTANT FIX

                "detections": detections,
                "num_detections": len(detections),
                "avg_conf": avg_conf,
                "inference_time": inference_time,

                "normal_probability": prediction_result.get("normal_probability"),
                "pneumonia_probability": prediction_result.get("pneumonia_probability"),
            }
            
            return result

        except Exception as e:
            raise CustomException(e, sys)