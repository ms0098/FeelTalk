"""
FeelTalk — AI Chatbot powered by MistralAI
Entry point for the FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import chat, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Using this instead of deprecated @app.on_event decorators.
    """
    # Startup: runs before the app starts accepting requests
    print("FeelTalk is starting up...")
    yield
    # Shutdown: runs when the app is shutting down
    print("FeelTalk is shutting down.")


# Initialize the FastAPI app with metadata for the auto-generated docs
app = FastAPI(
    title="FeelTalk Chatbot",
    description="An AI chatbot powered by MistralAI with user authentication and personalized roasts.",
    version="1.0.0",
    lifespan=lifespan,
)

# Register routers
app.include_router(auth.router)
app.include_router(chat.router)


@app.get("/", summary="Health check")
def root() -> dict:
    """Simple health check endpoint to confirm the server is running."""
    return {
        "status": "ok",
        "message": "FeelTalk is running. Visit /docs for the API.",
        "endpoints": {
            "signup": "POST /auth/signup",
            "unauthenticated_roast": "POST /chat/",
            "authenticated_roast": "POST /chat/roast (requires X-Auth-Token header)",
        },
    }
