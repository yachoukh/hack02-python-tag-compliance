# Seed resources

The facilitator deploys `seed-tag-demo.bicep` to `rg-copilot-hack-tags-demo` in
`swedencentral`. Participants should not deploy it during the hack.

Validate the file locally:

```powershell
az bicep build --file seed\seed-tag-demo.bicep --stdout
az bicep lint --file seed\seed-tag-demo.bicep
```

## Expected compliance results

The template creates six cheap or near-zero-cost resources. All include
`purpose=copilot-hackathon`.

| Resource | Expected result |
| --- | --- |
| `nsg-tags-compliant-01` | compliant |
| `rt-tags-compliant-01` | compliant |
| `id-tags-missing-owner-cost` | missing `owner` and `costCenter` |
| `vnet-tags-invalid-env` | invalid `environment=Production` |
| storage account `st<unique>tags` | invalid `costCenter=1234` |
| `nsg-tags-purpose-only` | missing all five mandatory tags |

Summary: 6 resources, 2 compliant, 4 non-compliant, 9 total violations.
