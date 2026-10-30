# backend/app/routers/emergency.py
# POST /emergency - Phase 0 STUB: always returns the fire emergency.
# Numbers and safety lines are NEEDS HUMAN VERIFICATION.

from fastapi import APIRouter

from app.models import EmergencyRequest, EmergencyResponse, Hospital

router = APIRouter()

MESSAGE_HI = "आग लगी है! तुरंत 101 (दमकल) या 112 पर कॉल करें।"
MESSAGE_MR = "आग लागली आहे! लगेच 101 (अग्निशमन) किंवा 112 वर कॉल करा."
SAFETY_HI = "तुरंत सुरक्षित जगह पर बाहर निकलें।"  # NEEDS HUMAN VERIFICATION
SAFETY_MR = "लगेच सुरक्षित जागी बाहेर पडा."  # NEEDS HUMAN VERIFICATION


@router.post("/emergency", response_model=EmergencyResponse)
async def emergency(req: EmergencyRequest):
    is_marathi = req.language == "mr"
    return EmergencyResponse(
        type="fire",
        number="101",  # NEEDS HUMAN VERIFICATION (112 is the unified number)
        call_uri="tel:101",
        message_text=MESSAGE_MR if is_marathi else MESSAGE_HI,
        audio_url=None,
        safety_line=SAFETY_MR if is_marathi else SAFETY_HI,
        hospitals=[
            Hospital(
                name="PLACEHOLDER - Civil Hospital, Nashik",
                distance_km=3.2,
                maps_url="https://www.google.com/maps/search/?api=1&query=Civil+Hospital+Nashik",
            )
        ],
    )