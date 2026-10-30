# backend/app/main.py
# The DHARA backend server. Phase 0: every endpoint returns a stub answer.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ask, draft, emergency, panchayat, sms

app = FastAPI(title="DHARA backend (Phase 0 stub)")

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


@app.get("/")
async def root():
    return {"app": "DHARA", "status": "stub backend running"}