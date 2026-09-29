# Planted-defect playground

`legacy_tag_report.py` is a plausible earlier version of the Azure tag reporter that someone "already wrote" in a hurry. Your job is not to trust it.

## Exercise

1. Ask Copilot to review the file for correctness, Azure SDK behavior, reporting safety, and operational risk.
2. Rank the findings by severity and explain the impact in a tag-compliance report.
3. Write failing tests or small reproductions that prove each important bug.
4. Fix the implementation only after you have evidence.
5. Compare your fixes with the main challenge implementation so the same mistakes do not come back.

## Suggested prompts

- `Review playground/legacy_tag_report.py for bugs that would make an Azure tag compliance report incomplete or misleading.`
- `Write pytest tests with fake resource objects that prove the highest-risk issues in this legacy script.`
- `Which findings are correctness issues, which are security/reporting issues, and which are operability issues?`

Do not run write, deploy, delete, or tag-update Azure commands for this exercise. Keep it read-only.
