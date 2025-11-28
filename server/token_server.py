"""
Token server for LiveKit Voice Assistant
Generates JWT tokens for Flutter clients to connect to LiveKit
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from livekit import api
from datetime import timedelta
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS for web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# LiveKit credentials from .env
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")

# Validate credentials on startup
if not all([LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL]):
    logger.error("Missing LiveKit credentials in .env file")
    logger.error(f"LIVEKIT_API_KEY: {'✓' if LIVEKIT_API_KEY else '✗'}")
    logger.error(f"LIVEKIT_API_SECRET: {'✓' if LIVEKIT_API_SECRET else '✗'}")
    logger.error(f"LIVEKIT_URL: {'✓' if LIVEKIT_URL else '✗'}")
else:
    logger.info("LiveKit credentials loaded successfully")
    logger.info(f"LiveKit URL: {LIVEKIT_URL}")

@app.get("/token")
async def create_token(
    identity: str = "flutter-user",
    room: str = "voice-assistant"
):
    """
    Generate a token for connecting to LiveKit
    
    Args:
        identity: User identifier (default: flutter-user)
        room: Room name to join (default: voice-assistant)
    
    Returns:
        JSON with accessToken and url
    """
    
    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        raise HTTPException(
            status_code=500, 
            detail="LiveKit credentials not configured. Check .env file."
        )
    
    try:
        # Create access token
        token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        
        # Set user identity
        token.with_identity(identity).with_name(identity)
        
        # Grant permissions
        token.with_grants(api.VideoGrants(
            room_join=True,
            room=room,
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True,
        ))
        
        # Set expiration (24 hours)
        token.with_ttl(timedelta(hours=24))
        
        # Generate JWT
        jwt_token = token.to_jwt()
        
        logger.info(f"Token generated for {identity} in room {room}")
        
        return {
            "accessToken": jwt_token,
            "url": LIVEKIT_URL,
            "identity": identity,
            "room": room
        }
        
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail=f"Token generation failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "livekit_configured": bool(LIVEKIT_API_KEY and LIVEKIT_API_SECRET),
        "url": LIVEKIT_URL
    }

@app.get("/")
async def root():
    """Root endpoint with usage instructions"""
    return {
        "message": "LiveKit Token Server",
        "endpoints": {
            "/token": "Get access token for LiveKit",
            "/health": "Health check",
        },
        "usage": "GET /token?identity=your-name&room=your-room"
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8080))
    logger.info(f"Starting token server on port {port}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )