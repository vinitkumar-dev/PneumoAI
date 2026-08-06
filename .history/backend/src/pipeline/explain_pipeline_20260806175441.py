import sys
from datetime import datetime

from src.pipeline.predict_pipeline import PredictionPipeline
from src.components.gradcam_generator import GradCAMGenerator
from src.exception import CustomException
from src.logger import logging


class ExplainPipeline:

    def __init__(self):
        self.predictor = PredictionPipeline()

        try:
            self.gradcam = GradCAMGenerator()
        except Exception as e:
            logging.exception("GradCAM initialization failed.")
            self.gradcam = None

        logging.info("ExplainPipeline Initialized")

    def explain(self, image_path):

        try:
            prediction_result = self.predictor.predict(image_path)

            prediction = prediction_result["prediction"]

            heatmap_path = None

            # GradCAM should NEVER crash prediction
            if prediction == "PNEUMONIA" and self.gradcam is not None:
                try:
                    heatmap_path = self.gradcam.generate_heatmap(image_path)
                except Exception:
                    logging.exception("GradCAM generation failed.")
                    heatmap_path = None

            return {
                "status": "success",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "prediction": prediction,
                "confidence": prediction_result["confidence"],

                "normal_probability": prediction_result["normal_probability"],
                "pneumonia_probability": prediction_result["pneumonia_probability"],

                "heatmap": heatmap_path,

                "yolo": prediction_result.get("yolo_image"),

                "detections": prediction_result.get("detections", []),
                "num_detections": prediction_result.get("num_detections", 0),
                "avg_conf": prediction_result.get("avg_conf", 0),

                "inference_time": prediction_result.get("inference_time", 0),
            }

        except Exception as e:
            logging.exception("ExplainPipeline failed")
            raise CustomException(e, sys)