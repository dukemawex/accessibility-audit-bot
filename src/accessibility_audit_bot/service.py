from __future__ import annotations

import json
from pathlib import Path

from .gemini_client import generate_backlog
from .scanner import run_axe_scan
from .tavily_client import fetch_wcag_summaries


def run_audit(target_url: str | None = None, root_dir: Path | None = None) -> dict:
    root = root_dir or Path.cwd()
    artifacts_dir = root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    page_url = target_url or f"file://{(root / 'sample_site' / 'index.html').resolve()}"
    violations = run_axe_scan(page_url, root / "src" / "accessibility_audit_bot" / "assets" / "axe.min.js")
    sources = fetch_wcag_summaries()
    backlog_md = generate_backlog(violations, sources)

    (artifacts_dir / "violations.json").write_text(
        json.dumps(violations, indent=2), encoding="utf-8"
    )
    (artifacts_dir / "sources.json").write_text(json.dumps(sources, indent=2), encoding="utf-8")
    (artifacts_dir / "remediation_backlog.md").write_text(backlog_md, encoding="utf-8")

    return {
        "violations_count": len(violations.get("violations", [])),
        "artifacts": {
            "violations_json": artifacts_dir / "violations.json",
            "remediation_backlog_md": artifacts_dir / "remediation_backlog.md",
            "sources_json": artifacts_dir / "sources.json",
        },
        "backlog_preview": "\n".join(backlog_md.splitlines()[:8]),
    }
