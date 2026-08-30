"""
Model Training Pipeline with Transfer Learning
-----------------------------------------------
Trains a MobileNetV2/EfficientNet classifier on agricultural crop disease images.
Includes EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, and history logging.
"""
import argparse
import json
import os
from pathlib import Path
import numpy as np

from ml.config.config import (
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    IMAGE_CHANNELS,
    BATCH_SIZE,
    EPOCHS,
    LEARNING_RATE,
    MODELS_DIR,
    DEFAULT_MODEL_WEIGHTS,
)
from ml.datasets.dataset_loader import verify_dataset_structure, create_data_generators


def build_transfer_learning_model(num_classes: int, architecture: str = "mobilenet_v2"):
    """
    Builds a transfer learning model with a pretrained backbone and custom classification head.
    """
    import tensorflow as tf
    from tensorflow.keras import layers, models

    input_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)

    if architecture == "mobilenet_v2":
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=input_shape,
            include_top=False,
            weights="imagenet",
        )
    elif architecture == "efficientnet_b0":
        base_model = tf.keras.applications.EfficientNetB0(
            input_shape=input_shape,
            include_top=False,
            weights="imagenet",
        )
    else:
        raise ValueError(f"Unsupported architecture: {architecture}")

    # Freeze base model weights for initial transfer learning
    base_model.trainable = False

    # Classification Head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(name="avg_pool"),
        layers.BatchNormalization(),
        layers.Dropout(0.3, name="top_dropout"),
        layers.Dense(256, activation="relu", name="dense_256"),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation="softmax", name="predictions"),
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")],
    )

    return model, base_model


def train(
    dataset_dir: str,
    output_model_path: Path = DEFAULT_MODEL_WEIGHTS,
    epochs: int = EPOCHS,
    batch_size: int = BATCH_SIZE,
    architecture: str = "mobilenet_v2",
):
    """
    Main training execution function.
    """
    import tensorflow as tf

    print("=" * 60)
    print("SOIL & CROP HEALTH ANALYZER — MODEL TRAINING PIPELINE")
    print("=" * 60)

    dataset_path = Path(dataset_dir)
    status = verify_dataset_structure(dataset_path)
    if not status["valid"]:
        print(f"[ERROR] {status['error']}")
        return

    num_classes = status["num_classes"]
    print(f"Found {status['total_images']} images across {num_classes} classes.")

    train_gen, val_gen = create_data_generators(
        str(dataset_path),
        batch_size=batch_size,
    )

    # Save class indices mapping
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    class_indices_file = MODELS_DIR / "class_indices.json"
    with open(class_indices_file, "w", encoding="utf-8") as f:
        json.dump(train_gen.class_indices, f, indent=2)
    print(f"Saved class index mappings to {class_indices_file}")

    print(f"Building {architecture} transfer learning model...")
    model, base_model = build_transfer_learning_model(num_classes, architecture=architecture)
    model.summary()

    # Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(output_model_path),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
    ]

    print(f"\nStarting training for {epochs} epochs...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=callbacks,
    )

    # Save training history metrics
    history_file = MODELS_DIR / "training_history.json"
    serializable_history = {k: [float(v) for v in vals] for k, vals in history.history.items()}
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(serializable_history, f, indent=2)
    print(f"Saved training history to {history_file}")

    print(f"\nModel training completed successfully! Best weights saved to: {output_model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Soil & Crop Health Plant Disease CNN Model")
    parser.add_argument("--dataset_dir", type=str, required=True, help="Path to dataset root folder")
    parser.add_argument("--epochs", type=int, default=EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--arch", type=str, default="mobilenet_v2", choices=["mobilenet_v2", "efficientnet_b0"])
    parser.add_argument("--output", type=str, default=str(DEFAULT_MODEL_WEIGHTS), help="Output weights file path")

    args = parser.parse_args()
    train(
        dataset_dir=args.dataset_dir,
        output_model_path=Path(args.output),
        epochs=args.epochs,
        batch_size=args.batch_size,
        architecture=args.arch,
    )
