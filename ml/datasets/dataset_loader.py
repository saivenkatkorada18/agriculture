"""
Agricultural Dataset Loader & Splitter
--------------------------------------
Loads directory-based crop disease datasets (such as PlantVillage or Kaggle Plant Pathology)
and prepares train, validation, and test data generators or datasets.
"""
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List
import os

from ml.config.config import (
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    BATCH_SIZE,
    VALIDATION_SPLIT,
    TEST_SPLIT,
    RANDOM_STATE,
    SUPPORTED_CLASSES,
)


def verify_dataset_structure(dataset_dir: Path) -> Dict[str, Any]:
    """
    Scans dataset directory for class subfolders and sample counts.
    """
    if not dataset_dir.exists():
        return {
            "valid": False,
            "error": f"Dataset directory '{dataset_dir}' does not exist.",
            "classes": {},
            "total_images": 0,
        }

    class_counts = {}
    total_images = 0
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}

    for item in dataset_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            count = sum(1 for f in item.iterdir() if f.is_file() and f.suffix.lower() in valid_exts)
            class_counts[item.name] = count
            total_images += count

    if total_images == 0:
        return {
            "valid": False,
            "error": f"No valid images found in subdirectories of '{dataset_dir}'.",
            "classes": class_counts,
            "total_images": 0,
        }

    return {
        "valid": True,
        "classes": class_counts,
        "total_images": total_images,
        "num_classes": len(class_counts),
    }


def create_data_generators(
    dataset_dir: str,
    target_size: Tuple[int, int] = (IMAGE_HEIGHT, IMAGE_WIDTH),
    batch_size: int = BATCH_SIZE,
    val_split: float = VALIDATION_SPLIT,
):
    """
    Creates augmented training and validation data generators via Keras ImageDataGenerator.
    """
    try:
        import tensorflow as tf
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
    except ImportError:
        raise RuntimeError("TensorFlow is required to instantiate Keras data generators.")

    # Training augmentation: rotation, zoom, horizontal flip, shear, brightness
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=val_split,
    )

    # Validation only receives normalization
    val_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=val_split,
    )

    train_gen = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="training",
        shuffle=True,
        seed=RANDOM_STATE,
    )

    val_gen = val_datagen.flow_from_directory(
        dataset_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation",
        shuffle=False,
        seed=RANDOM_STATE,
    )

    return train_gen, val_gen
