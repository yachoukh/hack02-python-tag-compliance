"""Report rendering helpers."""

from pathlib import Path

from tag_compliance.models import ComplianceSummary, EvaluationResult


def render_report(
    results: list[EvaluationResult], summary: ComplianceSummary, report_format: str
) -> str:
    """Render a report in table, csv, json, or md format."""
    raise NotImplementedError("Challenge 5: implement report rendering")


def write_report(content: str, output: str | Path | None) -> None:
    """Write a report to a file, or to standard output when output is None."""
    raise NotImplementedError("Challenge 5: implement report output")
