"""Shared dataclasses for tag compliance."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ViolationKind = Literal["missing", "invalid-value", "invalid-case"]


@dataclass(frozen=True)
class TagRule:
    """Validation rule for one required tag."""

    key: str
    description: str = ""
    required: bool = True
    non_empty: bool = False
    pattern: str | None = None
    allowed_values: tuple[str, ...] = ()


@dataclass(frozen=True)
class TagPolicy:
    """A collection of tag rules loaded from YAML."""

    required_tags: tuple[TagRule, ...]
    optional_tags: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ResourceRecord:
    """Small resource shape used by both Azure and offline fixture loading."""

    id: str
    name: str
    type: str
    resource_group: str
    location: str
    tags: dict[str, str]


@dataclass(frozen=True)
class TagViolation:
    """One policy violation for one resource."""

    resource_id: str
    resource_name: str
    resource_group: str
    tag_key: str
    kind: ViolationKind
    message: str
    actual_value: str | None = None


@dataclass(frozen=True)
class EvaluationResult:
    """Evaluation output for one resource."""

    resource: ResourceRecord
    violations: tuple[TagViolation, ...]

    @property
    def compliant(self) -> bool:
        """Return True when the resource has no violations."""
        return not self.violations


@dataclass(frozen=True)
class ComplianceSummary:
    """Aggregate compliance counts."""

    resource_count: int
    compliant_count: int
    non_compliant_count: int
    violation_count: int
