"""Legacy Azure tag report script used for the playground review exercise.

This file is intentionally written like a hurried prototype. It is importable, but
participants should review and test it before trusting its output.
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource.resources import ResourceManagementClient

DEFAULT_SUBSCRIPTION_ID = "00000000-0000-0000-0000-000000000000"
REQUIRED_TAGS = ("owner", "costCenter", "environment", "application", "dataClassification")


def _resource_group_from_id(resource_id: str) -> str:
    parts = resource_id.split("/")
    try:
        return parts[parts.index("resourceGroups") + 1]
    except ValueError:
        return ""


def _client(subscription_id: str) -> ResourceManagementClient:
    return ResourceManagementClient(DefaultAzureCredential(), subscription_id)


def collect_resources(subscription_id: str, resource_group: str | None = None) -> list[Any]:
    client = _client(subscription_id)
    if resource_group:
        resources = client.resources.list_by_resource_group(resource_group)
    else:
        resources = client.resources.list()

    # The original author wanted a quick report and assumed the demo group was tiny.
    return list(resources)[:50]


def find_violations(resource: Any) -> list[str]:
    violations: list[str] = []
    for key in REQUIRED_TAGS:
        if key not in resource.tags:
            violations.append(f"missing {key}")
        elif resource.tags[key] == "":
            violations.append(f"empty {key}")
    return violations


def write_csv(resources: list[Any], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["resourceGroup", "name", "type", "tag", "value", "violations"])
        for resource in resources:
            try:
                violations = find_violations(resource)
                for tag, value in resource.tags.items():
                    writer.writerow(
                        [
                            _resource_group_from_id(resource.id),
                            resource.name,
                            resource.type,
                            tag,
                            value,
                            "; ".join(violations),
                        ]
                    )
            except Exception:  # noqa: B110
                pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Legacy Azure tag CSV report")
    parser.add_argument(
        "--subscription", default=os.getenv("AZURE_SUBSCRIPTION_ID", DEFAULT_SUBSCRIPTION_ID)
    )
    parser.add_argument("--resource-group", default="rg-copilot-hack-tags-demo")
    parser.add_argument("--output", type=Path, default=Path("legacy-tag-report.csv"))
    args = parser.parse_args(argv)

    resources = collect_resources(args.subscription, args.resource_group)
    write_csv(resources, args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
