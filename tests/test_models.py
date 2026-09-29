from tag_compliance.models import EvaluationResult, ResourceRecord


def test_evaluation_result_compliant_property() -> None:
    resource = ResourceRecord(
        id="/subscriptions/000/resourceGroups/rg/providers/type/name",
        name="name",
        type="type",
        resource_group="rg",
        location="swedencentral",
        tags={},
    )

    result = EvaluationResult(resource=resource, violations=())

    assert result.compliant is True
