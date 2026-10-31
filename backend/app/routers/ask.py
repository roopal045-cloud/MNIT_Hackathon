# backend/app/routers/ask.py
# POST /ask: audio OR text in -> emergency check -> answer -> voice out.
# The normal answer is still a PLACEHOLDER until rag.py + llm.py are connected.

from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from app.models import AskResponse, Source
from app.services.asr import transcribe
from app.services.emergency import detect_emergency, get_emergency_reply
from app.services.tts import make_speech

router = APIRouter()

# PLACEHOLDER answers. NEEDS HUMAN VERIFICATION (72 hours, wording).
ANSWER_HI = (
    "बारिश से कपास की फसल खराब हो तो नुकसान के 72 घंटे के अंदर "
    "फसल बीमा कंपनी या कृषि कार्यालय को सूचना दें। खेत की फोटो साथ रखें।"
)
ANSWER_MR = (
    "पावसामुळे कापसाचे नुकसान झाल्यास 72 तासांच्या आत "
    "पीक विमा कंपनीला किंवा कृषी कार्यालयाला कळवा. शेताचे फोटो जवळ ठेवा."
)
NO_INPUT_HI = "कृपया बोलकर या लिखकर सवाल पूछें।"
NO_INPUT_MR = "कृपया बोलून किंवा लिहून प्रश्न विचारा."

LOW_DATA_MAX_CHARS = 200


def _short(text, limit):
    # low_data mode: shorter voice file (cut at a sentence end)
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for mark in ("।", "."):
        i = cut.rfind(mark)
        if i > 40:
            return cut[: i + 1]
    return cut


@router.post("/ask", response_model=AskResponse)
async def ask(
    audio: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    language: str = Form("hi"),
    mode: str = Form("normal"),
    role: str = Form("farmer"),
):
    lang = "mr" if language == "mr" else "hi"

    # 1. Get the words: from audio if given, otherwise from text.
    transcript = (text or "").strip()
    if audio is not None:
        data = await audio.read()
        if data:
            try:
                transcript = (transcribe(data, lang) or "").strip()
            except Exception as e:
                print("[ask] transcribe failed:", e)

    # 2. Nothing heard or typed.
    if not transcript:
        msg = NO_INPUT_MR if lang == "mr" else NO_INPUT_HI
        return AskResponse(
            transcript="", language=lang, is_emergency=False, answer_text=msg,
            audio_url=make_speech(msg, lang), source=None, confidence=0.0,
            refused=True, offer_application=None,
        )

    # 3. Emergency check runs FIRST. No search, no AI.
    etype = detect_emergency(transcript)
    if etype:
        reply = get_emergency_reply(etype, lang)
        spoken = (reply["message_text"] + " " + reply["safety_line"]).strip()
        if mode == "low_data":
            spoken = _short(spoken, LOW_DATA_MAX_CHARS)
        return AskResponse(
            transcript=transcript, language=lang, is_emergency=True,
            answer_text=reply["message_text"], audio_url=make_speech(spoken, lang),
            source=None, confidence=1.0, refused=False, offer_application=None,
        )

    # 4. Normal answer (PLACEHOLDER until rag.py and llm.py are connected).
    answer = ANSWER_MR if lang == "mr" else ANSWER_HI
    spoken = _short(answer, LOW_DATA_MAX_CHARS) if mode == "low_data" else answer
    return AskResponse(
        transcript=transcript, language=lang, is_emergency=False,
        answer_text=answer, audio_url=make_speech(spoken, lang),
        source=Source(
            doc="PMFBY guidelines (PLACEHOLDER - NEEDS HUMAN VERIFICATION)",
            page="NEEDS HUMAN VERIFICATION",
            snippet="Localized calamity: inform within 72 hours (verify in real document)",
        ),
        confidence=0.86, refused=False, offer_application="crop_damage",
    )
