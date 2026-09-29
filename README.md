# Hack 02: Python Azure Tag Compliance

Build a Python CLI that inventories Azure resources, checks their tags against a shared policy, and emits a report that a human or CI pipeline can trust.

Participants start on `main`, where the package is intentionally incomplete and `tests/test_challenges.py` marks the learning path. The `solution` branch contains the complete reference implementation and fuller tests.

## Why this scenario works for a hackathon

- **Real cloud-governance pain** - teams often need quick evidence that resources have owner, cost, environment, application, and data-classification tags.
- **Safe by design** - the app lists resources only; it does not write tags, deploy infrastructure, or delete anything.
- **Small but realistic** - participants touch dataclasses, YAML, Azure SDK paging, CLI flags, reports, CI, and test doubles.
- **Great Copilot practice** - the task exposes common hallucinations: outdated Azure SDK imports, pagination shortcuts, `{}` vs `None` tags, and case-sensitive tag comparisons.
- **Demoable in five minutes** - run against fixture data first, then against `rg-copilot-hack-tags-demo` when ready.

## Hackathon settings

| Setting | Value |
|---|---|
| Azure DevOps org | <https://dev.azure.com/azultechlab> |
| Participant project | `Copilot-Hackathon` |
| Facilitator project | `Copilot-Hackathon-Facilitator` |
| Repo | `hack02-python-tag-compliance` |
| Region | `swedencentral` |
| Demo resource group | `rg-copilot-hack-tags-demo` |
| Service connection | `sc-copilot-hack-sandbox` |

Mandatory tags are `owner`, `costCenter`, `environment`, `application`, and `dataClassification`. Seeded hackathon resources also carry `purpose=copilot-hackathon`.

## Prerequisites

| Need | Notes |
|---|---|
| Python 3.11+ | The package and tests target Python 3.11 or newer. |
| Azure CLI login | Run `az login` for live Azure mode; fixture mode does not need Azure. |
| Reader on the sandbox subscription | Required only for live listing of `rg-copilot-hack-tags-demo`. |
| VS Code + GitHub Copilot | Use Chat, inline completions, `/explain`, `/tests`, `/fix`, and agent mode. |
| Optional MCP servers | Azure MCP and Microsoft Learn MCP help ground SDK usage and tagging guidance in real docs instead of guessed API shapes. |

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -e .[dev]
```

## Starter kit

| File | What it is |
|---|---|
| `README.md` | Orientation, setup, usage, agenda, and links. |
| `CHALLENGES.md` | Five-level challenge ladder with points, prompts, success criteria, and hints. |
| `RUBRIC.md` | Weighted judging rubric and likely judge questions. |
| `tag-policy.yaml` | Policy-as-data for the mandatory tags. |
| `tests/fixtures/resources.json` | Offline resource inventory with deliberate edge cases. |
| `src/tag_compliance/*.py` | Starter package: models, policy loader, evaluator, Azure client, reports, and CLI. |
| `tests/test_challenges.py` | Starter challenge tests; do not change the intended pass/fail design on `main`. |
| `azure-pipelines.yml` | CI plus live report stage for `solution` and `ready/*` branches. |
| `seed/` | Facilitator-only Bicep that creates the demo resources. Participants read it; they do not deploy it. |
| `playground/` | Legacy-report review exercise for finding and ranking planted defects with Copilot. |
| `.github/skills/` | Repo skills for Azure sandbox conventions and safe resource inventory code. |
| `.vscode/mcp.json` | Azure MCP and Microsoft Learn MCP server wiring for VS Code. |

## Usage

Offline fixture mode, useful during the challenges:

```powershell
python -m tag_compliance --policy tag-policy.yaml --input tests\fixtures\resources.json --format table
```

Azure mode, after the implementation is complete and you are signed in:

```powershell
$env:AZURE_SUBSCRIPTION_ID = "<subscription-id>"
python -m tag_compliance --policy tag-policy.yaml --resource-group rg-copilot-hack-tags-demo --format md
```

Run quality checks:

```powershell
ruff check .
ruff format --check .
pytest
```

The `main` branch is the starter. Work on your own branch, for example `users/<alias>/tags`, and push to `ready/<team>` to run the live Azure report.

## Challenge ladder and judging

- Start with the [challenge ladder](CHALLENGES.md).
- Review the [judging rubric](RUBRIC.md) before demos.

## Suggested one-day agenda

| Time | Item |
|---|---|
| 09:00 | Kickoff: why tag compliance matters and what the app must prove. |
| 09:20 | Preflight: clone, install, run starter tests, inspect fixture data with Copilot. |
| 10:00 | Level 1 - Make it run. |
| 10:45 | Level 2 - Make it correct with offline policy/evaluator tests. |
| 12:00 | Lunch / facilitator office hours. |
| 13:00 | Level 3 - Make it real with Azure SDK listing and the playground review. |
| 14:30 | Level 4 - Reports, CSV safety, exit codes, and pipeline readiness. |
| 15:45 | Level 5 - Wildcards. |
| 16:30 | Team demos, 5 minutes each. |
| 17:15 | Judging, lessons learned, and wrap-up. |

## What good looks like

A strong solution produces the same compliance result from fixture data and live Azure data, handles null and oddly cased tags, consumes every page of Azure results, writes safe machine-readable reports, and fails CI only when violations should block the build. A strong team also shows how Copilot helped, where they verified Copilot's suggestions against tests or MCP-grounded docs, and how they caught at least one plausible but wrong suggestion.

## Reference material

- `azure-mgmt-resource` package docs - <https://learn.microsoft.com/python/api/overview/azure/resources?view=azure-python>
- `ResourceManagementClient` docs - <https://learn.microsoft.com/python/api/azure-mgmt-resource/azure.mgmt.resource.resources.resourcemanagementclient?view=azure-python>
- Azure tagging guidance - <https://learn.microsoft.com/azure/azure-resource-manager/management/tag-resources>
- Azure Resource Graph overview - <https://learn.microsoft.com/azure/governance/resource-graph/overview>
- Azure MCP server - <https://github.com/Azure/azure-mcp>
- Microsoft Learn MCP - <https://learn.microsoft.com/training/support/mcp>
- GitHub Copilot in VS Code - <https://code.visualstudio.com/docs/copilot/overview>
