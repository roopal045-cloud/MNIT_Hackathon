# backend/app/routers/panchayat.py
# GET /panchayat/stats - Phase 0 STUB: simulated counts of questions by topic.
# These numbers are made up for the demo and are flagged simulated=True.

from fastapi import APIRouter

from app.models import PanchayatStatsResponse, TopicCount

router = APIRouter()


@router.get("/panchayat/stats", response_model=PanchayatStatsResponse)
async def panchayat_stats():
    return PanchayatStatsResponse(
        topics=[
            TopicCount(topic="Crop damage", count=42),
            TopicCount(topic="Schemes", count=31),
            TopicCount(topic="Health", count=18),
            TopicCount(topic="Emergency", count=6),
        ],
        simulated=True,
    )