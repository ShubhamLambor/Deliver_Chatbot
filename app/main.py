# app/main.py

from app.api.chat import chat_response

if __name__ == "__main__":
    print("🚚 Delivery Partner Chatbot (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        reply = chat_response(user_input)
        print("Bot:", reply)
