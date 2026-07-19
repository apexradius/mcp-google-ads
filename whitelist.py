# Vulture whitelist — false positives that are intentional, not dead code.
# Run: uvx vulture gads whitelist.py --min-confidence 90
#
# `breakdown` is a public parameter of the compare_periods MCP tool (part of the
# exposed tool schema). Vulture flags it because the current body always breaks
# down by campaign and never reads the arg — a latent bug in compare_periods, not
# dead code. The parameter stays in the public contract; do not delete it.
breakdown  # unused variable (gads/server.py:281)
