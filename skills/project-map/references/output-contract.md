# Project Map — output contract (load only while creating docs)

## Minimum viable documentation

**Root `AGENTS.md` (roughly 20–80 lines):**
- One-sentence project purpose and links to current docs.
- Exact (verified or clearly labeled unverified) start/build/test/lint commands; list prerequisite tools.
- Real code layout: a few high-level module boundaries, not a directory dump.
- Nonnegotiable correctness and security rules already reflected in code: contracts, migration policy, config/secrets, generated files.
- Minimum verification for common changes; no empty platitudes or copied language style guides.
- When to consult `docs/code-map.md` or `docs/architecture.md`.

**README (existing file preferred):** short what/why, supported prerequisites and run instructions (if known), doc index link. Do not replace good onboarding text.

**`docs/INDEX.md` (only nontrivial projects):** a concise routing page:
```
New contributor → README → AGENTS.md
Finding a feature → code-map.md
Understanding boundaries/flows → architecture.md
Operating/deploying → operations.md (if applicable)
Historical why → decisions/ (if applicable)
```

**`docs/code-map.md` (if multiple features/packages):** table: user concept | entry point | business logic | persistence/integration | relevant test | how to change. Prefer paths that exist; keep lines short. Record unusual ownership boundaries.

**`docs/architecture.md` (if architecture not obvious):** system in 5–12 sentences, runtime components, 1–2 key flows, boundaries, external deps, constraints/unknowns; optionally one simple Mermaid diagram (not decorative complexity). Distinguish actual from planned architecture.

**`docs/operations.md` (if operationally useful):** launch/build/test checks, non-secret environment variable names, deployment path, observability/rollback pointers, operational hazards; never credentials or real `.env` values.

**ADR (only for meaningful decisions):** status, context, decision, alternatives, consequences; never fabricate historical rationale. Create a proposed ADR for a new decision, not a retroactive fictional one.

## Quality bar
- [ ] All new doc paths exist and index links resolve relatively.
- [ ] Facts are traceable to code, tests, manifests, or explicit user statements.
- [ ] Commands actually run or say why not; no false green status.
- [ ] No sensitive values, keys, tokens, full `.env`, personal data.
- [ ] One canonical home for each fact; other pages link rather than copy.
- [ ] No redundant diagrams, per-function descriptions, or placeholders.
- [ ] No rewritten code, configs, dependency lockfiles, or generated sources.
- [ ] Docs additions proportional to project's size and actual needs.
