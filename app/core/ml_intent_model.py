import json
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

MODEL_PATH = "intent_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"


class IntentModel:
    def __init__(self):
        # Improved TF-IDF with better settings for short text
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),  # Captures 1, 2, and 3-word phrases
            max_features=1000,  # Increased vocabulary size
            lowercase=True,  # Normalizes case
            min_df=1,  # Keep even rare words (important for small datasets)
            sublinear_tf=True,  # Better scaling for TF weights
            strip_accents='unicode'  # Handle special characters
        )

        # LinearSVC is better for text classification than Logistic Regression
        base_model = LinearSVC(
            C=1.0,  # Regularization
            max_iter=2000,  # More iterations
            random_state=42,
            dual=False  # Faster for small datasets
        )

        # Wrap SVM to get probability predictions (needed for confidence)
        self.model = CalibratedClassifierCV(base_model, cv=3)

    def train(self, data_path: str):
        """Reads JSON, trains model, and evaluates accuracy."""
        print("🧠 Training started...")

        with open(data_path, "r", encoding="utf-8") as f:
            intents = json.load(f)

        texts = []
        labels = []

        for intent, examples in intents.items():
            for text in examples:
                texts.append(text)
                labels.append(intent)

        print(f"📊 Processing {len(texts)} training examples...")

        # Smaller test set for small datasets (10% instead of 20%)
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.1, random_state=42, stratify=labels
        )

        print(f"🔹 Training samples: {len(X_train)}")
        print(f"🔹 Test samples: {len(X_test)}")

        # Vectorize
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        # Train
        print("⚙️ Training model...")
        self.model.fit(X_train_vec, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%")
        print("\n📋 Detailed Report:")
        print(classification_report(y_test, y_pred, zero_division=0))

        # Save
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.vectorizer, VECTORIZER_PATH)
        print("\n💾 Model saved successfully!")

    def predict(self, message: str):
        """Predicts intent with confidence score."""
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            return "unknown", 0.0

        if not hasattr(self, 'is_loaded'):
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.is_loaded = True

        X = self.vectorizer.transform([message])
        intent = self.model.predict(X)[0]
        confidence = self.model.predict_proba(X).max()

        return intent, confidence
