# backend/app/routers/ask.py
# POST /ask: audio OR text in -> emergency check -> search the documents ->
# Gemini words the answer -> voice out. If nothing reliable is found, it refuses
# politely and points to a human office.

from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from app.models import AskResponse, Source
from app.services.asr import transcribe
from app.services.emergency import detect_emergency, get_emergency_reply
from app.services.llm import word_answer
from app.services.rag import search
from app.services.tts import make_speech

router = APIRouter()

NO_INPUT_HI = "कृपया बोलकर या लिखकर सवाल पूछें।"
NO_INPUT_MR = "कृपया बोलून किंवा लिहून प्रश्न विचारा."

# Refusal: no phone numbers here until they are verified.
REFUSE_HI = (
    "इसका पक्का जवाब मुझे सरकारी दस्तावेज़ों में नहीं मिला। "
    "कृपया अपने ग्राम पंचायत कार्यालय, CSC केंद्र या किसान कॉल सेंटर से पूछें।"
)
REFUSE_MR = (
    "याचे खात्रीशीर उत्तर मला सरकारी कागदपत्रांत सापडले नाही. "
    "कृपया तुमच्या ग्रामपंचायत कार्यालयात, CSC केंद्रात किंवा किसान कॉल सेंटरला विचारा."
)

LOW_DATA_MAX_CHARS = 200
MIN_SCORE = 0.70  # below this the search result is too weak to trust

# which application the "Shall I prepare your application?" offer is for
OFFER_FOR_SCHEME = {"pmfby": "crop_damage", "pmmvy": "pregnancy_benefit"}


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


def _best_snippet(text, key="72", limit=220):
    # the sentence that contains the key number, otherwise the start of the chunk
    for part in text.replace("\n", " ").split(". "):
        if key in part:
            part = part.strip()
            return part if len(part) <= limit else part[:limit].rsplit(" ", 1)[0] + "..."
    return text[:200]

def _refusal(transcript, lang, mode):
    msg = REFUSE_MR if lang == "mr" else REFUSE_HI
    spoken = _short(msg, LOW_DATA_MAX_CHARS) if mode == "low_data" else msg
    return AskResponse(
        transcript=transcript, language=lang, is_emergency=False, answer_text=msg,
        audio_url=make_speech(spoken, lang), source=None, confidence=0.0,
        refused=True, offer_application=None,
    )


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

    # 4. Search the official documents.
    try:
        found = search(transcript, n=3)
    except Exception as e:
        print("[ask] search failed:", e)
        return _refusal(transcript, lang, mode)

    chunks = found["chunks"]
    if not chunks or chunks[0]["score"] < MIN_SCORE:
        return _refusal(transcript, lang, mode)

    # 5. Gemini words the answer ONLY from the found text.
    source_text = "\n\n".join(c["text"] for c in chunks)
    answer = word_answer(transcript, source_text, lang, role)
    if not answer:
        return _refusal(transcript, lang, mode)

    best = chunks[0]
    spoken = _short(answer, LOW_DATA_MAX_CHARS) if mode == "low_data" else answer
    return AskResponse(
        transcript=transcript, language=lang, is_emergency=False,
        answer_text=answer, audio_url=make_speech(spoken, lang),
        source=Source(
            doc=best["doc"],
            page=str(best["page"]),
            snippet=_best_snippet(best["text"]),
        ),
        confidence=min(1.0, best["score"]), refused=False,
        offer_application=OFFER_FOR_SCHEME.get(found["scheme"]),
    )