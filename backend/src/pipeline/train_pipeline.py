import os
import sys
import json

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation

from src.exception import CustomException
from src.logger import logging


class TrainingPipeline:

    def start_training_pipeline(self):

        try:

            logging.info(
                "Training Pipeline Started"
            )

            # ==================================
            # DATA INGESTION
            # ==================================
            ingestion = DataIngestion()

            yaml_path = (
                ingestion
                .initiate_data_ingestion()
            )

            logging.info(
                f"Dataset YAML: {yaml_path}"
            )

            # ==================================
            # DATA TRANSFORMATION
            # ==================================
            transformation = (
                DataTransformation()
            )

            dataset_info = (
                transformation
                .initiate_data_transformation(
                    yaml_path
                )
            )

            logging.info(
                "Data Transformation Completed"
            )

            # ==================================
            # MODEL TRAINING
            # ==================================
            trainer = ModelTrainer()

            model_path = (
                trainer
                .initiate_model_training(
                    dataset_info["yaml_path"]
                )
            )

            logging.info(
                f"Best Model Saved At: {model_path}"
            )

            # ==================================
            # MODEL EVALUATION
            # ==================================
            evaluator = (
                ModelEvaluation()
            )

            metrics = (
                evaluator
                .initiate_model_evaluation(
                    dataset_info["yaml_path"]
                )
            )

            logging.info(
                f"Evaluation Metrics: {metrics}"
            )

            # ==================================
            # SAVE METRICS
            # ==================================
            model_name = "yolov8"

            metrics_dir = os.path.join(
                "artifacts",
                model_name,
                "metrics"
            )

            os.makedirs(
                metrics_dir,
                exist_ok=True
            )

            metrics_file = os.path.join(
                metrics_dir,
                "metrics.json"
            )

            with open(
                metrics_file,
                "w"
            ) as f:

                json.dump(
                    metrics,
                    f,
                    indent=4
                )

            logging.info(
                f"Metrics Saved: {metrics_file}"
            )

            # ==================================
            # LEADERBOARD
            # ==================================
            leaderboard_file = os.path.join(
                "artifacts",
                "leaderboard.json"
            )

            entry = {

                "model":
                model_name,

                "mAP50":
                metrics["mAP50"],

                "mAP50_95":
                metrics["mAP50_95"],

                "precision":
                metrics["precision"],

                "recall":
                metrics["recall"]
            }

            if os.path.exists(
                leaderboard_file
            ):

                with open(
                    leaderboard_file,
                    "r"
                ) as f:

                    leaderboard = json.load(f)

            else:

                leaderboard = []

            leaderboard.append(
                entry
            )

            with open(
                leaderboard_file,
                "w"
            ) as f:

                json.dump(
                    leaderboard,
                    f,
                    indent=4
                )

            logging.info(
                "Leaderboard Updated"
            )

            logging.info(
                "Training Pipeline Completed Successfully"
            )

            # print(metrics)

            return model_path

        except Exception as e:

            logging.error(
                f"Training Pipeline Failed: {e}"
            )

            raise CustomException(
                e,
                sys
            )