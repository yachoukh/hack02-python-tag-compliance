from pathlib import Path

import pytest

from tag_compliance.evaluator import evaluate_resource
from tag_compliance.models import ResourceRecord, TagPolicy, TagRule
from tag_compliance.policy import load_policy


@pytest.mark.skip(reason="Challenge 2: remove skip when implemented")
def test_policy_loader_reads_required_tags() -> None:
    policy = load_policy(Path("tag-policy.yaml"))
    assert [rule.key for rule in policy.required_tags] == [
        "owner",
        "costCenter",
        "environment",
        "application",
        "dataClassification",
    ]


@pytest.mark.skip(reason="Challenge 3: remove skip when implemented")
def test_evaluator_flags_missing_owner() -> None:
    policy = TagPolicy(required_tags=(TagRule(key="owner", non_empty=True),))
    resource = ResourceRecord(
        id="/subscriptions/000/resourceGroups/rg/providers/type/name",
        name="name",
        type="type",
        resource_group="rg",
        location="swedencentral",
        tags={},
    )

    result = evaluate_resource(resource, policy)

    assert result.violations[0].kind == "missing"
