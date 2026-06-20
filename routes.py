import uuid

from arq.jobs import Job
from fastapi import APIRouter, Depends, HTTPException, Request

from core.models import (
    BulkJobAccepted,
    BulkScrapeRequest,
    HealthResponse,
    JobAccepted,
    JobStatus,
    JobStatusResponse,
    ScrapeRequest,
)
from dependencies import EngineType, get_scraping_engine

router = APIRouter(tags=["scraping"])


# ── health ────────────────────────────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse)
async def health(request: Request):
    try:
        await request.app.state.arq_pool.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "unreachable"

    return HealthResponse(
        status="ok" if redis_status == "ok" else "degraded",
        redis=redis_status,
    )


# ── single scrape ─────────────────────────────────────────────────────────────

@router.post("/scrape", response_model=JobAccepted, status_code=202)
async def enqueue_scrape(
    request: Request,
    payload: ScrapeRequest,
    engine: EngineType = Depends(get_scraping_engine),
):
    job_id = str(uuid.uuid4())

    await request.app.state.arq_pool.enqueue_job(
        "run_scrape",
        job_id=job_id,
        url=str(payload.url),
        webhook_url=str(payload.webhook_url),
        engine=engine.value,
        extract=payload.extract_content,
    )

    return JobAccepted(job_id=job_id, status=JobStatus.queued)


# ── job status ────────────────────────────────────────────────────────────────

@router.get("/scrape/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str, request: Request):
    job = Job(job_id=job_id, redis=request.app.state.arq_pool)
    status = await job.status()

    # arq's "not_found" string means the ID was never queued or already expired
    if str(status) == "JobStatus.not_found":
        raise HTTPException(status_code=404, detail=f"Job {job_id!r} not found")

    result = None
    error = None

    if str(status) == "JobStatus.complete":
        try:
            # timeout=0 returns immediately if the result is already stored
            raw = await job.result(timeout=0)
            if isinstance(raw, dict) and "error" in raw:
                error = raw["error"]
            else:
                result = raw
        except Exception:
            pass

    return JobStatusResponse(
        job_id=job_id,
        status=str(status).replace("JobStatus.", ""),
        result=result,
        error=error,
    )


# ── bulk scrape ───────────────────────────────────────────────────────────────

@router.post("/scrape/bulk", response_model=BulkJobAccepted, status_code=202)
async def enqueue_bulk_scrape(request: Request, payload: BulkScrapeRequest):
    pool = request.app.state.arq_pool
    accepted: list[JobAccepted] = []

    for target in payload.targets:
        job_id = str(uuid.uuid4())

        # inline engine selection since we can't use Depends per-item in a loop
        from dependencies import EngineType, _parse_domain, HEAVY_DOMAINS

        try:
            domain = _parse_domain(str(target.url))
            needs_browser = any(
                domain == d or domain.endswith(f".{d}") for d in HEAVY_DOMAINS
            )
            engine = EngineType.playwright if needs_browser else EngineType.httpx
        except Exception:
            engine = EngineType.httpx

        await pool.enqueue_job(
            "run_scrape",
            job_id=job_id,
            url=str(target.url),
            webhook_url=str(target.webhook_url),
            engine=engine.value,
            extract=target.extract_content,
        )
        accepted.append(JobAccepted(job_id=job_id, status=JobStatus.queued))

    return BulkJobAccepted(jobs=accepted, enqueued=len(accepted))
