from pathlib import Path

from accessibility_audit_bot.service import run_audit


def test_run_audit_creates_artifacts(tmp_path: Path):
    repo = Path(__file__).resolve().parents[1]

    (tmp_path / "sample_site").mkdir()
    (tmp_path / "sample_site" / "index.html").write_text(
        (repo / "sample_site" / "index.html").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "src" / "accessibility_audit_bot" / "assets").mkdir(parents=True)
    (tmp_path / "src" / "accessibility_audit_bot" / "assets" / "axe.min.js").write_text(
        (repo / "src" / "accessibility_audit_bot" / "assets" / "axe.min.js").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    result = run_audit(root_dir=tmp_path)

    assert result["violations_count"] >= 1
    assert (tmp_path / "artifacts" / "violations.json").exists()
    assert (tmp_path / "artifacts" / "sources.json").exists()
    assert (tmp_path / "artifacts" / "remediation_backlog.md").exists()
