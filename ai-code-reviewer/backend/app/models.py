from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import uuid


def new_id() -> str:
    return uuid.uuid4().hex


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class FindingCategory(str, Enum):
    bug = "bug"
    security = "security"
    performance = "performance"
    style = "style"
    best_practice = "best_practice"


class ReviewStatus(str, Enum):
    queued = "queued"
    analyzing = "analyzing"
    completed = "completed"
    failed = "failed"


# ---------- Request payloads ----------

class AnalyzeRequest(BaseModel):
    repo_full_name: str = Field(..., description="e.g. 'org/repo'")
    pr_number: int
    pr_title: str
    author: str
    language: str = "auto"
    diff: str = Field(..., description="Unified diff / patch text of the PR")


class RuleUpdateRequest(BaseModel):
    name: str
    category: FindingCategory
    enabled: bool = True
    severity_threshold: Severity = Severity.medium
    org_id: str = "default"


# ---------- Core entities ----------

class Finding(BaseModel):
    id: str = Field(default_factory=new_id)
    review_id: str
    file: str
    line: Optional[int] = None
    severity: Severity
    category: FindingCategory
    message: str
    suggestion: Optional[str] = None
    doc_link: Optional[str] = None


class Review(BaseModel):
    id: str = Field(default_factory=new_id)
    repo_full_name: str
    pr_number: int
    pr_title: str
    author: str
    status: ReviewStatus = ReviewStatus.queued
    score: Optional[float] = None
    findings_count: int = 0
    critical_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    error: Optional[str] = None


class Rule(BaseModel):
    id: str = Field(default_factory=new_id)
    org_id: str = "default"
    name: str
    category: FindingCategory
    enabled: bool = True
    severity_threshold: Severity = Severity.medium
    created_at: datetime = Field(default_factory=datetime.utcnow)
