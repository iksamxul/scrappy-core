__author__ = "Sam"

import re
from enum import Enum

from fastapi import Request

# domains that consistently get JS-walled or 403'd with a plain httpx request
HEAVY_DOMAINS = frozenset({
    "linkedin.com",
    "instagram.com",
    "x.com",
    "twitter.com",
    "glassdoor.com",
    "zillow.com",
    "realtor.com",
})

# TODO: cloudflare is still slipping through on a few of these even with playwright,
#       need to look into patchright or a stealth plugin


class EngineType(str, Enum):
    httpx = "httpx"
    playwright = "playwright"


def _parse_domain(url: str) -> str:
    m = re.search(r"https?://(?:www\.)?([^/?#]+)", url)
    if not m:
        raise ValueError(f"Can't extract domain from: {url!r}")
    return m.group(1).lower()


async def get_scraping_engine(request: Request) -> EngineType:
    """
    Inspects the target URL from the request body and returns the appropriate
    scraping engine. Starlette caches the body after first read so this is
    safe to call alongside a Pydantic body param in the same route.
    """
    try:
        body = await request.json()
        domain = _parse_domain(str(body.get("url", "")))
    except Exception:
        return EngineType.httpx

    needs_browser = any(
        domain == d or domain.endswith(f".{d}") for d in HEAVY_DOMAINS
    )
    return EngineType.playwright if needs_browser else EngineType.httpx
