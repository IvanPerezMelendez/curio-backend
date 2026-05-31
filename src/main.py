from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.modules.auth.router import router as auth_router
from src.modules.chat.router import router as chat_router
from src.modules.content.router import router as content_router
from src.modules.sessions.router import router as sessions_router
from src.modules.users.router import router as users_router

app = FastAPI(
    title="Curio API",
    version="0.1.0",
    description="Backend for the Curio spaced-repetition PWA.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(sessions_router)
app.include_router(content_router)
app.include_router(chat_router)


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}
