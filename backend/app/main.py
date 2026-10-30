# backend/app/main.py
# The DHARA backend server.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import ask, draft, emergency, panchayat, sms
from app.services.tts import AUDIO_DIR

app = FastAPI(title="DHARA backend")

# CORS lets the local front end (a web page on another address) call this server.
# "*" is fine for local testing and the demo; do not use it in a real product.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask.router)
app.include_router(emergency.router)
app.include_router(draft.router)
app.include_router(sms.router)
app.include_router(panchayat.router)

# Make the generated voice files downloadable at /audio/<name>.mp3
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")


@app.get("/")
async def root():
    return {"app": "DHARA", "status": "backend running"}