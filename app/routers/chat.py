"""
Chat router — handles all /chat endpoints.
Language is auto-detected from the user's message before the roast is generated.
Optionally accepts X-Auth-Token header for personalized roasts.
"""

from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.models.schemas import ChatRequest, ChatResponse
from app.services import mistral_service
from app.services.auth_service import decode_token

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse, summary="Send a message and get roasted")
def send_roast(
    request: ChatRequest,
    x_auth_token: Optional[str] = Header(None),
) -> ChatResponse:
    """
    Send a user message and get a roast.

    **Two modes:**
    
    1. **Unauthenticated** (no header):
       - Generic roast without personalization
       - Just send the message
    
    2. **Authenticated** (with `X-Auth-Token` header):
       - Personalized roast using your profile data
       - First signup at `POST /auth/signup` to get token
       - Include token in `X-Auth-Token` header
    
    **Example (unauthenticated):**
    ```
    curl -X POST http://localhost:8000/chat/ \\
      -H "Content-Type: application/json" \\
      -d '{"message": "I am very lazy"}'
    ```
    
    **Example (authenticated):**
    ```
    curl -X POST http://localhost:8000/chat/ \\
      -H "X-Auth-Token: gASVtwAAAAAAAAB9lCiMCHVzZXJuYW1l..." \\
      -H "Content-Type: application/json" \\
      -d '{"message": "I am very lazy"}'
    ```
    
    The roast will automatically reference your profile (name, profession, etc.) if authenticated.
    """
    user_profile = None

    # If token is provided, decode it to get user profile
    if x_auth_token:
        try:
            user_profile = decode_token(x_auth_token)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    try:
        # Generate response with mode (with or without user profile personalization)
        reply, model_used, detected_language, detected_style, profile = mistral_service.chat(
            user_message=request.message,
            language=request.language,
            region_style=request.region_style,
            history=request.history,
            user_profile=user_profile,
            mode=request.mode,
        )

        return ChatResponse(
            reply=reply,
            model=model_used,
            detected_language=detected_language,
            detected_style=detected_style,
            user_info=profile,
        )

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error: {str(e)}")
