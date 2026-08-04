from app.database import get_db

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/dashboard")
async def get_dashboard():
    """
    FR-5: Aggregate metrics for the analytics dashboard — review volume, average
    score, severity breakdown, and recent activity.
    """
    db = get_db()

    total_reviews = await db.reviews.count_documents({"status": "completed"})
    total_findings = await db.findings.count_documents({})

    severity_pipeline = [
        {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
    ]
    severity_breakdown = {
        doc["_id"]: doc["count"] async for doc in db.findings.aggregate(severity_pipeline)
    }

    category_pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
    ]
    category_breakdown = {
        doc["_id"]: doc["count"] async for doc in db.findings.aggregate(category_pipeline)
    }

    score_pipeline = [
        {"$match": {"score": {"$ne": None}}},
        {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}},
    ]
    score_result = await db.reviews.aggregate(score_pipeline).to_list(1)
    avg_score = round(score_result[0]["avg_score"], 1) if score_result else None

    duration_pipeline = [
        {"$match": {"duration_ms": {"$ne": None}}},
        {"$group": {"_id": None, "avg_duration_ms": {"$avg": "$duration_ms"}}},
    ]
    duration_result = await db.reviews.aggregate(duration_pipeline).to_list(1)
    avg_duration_ms = (
        round(duration_result[0]["avg_duration_ms"]) if duration_result else None
    )

    recent = await db.reviews.find({}, {"_id": 0}).sort("created_at", -1).limit(10).to_list(10)

    return {
        "metrics": {
            "total_reviews": total_reviews,
            "total_findings": total_findings,
            "avg_quality_score": avg_score,
            "avg_review_time_ms": avg_duration_ms,
        },
        "severity_breakdown": severity_breakdown,
        "category_breakdown": category_breakdown,
        "recent_reviews": recent,
    }
