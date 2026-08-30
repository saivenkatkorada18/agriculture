"""
Machine Learning & Computer Vision Configuration
"""
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ML_DIR = BASE_DIR / "ml"
MODELS_DIR = ML_DIR / "models"
DATASETS_DIR = ML_DIR / "datasets"

# Image Preprocessing & Model Input Dimensions
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 224
IMAGE_CHANNELS = 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)

# Training Hyperparameters
BATCH_SIZE = 32
EPOCHS = 25
LEARNING_RATE = 0.0001
VALIDATION_SPLIT = 0.20
TEST_SPLIT = 0.10
RANDOM_STATE = 42

# Decision & Confidence Thresholds
CONFIDENCE_THRESHOLD = 0.60  # Predictions below 60% trigger low-confidence alert
TOP_K_PREDICTIONS = 3

# Supported Agricultural Crop & Disease Classes
SUPPORTED_CLASSES: List[str] = [
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___healthy",
    "Tomato___Leaf_Mold",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___healthy",
    "Grape___Black_rot",
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
]

# Model Architecture Choice: "mobilenet_v2" | "efficientnet_b0" | "resnet50"
DEFAULT_ARCHITECTURE = "mobilenet_v2"
DEFAULT_MODEL_WEIGHTS = MODELS_DIR / "plant_disease_mobilenetv2.h5"
DISEASE_INFO_PATH = MODELS_DIR / "disease_info.json"
