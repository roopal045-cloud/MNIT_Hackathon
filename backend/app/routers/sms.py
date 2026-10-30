# backend/app/routers/sms.py
# POST /sms - Phase 0 STUB: keyword replies for the mock feature-phone screen.
# All numbers and steps are NEEDS HUMAN VERIFICATION. Label as "prototype".

from fastapi import APIRouter

from app.models import SmsRequest, SmsResponse

router = APIRouter()


@router.post("/sms", response_model=SmsResponse)
async def sms(req: SmsRequest):
    keyword = req.text.strip().upper()

    if keyword == "FASAL":
        reply = (
            "FASAL: 1) Inform insurer within 72 hrs "
            "2) Take photos of the field "
            "3) Visit krishi office "
            "(PLACEHOLDER - NEEDS HUMAN VERIFICATION)"
        )
    elif keyword == "EMERGENCY":
        reply = (
            "EMERGENCY: 112 (all), 101 fire, 108 ambulance, 100 police "
            "(NEEDS HUMAN VERIFICATION)"
        )
    else:
        reply = "Send FASAL for crop damage help, or EMERGENCY for emergency numbers."

    return SmsResponse(reply_text=reply)