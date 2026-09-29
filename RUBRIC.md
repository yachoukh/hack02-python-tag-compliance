# Judging rubric

| Criterion | Weight | What excellent looks like |
|---|---:|---|
| Works end-to-end against live Azure | 30% | The CLI runs against `rg-copilot-hack-tags-demo`, consumes every returned resource, produces a report artifact, and never mutates Azure. |
| Correctness on edge cases | 25% | Handles `tags is None`, case-insensitive tag keys, wrong-case keys, empty-string values, `costCenter` `CC-####`, allowed values, and paged iterators with tests. |
| Copilot leverage | 20% | Uses Copilot prompts, tests, explanations, skills, and MCP effectively; verifies suggestions; catches the bad `azure-mgmt-resource` import path. |
| Report usability and CI integration | 15% | Table/CSV/JSON/Markdown are readable and safe, CSV injection is neutralized, exit codes support CI gating, and the pipeline is understood. |
| Demo and storytelling | 10% | The team explains the governance problem, tradeoffs, test evidence, Copilot wins/misses, and next production steps clearly. |

## What judges will ask

- Show the exact command you ran against fixture data and against live Azure.
- How do you know your Azure listing consumed all pages?
- What happens when a resource has `tags = None`?
- How do you treat `Owner` when the policy requires `owner`?
- How do you validate `costCenter`?
- Why is CSV quoting not enough to prevent CSV injection?
- Where did Copilot suggest something wrong, and how did you catch it?
- Which tests prove the most important edge cases?
- Why does the pipeline use `--no-fail` for the live report artifact?
- What would you change before making this a production control?
