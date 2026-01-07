# app/core/intent_detector.py

INTENTS = {
    "order_status": ["order status", "current order", "active order"],
    "earnings": ["earning", "income", "payment", "salary"],
    "pickup_issue": ["pickup problem", "restaurant closed", "late pickup"],
    "delivery_issue": ["customer not responding", "wrong address"],
    "cancel_order": ["cancel order", "order cancel"],
    "support": ["help", "support", "issue"]
}

def detect_intent(message: str) -> str:
    message = message.lower()
    for intent, phrases in INTENTS.items():
        for phrase in phrases:
            if phrase in message:
                return intent
    return "unknown"
