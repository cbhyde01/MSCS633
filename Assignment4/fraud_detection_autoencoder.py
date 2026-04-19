"""Fraud Detection with PyOD AutoEncoder.

This script trains an AutoEncoder-based anomaly detector using the
Kaggle credit card fraud dataset (creditcard.csv).

Dataset reference:
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from pyod.models.auto_encoder import AutoEncoder
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Train a PyOD AutoEncoder for credit card fraud detection."
    )
    parser.add_argument(
        "--data",
        type=str,
        default="creditcard.csv",
        help="Path to Kaggle credit card dataset CSV file.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.30,
        help="Test split size (default: 0.30).",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=20,
        help="Number of training epochs for the AutoEncoder.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=256,
        help="Training batch size.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help=(
            "Do not auto-download from KaggleHub if --data is missing. "
            "By default, the script will try to download the dataset."
        ),
    )
    return parser.parse_args()


def load_data(csv_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load and validate dataset."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    df = pd.read_csv(csv_path)
    if "Class" not in df.columns:
        raise ValueError("Expected target column 'Class' in dataset.")

    x = df.drop(columns=["Class"]).to_numpy(dtype=np.float32)
    y = df["Class"].to_numpy(dtype=np.int32)
    return x, y


def resolve_data_path(data_arg: str, try_download: bool) -> Path:
    """Resolve the dataset path, downloading via KaggleHub if needed."""
    csv_path = Path(data_arg)
    if csv_path.exists():
        return csv_path

    if not try_download:
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    try:
        import kagglehub  # Imported lazily so local CSV can run without this package.
    except ImportError as exc:
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}. Install kagglehub or provide --data path."
        ) from exc

    print("Local dataset not found. Downloading from KaggleHub...")
    dataset_dir = Path(kagglehub.dataset_download("mlg-ulb/creditcardfraud"))

    candidate = dataset_dir / "creditcard.csv"
    if candidate.exists():
        print(f"Dataset downloaded to: {candidate}")
        return candidate

    matches = list(dataset_dir.rglob("creditcard.csv"))
    if matches:
        print(f"Dataset found at: {matches[0]}")
        return matches[0]

    raise FileNotFoundError(
        "KaggleHub download completed, but creditcard.csv was not found in the dataset folder."
    )


def main() -> None:
    """Train and evaluate the fraud detection model."""
    args = parse_args()

    data_path = resolve_data_path(args.data, try_download=not args.skip_download)
    x, y = load_data(data_path)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    # Train only on non-fraud samples for unsupervised anomaly learning.
    x_train_normal = x_train[y_train == 0]

    scaler = StandardScaler()
    x_train_normal_scaled = scaler.fit_transform(x_train_normal)
    x_test_scaled = scaler.transform(x_test)

    contamination = max(float(np.mean(y_train)), 1e-4)

    model = AutoEncoder(
        hidden_neuron_list=[64, 32, 32, 64],
        contamination=contamination,
        epoch_num=args.epochs,
        batch_size=args.batch_size,
        preprocessing=False,  # We already scaled manually.
        random_state=args.random_state,
        verbose=1,
    )

    model.fit(x_train_normal_scaled)

    y_pred = model.predict(x_test_scaled)
    anomaly_scores = model.decision_function(x_test_scaled)

    print("\n=== Fraud Detection Results (AutoEncoder / PyOD) ===")
    print(f"Train size: {len(x_train):,}")
    print(f"Test size:  {len(x_test):,}")
    print(f"Fraud ratio in test set: {np.mean(y_test):.4f}")

    print("\nConfusion Matrix [TN FP; FN TP]:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=4))

    roc_auc = roc_auc_score(y_test, anomaly_scores)
    pr_auc = average_precision_score(y_test, anomaly_scores)
    print(f"ROC-AUC (scores): {roc_auc:.4f}")
    print(f"PR-AUC  (scores): {pr_auc:.4f}")


if __name__ == "__main__":
    main()
