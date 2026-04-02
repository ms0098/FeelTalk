# FeelTalk — AI Chatbot with Personalized Roasts

An intelligent chatbot powered by **MistralAI** that delivers savage, personalized roasts in your language and regional style. Built with **FastAPI**, **Pydantic**, and structured outputs (JSON schema).

## Features

✨ **Language Detection** — Automatically detects the language(s) in your message (Hinglish, Hindi, English, Marathi, etc.)

🎤 **Regional Roasting** — Uses region-specific slang and insults (Mumbai tapori, Gen-Z internet, etc.)

👤 **User Profiles** — Create a profile and get **personalized roasts** that reference your name, profession, and personality

🔐 **Token-Based Auth** — Binary token (Base64-encoded pickle) for stateless authentication

🏗️ **Structured LLM Outputs** — Uses Mistral's `json_schema` mode for guaranteed JSON parsing

🌐 **Multi-Language Support** — Responds in the same language mix you use

---

## Quick Start

### 1. Start the Server

```bash
cd c:\wrokspace\practice\FeelTalk
uv run uvicorn main:app --reload --port 8000
```

Server runs at: **http://127.0.0.1:8000**

### 2. Try the Interactive Docs

Open in browser: **http://127.0.0.1:8000/docs** (Swagger UI)

---

## 🌍 How It Works

### Region-Based Language & Style Detection

When you sign up with your region, FeelTalk **automatically determines**:
- **Language** — The language(s) to use (e.g., Hindi, English, Marathi)
- **Region Style** — The regional roasting style (e.g., Mumbai tapori, Bangalore tech humor)

**Key point:** If you **don't specify a region, it defaults to Delhi** with Delhi/North Indian street roast style.

**Supported regions include:** 
- **Indian cities:** Delhi, Mumbai, Bangalore, Chennai, Kolkata, Hyderabad, Pune, Gurgaon, and many more
- **Countries:** USA, UK, Australia, Canada, Germany, France, Spain, Mexico, Brazil, Japan, China, South Korea, Pakistan, Bangladesh, Nigeria, Kenya, Singapore, Malaysia, Russia, Turkey, Argentina, Chile, Colombia, and many more

---

## API Endpoints

### `POST /auth/signup` — Create User Account

Register a new user and get an authentication token. **Region determines the language and roasting style. Defaults to Delhi if not provided.**

**Request:**
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "amir_mumbai",
    "gender": "Male",
    "profession": "Actor",
    "description": "I am dramatic and emotional",
    "region": "Mumbai"
  }'
```

**Response:**
```json
{
  "token": "gASVtwAAAAAAAAB9lCiMCHVzZXJuYW1l...",
  "username": "amir_mumbai",
  "message": "User 'amir_mumbai' from Mumbai registered successfully. Roasts will use: Hindi + English (Hinglish) in Mumbai tapori style. Use the token in X-Auth-Token header for personalized roasts."
}
```

**Note:** If `region` is not provided, it defaults to **Delhi** with Delhi/North Indian street roast style.

Save the `token` for authenticated requests. The roasts will now use the detected language and style for **your region**.

---

### `POST /chat/` — Get Roasted

Send a message and receive a savage roast. **Optionally provide token for personalized roasts with region-based language/style.**

#### Option 1: Unauthenticated (Generic Roast)

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Main bohot intelligent hoon"}'
```

**Response:**
```json
{
  "reply": "Arre bhai tu intelligent? Teri toh IQ zero hai...",
  "model": "mistral-medium-latest",
  "detected_language": "Hindi",
  "detected_style": "Mumbai tapori",
  "user_info": null
}
```

#### Option 2: Authenticated (Personalized Roast)

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "X-Auth-Token: gASVtwAAAAAAAAB9lCiMCHVzZXJuYW1l..." \
  -H "Content-Type: application/json" \
  -d '{"message": "Main bohot intelligent hoon"}'
```

**Response:**
```json
{
  "reply": "Arre bhai tu intelligent? 3 AM code karke genius banne ka sapna dekhta hai? Teri coding skills dekh ke...",
  "model": "mistral-medium-latest",
  "detected_language": "Hindi + English (Hinglish)",
  "detected_style": "Mumbai tapori",
  "user_info": {
    "username": "coderboy",
    "gender": "Male",
    "profession": "Full Stack Developer",
    "description": "I code at 3 AM and think I am a genius",
    "region": "Mumbai"
  }
}
```

Key features:
- **Language & Style** are **automatically determined by region** (Mumbai → Hinglish + Mumbai tapori)
- The roast **references user's profile** (name, profession, region)
- Response includes full user profile (region field now included)

---

## 🌍 Supported Regions & Cities

### India
| Region/City | Language | Roasting Style |
|-------------|----------|-----------------|
| Delhi (default) | Hindi + English | Delhi/North Indian street roast |
| Mumbai | Hindi + English | Mumbai tapori |
| Bangalore | Kannada + English | Bangalore tech humor |
| Chennai | Tamil + English | Chennai South Indian style |
| Kolkata | Bengali + English | Kolkata intellectual roast |
| Hyderabad | Telugu + English | Hyderabad tech swagger |
| Pune | Marathi + English | Pune attitude |
| Gurgaon | Hindi + English | Gurgaon corporate roast |
| Noida | Hindi + English | North Indian street roast |
| Indore | Hindi | Indore street style |
| Jaipur | Hindi | Jaipur royal roast |
| Lucknow | Urdu + Hindi | Lucknow Awadhi style |
| Ahmedabad | Gujarati + English | Ahmedabad Gujarati humor |
| Surat | Gujarati + English | Surat diamond city swagger |
| Chandigarh | Punjabi + English | Chandigarh Punjabi swagger |
| Amritsar | Punjabi | Punjab Punjabi roast |
| Goa | Konkani + English | Goa beach vibes |
| Kochi | Malayalam + English | Kochi Kerala style |

### International
| Region | Language | Roasting Style |
|--------|----------|-----------------|
| USA | English | Gen-Z internet |
| UK | English | British sarcasm |
| Australia | English | Australian slang |
| Canada | English | Canadian humor |
| Germany | German | German directness |
| France | French | French wit |
| Spain | Spanish | Spanish passion |
| Mexico | Spanish | Mexican street style |
| Brazil | Portuguese | Brazilian swagger |
| Japan | Japanese | Japanese politeness |
| China | Mandarin | Chinese humor |
| South Korea | Korean | K-pop sass |
| Pakistan | Urdu + English | Pakistan street style |
| Bangladesh | Bengali + English | Dhaka banter |
| Nigeria | English + Pidgin | Nigerian swagger |
| Singapore | English + Mandarin | Singapore sass |

*Full list available in `app/utils/country_mapper.py`*

---

## Request Parameters

### `/chat/` Endpoint

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | ✅ | Your message to be roasted |
| `mode` | string | ❌ | Feel mode to use (default: "angry roast") |
| `language` | string | ❌ | Override detected/region-based language (e.g., `"Hindi"`, `"Hinglish"`) |
| `region_style` | string | ❌ | Override detected/region-based style (e.g., `"Mumbai tapori"`, `"Bangalore tech humor"`) |
| `history` | array | ❌ | Previous messages for multi-turn conversations |

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `X-Auth-Token` | ❌ | Token from signup. If provided, roast uses your region's language/style + personalization. |
| `Content-Type` | ✅ | Must be `application/json` |

---

## 🎨 Feel Modes

The `/chat/` endpoint supports multiple feel modes that change the tone and style of responses based on message intent:

### Available Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `angry roast` | Brutal, toxic, abusive roasts | Default roasting |
| `soft roast` | Gentle, witty, playful roasts | Light teasing |
| `general motivation` | Encouraging and supportive messages | Inspiration |
| `religious motivation` | Faith-based inspirational messages | Spiritual guidance |
| `seductive roast` | Flirty, charming roasts | Playful flirtation |
| `seductive motivation` | Charming and encouraging messages | Inspirational flirtation |
| `flirty` | Playful and charming banter | Fun engagement |
| `dumb friend` | Silly and absurd humor | Comedy relief |

### Mode Request Example

```bash
# Get a soft roast
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I think I am very intelligent",
    "mode": "soft roast"
  }'
```

### Intent-Based Response Lengths

Each mode automatically adjusts response length based on **message intent**:

- **Greeting Intent** (greetings: Hi, Hello, Hey, etc.) → **1-2 lines**
  - User: "Hi"
  - Response: 1-2 line greeting response (tailored to the mode)

- **Short Intent** (simple statements, 1-3 words) → **1-2 lines**
  - User: "I am smart"
  - Response: 1-2 line reply

- **Medium Intent** (normal messages, 4-15 words) → **4-5 lines**
  - User: "I think I am very smart"
  - Response: 4-5 line reply

- **Long Intent** (detailed messages, 16+ words) → **7-10 lines**
  - User: "I have been working hard all day and I think I deserve recognition for my efforts"
  - Response: 7-10 line detailed reply

---

When making a roast request with a token, the API follows this priority:

1. **Region-based** (if user profile has region) — Language & style determined by signup region
2. **Explicit override** (if language/region_style params provided) — Use those instead
3. **Message detection** (if no token, no params) — Detect from message content

```
Example Priority Order:
Token with Mumbai → Hindi + Hinglish + Mumbai tapori
                     ↓
           (override lang="English" param)
                     ↓
           English + Mumbai tapori (language overridden, style from region)
```

**Default Region:** If user doesn't provide a region during signup, **Delhi** is used as the default with Delhi/North Indian street roast style.

---

## Architecture

### Language Detection Flow

```
User with token (Mumbai) sends message:
    ↓
Region detected: "Mumbai"
    ↓
Language & style auto-determined: Hindi + Hinglish, Mumbai tapori
    ↓
System prompt includes user profile + language/style
    ↓
mistral-medium-latest generates personalized roast
    ↓
Response returned with language, style, and user_info
```

### Unauthenticated User Message

```
User without token sends message:
    ↓
mistral-small-latest detects message language/style
    ↓
System prompt built with detected values
    ↓
mistral-medium-latest generates generic roast
    ↓
Response returned with detected language/style, user_info=null
```

### Authentication & Token Flow

```
Signup (POST /auth/signup with region, defaults to Delhi)
  ↓ User profile + region collected
  ↓ Region mapped to: language + region_style
  ↓ Encoded as: JSON → Pickle → Base64 string
  ↓ Token returned

Later request (POST /chat/ with X-Auth-Token header)
  ↓ Token decoded: Base64 → Pickle → JSON → UserProfile
  ↓ Region extracted from profile
  ↓ Language & style auto-determined from region
  ↓ User profile injected into roast system prompt
  ↓ Personalized roast generated with region-based language/style
```

---

## Project Structure

```
FeelTalk/
├── .env                           # API keys (gitignored)
├── main.py                        # FastAPI app entry point
├── pyproject.toml                 # UV dependencies
│
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic models (User, Chat, Auth)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── mistral_service.py     # LLM logic + structured output
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── country_mapper.py      # Region → Language + Region style mapping
│   │   └── modes/                 # Modular mode system
│   │       ├── __init__.py        # Exports all modes + utility functions
│   │       ├── angry_roast.py     # Angry roast mode prompts (short/medium/long)
│   │       ├── soft_roast.py      # Soft roast mode prompts (short/medium/long)
│   │       ├── general_motivation.py    # General motivation mode prompts
│   │       ├── religious_motivation.py  # Religious motivation mode prompts
│   │       ├── seductive_roast.py # Seductive roast mode prompts
│   │       ├── seductive_motivation.py  # Seductive motivation mode prompts
│   │       ├── flirty.py          # Flirty mode prompts
│   │       └── dumb_friend.py     # Dumb friend mode prompts
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py                # POST /auth/signup
│       └── chat.py                # POST /chat/
```

### 🎨 Modular Modes System

Each AI response mode is organized as a **separate Python file** in `app/utils/modes/`:

- **Structure:** Each mode defines prompts for three message intents:
  - `short` — 1-2 line response (for greetings/short messages)
  - `medium` — 4-5 line response (for medium-length messages)
  - `long` — 7-10 line response (for detailed/complex messages)

- **Available Modes:**
  1. **angry_roast** — Brutal, toxic, abusive roasts (default)
  2. **soft_roast** — Gentle, witty, playful roasts
  3. **general_motivation** — Encouraging and supportive messages
  4. **religious_motivation** — Faith-based inspirational messages
  5. **seductive_roast** — Flirty, charming roasts
  6. **seductive_motivation** — Charming and encouraging messages
  7. **flirty** — Playful and charming banter
  8. **dumb_friend** — Silly and absurd humor

- **Exports from `__init__.py`:**
  - `MODES` — Dictionary mapping mode names to prompt dictionaries
  - `get_mode_prompt(mode, intent)` — Fetch the correct prompt template
  - `get_available_modes()` — List all available modes

---

## Key Technologies

- **FastAPI** — Modern async Python web framework
- **Pydantic v2** — Data validation + structured outputs
- **MistralAI** — `mistral-medium-latest` model with JSON schema mode
- **UV** — Fast Python package manager
- **Pickle + Base64** — Token serialization

---

## Structured Output (JSON Schema)

All LLM calls use Mistral's **`response_format="json_schema"`** for guaranteed JSON parsing:

1. **Language Detection** → `LanguageDetectionResult` (language, region_style)
2. **Roast Generation** → `RoastReply` (reply text only)

This ensures the API never returns malformed responses.

---

## Environment Setup

Create `.env` file:

```env
MISTRAL_API_KEY=<your-api-key>
MISTRAL_MODEL=mistral-medium-latest
```

---

## Example: Full Flow

```bash
# 1. Signup
TOKEN=$(curl -s -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "dev_life",
    "gender": "Female",
    "profession": "DevOps Engineer",
    "description": "I debug production at 2 AM"
  }' | jq -r '.token')

# 2. Get personalized roast using token
curl -X POST http://localhost:8000/chat/ \
  -H "X-Auth-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "मुझे तो production में issues नहीं होते"}'
```

---

## API Status Codes

| Code | Meaning |
|------|---------|
| `200` | Roast generated successfully |
| `400` | Invalid request data |
| `401` | Invalid or missing auth token |
| `500` | Server error (missing API key, etc.) |
| `502` | Mistral API error |

---

## Notes

- **Token Security**: Tokens are Base64-encoded pickles (not encrypted). For production, consider using JWT or encryption.
- **Rate Limits**: Depends on Mistral API limits.
- **Language Support**: Best with languages MistralAI supports (English, Hindi, Spanish, French, German, etc.).

---

## Testing

Use the interactive docs: **http://localhost:8000/docs**

Or test with Python:

```python
import httpx

# Unauthenticated
resp = httpx.post("http://localhost:8000/chat/", json={"message": "I'm lazy"})
print(resp.json())

# Authenticated
token = "..."  # from signup
resp = httpx.post(
    "http://localhost:8000/chat/",
    headers={"X-Auth-Token": token},
    json={"message": "I'm lazy"}
)
print(resp.json())
```

---

Made with ❤️ using MistralAI + FastAPI
