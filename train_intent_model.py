from app.core.ml_intent_model import IntentModel

if __name__ == "__main__":
    # Initialize and train
    ai = IntentModel()
    ai.train("app/data/intents.json")
