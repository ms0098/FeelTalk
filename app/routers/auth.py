"""
Authentication router — handles user signup and token generation.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import UserSignup, UserProfile, AuthToken
from app.services.auth_service import encode_token
from app.utils.country_mapper import get_language_and_style_by_region

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthToken, summary="Create a new user account and get auth token")
def signup(request: UserSignup) -> AuthToken:
    """
    Create a new user account with profile information.

    Returns an `X-Auth-Token` header value (Base64-encoded binary token) that encodes:
    - username
    - gender
    - profession
    - description
    - region (defaults to "Delhi" if not provided)

    The region is used to **automatically determine** the language and regional roasting style.

    **Supported regions:** Delhi, Mumbai, Bangalore, Chennai, Kolkata, Hyderabad, Pune, Gurgaon, 
    USA, UK, Australia, Canada, Germany, France, Spain, Mexico, Brazil, Japan, China, 
    South Korea, Pakistan, Bangladesh, and many more cities and countries!

    **Example usage after signup:**
    ```
    curl -X POST http://localhost:8000/chat/ \\
      -H "X-Auth-Token: <token-from-signup>" \\
      -H "Content-Type: application/json" \\
      -d '{"message": "I am very lazy"}'
    ```
    """
    try:
        # Validate region and get language/style
        language, region_style = get_language_and_style_by_region(request.region)

        # Create user profile from signup data
        user_profile = UserProfile(
            username=request.username,
            gender=request.gender,
            profession=request.profession,
            description=request.description,
            region=request.region,
        )

        # Encode profile into a binary token
        token = encode_token(user_profile)

        return AuthToken(
            token=token,
            username=request.username,
            message=f"User '{request.username}' from {request.region} registered successfully. "
            f"Roasts will use: {language} in {region_style} style. "
            f"Use the token in X-Auth-Token header for personalized roasts.",
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during signup: {str(e)}")
