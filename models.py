from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    complete = "complete"
    failed = "failed"
    not_found = "not_found"


class ScrapeRequest(BaseModel):
    url: HttpUrl
    webhook_url: HttpUrl
    extract_content: bool = False  # run HTML parsing pass after scraping


class JobAccepted(BaseModel):
    job_id: str
    status: JobStatus = JobStatus.queued


class BulkScrapeRequest(BaseModel):
    targets: list[ScrapeRequest] = Field(..., min_length=1, max_length=20)


class BulkJobAccepted(BaseModel):
    jobs: list[JobAccepted]
    enqueued: int


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Any | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    redis: str
