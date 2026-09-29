# Challenge ladder

Use GitHub Copilot, Copilot Chat, inline completion, `/explain`, `/tests`, `/fix`, `@workspace`, skills, MCP, and agent mode to complete the starter repo. The levels are cumulative: keep earlier behavior working as you climb.

## Level 1 - Make it run (20 pts)

### Challenge 1.1: Explore the repo with Copilot

**Goal:** Understand the package, tests, policy file, fixture data, pipeline, and where each TODO belongs.

**Suggested Copilot prompts:**

- Chat: `@workspace Explain how this repo is organized and where each challenge should be implemented.`
- Chat: `/explain src/tag_compliance/models.py`
- Agent mode: `Inspect the starter code and summarize the TODOs without changing files.`

**Success criteria:** You can describe the CLI flow from policy loading to resource loading, evaluation, summary, report rendering, and exit code.

**Hints:** Start with `models.py`, then read `tests/test_challenges.py`, `tag-policy.yaml`, and `tests/fixtures/resources.json`.

### Challenge 1.2: Get the starter checks running

**Goal:** Create the virtual environment, install the package, run the CLI help, and run the starter tests that should already pass.

**Suggested Copilot prompts:**

- Chat: `Explain the commands in README.md setup and what each one installs.`
- Chat: `Why are some tests skipped in tests/test_challenges.py and what should pass before I implement anything?`

**Success criteria:** `python -m tag_compliance --help` works, `pytest` runs, and only the intentional challenge-driving tests are skipped or failing according to the starter design.

**Hints:** Do not edit the tests just to make Level 1 green. The skips are the map.

## Level 2 - Make it correct (25 pts)

### Challenge 2.1: Implement the policy loader

**Goal:** Load `tag-policy.yaml` into `TagPolicy` and `TagRule` dataclasses.

**Suggested Copilot prompts:**

- Inline: `# load the YAML requiredTags into TagRule objects`
- Chat: `Write pytest tests for loading allowedValues and regex patterns from tag-policy.yaml.`
- `/fix`: Use it on parsing errors or failing tests.

**Success criteria:** The loader returns all five mandatory tag rules with `nonEmpty`, `allowedValues`, and `pattern` fields mapped correctly.

**Hints:** Use `yaml.safe_load`; keep file I/O in `policy.py`; translate YAML names such as `nonEmpty` and `allowedValues` to Python field names.

### Challenge 2.2: Implement tag evaluation

**Goal:** Detect missing tags, invalid values, invalid formats, empty required values, and wrong-case keys.

**Suggested Copilot prompts:**

- Chat: `@workspace Implement pure tag evaluation functions for missing, invalid-value, regex pattern, empty-value, and invalid-case violations.`
- Inline: `# if a tag exists with the wrong casing, return an invalid-case violation`
- `/tests`: Generate parameterized tests for each violation kind.

**Success criteria:** Compliant resources pass; non-compliant resources list clear violations against `tests/fixtures/resources.json`.

**Hints:** Azure tag keys are case-insensitive. Treat `Owner` as `invalid-case` for `owner`, not as a separate missing tag. A resource can have `tags` as `None`, not `{}`. Empty-string tag values must not satisfy `nonEmpty`. The `costCenter` rule is the regex `CC-####`, for example `CC-1234`.

### Challenge 2.3: Keep the code testable

**Goal:** Make policy and evaluation logic pure enough that unit tests do not call Azure or depend on environment variables.

**Suggested Copilot prompts:**

- Chat: `Add tests that prove tag keys are compared case-insensitively but reported with the policy key.`
- Chat: `Create tests for null tags and empty string tag values without using Azure.`

**Success criteria:** The core compliance logic is covered by offline tests, including null tags, case mismatches, empty strings, invalid `environment`, invalid `dataClassification`, and invalid `costCenter` format.

**Hints:** Prefer small helper functions over a large CLI-only implementation.

## Level 3 - Make it real (25 pts)

### Challenge 3.1: Implement Azure resource listing

**Goal:** List resources with `azure-identity` `DefaultAzureCredential` and `azure-mgmt-resource` `ResourceManagementClient`, optionally scoped to `rg-copilot-hack-tags-demo`.

**Suggested Copilot prompts:**

- Chat: `Create a small AzureResourceProvider class that can be mocked in tests.`
- Chat: `Use DefaultAzureCredential with ResourceManagementClient to list resources subscription-wide or by resource group.`
- `/explain`: Ask Copilot to explain the Azure SDK paging object.
- MCP: `Use Microsoft Learn MCP to verify the ResourceManagementClient import path and list methods.`

**Success criteria:** Azure access is isolated behind a small interface or protocol, live mode lists all resources in the target scope, and tests can mock the provider without network access.

> **Heads-up:** `azure-mgmt-resource` 26+ moved the client. Use `from azure.mgmt.resource.resources import ResourceManagementClient`. Copilot may suggest the older `from azure.mgmt.resource import ResourceManagementClient`, which fails at runtime. This is a good moment to check Copilot's suggestion against the SDK docs or Microsoft Learn MCP.

**Hints:** Support `--resource-group`; do not call Azure when `--input` is provided. Consume the full paged iterator. Do not slice the first page, call only `next()`, or break after the first result batch.

### Challenge 3.2: Review the planted-defect playground

**Goal:** Treat `playground/legacy_tag_report.py` as code a teammate wrote in a hurry. Use Copilot to review it, rank the issues, and design failing tests before fixing anything.

**Suggested Copilot prompts:**

- Chat: `Review playground/legacy_tag_report.py for correctness, Azure SDK, security, and reporting defects. Rank findings by severity.`
- Chat: `Write pytest tests that prove the highest-risk defects in the legacy tag reporter.`
- Chat: `Which issues are compliance correctness bugs, which are operational bugs, and which are security/reporting bugs?`

**Success criteria:** Your team can explain at least five distinct defects, show a failing test or small reproduction for each, and propose safe fixes without mutating Azure.

**Hints:** Look for paging behavior, tag shape assumptions, tag-key casing, CSV output safety, exception handling, and hardcoded environment assumptions.

## Level 4 - Make it production-shaped (20 pts)

### Challenge 4.1: Generate useful reports

**Goal:** Output table, CSV, JSON, and Markdown reports with a clear summary.

**Suggested Copilot prompts:**

- Chat: `Implement report renderers for table, csv, json, and markdown using only the standard library.`
- Chat: `Add tests for CSV, JSON, Markdown, and table report output.`
- `/fix`: Use on formatting or escaping issues.

**Success criteria:** Offline runs show violations clearly, JSON is machine-readable, Markdown is demo-friendly, and CSV opens safely in spreadsheet tools.

**Hints:** Use the standard `csv` module, but remember CSV quoting is not the same as CSV-injection protection. Prefix or otherwise neutralize cell values that start with `=`, `+`, `-`, or `@` before writing CSV.

### Challenge 4.2: Add CI-friendly exit codes

**Goal:** Return exit code `1` when violations exist and fail-on-violations is enabled; support `--no-fail` for report-only demos.

**Suggested Copilot prompts:**

- Inline: `# return exit code 1 when violations exist and fail_on_violations is true`
- Chat: `Add CLI tests for --no-fail and default fail-on-violations behavior.`

**Success criteria:** The CLI can gate CI when policy violations exist and can also publish reports without failing the live-report stage.

**Hints:** Keep report generation and exit-code decision separate so both are easy to test.

### Challenge 4.3: Get the pipeline green

**Goal:** Run the local quality checks and understand when `azure-pipelines.yml` runs the live Azure report.

**Suggested Copilot prompts:**

- Chat: `Explain the LiveReport stage and how to enable it for my feature branch.`
- Agent mode: `Explain the LiveReport stage condition and which branches trigger it.`
- MCP: `Use Azure MCP or Microsoft Learn MCP to verify Azure CLI and tagging docs that relate to this pipeline.`

**Success criteria:** `ruff check .`, `ruff format --check .`, and `pytest` pass locally; the pipeline publishes a `tag-report` artifact on `solution` or `ready/<team>`.

**Hints:** LiveReport is skipped on normal branches. When your code is ready, push it to a branch named `ready/<team>` and LiveReport runs against Azure automatically.

## Level 5 - Wildcards (10 pts)

Pick one or propose your own.

### Challenge 5.1: Azure Resource Graph inventory

**Goal:** Replace per-resource-group listing with Azure Resource Graph for faster subscription-wide queries.

**Suggested Copilot prompts:**

- Chat: `Design an Azure Resource Graph query that returns id, name, type, resourceGroup, location, and tags for tag compliance.`
- MCP: `Use Microsoft Learn MCP to compare Resource Graph with ResourceManagementClient list calls.`

**Success criteria:** The report can use Resource Graph results without changing the evaluator.

**Hints:** Keep the `ResourceRecord` boundary stable.

### Challenge 5.2: Auto-remediation dry run

**Goal:** Print proposed `az tag` or `az resource tag` commands without applying them.

**Suggested Copilot prompts:**

- Chat: `Add a dry-run remediation report that suggests commands but never executes them.`

**Success criteria:** The output helps an operator fix resources manually and cannot mutate Azure by default.

**Hints:** Never write tags in the hackathon app. Make dry run explicit in naming and tests.

### Challenge 5.3: Policy-as-code diffing

**Goal:** Compare two versions of `tag-policy.yaml` and explain which resources would become newly non-compliant.

**Suggested Copilot prompts:**

- Chat: `Create a policy diff command that evaluates old and new tag policies against the same fixture data.`

**Success criteria:** Teams can preview governance-rule changes before enforcing them.

**Hints:** Reuse the evaluator and report machinery.

### Challenge 5.4: Cost attribution by tag

**Goal:** Sketch or prototype a report grouping resources by `costCenter` and `application`.

**Suggested Copilot prompts:**

- Chat: `Design a cost attribution summary from compliant tag data without calling billing APIs.`

**Success criteria:** The demo tells a governance story beyond pass/fail.

**Hints:** This can be a report-only enhancement using the existing resource inventory.

### Challenge 5.5: Copilot-authored Azure Policy definition

**Goal:** Ask Copilot to draft an `az policy` definition or Bicep policy resource equivalent to the tag rules, then verify it against official docs.

**Suggested Copilot prompts:**

- Chat: `Draft an Azure Policy definition that audits required tags owner, costCenter, environment, application, and dataClassification.`
- MCP: `Use Microsoft Learn MCP to verify the Azure Policy alias and effect syntax.`

**Success criteria:** The team can explain what the Python reporter does better for learning and what Azure Policy does better for enforcement.

**Hints:** Do not deploy the policy during the hack unless the facilitator explicitly asks.
