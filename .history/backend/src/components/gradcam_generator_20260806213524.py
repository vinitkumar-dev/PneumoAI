# import os
# import sys
# import torch
# import cv2
# import numpy as np

# from PIL import Image
# from torchvision import models, transforms
# import torch.nn as nn

# from pytorch_grad_cam import GradCAM
# from pytorch_grad_cam.utils.image import show_cam_on_image

# from src.exception import CustomException
# from src.logger import logging


# class GradCAMGenerator:

#     def __init__(self):

#         self.device = torch.device(
#             "cuda" if torch.cuda.is_available() else "cpu"
#         )

#         self.model_path = os.path.join(
#             "artifacts",
#             "efficientnet_b0",
#             "model",
#             "model.pt"
#         )

#         self.transform = transforms.Compose([
#             transforms.Resize((224, 224)),
#             transforms.ToTensor(),
#             transforms.Normalize(
#                 [0.485, 0.456, 0.406],
#                 [0.229, 0.224, 0.225]
#             )
#         ])

#         self.model = self.load_model()

#     # =========================
#     # LOAD MODEL (FIXED)
#     # =========================
#     def load_model(self):

#         try:
#             logging.info("Loading GradCAM model...")

#             if not os.path.exists(self.model_path):
#                 raise FileNotFoundError(
#                     f"Model not found: {self.model_path}"
#                 )

#             checkpoint = torch.load(
#                 self.model_path,
#                 map_location=self.device
#             )

#             state_dict = (
#                 checkpoint["model_state_dict"]
#                 if isinstance(checkpoint, dict)
#                 else checkpoint
#             )

#             # ✅ MUST MATCH TRAINING MODEL (NO 512 LAYER)
#             model = models.efficientnet_b0(weights=None)

#             in_features = model.classifier[1].in_features

#             model.classifier = nn.Sequential(
#                 nn.Dropout(0.5),
#                 nn.Linear(in_features, 2)
#             )

#             model.load_state_dict(state_dict, strict=True)

#             model.to(self.device)
#             model.eval()

#             logging.info("GradCAM model loaded successfully")

#             return model

#         except Exception as e:
#             logging.error(f"Model loading failed: {e}")
#             raise CustomException(e, sys)

#     # =========================
#     # GRADCAM GENERATION
#     # =========================
#     def generate_heatmap(self, image_path):

#         try:
#             logging.info(f"Generating GradCAM for: {image_path}")

#             image = Image.open(image_path).convert("RGB")

#             rgb_img = np.array(
#                 image.resize((224, 224))
#             ).astype(np.float32) / 255.0

#             input_tensor = self.transform(image).unsqueeze(0).to(self.device)

#             # ✅ CORRECT FOR EFFICIENTNET
#             target_layers = [self.model.features[-1]]

#             cam = GradCAM(
#                 model=self.model,
#                 target_layers=target_layers
#             )

#             grayscale_cam = cam(input_tensor=input_tensor)[0]

#             visualization = show_cam_on_image(
#                 rgb_img,
#                 grayscale_cam,
#                 use_rgb=True
#             )

#             save_dir = os.path.join(
#                 "artifacts",
#                 "efficientnet_b0",
#                 "plots"
#             )

#             os.makedirs(save_dir, exist_ok=True)

#             filename = os.path.splitext(
#                 os.path.basename(image_path)
#             )[0] + "_gradcam.jpg"

#             output_path = os.path.join(save_dir, filename)

#             cv2.imwrite(
#                 output_path,
#                 cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR)
#             )

#             logging.info(f"GradCAM saved at: {output_path}")

#             return output_path

#         except Exception as e:
#             logging.error(f"GradCAM failed: {e}")
#             raise CustomException(e, sys)