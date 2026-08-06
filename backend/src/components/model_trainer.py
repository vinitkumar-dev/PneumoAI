import os
import sys

from dataclasses import dataclass

from ultralytics import YOLO

from src.exception import CustomException
from src.logger import logging


# ==================================
# CONFIG
# ==================================
@dataclass
class ModelTrainerConfig:

    trained_model_path = os.path.join(
        "artifacts",
        "yolov8",
        "model"
    )


# ==================================
# TRAINER
# ==================================
class ModelTrainer:

    def __init__(self):

        self.model_trainer_config = (
            ModelTrainerConfig()
        )

    def initiate_model_training(
        self,
        yaml_path
    ):

        try:

            logging.info(
                "YOLOv8 Training Started"
            )

            os.makedirs(
                self.model_trainer_config.trained_model_path,
                exist_ok=True
            )

            # ==================================
            # CHECK IF MODEL ALREADY EXISTS
            # ==================================
            existing_model_path = os.path.join(
                self.model_trainer_config.trained_model_path,
                "train",
                "weights",
                "best.pt"
            )

            if os.path.exists(existing_model_path):

                logging.info(
                    f"Model already exists: {existing_model_path}"
                )

                logging.info(
                    "Skipping training..."
                )

                return existing_model_path

            # ==================================
            # LOAD PRETRAINED YOLO MODEL
            # ==================================
            model = YOLO(
                "yolov8n.pt"
            )

            logging.info(
                "YOLOv8 Model Loaded"
            )

            # ==================================
            # TRAIN MODEL
            # ==================================
            results = model.train(

                data=yaml_path,

                epochs=50,

                imgsz=640,

                batch=16,

                project=self.model_trainer_config.trained_model_path,

                name="train",

                exist_ok=True,

                pretrained=True,

                patience=10,

                save=True
            )

            logging.info(
                "Training Completed"
            )

            # ==================================
            # GET ACTUAL SAVE DIRECTORY
            # ==================================
            best_model_path = os.path.join(
                results.save_dir,
                "weights",
                "best.pt"
            )

            if not os.path.exists(best_model_path):

                raise FileNotFoundError(
                    f"best.pt not found at {best_model_path}"
                )

            logging.info(
                f"Best Model Saved At: {best_model_path}"
            )

            return best_model_path

        except Exception as e:

            raise CustomException(
                e,
                sys
            )