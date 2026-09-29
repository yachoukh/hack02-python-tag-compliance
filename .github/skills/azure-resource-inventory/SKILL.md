---
name: azure-resource-inventory
description: Enumerate Azure resources safely and correctly from Python. Use when writing or reviewing code that lists Azure resources with azure-identity, azure-mgmt-resource, Azure Resource Graph, resource groups, tags, or compliance reports, especially when paging, tag casing, null tags, or SDK import paths matter.
---

# Azure resource inventory in Python

Use this skill when code needs to read Azure resources for reporting, compliance, or inventory. The default posture is read-only.

## Authentication

Use `DefaultAzureCredential` from `azure.identity` so local Azure CLI login, managed identity, and pipeline identity can all work without code changes.

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource.resources import ResourceManagementClient

credential = DefaultAzureCredential()
client = ResourceManagementClient(credential, subscription_id)
```

Do not commit subscription IDs, tenant IDs, client secrets, PATs, or connection strings. Read subscription IDs from CLI arguments, environment variables, or the current Azure CLI account.

## Correct `azure-mgmt-resource` import

For `azure-mgmt-resource` 26+, the correct import is:

```python
from azure.mgmt.resource.resources import ResourceManagementClient
```

The older import fails at runtime:

```python
from azure.mgmt.resource import ResourceManagementClient  # wrong for 26+
```

Copilot often suggests the older path. Verify against Microsoft Learn or package docs before accepting it.

## Consume paged iterators fully

Azure SDK list methods return iterable paged results. Treat them as streams and consume every item.

```python
if resource_group:
    azure_resources = client.resources.list_by_resource_group(resource_group)
else:
    azure_resources = client.resources.list()

records = [to_record(resource) for resource in azure_resources]
```

Do not use `next(...)`, `list(... )[:50]`, `by_page()` without nested iteration, or `break` after the first page unless you are deliberately sampling and the report says so.

## Tags can be `None`

Azure resources with no tags may expose `resource.tags` as `None`, not `{}`.

```python
raw_tags = resource.tags or {}
```

Treat empty-string values as missing when the policy says non-empty.

## Tag keys are case-insensitive

Azure tag keys are case-insensitive. Normalize for lookup, but preserve enough original data to report wrong-case keys.

```python
actual_by_lower = {key.lower(): key for key in tags}
if required_key.lower() in actual_by_lower:
    actual_key = actual_by_lower[required_key.lower()]
    if actual_key != required_key:
        report_invalid_case(actual_key, required_key)
```

## Mapping Azure resources

Keep the Azure SDK shape at the boundary. Convert SDK objects to your app model immediately:

- `id`
- `name`
- `type`
- `resource_group`
- `location`
- `tags` as a dict

Derive `resource_group` from `resource.id` only when the SDK object does not expose it directly.

## When to use Azure Resource Graph

Use `ResourceManagementClient` for beginner-friendly per-subscription or per-resource-group inventory and small demos. Consider Azure Resource Graph when you need fast subscription-wide or tenant-wide querying, cross-subscription inventory, filtering at the service, or joining tag data with other metadata.

A Resource Graph result should still be converted into the same internal resource model as SDK list results.

## Throttling and retry

Azure SDK clients include retry policies. For large inventories:

- Prefer service-side filtering or Resource Graph over client-side filtering.
- Avoid parallel fan-out until you know the API limits.
- Log scope and counts, not secrets.
- Let retryable Azure exceptions surface with context; do not swallow broad exceptions silently.
