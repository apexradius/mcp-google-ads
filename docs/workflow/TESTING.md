# Google Ads reporting MCP: acceptance evidence

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | tests/test_server.py uses unittest and mock; it asserts the exact ten-tool registration set and schemas, missing-config behavior and customer-ID normalization. |
| **Where?** | tests/test_server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to choose a check that proves the changed behavior without claiming broader evidence. |
| **Why this approach?** | tests/test_server.py uses unittest and mock; it asserts the exact ten-tool registration set and schemas, missing-config behavior and customer-ID normalization. |
| **Why it matters?** | A registration or document check cannot prove live authentication, provider state or the installed user path. |

## Required proof by behavior

tests/test_server.py uses unittest and mock; it asserts the exact ten-tool registration set and schemas, missing-config behavior and customer-ID normalization. These are hermetic seams, not report correctness or live authentication evidence. For a code change, use python -m unittest discover -s tests after verifying the local dependency environment. Add a targeted fake-client test for any changed GAQL/report mapping; do not call real advertising accounts for a documentation check.

## Product acceptance baseline

Account profiles must resolve explicitly or through the configured default, unknown profiles must fail, and missing configuration must return a clean error. Ten registered tools expose discovery and reporting, not campaign creation, budget edits, billing or conversion uploads. Required report context is customer, credential profile, date range, metric units and row limit. Preserve honest missing data rather than infer zero spend from every empty result.

## Evidence custody

Inspected means source/test definitions were read. Locally verified means the named executable check actually ran and its result was observed. Live verified requires the deployed, installed or user-facing path. Historical checkmarks and CI configuration are not fresh results. Use the exact candidate, environment, test input class, observed result and limitations in a receipt. Read [AGENTS](AGENTS.md) for conditional AXI/crew custody; do not create a pipeline merely because this file exists.

## Supporting sources

- [tests/test_server.py](../../tests/test_server.py)

## Document checker dependency

Install the pinned CommonMark parser with `python -m pip install -r tools/requirements-workflow.txt` before running the document checkers and their fixtures. `markdown-it-py` parses actual navigation tokens; it does not render pages, fetch links or establish reader comprehension. CI uses Python 3.12 and the same pinned dependency.

## Continue

Return to [INDEX.md](../../INDEX.md) and finish all routes relevant to the latest task before acting. After verification, update affected owning facts, REPORT and HANDOFFS.
