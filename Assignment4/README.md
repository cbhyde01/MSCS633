# MSCS633 Assignment 4 - Fraud Detection with PyOD AutoEncoder

This project trains an AutoEncoder anomaly detector (PyOD) on the Kaggle anonymized credit card fraud dataset.

## Files

- `fraud_detection_autoencoder.py` - Main Python source code
- `requirements.txt` - Manifest file with Python dependencies

## Dataset

Dataset source:

- https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

You can either:

1. Place `creditcard.csv` in the project root, or
2. Let the script auto-download it through `kagglehub`.

If you use auto-download, make sure your Kaggle credentials are configured.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python fraud_detection_autoencoder.py --epochs 20 --batch-size 256
```

Optional: disable auto-download and require local CSV path

```bash
python fraud_detection_autoencoder.py --data creditcard.csv --skip-download
```

## What the script does

1. Loads data and splits train/test using stratification.
2. Trains on non-fraud records only (unsupervised anomaly detection pattern).
3. Scales features with `StandardScaler`.
4. Trains `pyod.models.auto_encoder.AutoEncoder`.
5. Prints confusion matrix, classification report, ROC-AUC, and PR-AUC.

