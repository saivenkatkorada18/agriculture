"""
Model Evaluation and Metrics Reporting
--------------------------------------
Evaluates trained plant disease model against test dataset, generating:
- Overall Accuracy
- Precision, Recall, F1-Score per class
- Macro and Weighted Averages
- Confusion Matrix JSON / Array
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Any
import numpy as np

from ml.config.config import (
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    BATCH_SIZE,
    MODELS_DIR,
    DEFAULT_MODEL_WEIGHTS,
)


def evaluate_model(
    test_dir: str,
    model_path: Path = DEFAULT_MODEL_WEIGHTS,
    output_metrics_file: Path = MODELS_DIR / "evaluation_metrics.json",
) -> Dict[str, Any]:
    """
    Evaluates model performance and outputs JSON metrics.
    """
    try:
        import tensorflow as tf
        from sklearn.metrics import classification_report, confusion_matrix
    except ImportError:
        raise RuntimeError("TensorFlow and scikit-learn are required for model evaluation.")

    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(str(model_path))

    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.0)
    test_gen = test_datagen.flow_from_directory(
        test_dir,
        target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=False,
    )

    print("Running predictions on test set...")
    predictions = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(predictions, axis=1)
    y_true = test_gen.classes
    class_labels = list(test_gen.class_indices.keys())

    # Calculate metrics
    report_dict = classification_report(
        y_true,
        y_pred,
        target_names=class_labels,
        output_dict=True,
        zero_division=0,
    )

    conf_matrix = confusion_matrix(y_true, y_pred).tolist()

    overall_accuracy = report_dict.get("accuracy", 0.0)

    results = {
        "accuracy": round(float(overall_accuracy), 4),
        "macro_f1": round(float(report_dict.get("macro avg", {}).get("f1-score", 0.0)), 4),
        "weighted_f1": round(float(report_dict.get("weighted avg", {}).get("f1-score", 0.0)), 4),
        "class_report": report_dict,
        "confusion_matrix": conf_matrix,
        "class_names": class_labels,
        "total_test_samples": int(len(y_true)),
    }

    # Save to file
    output_metrics_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_metrics_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Overall Accuracy: {overall_accuracy * 100:.2f}%")
    print(f"Macro F1 Score:   {results['macro_f1']:.4f}")
    print(f"Weighted F1:      {results['weighted_f1']:.4f}")
    print(f"Saved complete evaluation report to: {output_metrics_file}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Soil & Crop Health Plant Disease Model")
    parser.add_argument("--test_dir", type=str, required=True, help="Path to test dataset directory")
    parser.add_argument("--model_path", type=str, default=str(DEFAULT_MODEL_WEIGHTS), help="Path to .h5 model file")
    parser.add_argument("--output", type=str, default=str(MODELS_DIR / "evaluation_metrics.json"))

    args = parser.parse_args()
    evaluate_model(
        test_dir=args.test_dir,
        model_path=Path(args.model_path),
        output_metrics_file=Path(args.output),
    )
