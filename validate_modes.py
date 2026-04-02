"""Quick validation of modular modes system."""

try:
    # Test 1: Import all modes
    from app.utils.modes import (
        MODES, get_mode_prompt, get_available_modes,
        ANGRY_ROAST, SOFT_ROAST, GENERAL_MOTIVATION,
        RELIGIOUS_MOTIVATION, SEDUCTIVE_ROAST, SEDUCTIVE_MOTIVATION,
        FLIRTY, DUMB_FRIEND
    )
    print("[PASS] All modes imported successfully")
    
    # Test 2: Check all modes available
    modes = get_available_modes()
    assert len(modes) == 8, f"Expected 8 modes, got {len(modes)}"
    print(f"[PASS] All 8 modes available: {modes}")
    
    # Test 3: Check each mode has 4 intent levels
    for mode_name in modes:
        mode_dict = MODES[mode_name]
        intents = list(mode_dict.keys())
        assert len(intents) == 4, f"{mode_name} has {len(intents)} intents, expected 4"
        assert "greeting" in intents, f"{mode_name} missing 'greeting' intent"
        assert "short" in intents, f"{mode_name} missing 'short' intent"
        assert "medium" in intents, f"{mode_name} missing 'medium' intent"
        assert "long" in intents, f"{mode_name} missing 'long' intent"
    print("[PASS] All modes have 4 intent levels (greeting, short, medium, long)")
    
    # Test 4: Test detect_message_intent
    from app.services.mistral_service import detect_message_intent
    
    tests = [
        ("hi", "greeting"),
        ("hello world", "short"),
        ("this is a medium message here", "medium"),
        ("this is a very long message with many words to test the detection of long messages", "long"),
    ]
    
    for msg, expected_intent in tests:
        intent, lines = detect_message_intent(msg)
        assert intent == expected_intent, f"'{msg}' -> expected {expected_intent}, got {intent}"
    print("[PASS] Intent detection working correctly")
    
    # Test 5: Verify prompt retrieval
    prompt = get_mode_prompt("angry roast", "greeting")
    assert len(prompt) > 0, "Greeting prompt is empty"
    assert "greeting" in prompt.lower() or "toxic" in prompt.lower(), "Greeting prompt has wrong content"
    print("[PASS] Greeting prompt retrieval working")
    
    print("\n[SUCCESS] All validation tests passed!")
    print("Modular modes system is ready to use.")
    
except Exception as e:
    print(f"[FAIL] {str(e)}")
    import traceback
    traceback.print_exc()
