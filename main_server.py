from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
from app.api.chat import chat_response

# Initialize FastAPI
app = FastAPI(
    title="Tiffinity Delivery Chatbot API",
    description="AI-powered support for delivery partners",
    version="1.0.0"
)

# CORS: Allow Flutter app to connect from any device
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"


class ChatResponse(BaseModel):
    response: str
    status: str
    confidence: float = 0.0


# Health Check Endpoint
@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "Tiffinity Delivery Chatbot",
        "version": "1.0.0"
    }


# Main Chat Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Receives a message from the delivery partner and returns AI response.
    """
    try:
        if not request.message or request.message.strip() == "":
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Get bot response
        bot_reply = chat_response(request.message)

        # Optional: Calculate confidence if available
        # (You can enhance chat_response to return confidence)

        return ChatResponse(
            response=bot_reply,
            status="success",
            confidence=0.85  # Placeholder for now
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# Print server info on startup
if __name__ == "__main__":
    import socket
    import uvicorn

    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "127.0.0.1"

    print("=" * 60)
    print("🚀 Tiffinity Chatbot Server Starting...")
    print("=" * 60)
    print(f"📡 Local URL:    http://127.0.0.1:8000")
    print(f"📱 Network URL:  http://{ip_address}:8000")
    print(f"📖 API Docs:     http://{ip_address}:8000/docs")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
