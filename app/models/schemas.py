"""
Pydantic schemas for request and response validation.
These define the shape of data coming in and going out of the API.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ---------------------------------------------------------------------------
# Authentication and User Schemas
# ---------------------------------------------------------------------------


class UserSignup(BaseModel):
    """
    Request body for user signup (POST /auth/signup).
    Contains user profile information that will be encoded into the auth token.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username (3-50 characters)",
    )
    gender: str = Field(
        ...,
        description="User's gender (e.g., 'Male', 'Female', 'Non-binary', 'Prefer not to say')",
    )
    profession: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's profession or job title",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="About yourself - can be used for personalized roasts (10-500 characters)",
    )
    region: str = Field(
        default="Delhi",
        description="Your region/country (e.g., 'Delhi', 'Mumbai', 'USA', 'UK', 'Australia'). Default: Delhi. Used to auto-detect language and region style.",
    )


class UserProfile(BaseModel):
    """
    Decoded user profile from the auth token.
    Contains all user information extracted from the binary token.
    """

    username: str = Field(..., description="User's username")
    gender: str = Field(..., description="User's gender")
    profession: str = Field(..., description="User's profession")
    description: str = Field(..., description="User's description about themselves")
    region: str = Field(..., description="User's region/country")


class AuthToken(BaseModel):
    """Response returned after successful signup."""

    token: str = Field(
        ...,
        description="Base64-encoded binary token containing encrypted user profile. Use this in X-Auth-Token header.",
    )
    username: str = Field(..., description="The registered username")
    message: str = Field(..., description="Success message")


class AuthenticatedChatRequest(BaseModel):
    """
    Authenticated chat request using a token.
    The token must be provided in the `X-Auth-Token` header instead.
    """

    message: str = Field(..., min_length=1, description="The user's message to be roasted")
    mode: str = Field(
        default="angry roast",
        description="Feel mode: 'angry roast' (default), 'soft roast', 'general motivation', 'religious motivation', 'seductive roast', 'seductive motivation', 'flirty', 'dumb friend'"
    )
    language: Optional[str] = Field(
        default=None,
        description="Override detected language (e.g. 'Hindi', 'Hinglish', 'English'). Auto-detected if not provided.",
    )
    region_style: Optional[str] = Field(
        default=None,
        description="Override regional roast style (e.g. 'Mumbai tapori', 'Gen-Z internet'). Auto-suggested if not provided.",
    )
    history: Optional[list["ChatMessage"]] = Field(
        default=None,
        description="Previous conversation messages for multi-turn context",
    )


class ChatMessage(BaseModel):
    """A single message in the conversation."""

    role: str = Field(..., description="Role of the sender: 'user' or 'assistant'")
    content: str = Field(..., description="The text content of the message")


class ChatRequest(BaseModel):
    """
    Request body for the chat endpoint.

    Language and region_style are auto-detected from the message by default.
    You can pass them explicitly to override detection (useful for testing).
    """

    message: str = Field(..., min_length=1, description="The user's message to be roasted")

    mode: str = Field(
        default="angry roast",
        description="Feel mode: 'angry roast' (default), 'soft roast', 'general motivation', 'religious motivation', 'seductive roast', 'seductive motivation', 'flirty', 'dumb friend'"
    )

    # Optional override — if omitted, language is auto-detected from the message.
    # Supports mixed language names like "Hinglish", "Hindi + Marathi", etc.
    language: Optional[str] = Field(
        default=None,
        description="Override detected language (e.g. 'Hindi', 'Hinglish', 'English'). Auto-detected if not provided.",
    )

    # Optional override — if omitted, style is auto-suggested based on detected language.
    region_style: Optional[str] = Field(
        default=None,
        description="Override regional roast style (e.g. 'Mumbai tapori', 'Gen-Z internet'). Auto-suggested if not provided.",
    )

    # Optional conversation history for multi-turn roast sessions
    history: Optional[list[ChatMessage]] = Field(
        default=None,
        description="Previous conversation messages for multi-turn context",
    )


class ChatResponse(BaseModel):
    """Response body returned from the chat endpoint."""

    reply: str = Field(..., description="The savage roast reply from the AI")
    model: str = Field(..., description="The model used to generate the roast")
    # Echo back what language(s) and style were used — useful for debugging
    detected_language: str = Field(
        ..., description="Language(s) detected or used in the reply"
    )
    detected_style: str = Field(
        ..., description="Regional style detected or used in the reply"
    )
    # If authenticated, echo back the user info used for personalization
    user_info: Optional[UserProfile] = Field(
        default=None,
        description="(Authenticated only) User profile used for personalization",
    )


# ---------------------------------------------------------------------------
# Structured-output shapes for Mistral `response_format` (json_schema) calls.
# ---------------------------------------------------------------------------


class LanguageDetectionResult(BaseModel):
    """
    Parsed output from the language-detection LLM call.
    Must match the json_schema passed to Mistral chat.complete.
    """

    language: str = Field(
        ...,
        description=(
            "All languages used in the user message (e.g. English, Hindi, Hinglish, "
            "or 'Hindi + Marathi' if mixed)."
        ),
    )
    region_style: str = Field(
        ...,
        description=(
            "Best regional roast style to match (e.g. 'Mumbai tapori', 'Gen-Z internet')."
        ),
    )


class RoastReply(BaseModel):
    """
    Parsed output from the main roast LLM call.
    The API still exposes only `reply` string to clients; this wraps the model output.
    """

    reply: str = Field(
        ...,
        description="2–4 lines of savage roast text in the same language mix as the user.",
    )
