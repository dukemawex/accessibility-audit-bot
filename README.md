# accessibility-audit-bot

`accessibility-audit-bot` combines automated a11y scanning with an LLM-prioritized remediation backlog.

## Mission
- Run stable accessibility scans using **Playwright + axe-core** against a local HTML sample.
- Retrieve WCAG guidance summaries through **Tavily**.
- Use **Gemini** to produce a prioritized remediation backlog with fix instructions.
- Emit machine- and human-friendly artifacts:
  - `artifacts/violations.json`
  - `artifacts/remediation_backlog.md`
  - `artifacts/sources.json`
- Provide an API demo endpoint at `POST /audit`.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
playwright install chromium
uvicorn accessibility_audit_bot.app:app --reload
```

Call the endpoint:
```bash
curl -X POST http://127.0.0.1:8000/audit -H 'content-type: application/json' -d '{}'
```

## Environment variables
- `TAVILY_API_KEY` (optional; falls back to embedded WCAG summaries)
- `GEMINI_API_KEY` (optional; falls back to deterministic markdown backlog)

## Project layout
- `sample_site/index.html`: deterministic local fixture scanned in CI.
- `src/accessibility_audit_bot/scanner.py`: Playwright + axe scan runner.
- `src/accessibility_audit_bot/tavily_client.py`: WCAG summary retrieval.
- `src/accessibility_audit_bot/gemini_client.py`: backlog generation.
- `src/accessibility_audit_bot/service.py`: orchestration and artifact writing.
- `src/accessibility_audit_bot/app.py`: FastAPI `/audit` endpoint.
