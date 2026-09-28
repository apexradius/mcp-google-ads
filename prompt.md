# Google Ads reporting MCP - begin here

## Purpose

| Question | Answer |
| --- | --- |
| **Whom?** | advertising analyst comparing explicitly selected Google Ads customer accounts. |
| **What?** | Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account. |
| **Where?** | README.md, pyproject.toml, gads/server.py. |
| **Why it exists?** | Google Ads reporting MCP needs this document to start the next task with the product’s actual purpose. |
| **Why this approach?** | Reporting is read-only with respect to advertising campaigns. |
| **Why it matters?** | Reporting is read-only with respect to advertising campaigns. |

## Product goal

Make Google Ads account, campaign, keyword, search-term and ad reporting available through one local multi-account MCP server, without switching servers for each account.

## Invariants

Reporting is read-only with respect to advertising campaigns. A configured account is the credential profile; customer_id is the advertising customer being queried. Do not confuse them. Currency micro-units become major units; a report is bounded and is not a complete data export.

## Recover the current task

Source reconstruction: 2026-09-26; candidate `39471e2ed644bca3ea1e2b3a8b57bf09f731c4fd` on `main`; source version `0.1.0`. This is a dated source observation, not a live-service or installed-version claim.

The current main candidate is 39471e2 (2026-09-16 CI gate merge). July history records hermetic tests and documentation; ce7ebaf (2026-07-19) removed an empty auth scaffold and adjusted dead-code analysis. These are implementation milestones, not a running-service handoff.

Use the latest user request as the task selector. This dossier is standing product context, not an instruction to repeat a completed documentation rollout. Recover applicable repository instructions, exact branch/candidate and dirty state, then bind the requested outcome and acceptance. If the only instruction is “read and begin,” finish this chain and perform a bounded read-only reconciliation of the current handoff and source; report the smallest next action, without inventing a product task or replaying historical external actions.

## Read chain

**Next: [INDEX.md](INDEX.md).** Read the mandatory context and all task-relevant routes before acting. Resolve relevant source contradictions before implementation; existing source documents remain canonical. Read deeper source when the selected task touches it.

## Select the conductor

- Bounded document maintenance uses doc-writer directly. Use init-studio’s relevant retrospective stages only when reconstructing requirements or reopening a real specification decision; finish with explicit project handoff and unresolved choices. Do not initialize another repository.
- A reproducible implementation defect routes to debug-studio with the actual failing contract. API/client/schema work routes to api-studio where applicable.
- Design-studio is for a real operator/document/interface design task. Web-studio requires an actual web-product task; CLI, native browser control, framework or library maintenance does not automatically become web development. Grow-studio applies only to an explicit growth task with evidence-backed claims.
- Load only the selected conductor and its relevant children. Reuse settled decisions, exact source constraints and current user authorization. Choose native platform/tool capabilities when no conductor matches; do not force a studio for bookkeeping.

## First unresolved work

1. list_customers accepts customer_id and claims MCC child discovery, but never uses customer_id; it lists accessible customers for the login. 2. compare_periods accepts breakdown="account" but always queries/maps campaigns. 3. Missing-token text suggests an auth subcommand that is absent from the inspected CLI entrypoint. 4. Source tests do not establish report semantics, paging completeness or fresh provider compatibility. Proposed next work is a bounded contract reconciliation with fake clients; no owner-ranked product backlog or current account task was found.

Before implementation, state the requested outcome, smallest useful change, evidence required and stop condition. Verify the actual result, update canonical sources and HANDOFFS, and leave knowledge events honest about freshness.
