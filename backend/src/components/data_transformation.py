import os
import sys

from src.exception import CustomException
from src.logger import logging


class DataTransformation:

    def __init__(self):

        self.img_size = 640

    def initiate_data_transformation(
        self,
        yaml_path
    ):

        try:

            logging.info(
                "YOLOv8 Data Transformation Started"
            )

            if not os.path.exists(yaml_path):

                raise Exception(
                    f"YAML file not found : {yaml_path}"
                )

            logging.info(
                f"Dataset Config : {yaml_path}"
            )

            logging.info(
                f"Image Size : {self.img_size}"
            )

            logging.info(
                "YOLOv8 handles augmentations automatically"
            )

            logging.info(
                "Data Transformation Completed"
            )

            return {
                "yaml_path": yaml_path,
                "img_size": self.img_size
            }

        except Exception as e:

            raise CustomException(
                e,
                sys
            )