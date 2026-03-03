from __future__ import annotations

from .models import AuditRequest, AuditResponse
from .service import run_audit

try:
    from fastapi import FastAPI
except ModuleNotFoundError:  # pragma: no cover
    FastAPI = None

if FastAPI is not None:
    app = FastAPI(title="accessibility-audit-bot", version="0.1.0")

    @app.post("/audit", response_model=AuditResponse)
    def audit(payload: AuditRequest) -> AuditResponse:
        result = run_audit(payload.target_url)
        return AuditResponse(**result)
