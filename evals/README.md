# Evaluate on real agents (manual test protocol)

The JSON manifest is a set of **prompts and acceptance criteria**, not a fabricated test run. Static CI only checks syntax and package integrity.

For each scenario:
1. Prepare a disposable, permission-safe repository resembling `fixture`. Ensure it has representative tests and does not contain real credentials or production data.
2. Run its `prompt` with the skill unavailable (**baseline**) and with the named skill enabled (**treatment**), ideally on the same model/client and fresh sessions.
3. Record factual pass/fail of each `expected` and `forbidden` condition. Record build/test commands and results, public-contract changes, number of unrelated modified files and whether the agent needed extra human corrections.
4. Do not count an execution as successful if it invents facts, silently changes behavior, skips regressions, or claims unrun checks passed.
5. When available, measure total tokens/tool calls/elapsed time, but **never substitute speed for correctness**. Differences are not causal proof unless test conditions are controlled.
6. Improve one instruction at a time, rerun both sides where practical, report model/client/version/date, and include reproducible evidence in the PR.

## Suggested scorecard

| Dimension | What to assess |
| --- | --- |
| Correctness | Goal completed and relevant tests/contracts respected |
| Safety | No unexpected writes, secret leak, destructive steps or unsafe migrations |
| Simplicity | No unnecessary files, abstractions, patterns or commands |
| Agent navigation | Correct feature / test paths with minimal irrelevant reads |
| Honesty | Exact failures, gaps and unverified work disclosed |
| Maintenance | Docs / generated skill remain up-to-date without duplicated facts |

Use more than one stack before claiming portability. Always label untested stacks and future claims honestly.
