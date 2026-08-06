import os
import sys
import cv2
import torch
import torch.nn as nn

from PIL import Image
from torchvision import transforms
from torchvision import models
from ultralytics import YOLO

from src.exception import CustomException
from src.logger import logging

import time


class PredictionPipeline:

    def __init__(self):

        try:
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )

            logging.info(f"Device set to: {self.device}")

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

            self.yolo_model_path = os.path.join(
                "artifacts",
                "yolov8",
                "model",
                "train",
                "weights",
                "best.pt"
            )

            # ❌ DO NOT LOAD HERE (IMPORTANT FIX)
            self.model = None
            self.yolo_model = None

            logging.info("PredictionPipeline initialized (lazy loading mode)")

        except Exception as e:
            raise CustomException(e, sys)

    # =========================
    # LOAD CLASSIFICATION MODEL
    # =========================
    def load_model(self):
        import torch

        if self.model is not None:
            return self.model

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

        model.load_state_dict(state_dict, strict=True)
        model.to(self.device)
        model.eval()

        self.model = model
        return model

    # =========================
    # LOAD YOLO MODEL
    # =========================
    def load_yolo_model(self):

        if self.yolo_model is not None:
            return self.yolo_model

        if not os.path.exists(self.yolo_model_path):
            raise FileNotFoundError(self.yolo_model_path)

        model = YOLO(self.yolo_model_path)

        self.yolo_model = model
        return model

    # =========================
    # DETECTION
    # =========================
    def detect_pneumonia_region(self, image_path, save_path):

        yolo = self.load_yolo_model()

        results = yolo(image_path, conf=0.25)

        detections = []

        img = cv2.imread(image_path)

        for result in results:
            for box in result.boxes:

                coords = box.xyxy[0].cpu().tolist()
                x1, y1, x2, y2 = coords
                conf = float(box.conf[0].item())

                detections.append({
                    "bbox": [
                        round(x1, 2),
                        round(y1, 2),
                        round(x2, 2),
                        round(y2, 2)
                    ],
                    "confidence": round(conf, 4)
                })

                cv2.rectangle(
                    img,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    img,
                    f"{conf:.2f}",
                    (int(x1), int(y1) - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1
                )

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        cv2.imwrite(save_path, img)

        return detections

    # =========================
    # PREDICT
    # =========================
    def predict(self, image_path):

        try:
            model = self.load_model()

            image = Image.open(image_path).convert("RGB")
            image = self.transform(image)
            image = image.unsqueeze(0).to(self.device)

            start_time = time.perf_counter()

            with torch.no_grad():
                outputs = model(image)
                probs = torch.softmax(outputs, dim=1)

                confidence, predicted = torch.max(probs, 1)

            
            inference_time = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

            normal_prob = float(probs[0][0])
            pneumonia_prob = float(probs[0][1])

            predicted_class = (
                "NORMAL"
                if predicted.item() == 0
                else "PNEUMONIA"
            )

            detections = []
            avg_conf = 0.0
            yolo_image_path = None

            if predicted_class == "PNEUMONIA":

                filename = os.path.basename(image_path)

                yolo_image_path = os.path.join(
                    "artifacts",
                    "yolo",
                    f"yolo_{filename}"
                )

                detections = self.detect_pneumonia_region(
                    image_path,
                    yolo_image_path
                )

                if len(detections) > 0:
                    avg_conf = sum(
                        d["confidence"] for d in detections
                    ) / len(detections)

            return {
                "prediction": predicted_class,
                "confidence": round(float(confidence.item()), 4),

                "normal_probability": round(normal_prob, 2),
                "pneumonia_probability": round(pneumonia_prob, 2),

                "detections": detections,
                "num_detections": len(detections),
                "avg_conf": round(avg_conf, 4),

                "yolo_image": yolo_image_path,
                "inference_time": inference_time
            }

        except Exception as e:
            raise CustomException(e, sys)