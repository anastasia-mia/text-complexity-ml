from sqlalchemy import text
import pandas as pd
from src.db.database import engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib

QUERY = text("SELECT * FROM metrics")

df = pd.read_sql(QUERY, engine)

TARGET_COL = "level_id"
DROP_COLS = ["id", TARGET_COL]

FEATURE_COLS = [c for c in df.columns if c not in DROP_COLS]

X = df[FEATURE_COLS]
y = df[TARGET_COL]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Test accuracy:", acc)

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

bundle = {
    "model": model,
    "feature_cols": FEATURE_COLS,
}

joblib.dump(bundle, "cefr_random_forest.pkl")
print("Model saved to cefr_random_forest.pkl")