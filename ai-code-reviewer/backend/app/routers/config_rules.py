from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import Rule, RuleUpdateRequest

router = APIRouter(prefix="/api/v1/config", tags=["config"])


@router.post("/rules")
async def upsert_rule(payload: RuleUpdateRequest):
    """FR-4: Create or update a team's review rule configuration."""
    db = get_db()
    existing = await db.rules.find_one({"org_id": payload.org_id, "name": payload.name})

    if existing:
        await db.rules.update_one(
            {"id": existing["id"]},
            {
                "$set": {
                    "enabled": payload.enabled,
                    "severity_threshold": payload.severity_threshold,
                    "category": payload.category,
                }
            },
        )
        updated = await db.rules.find_one({"id": existing["id"]}, {"_id": 0})
        return updated

    rule = Rule(
        org_id=payload.org_id,
        name=payload.name,
        category=payload.category,
        enabled=payload.enabled,
        severity_threshold=payload.severity_threshold,
    )
    await db.rules.insert_one(rule.model_dump())
    return rule.model_dump()


@router.get("/rules")
async def list_rules(org_id: str = "default"):
    db = get_db()
    return await db.rules.find({"org_id": org_id}, {"_id": 0}).to_list(200)


@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: str):
    db = get_db()
    result = await db.rules.delete_one({"id": rule_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"deleted": True}
