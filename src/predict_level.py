import joblib
import pandas as pd

bundle = joblib.load("cefr_random_forest.pkl")
model = bundle["model"]
FEATURE_COLS = bundle["feature_cols"]

def predict_from_metrics(metrics: dict):
    x = pd.DataFrame([metrics], columns=FEATURE_COLS)
    y_pred = model.predict(x)[0]
    proba = model.predict_proba(x)[0]

    probabilities = {str(i+1): float(p) for i, p in enumerate(proba)}
    return int(y_pred), probabilities