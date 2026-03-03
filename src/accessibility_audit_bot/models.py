from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel, Field


class AuditRequest(BaseModel):
    target_url: str | None = Field(
        default=None,
        description="Optional URL to audit. If omitted, local sample HTML is scanned.",
    )


class SourceSummary(BaseModel):
    title: str
    url: str
    summary: str


class ArtifactPaths(BaseModel):
    violations_json: Path
    remediation_backlog_md: Path
    sources_json: Path


class AuditResponse(BaseModel):
    violations_count: int
    artifacts: ArtifactPaths
    backlog_preview: str
