import joblib
import os

MODEL_PATH = "app/ml/churn_model.pkl"

_model_cache = None

def get_churn_model():
    global _model_cache

    if _model_cache is None:
        if not os.path.exists(MODEL_PATH):
            raise Exception("Churn model not trained yet")

        _model_cache = joblib.load(MODEL_PATH)["model"]

    return _model_cache
