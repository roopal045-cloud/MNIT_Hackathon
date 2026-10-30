# backend/app/routers/ask.py
# POST /ask - Phase 0 STUB: returns fixed answers, no AI yet.
# Everything marked NEEDS HUMAN VERIFICATION must be checked against
# the real official document before the demo.

from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from app.models import AskResponse, Source

router = APIRouter()

FIRE_WORDS = ["आग", "आगी", "fire"]

ANSWER_MR = (
    "पावसामुळे कापसाचे नुकसान झाले असेल, तर नुकसान झाल्यापासून ७२ तासांच्या आत "
    "पीक विमा कंपनीला, कृषी कार्यालयाला किंवा पीक विमा ॲपवर कळवा. "
    "शेताचे फोटो जवळ ठेवा."
)
ANSWER_HI = (
    "बारिश से कपास की फसल खराब हुई हो तो नुकसान के 72 घंटे के अंदर "
    "फसल बीमा कंपनी, कृषि कार्यालय या फसल बीमा ऐप पर सूचना दें। "
    "खेत की फोटो साथ रखें।"
)
TRANSCRIPT_MR = "माझ्या कापसाचे पावसाने नुकसान झाले, काय करावे?"
TRANSCRIPT_HI = "मेरी कपास की फसल बारिश से खराब हो गई, क्या करूँ?"


@router.post("/ask", response_model=AskResponse)
async def ask(
    audio: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    language: str = Form("hi"),
    mode: str = Form("normal"),
    role: str = Form("farmer"),
):
    lang = "mr" if language == "mr" else "hi"
    spoken = text or ""

    # Stub emergency: if the text mentions fire, flag it as an emergency.
    if any(word in spoken.lower() for word in FIRE_WORDS):
        return AskResponse(
            transcript=spoken,
            language=lang,
            is_emergency=True,
            answer_text="",
            audio_url=None,
            source=None,
            confidence=1.0,
            refused=False,
            offer_application=None,
        )

    # Stub normal answer: cotton rain damage.
    return AskResponse(
        transcript=spoken or (TRANSCRIPT_MR if lang == "mr" else TRANSCRIPT_HI),
        language=lang,
        is_emergency=False,
        answer_text=ANSWER_MR if lang == "mr" else ANSWER_HI,
        audio_url=None,
        source=Source(
            doc="PMFBY guidelines (PLACEHOLDER - NEEDS HUMAN VERIFICATION)",
            page="NEEDS HUMAN VERIFICATION",
            snippet="Localized calamity: inform within 72 hours (verify in real document)",
        ),
        confidence=0.86,
        refused=False,
        offer_application="crop_damage",
    )