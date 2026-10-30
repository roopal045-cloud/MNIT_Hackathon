# backend/app/routers/draft.py
# POST /draft - Phase 0 STUB: fixed checklist, no real PDF yet.
# Nothing is submitted anywhere, and no Aadhaar or ID numbers are collected.

from fastapi import APIRouter

from app.models import ChecklistItem, DraftRequest, DraftResponse

router = APIRouter()


@router.post("/draft", response_model=DraftResponse)
async def draft(req: DraftRequest):
    is_marathi = req.language == "mr"
    missing_item = "नुकसानीचे फोटो" if is_marathi else "नुकसान की फोटो"

    return DraftResponse(
        pdf_url=None,  # real PDF link comes in Phase 4
        checklist=[
            ChecklistItem(
                item="७/१२ उतारा" if is_marathi else "7/12 उतारा (भूमि रिकॉर्ड)",
                status="have",
            ),
            ChecklistItem(
                item="बँक पासबुक" if is_marathi else "बैंक पासबुक",
                status="have",
            ),
            ChecklistItem(item=missing_item, status="missing"),
        ],
        checklist_audio_url=None,
        missing=[missing_item],
    )