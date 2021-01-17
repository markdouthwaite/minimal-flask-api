import time
import json
from datetime import datetime
from typing import Optional, List, Any

import fire
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score


np.random.seed(42)

TIMESTAMP_FMT = "%m-%d-%Y, %H:%M:%S"

LABEL: str = "target"

NUMERIC_FEATURES: List[str] = [
    "age",
    "trestbps",
    "chol",
    "fbs",
    "thalach",
    "exang",
    "oldpeak",
]

CATEGORICAL_FEATURES: List[str] = ["sex", "cp", "restecg", "ca", "slope", "thal"]


def create_pipeline(
    categorical_features: List[str], numeric_features: List[str]
) -> Pipeline:

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    return Pipeline(
        steps=[("preprocessor", preprocessor), ("classifier", LogisticRegression())]
    )


def train(
    path: str,
    test_size: float = 0.2,
    dump: bool = True,
    categorical_features: Optional[List[str]] = None,
    numeric_features: Optional[List[str]] = None,
    label: Optional[str] = None,
    **kwargs: Optional[Any],
) -> None:

    start = time.time()

    if categorical_features is None:
        categorical_features = CATEGORICAL_FEATURES

    if numeric_features is None:
        numeric_features = NUMERIC_FEATURES

    if label is None:
        label = LABEL

    df = pd.read_csv(path, **kwargs)

    features = df[[*categorical_features, *numeric_features]]
    target = df[label]

    tx, vx, ty, vy = train_test_split(features, target, test_size=test_size)

    model = create_pipeline(
        categorical_features=categorical_features, numeric_features=numeric_features
    )
    model.fit(tx, ty)

    end = time.time()

    acc = accuracy_score(model.predict(tx), ty) * 100
    val_acc = accuracy_score(model.predict(vx), vy) * 100
    roc_auc = roc_auc_score(vy, model.predict_proba(vx)[:, -1])

    print(f"Training accuracy: {acc:.2f}%")
    print(f"Validation accuracy: {val_acc:.2f}%")
    print(f"ROC AUC score: {roc_auc:.2f}")

    metrics = dict(
        elapsed=end - start,
        acc=acc,
        val_acc=val_acc,
        roc_auc=roc_auc,
        timestamp=datetime.now().strftime(TIMESTAMP_FMT),
    )

    if dump:
        joblib.dump(model, "data/pipeline.joblib")
        json.dump(metrics, open("data/metrics.json", "w"))


if __name__ == "__main__":
    fire.Fire(train)
