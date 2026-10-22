# Contributing

Keep the skills **smaller, truer, and more testable**, not more impressive-sounding.

1. Open an issue with a real repo type + an actual task where a skill gave a bad result (redact secrets). What happened? What would correct behavior look like?
2. Add or extend `evals/scenarios.json` with an observable pass/fail behavior. Prefer one failure case at a time.
3. Fix the shortest relevant skill instruction or focused reference. Avoid identical text in multiple skills, a new reference file for a 3-line rule, or language/framework-specific claims in the generic default.
4. Run `python3 tests/validate.py`; ideally test the scenario **with and without** the changed skill in at least one real agent. Include what model/client was tested and results; never invent metrics.
5. In the PR, list changed files, rationale, expected benefit, scenarios tried, and any tradeoffs.

## Style

- Exact paths and commands only when they exist; qualify examples and assumptions.
- Third-person frontmatter description that says **when to trigger**.
- Root `SKILL.md` ideally < 200 lines; details in one-hop `references/` only when worthwhile.
- Scope: docs bootstrap vs code refactor vs project skill generator. No implicit behavior-crossing.
- No new package dependencies unless a real failing scenario warrants them.
- Strong behavior gates (test checks, approval, secrets hygiene); avoid rigid aesthetics (file length caps, forced patterns, one true directory layout).
- Do not claim that any skill can guarantee bug-free changes.
