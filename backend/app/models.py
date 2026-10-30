# backend/app/models.py
# Pydantic models that match the shared DHARA API contract exactly.
# (Pydantic = a tool that checks data has the right shape.)

from typing import Literal, Optional

from pydantic import BaseModel

Language = Literal["hi", "mr"]
Mode = Literal["normal", "low_data"]
Role = Literal["farmer", "asha"]
Scheme = Literal["crop_damage", "pregnancy_benefit"]


# ---------- POST /ask ----------
# The request is multipart form data (audio file OR text field), so its
# fields are read directly in routers/ask.py. Only the answer is a model.

class Source(BaseModel):
    doc: str
    page: str
    snippet: str


class AskResponse(BaseModel):
    transcript: str
    language: Language
    is_emergency: bool
    answer_text: str
    audio_url: Optional[str] = None
    source: Optional[Source] = None
    confidence: float
    refused: bool
    offer_application: Optional[Scheme] = None


# ---------- POST /emergency ----------

class EmergencyRequest(BaseModel):
    language: Language
    type: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class Hospital(BaseModel):
    name: str
    distance_km: float
    maps_url: str


class EmergencyResponse(BaseModel):
    type: str
    number: str
    call_uri: str
    message_text: str
    audio_url: Optional[str] = None
    safety_line: str
    hospitals: list[Hospital]


# ---------- POST /draft ----------

class DraftRequest(BaseModel):
    scheme: Scheme
    language: Language
    answers: dict


class ChecklistItem(BaseModel):
    item: str
    status: Literal["have", "missing"]


class DraftResponse(BaseModel):
    pdf_url: Optional[str] = None
    checklist: list[ChecklistItem]
    checklist_audio_url: Optional[str] = None
    missing: list[str]


# ---------- POST /sms ----------

class SmsRequest(BaseModel):
    text: str


class SmsResponse(BaseModel):
    reply_text: str


# ---------- GET /panchayat/stats ----------

class TopicCount(BaseModel):
    topic: str
    count: int


class PanchayatStatsResponse(BaseModel):
    topics: list[TopicCount]
    simulated: bool = True