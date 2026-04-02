"""
Modes system for FeelTalk.
Each mode defines different AI response styles with prompts based on message intent.

Available modes:
- angry_roast: Brutal, toxic, abusive roasts
- soft_roast: Gentle, witty, playful roasts
- general_motivation: Encouraging and supportive messages
- religious_motivation: Faith-based inspirational messages
- seductive_roast: Flirty, charming roasts
- seductive_motivation: Charming and encouraging messages
- flirty: Playful and charming banter
- dumb_friend: Silly and absurd humor
"""

from app.utils.modes.angry_roast import ANGRY_ROAST
from app.utils.modes.soft_roast import SOFT_ROAST
from app.utils.modes.general_motivation import GENERAL_MOTIVATION
from app.utils.modes.religious_motivation import RELIGIOUS_MOTIVATION
from app.utils.modes.seductive_roast import SEDUCTIVE_ROAST
from app.utils.modes.seductive_motivation import SEDUCTIVE_MOTIVATION
from app.utils.modes.flirty import FLIRTY
from app.utils.modes.dumb_friend import DUMB_FRIEND

# Dictionary structure: MODES[mode_name][intent_type] = prompt_template
MODES = {
    "angry roast": ANGRY_ROAST,
    "soft roast": SOFT_ROAST,
    "general motivation": GENERAL_MOTIVATION,
    "religious motivation": RELIGIOUS_MOTIVATION,
    "seductive roast": SEDUCTIVE_ROAST,
    "seductive motivation": SEDUCTIVE_MOTIVATION,
    "flirty": FLIRTY,
    "dumb friend": DUMB_FRIEND,
}


def get_mode_prompt(mode: str, intent: str) -> str:
    """
    Get the prompt for a specific mode and intent.
    
    Args:
        mode: The feel mode (e.g., "angry roast", "soft roast", "motivation")
        intent: The message intent ("short", "medium", "long")
    
    Returns:
        The prompt template for that mode/intent combination
    """
    # Normalize mode name to lowercase
    mode_lower = mode.lower()
    
    # Return the prompt or fallback to angry roast if mode not found
    if mode_lower in MODES:
        if intent in MODES[mode_lower]:
            return MODES[mode_lower][intent]
        else:
            # Fallback intent to "long"
            return MODES[mode_lower].get("long", MODES["angry roast"]["long"])
    else:
        # Fallback mode (angry roast)
        return MODES["angry roast"].get(intent, MODES["angry roast"]["long"])


def get_available_modes() -> list[str]:
    """Get list of all available modes."""
    return sorted(list(MODES.keys()))
