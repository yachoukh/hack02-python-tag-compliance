# Agent guidance for this repo

Copilot CLI and Copilot coding agent read this file. Follow it before making changes in this repository.

## Python conventions

- Package code lives in `src/tag_compliance/`; tests live in `tests/`.
- Use Python 3.11+ type hints, dataclasses for shared shapes, and small pure functions where practical.
- Use `logging`, not `print`, except for intentional CLI output.
- Keep Azure SDK access behind `ResourceProvider`/`AzureResourceProvider` so unit tests can mock it.
- Unit tests must not call the network or require Azure credentials. Use `tests/fixtures/resources.json` or mocks.
- Use `ruff` and `pytest` as configured in `pyproject.toml`.

## Tag policy rules

Mandatory tags are:

| Tag | Rule |
|---|---|
| `owner` | Required and non-empty. |
| `costCenter` | Required and must match `CC-####`, for example `CC-1234`. |
| `environment` | Required and one of `dev`, `test`, `prod`. |
| `application` | Required and non-empty. |
| `dataClassification` | Required and one of `public`, `internal`, `confidential`. |

Hackathon seed resources also include optional `purpose=copilot-hackathon`.

## Sandbox resource groups

- `rg-copilot-hack-tags-demo` is the live target for this hack's tag-compliance report.
- Other shared hackathon groups use the `rg-copilot-hack-*` prefix and are not targets for this app unless the facilitator says so.
- The Azure DevOps service connection is `sc-copilot-hack-sandbox`.

## Always verify Copilot suggestions for

- `azure-mgmt-resource` 26+ import path: use `from azure.mgmt.resource.resources import ResourceManagementClient`, not `from azure.mgmt.resource import ResourceManagementClient`.
- Paged Azure SDK iterators: consume the full iterator; do not slice, call only `next()`, or break after the first page.
- Untagged resources: Azure may return `tags` as `None`, not `{}`.
- Tag keys: compare case-insensitively, while reporting wrong-case keys as `invalid-case` when appropriate.
- CSV output: neutralize cells that start with `=`, `+`, `-`, or `@`; quoting alone is not enough.
- Live mode: do not call Azure when `--input` fixture mode is selected.

## Never do this

- Never write tags, deploy resources, delete resources, or run destructive Azure commands from this repo.
- Never hardcode a real subscription ID, tenant ID, secret, connection string, PAT, or credential.
- Never commit generated coverage files, virtual environments, or local `.env` files.
- Never leak solution implementation code from the `solution` branch into `main`.
