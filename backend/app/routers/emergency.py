# backend/app/routers/emergency.py
# POST /emergency - real version. Pre-written reply, no AI, no document search.
# Numbers and safety lines come from data/emergency/emergency.json
# (NEEDS HUMAN VERIFICATION until VERIFICATION.md is confirmed).

from fastapi import APIRouter

from app.models import EmergencyRequest, EmergencyResponse
from app.services.emergency import get_emergency_reply

router = APIRouter()


@router.post("/emergency", response_model=EmergencyResponse)
async def emergency(req: EmergencyRequest):
    reply = get_emergency_reply(
        type_=req.type,
        language=req.language,
        lat=req.lat,
        lon=req.lon,
    )
    return EmergencyResponse(**reply)