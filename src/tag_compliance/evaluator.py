"""Pure tag compliance evaluation functions."""

from tag_compliance.models import ComplianceSummary, EvaluationResult, ResourceRecord, TagPolicy


def evaluate_resource(resource: ResourceRecord, policy: TagPolicy) -> EvaluationResult:
    """Evaluate one resource against the tag policy."""
    raise NotImplementedError("Challenge 3: implement tag evaluation")


def evaluate_resources(
    resources: list[ResourceRecord], policy: TagPolicy
) -> list[EvaluationResult]:
    """Evaluate many resources against the tag policy."""
    raise NotImplementedError("Challenge 3: evaluate all resources")


def summarize(results: list[EvaluationResult]) -> ComplianceSummary:
    """Create aggregate counts for evaluated resources."""
    raise NotImplementedError("Challenge 5: summarize evaluation results")
