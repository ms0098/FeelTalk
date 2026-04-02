"""
MistralAI service layer.
Handles all communication with the Mistral API.

Flow:
  1. detect_message_intent()  — determine message length/type (greeting, short, medium, long)
  2. detect_language()        — fast call (mistral-small-latest) to detect language(s) and region style
  3. chat()                   — roast call (mistral-medium-latest) with appropriate prompt based on intent
"""

import os
from pydantic import BaseModel
from mistralai.client import Mistral
from mistralai.client.models.responseformat import ResponseFormat
from mistralai.client.models.jsonschema import JSONSchema
from dotenv import load_dotenv
from app.models.schemas import ChatMessage, LanguageDetectionResult, RoastReply, UserProfile
from app.utils.country_mapper import get_language_and_style_by_region
from app.utils.modes import get_mode_prompt, get_available_modes

# Load environment variables from .env file
load_dotenv()


def _json_schema_response_format(model_cls: type[BaseModel], name: str) -> ResponseFormat:
    """
    Build Mistral's response_format for native JSON-schema structured output.
    Uses Pydantic's JSON Schema so the API guarantees parseable JSON matching the model.
    """
    return ResponseFormat(
        type="json_schema",
        json_schema=JSONSchema(
            name=name,
            schema_definition=model_cls.model_json_schema(),
        ),
    )


# ---------------------------------------------------------------------------
# Message Intent Detection
# ---------------------------------------------------------------------------
def detect_message_intent(user_message: str) -> tuple[str, int]:
    """
    Detect the intent and length of the user's message.
    
    Returns:
        (intent_type, recommended_lines)
        - intent_type: "greeting", "short", "medium", "long"
        - recommended_lines: 1-2, 1-2, 4-5, 7-10
    """
    message_lower = user_message.strip().lower()
    word_count = len(user_message.split())
    char_count = len(user_message.strip())

    # Greeting detection (single word or very short) → returns "greeting" intent
    greetings = {
        "hi", "hii", "hey", "hello", "yo", "sup", "what's up", "whatsup",
        "howdy", "hola", "namaste", "salaam", "kya", "kaise", "tera", "ello",
        "okay", "ok", "yep", "yeah", "sure", "thanks", "thank you",
        "bye", "goodbye", "see you", "cya", "lol", "lmao"
    }
    
    if message_lower in greetings or (word_count <= 1 and char_count <= 10):
        return "greeting", 1  # 1-2 line response

    # Short messages (1-3 words, simple statements)
    if word_count <= 3 or char_count <= 30:
        return "short", 2  # 1-2 line response

    # Medium messages (4-15 words, moderate statements)
    if word_count <= 15 or char_count <= 100:
        return "medium", 4  # 4-5 line response

    # Long messages (16+ words, complex statements, multiple sentences)
    return "long", 8  # 7-10 line response


# ---------------------------------------------------------------------------
# Language detection prompt (output shape enforced by LanguageDetectionResult).
# ---------------------------------------------------------------------------
LANGUAGE_DETECT_USER_PROMPT = """Analyse the following user message and identify:
1. All languages used (e.g. English, Hindi, Hinglish, Marathi, Tamil, etc.)
   - If the user mixes languages (like Hindi + English), capture BOTH.
2. The best regional roast style to match those languages.

User message:
{user_input}
"""


def get_mistral_client() -> Mistral:
    """
    Create and return a Mistral client using the API key from environment.
    Raises early if the key is missing.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set in the environment.")
    return Mistral(api_key=api_key)


def get_model() -> str:
    """Return the main roast model from env, defaulting to mistral-medium-latest."""
    return os.getenv("MISTRAL_MODEL", "mistral-medium-latest")


def detect_language(user_message: str, client: Mistral) -> tuple[str, str]:
    """
    Step 1 — Language detection with structured output (Pydantic json_schema).

    Returns:
        (language_str, region_style_str)
    Falls back on parse errors to ("English", "Gen-Z internet").
    """
    detect_model = "mistral-small-latest"
    prompt = LANGUAGE_DETECT_USER_PROMPT.format(user_input=user_message)

    response = client.chat.complete(
        model=detect_model,
        messages=[{"role": "user", "content": prompt}],
        response_format=_json_schema_response_format(
            LanguageDetectionResult,
            "language_detection",
        ),
    )

    raw = response.choices[0].message.content
    if not raw:
        return "Hindi", "Delhi/North Indian street roast"

    try:
        parsed = LanguageDetectionResult.model_validate_json(raw)
        return parsed.language, parsed.region_style
    except Exception:
        # If the model returns invalid JSON or schema drift, fall back to safe defaults
        return "Hindi", "Delhi/North Indian street roast"


def build_system_prompt(
    language: str,
    region_style: str,
    user_message: str,
    user_profile: UserProfile | None = None,
    intent: str = "long",
    mode: str = "angry roast",
) -> str:
    """
    Fill the roast system prompt template with:
    - detected (or overridden) language
    - detected (or overridden) region_style
    - the raw user message (embedded at the bottom for direct instruction)
    - optional user profile info for personalization
    - appropriate prompt based on message intent and mode
    """
    # Build personalization context if user profile is provided
    user_context = ""
    if user_profile:
        user_context = f"""
User Profile (for subtle personalization):
- Name: {user_profile.username}
- Context: {user_profile.gender}, {user_profile.profession}, {user_profile.description}

IMPORTANT: Use this context for subtle personalization only. Reference their name {user_profile.username} naturally if it fits. DO NOT explicitly mention their gender, profession, or description in the response. Keep the roast personal but indirect.
"""

    # Get mode-specific prompt based on intent
    prompt_template = get_mode_prompt(mode, intent)

    return prompt_template.format(
        language=language,
        region_style=region_style,
        user_input=user_message,
        user_context=user_context,
    )


def build_messages(
    user_message: str,
    language: str,
    region_style: str,
    history: list[ChatMessage] | None = None,
    user_profile: UserProfile | None = None,
    intent: str = "long",
    mode: str = "angry roast",
) -> list[dict]:
    """
    Build the final messages list for the API call.

    Structure:
    1. System prompt (appropriate prompt based on message intent and mode)
    2. Previous conversation history (if any)
    3. The user message (as the user role turn)
    """
    system_prompt = build_system_prompt(language, region_style, user_message, user_profile, intent, mode)

    messages = [{"role": "system", "content": system_prompt}]

    if history:
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

    messages.append({"role": "user", "content": user_message})

    return messages


def chat(
    user_message: str,
    language: str | None = None,
    region_style: str | None = None,
    history: list[ChatMessage] | None = None,
    user_profile: UserProfile | None = None,
    mode: str = "angry roast",
) -> tuple[str, str, str, str, UserProfile | None]:
    """
    Main entry point for response generation.

    Step 1: Detect message intent (greeting, short, medium, long)
    Step 2: If user profile provided with region, use region-based language/style.
            Otherwise, detect language(s) from user message.
    Step 3: Build prompt appropriate for the message intent and mode.
    Step 4: Call mistral-medium-latest with structured output.

    Returns:
        (reply, model_used, detected_language, detected_style, user_profile)
    """
    client = get_mistral_client()

    # Step 1: Detect message intent to determine response length
    intent, _ = detect_message_intent(user_message)

    # Step 2: Priority: user profile region > explicit language/style > message detection
    if user_profile and user_profile.region:
        # Use region-based language and style
        final_language, final_style = get_language_and_style_by_region(user_profile.region)
    elif language and region_style:
        final_language = language
        final_style = region_style
    else:
        final_language, final_style = detect_language(user_message, client)
        if language:
            final_language = language
        if region_style:
            final_style = region_style

    model = get_model()
    # Step 3: Build messages with intent and mode-aware prompt
    messages = build_messages(user_message, final_language, final_style, history, user_profile, intent, mode)

    # Step 4: Generate response with structured output
    response = client.chat.complete(
        model=model,
        messages=messages,
        response_format=_json_schema_response_format(RoastReply, "roast_reply"),
    )

    raw = response.choices[0].message.content
    if not raw:
        raise ValueError("Empty response from Mistral completion.")

    parsed = RoastReply.model_validate_json(raw)
    return parsed.reply, model, final_language, final_style, user_profile
