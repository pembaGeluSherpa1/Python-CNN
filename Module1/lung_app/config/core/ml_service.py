import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "lung_cancer_pipeline.pkl")

artifacts = joblib.load(MODEL_PATH)

model = artifacts["model"]
scaler = artifacts["scaler"]
label_encoder = artifacts["label_encoder"]
features_names = artifacts["features_name"]
columns_to_scale = artifacts["columns_to_scale"]

def predict_lung_cancer(input_data):
    df = pd.DataFrame([input_data], columns = features_names)

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

        df_scaled = df.copy()
        df_scaled[columns_to_scale] = scaler.transform(df[columns_to_scale])

        prediction = model.predict(df_scaled)[0]
        prediction_label = label_encoder.inverse_transform([prediction])[0]

        return prediction_label
