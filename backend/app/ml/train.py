import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

from app.models.customer import Customer


# =========================
# Load training data
# =========================
def load_training_data():
    customers = Customer.query.all()

    rows = []
    for c in customers:
        attrs = c.attributes

        # train ONLY on labeled data
        if "churn" in attrs:
            rows.append(attrs)

    return pd.DataFrame(rows)


# =========================
# Universal churn model training
# =========================
def train_churn_model():
    df = load_training_data()

    if df.empty:
        raise Exception("No churn-labeled data available")

    # -------------------------
    # Separate target
    # -------------------------
    y = df["churn"]
    X = df.drop(columns=["churn"])

    # -------------------------
    # Drop non-feature columns safely
    # -------------------------
    NON_FEATURE_COLUMNS = ["customer_id"]
    X = X.drop(columns=[c for c in NON_FEATURE_COLUMNS if c in X.columns])

    # -------------------------
    # Auto-detect feature types
    # -------------------------
    categorical_features = X.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    numerical_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if not categorical_features and not numerical_features:
        raise Exception("No usable features found for training")

    # -------------------------
    # Preprocessing pipeline
    # -------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numerical_features),
        ]
    )

    # -------------------------
    # Model
    # -------------------------
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1
            )),
        ]
    )

    # -------------------------
    # Train
    # -------------------------
    model.fit(X, y)

    # -------------------------
    # Save model
    # -------------------------
    joblib.dump(
        {
            "model": model,
            "categorical_features": categorical_features,
            "numerical_features": numerical_features
        },
        "app/ml/churn_model.pkl"
    )

    print("✅ Universal churn model trained")
    print("📊 Categorical features:", categorical_features)
    print("📈 Numerical features:", numerical_features)
