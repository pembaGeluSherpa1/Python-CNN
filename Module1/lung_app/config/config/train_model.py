import os

import joblib

import pandas as pd

import numpy as np


from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "survey_lung_cancer.csv")

MODEL_PATH = os.path.join(BASE_DIR, "lung_cancer_pipeline.pkl")



print("Loading dataset...")

df = pd.read_csv(DATA_PATH)


print("Dataset shape:", df.shape)

print(df.head())



# Separate features and target

X = df.iloc[:, :-1].copy()

y = df.iloc[:, -1].copy()



# Clean column names

X.columns = X.columns.str.strip().str.upper().str.replace(" ", "_")



# Clean and encode categorical feature columns

categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()

feature_encoders = {}


for col in categorical_cols:

   X[col] = X[col].astype(str).str.strip().str.upper()

   X[col] = X[col].replace(["NAN", "NONE", ""], np.nan)

   X[col] = X[col].fillna(X[col].mode()[0])


   # Special handling for gender

   if col == "GENDER":

       X[col] = X[col].map({

           "M": 1,

           "MALE": 1,

           "F": 0,

           "FEMALE": 0,

           "GF": 0

       })

       X[col] = X[col].fillna(0).astype(int)

   else:

       le = LabelEncoder()

       X[col] = le.fit_transform(X[col])

       feature_encoders[col] = le



# Convert all features to numeric

X = X.apply(pd.to_numeric, errors="coerce")

X = X.fillna(X.median(numeric_only=True))



# Clean and encode target

y = y.astype(str).str.strip().str.upper()

y = y.replace(["NAN", "NONE", ""], np.nan)

y = y.fillna(y.mode()[0])


label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)


print("Target mapping:")

print(dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))))



# Split data

X_train, X_test, y_train, y_test = train_test_split(

   X,

   y_encoded,

   test_size=0.2,

   random_state=42,

   stratify=y_encoded

)



# Scale numeric columns except binary gender if present

feature_names = X.columns.tolist()


columns_to_scale = [col for col in feature_names if col != "GENDER"]


scaler = StandardScaler()

X_train_scaled = X_train.copy()

X_test_scaled = X_test.copy()


X_train_scaled[columns_to_scale] = scaler.fit_transform(X_train[columns_to_scale])

X_test_scaled[columns_to_scale] = scaler.transform(X_test[columns_to_scale])



# Train model

model = RandomForestClassifier(

   n_estimators=200,

   random_state=42

)


model.fit(X_train_scaled, y_train)



# Evaluate

y_pred = model.predict(X_test_scaled)


print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))



# Save full pipeline

artifacts = {

   "model": model,

   "scaler": scaler,

   "label_encoder": label_encoder,

   "feature_names": feature_names,

   "columns_to_scale": columns_to_scale,

   "feature_encoders": feature_encoders

}


joblib.dump(artifacts, MODEL_PATH)


print("\nSaved model file at:")

print(MODEL_PATH)