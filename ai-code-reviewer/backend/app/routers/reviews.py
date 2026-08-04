from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import AnalyzeRequest, Review, Finding, ReviewStatus
from app.services.ai_reviewer import ai_reviewer

router = APIRouter(prefix="/api/v1/reviews", tags=["reviews"])


@router.post("/analyze")
async def analyze_pr(payload: AnalyzeRequest):
    """
    FR-1 / FR-2: Accepts a PR diff (normally delivered via a GitHub/GitLab/Bitbucket
    webhook upstream of this endpoint) and runs the AI analysis engine against it.
    """
    db = get_db()

    review = Review(
        repo_full_name=payload.repo_full_name,
        pr_number=payload.pr_number,
        pr_title=payload.pr_title,
        author=payload.author,
        status=ReviewStatus.analyzing,
    )
    await db.reviews.insert_one(review.model_dump())

    try:
        result = ai_reviewer.analyze_diff(
            pr_title=payload.pr_title,
            language=payload.language,
            diff=payload.diff,
        )
    except Exception as exc:  # noqa: BLE001
        await db.reviews.update_one(
            {"id": review.id},
            {"$set": {"status": ReviewStatus.failed, "error": str(exc)}},
        )
        raise HTTPException(status_code=502, detail=f"AI review engine failed: {exc}") from exc

    findings = [
        Finding(
            review_id=review.id,
            file=f["file"],
            line=f.get("line"),
            severity=f["severity"],
            category=f["category"],
            message=f["message"],
            suggestion=f.get("suggestion"),
        )
        for f in result.get("findings", [])
    ]
    if findings:
        await db.findings.insert_many([f.model_dump() for f in findings])

    critical_count = sum(1 for f in findings if f.severity in ("critical", "high"))

    await db.reviews.update_one(
        {"id": review.id},
        {
            "$set": {
                "status": ReviewStatus.completed,
                "score": result.get("score"),
                "findings_count": len(findings),
                "critical_count": critical_count,
                "completed_at": datetime.utcnow(),
                "duration_ms": result.get("duration_ms"),
            }
        },
    )

    return {
        "review_id": review.id,
        "status": "completed",
        "summary": result.get("summary"),
        "score": result.get("score"),
        "duration_ms": result.get("duration_ms"),
        "findings": [f.model_dump() for f in findings],
    }


@router.get("/{review_id}")
async def get_review(review_id: str):
    db = get_db()
    review = await db.reviews.find_one({"id": review_id}, {"_id": 0})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    findings = await db.findings.find({"review_id": review_id}, {"_id": 0}).to_list(500)
    return {"review": review, "findings": findings}


@router.get("")
async def list_reviews(limit: int = 20):
    db = get_db()
    cursor = db.reviews.find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
    return await cursor.to_list(limit)
