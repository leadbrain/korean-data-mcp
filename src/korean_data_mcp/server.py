"""
Korean Data MCP Server

Exposes Korean web data (Naver, Melon, Daangn, Bunjang, Musinsa, YES24)
as MCP tools powered by Apify actors.

Requires: APIFY_TOKEN environment variable
"""

import os
import asyncio
import httpx
from typing import Any
from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Apify helper
# ---------------------------------------------------------------------------

APIFY_BASE = "https://api.apify.com/v2"
APIFY_ACCOUNT = "oxygenated_quagmire"


def _get_token() -> str:
    token = os.environ.get("APIFY_TOKEN", "")
    if not token:
        raise RuntimeError(
            "APIFY_TOKEN environment variable is not set. "
            "Get your token at https://console.apify.com/account/integrations"
        )
    return token


async def _run_actor(actor_id: str, input_data: dict, timeout_secs: int = 60) -> list[dict]:
    """Run an Apify actor synchronously and return dataset items."""
    token = _get_token()
    url = f"{APIFY_BASE}/acts/{actor_id}/run-sync-get-dataset-items"
    params = {"token": token}

    async with httpx.AsyncClient(timeout=timeout_secs + 10) as client:
        resp = await client.post(url, json=input_data, params=params)
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="korean-data-mcp",
    instructions=(
        "Access real-time Korean web data including Naver place reviews, "
        "Melon music charts, Daangn/Bunjang marketplace listings, Korean news, "
        "and Musinsa fashion rankings. All tools require APIFY_TOKEN to be set."
    ),
)


# ---------------------------------------------------------------------------
# Tool 1: Naver Place Reviews
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_naver_place_reviews(
    place_url: str,
    max_reviews: int = 20,
) -> list[dict]:
    """
    Fetch reviews for a Naver Place (네이버 플레이스) listing.

    Args:
        place_url: Naver Place URL, e.g. https://map.naver.com/v5/entry/place/1234567890
        max_reviews: Maximum number of reviews to return (default 20, max 100)

    Returns:
        List of review objects with author, rating, content, date fields.
    """
    max_reviews = min(max_reviews, 100)
    return await _run_actor(
        f"{APIFY_ACCOUNT}/naver-place-reviews",
        {"placeUrl": place_url, "maxReviews": max_reviews},
    )


# ---------------------------------------------------------------------------
# Tool 2: Melon Chart
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_melon_chart(
    chart_type: str = "realtime",
    limit: int = 100,
) -> list[dict]:
    """
    Fetch the Melon music chart (멜론 차트).

    Args:
        chart_type: Chart to fetch — 'realtime' (실시간), 'hot100', 'daily', or 'weekly'
        limit: Number of songs to return (default 100, max 100)

    Returns:
        List of song objects with rank, title, artist, album fields.
    """
    limit = min(limit, 100)
    return await _run_actor(
        f"{APIFY_ACCOUNT}/melon-chart-scraper",
        {"chartType": chart_type, "limit": limit},
    )


# ---------------------------------------------------------------------------
# Tool 3: Daangn Marketplace
# ---------------------------------------------------------------------------

@mcp.tool()
async def search_daangn(
    keyword: str,
    region: str = "",
    max_items: int = 30,
) -> list[dict]:
    """
    Search Daangn Market (당근마켓) listings.

    Args:
        keyword: Search keyword in Korean or English
        region: Optional region filter (e.g. '서울', '강남구')
        max_items: Maximum number of listings to return (default 30, max 100)

    Returns:
        List of listing objects with title, price, location, image, url fields.
    """
    max_items = min(max_items, 100)
    input_data: dict[str, Any] = {"keyword": keyword, "maxItems": max_items}
    if region:
        input_data["region"] = region
    return await _run_actor(
        f"{APIFY_ACCOUNT}/daangn-market-scraper",
        input_data,
    )


# ---------------------------------------------------------------------------
# Tool 4: Bunjang Marketplace
# ---------------------------------------------------------------------------

@mcp.tool()
async def search_bunjang(
    keyword: str,
    max_items: int = 30,
    sort: str = "recent",
) -> list[dict]:
    """
    Search Bunjang (번개장터) — Korea's largest C2C marketplace.

    Args:
        keyword: Search keyword in Korean or English
        max_items: Maximum number of listings to return (default 30, max 100)
        sort: Sort order — 'recent' (최신순) or 'popular' (인기순)

    Returns:
        List of listing objects with title, price, condition, seller, image, url fields.
    """
    max_items = min(max_items, 100)
    return await _run_actor(
        f"{APIFY_ACCOUNT}/bunjang-market-scraper",
        {"keyword": keyword, "maxItems": max_items, "sort": sort},
    )


# ---------------------------------------------------------------------------
# Tool 5: Naver News
# ---------------------------------------------------------------------------

@mcp.tool()
async def search_naver_news(
    query: str,
    max_articles: int = 20,
    sort: str = "date",
) -> list[dict]:
    """
    Search Naver News (네이버 뉴스) for Korean news articles.

    Args:
        query: Search query in Korean or English
        max_articles: Maximum number of articles to return (default 20, max 100)
        sort: Sort order — 'date' (최신순) or 'sim' (관련도순)

    Returns:
        List of article objects with title, summary, source, date, url fields.
    """
    max_articles = min(max_articles, 100)
    return await _run_actor(
        f"{APIFY_ACCOUNT}/naver-news-scraper",
        {"query": query, "maxArticles": max_articles, "sort": sort},
    )


# ---------------------------------------------------------------------------
# Tool 6: Naver Place Search
# ---------------------------------------------------------------------------

@mcp.tool()
async def search_naver_places(
    keyword: str,
    location: str = "",
    max_places: int = 20,
) -> list[dict]:
    """
    Search Naver Map (네이버 지도) places by keyword.

    Args:
        keyword: Place type or name, e.g. '카페', '맛집', 'cafe'
        location: Location context, e.g. '홍대', '강남역', 'Itaewon'
        max_places: Maximum number of places to return (default 20, max 100)

    Returns:
        List of place objects with name, category, address, rating, reviewCount, url fields.
    """
    max_places = min(max_places, 100)
    search_query = f"{keyword} {location}".strip()
    return await _run_actor(
        f"{APIFY_ACCOUNT}/naver-place-search",
        {"query": search_query, "maxPlaces": max_places},
    )


# ---------------------------------------------------------------------------
# Tool 7: Musinsa Ranking
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_musinsa_ranking(
    category: str = "all",
    max_items: int = 50,
) -> list[dict]:
    """
    Fetch Musinsa (무신사) fashion ranking — Korea's leading fashion platform.

    Args:
        category: Category slug, e.g. 'all', 'outer', 'top', 'bottom', 'shoes', 'bag'
        max_items: Maximum number of items to return (default 50, max 100)

    Returns:
        List of product objects with rank, name, brand, price, discountRate, url fields.
    """
    max_items = min(max_items, 100)
    return await _run_actor(
        f"{APIFY_ACCOUNT}/musinsa-ranking-scraper",
        {"category": category, "maxItems": max_items},
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server via stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
