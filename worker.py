__author__ = "Sam"

import asyncio
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx
from arq.connections import RedisSettings

from core.config import settings
from core.parsing import extract_content

# TODO: hook this up to the rotating proxy pool once infra finalises the contract

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

_BASE_HEADERS = {
    "User-Agent": _UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


# ── robots.txt ────────────────────────────────────────────────────────────────

async def _robots_allowed(url: str) -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    try:
        async with httpx.AsyncClient(timeout=8) as client:
            resp = await client.get(robots_url, headers={"User-Agent": _UA})
            if resp.status_code != 200:
                return True  # no robots.txt → assume allowed

        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.parse(resp.text.splitlines())
        return rp.can_fetch(_UA, url)

    except Exception:
        return True  # network error on robots check shouldn't block the job


# ── retry wrapper ─────────────────────────────────────────────────────────────

async def _with_retry(coro_fn, *args, retries: int = 3, backoff: float = 1.5):
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            return await coro_fn(*args)
        except Exception as exc:
            last_exc = exc
            if attempt < retries - 1:
                await asyncio.sleep(backoff ** attempt)
    raise last_exc  # type: ignore[misc]


# ── engines ───────────────────────────────────────────────────────────────────

async def _fetch_httpx(url: str) -> dict:
    async with httpx.AsyncClient(
        timeout=settings.request_timeout, follow_redirects=True
    ) as client:
        resp = await client.get(url, headers=_BASE_HEADERS)
        resp.raise_for_status()
        return {"engine": "httpx", "status_code": resp.status_code, "html": resp.text}


async def _fetch_playwright(url: str) -> dict:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent=_UA,
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )
        page = await ctx.new_page()
        await page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
        await page.goto(
            url,
            wait_until="networkidle",
            timeout=settings.request_timeout * 1000,
        )
        html = await page.content()
        await browser.close()

    # TODO: wire up optional screenshot capture here - product team keeps asking for it
    return {"engine": "playwright", "status_code": 200, "html": html}


# ── arq tasks ─────────────────────────────────────────────────────────────────

async def run_scrape(
    ctx,
    *,
    job_id: str,
    url: str,
    webhook_url: str,
    engine: str,
    extract: bool = False,
):
    result: dict = {"job_id": job_id, "url": url, "status": "failed", "data": None}

    try:
        if not await _robots_allowed(url):
            raise PermissionError(f"robots.txt disallows scraping {url}")

        fetch_fn = _fetch_playwright if engine == "playwright" else _fetch_httpx
        data = await _with_retry(fetch_fn, url)

        if extract:
            data["extracted"] = extract_content(data["html"], base_url=url)

        result["data"] = data
        result["status"] = "complete"

    except Exception as exc:
        result["error"] = str(exc)

    finally:
        # webhook delivery is best-effort; a flaky endpoint shouldn't tank the job
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                await client.post(webhook_url, json=result)
            except Exception:
                pass


async def parse_content(ctx, *, job_id: str, html: str, base_url: str = "") -> dict:
    """
    Standalone parsing task — can be enqueued separately if you already have the
    raw HTML and just need the structured extraction pass.
    """
    return {
        "job_id": job_id,
        "status": "complete",
        "data": extract_content(html, base_url=base_url),
    }


class WorkerSettings:
    functions = [run_scrape, parse_content]
    redis_settings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        database=settings.redis_db,
    )
    max_jobs = settings.worker_concurrency
    job_timeout = 120
    keep_result = 3600
