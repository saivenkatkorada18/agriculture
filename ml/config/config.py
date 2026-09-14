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

# Supported Agricultural Crop & Disease Classes (38 total classes)
SUPPORTED_CLASSES: List[str] = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

# Model Architecture Choice: "mobilenet_v2" | "efficientnet_b0" | "resnet50"
DEFAULT_ARCHITECTURE = "mobilenet_v2"
DEFAULT_MODEL_WEIGHTS = MODELS_DIR / "plant_disease_model.keras"
DISEASE_INFO_PATH = MODELS_DIR / "disease_info.json"
CLASS_INDICES_PATH = MODELS_DIR / "class_indices.json"
