# ML Pipeline & Inference Conventions

## Architecture & Code Organization
- `ml/config/`: Configuration for image size (e.g. 224x224), batch sizes, classes, learning rate.
- `ml/preprocessing/`: OpenCV & PIL image normalization, CLAHE enhancement, tensor conversions.
- `ml/datasets/`: Dataset folder loader, train/val/test splits, balanced augmentation.
- `ml/training/`: Training script with MobileNetV2/EfficientNet transfer learning backbone, callbacks (`EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`).
- `ml/evaluation/`: Metrics generation (Accuracy, Precision, Recall, F1, Confusion Matrix).
- `ml/inference/`: Prediction engine with confidence score calibration and top-k output.

## Non-Negotiable Constraints
1. Never fabricate fake high-confidence prediction values.
2. Low-confidence threshold is set at `< 0.60`. Any prediction below this must trigger a warning state.
3. Soil analysis is strictly visual surface estimation (moisture index, surface cracking contours, color space classification, organic coverage score). Never claim laboratory chemical NPK/pH values from plain RGB images.
