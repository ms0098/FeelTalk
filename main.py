"""
FeelTalk — AI Chatbot powered by MistralAI
Entry point for the FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import chat, auth
import os


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

# Mount static files (CSS, JS, images)
static_path = os.path.join(os.path.dirname(__file__), "frontend", "assets")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/", summary="Serve Frontend")
async def serve_frontend():
    """Serve the main frontend index.html"""
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "index.html")
    return FileResponse(frontend_path)


@app.get("/health", summary="Health check")
def health_check() -> dict:
    """Health check endpoint to confirm the server is running."""
    return {
        "status": "ok",
        "message": "FeelTalk is running.",
        "endpoints": {
            "frontend": "GET /",
            "docs": "GET /docs",
            "signup": "POST /auth/signup",
            "chat": "POST /chat/",
        },
    }
