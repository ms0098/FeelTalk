"""
Authentication utilities for encoding/decoding user tokens.

Token format:
  - User profile (username, gender, profession, description) is serialized as JSON.
  - JSON is then pickled (binary serialization).
  - Pickled bytes are Base64-encoded to create a portable string token.

The token is used as the `X-Auth-Token` header in authenticated requests.
"""

import base64
import pickle
from app.models.schemas import UserProfile


def encode_token(user_profile: UserProfile) -> str:
    """
    Encode a UserProfile into a Base64-encoded binary token.

    Flow: UserProfile -> JSON -> pickle -> bytes -> Base64 string
    """
    # Convert Pydantic model to dict, then to JSON-compatible format
    profile_dict = user_profile.model_dump()

    # Pickle the dictionary (binary serialization)
    pickled = pickle.dumps(profile_dict)

    # Encode pickled bytes to Base64 string
    token = base64.b64encode(pickled).decode("utf-8")

    return token


def decode_token(token: str) -> UserProfile:
    """
    Decode a Base64-encoded binary token back to a UserProfile.

    Flow: Base64 string -> bytes -> pickle -> JSON -> UserProfile

    Raises:
        ValueError: If token is invalid or corrupted.
    """
    if not token or not isinstance(token, str):
        raise ValueError("Invalid token: must be a non-empty string.")

    try:
        # Decode Base64 string to bytes
        pickled = base64.b64decode(token.encode("utf-8"))

        # Unpickle the bytes to get the dictionary
        profile_dict = pickle.loads(pickled)

        # Validate and reconstruct the UserProfile Pydantic model
        user_profile = UserProfile.model_validate(profile_dict)

        return user_profile
    except (base64.binascii.Error, pickle.UnpicklingError, ValueError) as e:
        raise ValueError(f"Failed to decode token: {str(e)}")
