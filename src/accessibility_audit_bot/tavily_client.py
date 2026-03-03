from __future__ import annotations

import os
from typing import Any

FALLBACK_SOURCES = [
    {
        "title": "WCAG 2 Overview",
        "url": "https://www.w3.org/WAI/standards-guidelines/wcag/",
        "summary": "WCAG explains POUR principles and conformance levels A/AA/AAA.",
    },
    {
        "title": "Understanding Success Criterion 1.1.1",
        "url": "https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html",
        "summary": "All non-text content should have a text alternative.",
    },
]


def fetch_wcag_summaries(query: str = "WCAG accessibility remediation summary") -> list[dict[str, str]]:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return FALLBACK_SOURCES

    try:
        from tavily import TavilyClient
    except ModuleNotFoundError:
        return FALLBACK_SOURCES

    client = TavilyClient(api_key=api_key)
    result: dict[str, Any] = client.search(query=query, max_results=3, topic="general")
    return [
        {
            "title": item.get("title", "Untitled"),
            "url": item.get("url", ""),
            "summary": item.get("content", "")[:500],
        }
        for item in result.get("results", [])
    ] or FALLBACK_SOURCES
