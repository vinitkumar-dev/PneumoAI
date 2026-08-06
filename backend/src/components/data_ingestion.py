import os
import sys
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:

    dataset_path = "dataset"

    yaml_file = os.path.join(
        dataset_path,
        "rsna.yaml"
    )

    train_images = os.path.join(
        dataset_path,
        "images",
        "train"
    )

    val_images = os.path.join(
        dataset_path,
        "images",
        "val"
    )

    test_images = os.path.join(
        dataset_path,
        "images",
        "test"
    )


class DataIngestion:

    def __init__(self):

        self.ingestion_config = (
            DataIngestionConfig()
        )

    def initiate_data_ingestion(self):

        logging.info(
            "YOLOv8 Data Ingestion Started"
        )

        try:

            yaml_file = (
                self.ingestion_config.yaml_file
            )

            train_images = (
                self.ingestion_config.train_images
            )

            val_images = (
                self.ingestion_config.val_images
            )

            test_images = (
                self.ingestion_config.test_images
            )

            if not os.path.exists(yaml_file):
                raise Exception(
                    f"YAML file not found: {yaml_file}"
                )

            if not os.path.exists(train_images):
                raise Exception(
                    f"Train images not found: {train_images}"
                )

            if not os.path.exists(val_images):
                raise Exception(
                    f"Validation images not found: {val_images}"
                )

            if not os.path.exists(test_images):
                logging.warning(
                    "Test folder not found"
                )

            logging.info(
                "YOLO Dataset Verified Successfully"
            )

            return yaml_file

        except Exception as e:

            raise CustomException(
                e,
                sys
            )