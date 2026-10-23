
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from text_preprocessing import normalize_text

# Load English SMS dataset
english_df = pd.read_csv(
    "dataset/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="latin-1"
)

english_df = english_df[["label", "message"]].copy()
english_df["label"] = english_df["label"].map({
    "ham": "normal",
    "spam": "scam"
})

# Load Roman Urdu dataset
urdu_df = pd.read_csv("dataset/roman_urdu_messages.csv")
urdu_df = urdu_df[["label", "message"]].copy()

# Load extra English context dataset
extra_df = pd.read_csv("dataset/extra_context_messages.csv")
extra_df = extra_df[["label", "message"]].copy()

# Combine datasets
df = pd.concat(
    [english_df, urdu_df, extra_df],
    ignore_index=True
)

df["label"] = df["label"].astype(str).str.lower().str.strip()
df["message"] = df["message"].astype(str).str.strip()

df = df[df["label"].isin(["normal", "scam"])]
df = df.dropna(subset=["message"])
df = df[df["message"] != ""]
df = df.drop_duplicates(subset=["label", "message"]).reset_index(drop=True)

# Normalize text
df["message"] = df["message"].apply(normalize_text)

print("Combined dataset shape:", df.shape)
print("\nLabel distribution:")
print(df["label"].value_counts())

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    df["message"],
    df["label"],
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# Word and character TF-IDF features
features = FeatureUnion([
    (
        "word_tfidf",
        TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=50000
        )
    ),
    (
        "char_tfidf",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            sublinear_tf=True,
            max_features=50000
        )
    )
])

X_train_features = features.fit_transform(X_train)
X_test_features = features.transform(X_test)

# Train classifier
model = LinearSVC(
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_features, y_train)

# Evaluate model
y_pred = model.predict(X_test_features)

print("\n========== MODEL EVALUATION ==========")
print("Test accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("\nClassification report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred, labels=["normal", "scam"]))

# Save the complete feature extraction and model pipeline
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ("features", features),
    ("classifier", model)
])

os.makedirs("models", exist_ok=True)

joblib.dump(
    pipeline,
    "models/multilingual_scam_detector.pkl"
)

print("\nModel saved to models/multilingual_scam_detector.pkl")

