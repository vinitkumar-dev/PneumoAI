import os
import sys
import time

import torch
import torch.nn as nn

from PIL import Image
from torchvision import transforms
from torchvision import models

from ultralytics import YOLO

from src.exception import CustomException
from src.logger import logging


class PredictionPipeline:

    def __init__(self):

        try:

            self.device = torch.device(
                "cuda" if torch.cuda.is_available()
                else "cpu"
            )

            logging.info(
                f"Device: {self.device}"
            )


            self.transform = transforms.Compose([
                transforms.Resize((224,224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    [0.485,0.456,0.406],
                    [0.229,0.224,0.225]
                )
            ])


            self.model_path = os.path.join(
                "artifacts",
                "efficientnet_b0",
                "model",
                "model.pt"
            )


            self.model = None


            # ============================
            # YOLO SETUP
            # ============================

            self.yolo_model = None

            self.yolo_path = os.path.join(
                "artifacts",
                "yolo"
            )

            os.makedirs(
                self.yolo_path,
                exist_ok=True
            )


        except Exception as e:
            raise CustomException(e,sys)



    def load_model(self):

        if self.model:
            return self.model


        checkpoint = torch.load(
            self.model_path,
            map_location=self.device
        )


        state_dict = (
            checkpoint["model_state_dict"]
            if isinstance(checkpoint,dict)
            else checkpoint
        )


        model = models.efficientnet_b0(
            weights=None
        )


        in_features = (
            model.classifier[1].in_features
        )


        model.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(
                in_features,
                2
            )
        )


        model.load_state_dict(
            state_dict
        )


        model.to(
            self.device
        )


        model.eval()


        self.model=model


        return model



    def load_yolo(self):

        if self.yolo_model:
            return self.yolo_model


        try:

            # optional YOLO model
            self.yolo_model = YOLO(
                "yolov8n.pt"
            )

            return self.yolo_model


        except Exception as e:

            logging.warning(
                "YOLO loading failed"
            )

            return None



    def run_yolo(self,image_path):

        try:

            model = self.load_yolo()


            if model is None:
                return None,[],0


            results = model(
                image_path,
                verbose=False
            )


            if not results:
                return None,[],0


            result = results[0]


            filename = (
                os.path.splitext(
                    os.path.basename(image_path)
                )[0]
                +
                "_yolo.jpeg"
            )


            save_path=os.path.join(
                self.yolo_path,
                filename
            )


            plotted = result.plot()


            Image.fromarray(
                plotted
            ).save(
                save_path
            )


            detections=[]


            if result.boxes:

                for box in result.boxes:

                    detections.append({
                        "confidence":
                        float(
                            box.conf[0]
                        )
                    })


            return (
                save_path,
                detections,
                len(detections)
            )


        except Exception as e:

            logging.exception(
                "YOLO failed"
            )

            return None,[],0





    def predict(self,image_path):

        try:

            model=self.load_model()


            image=Image.open(
                image_path
            ).convert("RGB")


            tensor=self.transform(
                image
            )


            tensor=tensor.unsqueeze(0).to(
                self.device
            )


            start=time.perf_counter()


            with torch.no_grad():

                outputs=model(
                    tensor
                )

                probs=torch.softmax(
                    outputs,
                    dim=1
                )

                confidence,predicted=torch.max(
                    probs,
                    1
                )


            inference_time=round(
                (time.perf_counter()-start)*1000,
                2
            )


            prediction=(
                "NORMAL"
                if predicted.item()==0
                else
                "PNEUMONIA"
            )


            # =============================
            # RUN YOLO
            # =============================

            yolo_image,detections,count = (
                self.run_yolo(
                    image_path
                )
            )


            return {

                "prediction":
                prediction,


                "confidence":
                float(
                    confidence.item()
                ),


                "normal_probability":
                float(
                    probs[0][0]
                ),


                "pneumonia_probability":
                float(
                    probs[0][1]
                ),


                "detections":
                detections,


                "num_detections":
                count,


                "avg_conf":
                (
                    sum(
                        d["confidence"]
                        for d in detections
                    )/len(detections)
                    if detections
                    else 0
                ),


                "yolo_image":
                yolo_image,


                "inference_time":
                inference_time

            }


        except Exception as e:

            raise CustomException(
                e,
                sys
            )