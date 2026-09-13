import os
import sys
import time
from datetime import datetime

import torch
import torch.nn as nn

from PIL import Image
from torchvision import transforms, models

from src.exception import CustomException
from src.logger import logging


class PredictionPipeline:
    """
    Loads the trained EfficientNet-B0 checkpoint and classifies a chest
    X-ray image as NORMAL or PNEUMONIA.
    """

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

            # Lazy loaded on first use.
            self.model = None

        except Exception as e:
            raise CustomException(e, sys)

    def load_model(self):

        if self.model is not None:
            return self.model

        logging.info("Loading EfficientNet model")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model checkpoint not found at '{self.model_path}'. "
                f"Make sure artifacts/efficientnet_b0/model/model.pt is "
                f"present in the deployed repository (it must NOT be "
                f"excluded by .gitignore)."
            )

        checkpoint = torch.load(
            self.model_path,
            map_location=self.device
        )

        state_dict = (
            checkpoint["model_state_dict"]
            if isinstance(checkpoint, dict)
            else checkpoint
        )

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

        logging.info("EfficientNet loaded")

        return model

    def predict(self, image_path):

        try:
            model = self.load_model()

            image = Image.open(image_path).convert("RGB")

            tensor = self.transform(image)

            tensor = tensor.unsqueeze(0).to(self.device)

            start = time.perf_counter()

            with torch.no_grad():

                outputs = model(tensor)

                probs = torch.softmax(outputs, dim=1)

                confidence, predicted = torch.max(probs, 1)

            inference_time = round(
                (time.perf_counter() - start) * 1000,
                2
            )

            prediction = (
                "NORMAL"
                if predicted.item() == 0
                else "PNEUMONIA"
            )

            # Values below are on a 0-100 percentage scale and clamped so
            # rounding artifacts can never push them past the valid range.
            confidence_pct = max(0.0, min(100.0, round(float(confidence.item()) * 100, 2)))
            normal_pct = max(0.0, min(100.0, round(float(probs[0][0]) * 100, 2)))
            pneumonia_pct = max(0.0, min(100.0, round(float(probs[0][1]) * 100, 2)))

            return {

                "prediction": prediction,

                "confidence": confidence_pct,

                "normal_probability": normal_pct,

                "pneumonia_probability": pneumonia_pct,

                "inference_time": inference_time,

                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        except Exception as e:

            logging.exception("Prediction failed")

            raise CustomException(e, sys)
