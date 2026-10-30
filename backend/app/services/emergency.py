# backend/app/services/emergency.py - empty for now, filled in during Phase 1
# backend/app/services/emergency.py
# Emergency detection and pre-written replies. NO AI and NO document search here.
# Numbers and safety lines come from data/emergency/emergency.json and are
# NEEDS HUMAN VERIFICATION until Person B's VERIFICATION.md is filled in.
# Location is used for one request only and is never stored or logged.

import json
import math
from pathlib import Path
from urllib.parse import quote_plus

# services -> app -> backend -> project root
DATA_DIR = Path(__file__).resolve().parents[3] / "data"
EMERGENCY_FILE = DATA_DIR / "emergency" / "emergency.json"
HOSPITAL_FILE = DATA_DIR / "hospitals" / "nashik_fallback.json"


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


try:
    ENTRIES = {e["type"]: e for e in _load_json(EMERGENCY_FILE)["entries"]}
except Exception as err:
    print("WARNING: could not load emergency.json:", err)
    ENTRIES = {}

# English words, only so we can test from the docs page. NOT the real detection.
ENGLISH_TEST_WORDS = {
    "fire": "fire",
    "snake": "snakebite",
    "snakebite": "snakebite",
    "accident": "accident",
    "flood": "flood",
    "bleeding": "labour_bleeding",
    "poison": "pesticide_poisoning",
    "chest pain": "heart_breathing",
}

# Used when we do not know which emergency it is. NEEDS HUMAN VERIFICATION.
GENERIC = {
    "type": "general",
    "number": "112",
    "call_uri": "tel:112",
    "message_hi": "आपातकाल में तुरंत 112 पर कॉल करें।",
    "message_mr": "आपत्कालीन परिस्थितीत लगेच 112 वर कॉल करा.",
    "safety_line_hi": "",
    "safety_line_mr": "",
}

PUNCTUATION = set(".,;:!?\"'()[]{}<>-_/\\|।॥…–—“”‘’")


def _normalize(text):
    # lower case, punctuation to spaces, one space between words
    text = "".join(" " if ch in PUNCTUATION else ch for ch in text.lower())
    return " ".join(text.split())


def _hit(keyword, normalized):
    kw = _normalize(keyword)
    if not kw:
        return False
    if " " in kw:
        # phrase: match inside the text, also if the speech tool dropped spaces
        return kw in normalized or kw.replace(" ", "") in normalized.replace(" ", "")
    # single word: must be a whole word ("आग" should not match "आगे")
    return kw in normalized.split()


def detect_emergency(text):
    # Returns the emergency type (like "fire") or None. Tuned to over-trigger.
    if not text:
        return None
    normalized = _normalize(text)

    for type_, entry in ENTRIES.items():
        words = entry.get("trigger_keywords_hi", []) + entry.get("trigger_keywords_mr", [])
        for kw in words:
            if _hit(kw, normalized):
                return type_

    for kw, type_ in ENGLISH_TEST_WORDS.items():
        if _hit(kw, normalized):
            return type_
    return None


def _distance_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _hospitals(lat, lon):
    try:
        rows = _load_json(HOSPITAL_FILE)["hospitals"]
    except Exception:
        return []

    out = []
    for h in rows:
        dist = 0.0  # 0.0 means "unknown"
        if lat is not None and lon is not None and (h.get("lat") or h.get("lon")):
            dist = round(_distance_km(lat, lon, h["lat"], h["lon"]), 1)
        query = quote_plus(h["name"] + " " + h.get("address", ""))
        out.append({
            "name": h["name"],
            "distance_km": dist,
            "maps_url": "https://www.google.com/maps/search/?api=1&query=" + query,
        })
    # known distances first (nearest first), unknown ones last
    out.sort(key=lambda x: (x["distance_km"] == 0.0, x["distance_km"]))
    return out[:3]


def get_emergency_reply(type_=None, language="hi", lat=None, lon=None):
    # Builds the pre-written reply. audio_url is added later by the router.
    lang = "mr" if language == "mr" else "hi"
    entry = ENTRIES.get(type_) if type_ else None
    if entry is None:
        entry = GENERIC

    return {
        "type": entry["type"],
        "number": entry["number"],
        "call_uri": entry["call_uri"],
        "message_text": entry["message_" + lang],
        "audio_url": None,
        "safety_line": entry["safety_line_" + lang],
        "hospitals": _hospitals(lat, lon),
    }