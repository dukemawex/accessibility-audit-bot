from __future__ import annotations

import json
import os


def generate_backlog(violations: dict, sources: list[dict[str, str]]) -> str:
    prompt = (
        "You are an accessibility lead. Prioritize fixes by user impact and effort. "
        "Return markdown with columns: Priority, Issue, Why it matters, Remediation steps.\n\n"
        f"Violations:\n{json.dumps(violations.get('violations', []), indent=2)}\n\n"
        f"WCAG sources:\n{json.dumps(sources, indent=2)}"
    )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _fallback_backlog(violations)

    try:
        import google.generativeai as genai
    except ModuleNotFoundError:
        return _fallback_backlog(violations)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text or _fallback_backlog(violations)


def _fallback_backlog(violations: dict) -> str:
    rows = []
    for item in violations.get("violations", []):
        rows.append(
            f"| P1 | {item.get('id')} | {item.get('description')} | {item.get('help')} |"
        )

    if not rows:
        rows.append("| P3 | No critical issues found | Keep regression scans in CI | Monitor new UI changes |")

    header = "| Priority | Issue | Why it matters | Remediation steps |\n|---|---|---|---|"
    return "\n".join(["# Remediation Backlog", header, *rows])
