import joblib
from app.core.domain_filter import is_delivery_related
from app.core.rules import RESPONSES

try:
    model = joblib.load("intent_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    AI_LOADED = True
except:
    AI_LOADED = False


def chat_response(message: str) -> str:
    if not is_delivery_related(message):
        return "I can help only with delivery-related questions."

    if AI_LOADED:
        X = vectorizer.transform([message])
        predicted_intent = model.predict(X)[0]
        confidence = model.predict_proba(X).max()

        if confidence < 0.6:
            return RESPONSES.get("unknown", "I didn't understand that. Can you rephrase?")

        return RESPONSES.get(predicted_intent, RESPONSES["unknown"])

    return "System updating. Please try again."


