"""
Train a plant disease classifier on the PlantVillage dataset (38 classes).
Run this inside Antigravity (or any environment with TensorFlow + GPU access).

Steps this script performs:
1. Loads the PlantVillage dataset (folder of class-named subfolders of images)
2. Builds a MobileNetV2 transfer-learning model
3. Trains in two phases: frozen backbone, then fine-tuned top layers
4. Saves the final model as plant_disease_model.keras + class_indices.json

BEFORE RUNNING:
- Download and extract the dataset so you have a folder structure like:
    PlantVillage/
        Apple___Apple_scab/
            image1.jpg
            image2.jpg
        Apple___Black_rot/
            ...
        ... (38 folders total)

  Easiest way to get it in that shape:
    pip install datasets
    python -c "
from datasets import load_dataset
import os
from PIL import Image

ds = load_dataset('mohanty/PlantVillage', split='train')
out_dir = 'PlantVillage'
os.makedirs(out_dir, exist_ok=True)
counts = {}
for i, item in enumerate(ds):
    label = item['label'] if isinstance(item['label'], str) else ds.features['label'].int2str(item['label'])
    class_dir = os.path.join(out_dir, label)
    os.makedirs(class_dir, exist_ok=True)
    counts[label] = counts.get(label, 0) + 1
    img = item['image']
    img.save(os.path.join(class_dir, f'{counts[label]}.jpg'))
print('Done extracting', len(counts), 'classes')
"
"""

import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.applications import MobileNetV2

# ---------------------- CONFIG ----------------------
TRAIN_DIR = "ml/datasets/plant_village/New Plant Diseases Dataset(Augmented)/train"
VAL_DIR = "ml/datasets/plant_village/New Plant Diseases Dataset(Augmented)/valid"
IMG_SIZE = (224, 224)
BATCH_SIZE = 64
INITIAL_EPOCHS = 3                # phase 1: frozen backbone fine-tuning
FINE_TUNE_EPOCHS = 3               # phase 2: top layer fine-tuning
FINE_TUNE_AT_LAYER = 100           # unfreeze from this layer index onward
OUTPUT_MODEL_PATH = "ml/models/plant_disease_model.keras"
OUTPUT_CLASSES_PATH = "ml/models/class_indices.json"
# ------------------------------------------------------

def build_datasets():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        TRAIN_DIR,
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        VAL_DIR,
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )
    class_names = train_ds.class_names

    # Normalize pixel values to [0, 1] — MUST match what your inference code does later
    normalization_layer = layers.Rescaling(1.0 / 255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

    # Prefetch for speed (image_dataset_from_directory already shuffles natively)
    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

    return train_ds, val_ds, class_names


def build_augmentation():
    return tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.15),
        layers.RandomContrast(0.1),
        layers.RandomTranslation(0.1, 0.1),
    ])


def build_model(num_classes):
    base_model = MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False  # freeze for phase 1

    augmentation = build_augmentation()

    inputs = tf.keras.Input(shape=(*IMG_SIZE, 3))
    x = augmentation(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs)
    return model, base_model


def main():
    train_ds, val_ds, class_names = build_datasets()
    num_classes = len(class_names)
    print(f"Found {num_classes} classes: {class_names}")

    model, base_model = build_model(num_classes)

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(factor=0.3, patience=2),
        tf.keras.callbacks.ModelCheckpoint(
            "best_phase1.keras", save_best_only=True, monitor="val_accuracy"
        ),
    ]

    print("\n=== Phase 1: training top layers (backbone frozen) ===")
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=INITIAL_EPOCHS,
        callbacks=callbacks,
    )

    print("\n=== Phase 2: fine-tuning top backbone layers ===")
    base_model.trainable = True
    for layer in base_model.layers[:FINE_TUNE_AT_LAYER]:
        layer.trainable = False

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),  # much lower LR for fine-tuning
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks_ft = [
        tf.keras.callbacks.EarlyStopping(patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(factor=0.3, patience=2),
        tf.keras.callbacks.ModelCheckpoint(
            OUTPUT_MODEL_PATH, save_best_only=True, monitor="val_accuracy"
        ),
    ]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=FINE_TUNE_EPOCHS,
        callbacks=callbacks_ft,
    )

    # Final save (in case checkpoint above didn't trigger on the last epoch)
    model.save(OUTPUT_MODEL_PATH)

    # Save class index mapping — REQUIRED for correct inference later
    class_indices = {str(i): name for i, name in enumerate(class_names)}
    with open(OUTPUT_CLASSES_PATH, "w") as f:
        json.dump(class_indices, f, indent=2)

    print(f"\nSaved model to {OUTPUT_MODEL_PATH}")
    print(f"Saved class mapping to {OUTPUT_CLASSES_PATH}")

    # Quick validation report
    val_loss, val_acc = model.evaluate(val_ds)
    print(f"\nFinal validation accuracy: {val_acc:.4f}")
    print(f"Final validation loss: {val_loss:.4f}")


if __name__ == "__main__":
    main()
