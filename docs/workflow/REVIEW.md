# Google Ads MCP: documentation review continuity

Observed 2026-09-28 against source baseline `39471e2ed644bca3ea1e2b3a8b57bf09f731c4fd`. This is a bounded continuity check of the earlier independent source review, not a new runtime or product acceptance test.

The 7 primary-source hashes recorded in the prior review still match this candidate baseline. The project-specific role bodies are retained; this change adds portable navigation, an actual-source map, a domain glossary and executable document checks. Historical/local-only references remain explicitly unavailable rather than being invented or silently imported.

## Previously source-challenged scenarios

### Discover children for a specified MCC

Reader recovery: API/HANDOFFS correctly warn that customer_id is accepted but unused; list_customers calls list_accessible_customers for the selected login, then queries each returned customer. Recover a scoped handler correction or approved alternative, not a claimed filtered child list.

Source and dossier evidence: ["gads/server.py:list_customers", "docs/workflow/API.md", "docs/workflow/HANDOFFS.md"]

Result: pass

Evidence level: inspected

### Compare account totals without changing another profile’s default

Reader recovery: Use explicit account on read methods; set_default_account writes JSON. breakdown=account is ignored by compare_periods, which always selects campaign rows limited to 50 per period. Recover requested aggregate/date/currency contract before reporting account totals.

Source and dossier evidence: ["gads/server.py:compare_periods", "gads/server.py:set_default_account", "gads/accounts.py:set_default", "docs/workflow/API.md"]

Result: pass

Evidence level: inspected

## Source binding

| Source | SHA256 |
| --- | --- |
| `README.md` | `5091b0a5eee65f66aa16fddfca979717f131e439547ceb08ab15a4024d8cdc5a` |
| `pyproject.toml` | `f18b81397f7bc2af1ccadbc2e5c065c58d84fd45e54bf0bf72e62f1ad35bf1f0` |
| `gads/server.py` | `b3052f808cfeb30c8e6d91bbef9fda55a23de9b8f85e1dfc77e3692528ce3d37` |
| `gads/accounts.py` | `a2ab7a40e12eab900dab53fe54d8b8362949c06904dd448f63788fa467e4308b` |
| `gads/query.py` | `308645d03bd46995cd306914d6e14f2f4cb0b4a93e36138f71c4af7b6ab0beff` |
| `gads/retry.py` | `3155ed485705dc2f8a3858f5660194ab82d9bf9547999f504025c5c66bf6e01d` |
| `tests/test_server.py` | `5dd529340040d6a4f80860c98b0dc1b15400f85db229b358112c613bf84334ec` |

Prior review artifact names: `tooling-independent-review.json`. The owner retains these in the dated 2026-09-26 reconstruction evidence directory. A fresh clone can inspect the above source and scenarios without that private directory.

## Limits

No new fresh-runtime comprehension, deployed behavior, provider operation or release is claimed. The current user request selects work; these scenarios are examples, not standing tasks. Local/CI/merge/knowledge status is recorded separately in review.json.
