import os
import sys
import time

import torch
import torch.nn as nn

from PIL import Image
from torchvision import transforms
from torchvision import models

from src.exception import CustomException
from src.logger import logging


class PredictionPipeline:

    def __init__(self):

        try:
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )

            logging.info(f"Device: {self.device}")

            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    [0.485, 0.456, 0.406],
                    [0.229, 0.224, 0.225]
                )
            ])

            self.model_path = os.path.join(
                "artifacts",
                "efficientnet_b0",
                "model",
                "model.pt"
            )

            self.model = None

        except Exception as e:
            raise CustomException(e, sys)

    def load_model(self):

        if self.model is not None:
            return self.model

        checkpoint = torch.load(
            self.model_path,
            map_location=self.device
        )

        state_dict = checkpoint["model_state_dict"] if isinstance(checkpoint, dict) else checkpoint

        model = models.efficientnet_b0(weights=None)

        in_features = model.classifier[1].in_features

        model.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(in_features, 2)
        )

        model.load_state_dict(state_dict)

        model.to(self.device)
        model.eval()

        self.model = model

        return model

    def predict(self, image_path):

        try:

            model = self.load_model()

            image = Image.open(image_path).convert("RGB")

            image = self.transform(image)

            image = image.unsqueeze(0).to(self.device)

            start = time.perf_counter()

            with torch.no_grad():

                outputs = model(image)

                probs = torch.softmax(outputs, dim=1)

                confidence, predicted = torch.max(probs, 1)

            inference_time = round(
                (time.perf_counter() - start) * 1000,
                2
            )

            normal_prob = float(probs[0][0])

            pneumonia_prob = float(probs[0][1])

            prediction = (
                "NORMAL"
                if predicted.item() == 0
                else "PNEUMONIA"
            )

            return {

                "prediction": prediction,

                "confidence": float(confidence.item()),

                "normal_probability": normal_prob,

                "pneumonia_probability": pneumonia_prob,

                "detections": [],

                "num_detections": 0,

                "avg_conf": 0,

                "yolo_image": None,

                "inference_time": inference_time

            }

        except Exception as e:
            raise CustomException(e, sys)