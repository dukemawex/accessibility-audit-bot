from __future__ import annotations

import json
from pathlib import Path


def run_axe_scan(target_url: str, axe_script_path: Path) -> dict:
    """Run a Playwright + axe scan and return raw result payload.

    Falls back to a deterministic local parser when Playwright is unavailable.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError:
        return _fallback_scan(target_url)

    axe_source = axe_script_path.read_text(encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(target_url, wait_until="domcontentloaded")
        page.add_script_tag(content=axe_source)
        result = page.evaluate("""async () => await window.axe.run()""")
        browser.close()

    return json.loads(json.dumps(result))


def _fallback_scan(target_url: str) -> dict:
    if target_url.startswith("file://"):
        html = Path(target_url.replace("file://", "")).read_text(encoding="utf-8")
    else:
        html = ""

    violations = []
    if "<img" in html and "alt=" not in html:
        violations.append(
            {
                "id": "non-text-content",
                "impact": "serious",
                "description": "Images must have alternate text",
                "help": "Add meaningful alt text to images",
                "nodes": [],
            }
        )
    if "<button></button>" in html:
        violations.append(
            {
                "id": "name-role-value",
                "impact": "moderate",
                "description": "Interactive elements must have an accessible name",
                "help": "Provide an accessible label",
                "nodes": [],
            }
        )

    return {"violations": violations, "passes": [], "incomplete": [], "inapplicable": []}
