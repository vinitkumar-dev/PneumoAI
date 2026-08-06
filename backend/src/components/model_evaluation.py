import os
import sys

from dataclasses import dataclass

from ultralytics import YOLO

from src.exception import CustomException
from src.logger import logging


# =====================================
# CONFIG
# =====================================
@dataclass
class ModelEvaluationConfig:

    model_path = os.path.join(
        "artifacts",
        "yolov8",
        "model",
        "train",
        "weights",
        "best.pt"
    )



# =====================================
# EVALUATION
# =====================================
class ModelEvaluation:

    def __init__(self):

        self.config = (
            ModelEvaluationConfig()
        )

    def initiate_model_evaluation(
        self,
        yaml_path
    ):

        try:

            logging.info(
                "YOLOv8 Evaluation Started"
            )

            if not os.path.exists(
                self.config.model_path
            ):
                raise FileNotFoundError(
                    f"Model not found : "
                    f"{self.config.model_path}"
                )

            model = YOLO(
                self.config.model_path
            )

            results = model.val(
                data=yaml_path
            )

            metrics = {

                "mAP50":
                float(results.box.map50),

                "mAP50_95":
                float(results.box.map),

                "precision":
                float(results.box.mp),

                "recall":
                float(results.box.mr)
            }

            logging.info(
                f"mAP50 : "
                f"{metrics['mAP50']:.4f}"
            )

            logging.info(
                f"mAP50-95 : "
                f"{metrics['mAP50_95']:.4f}"
            )

            logging.info(
                f"Precision : "
                f"{metrics['precision']:.4f}"
            )

            logging.info(
                f"Recall : "
                f"{metrics['recall']:.4f}"
            )

            return metrics

        except Exception as e:

            raise CustomException(
                e,
                sys
            )