# Project Refactor — risk/verification gates

## Classify before editing
- **Low:** narrow local rename/extraction, private code, no persistent state, observable local tests. Small relevant unit checks may suffice.
- **Medium:** multiple modules, common utility, feature seam, navigation or validation logic. Add contract/feature integration coverage, build/typecheck, smoke tests.
- **High:** authentication/authorization, DB schema/data, migrations, public APIs, payment flows, concurrent work/queues, distributed state, infra/CI/deployment, concurrency, serialization formats. Explicit approval + staging/disposable tests, compatibility/rollback plan; if unavailable **do not report safety as verified**.

## Minimum evidence for behavior preservation
- Baseline exact commands + outcomes; label pre-existing red/skipped.
- Identify behavior at risk, including error paths, edge cases, security/permission boundaries and consumer contracts.
- Choose relevant tests:
  - Local business logic: focused unit tests with meaningful cases.
  - HTTP/API: response status/shape, auth/role outcomes, error semantics, routing.
  - Persistence: transactions, constraints, migration upgrade/rollback, idempotence; disposable DB.
  - Frontend: critical navigation, accessibility behavior where affected, forms, happy and error journeys.
  - Async/queues: retries, deduplication, ordering, idempotency, event formats.
  - Performance-sensitive code: compare reproducible baselines; avoid claims without measurements.
- Run focused tests after each step; broader relevant suite before finish. Assess test failures; don't update expected outputs merely to make them green.
- If there is no usable test suite, first write observed-behavior characterization tests at externally visible seams. Never infer correct expected values only from desired new design.

## Review checklist
- [ ] Scope restricted to stated goal; no opportunistic rewrites.
- [ ] Public API, DB schema and wire/event format unchanged OR explicitly approved and migrated.
- [ ] No new cycles / feature-private cross-imports / surprise shared mutable state.
- [ ] No dead files, broken imports, route registrations, missing assets/config, or altered build output.
- [ ] Security permissions, error handling, timing-sensitive behavior examined.
- [ ] Tests and build status accurately compared to baseline (including skipped checks).
- [ ] Docs/instructions reflect real new paths, not imagined future tree.
- [ ] `git diff --check`; final diff reviewed for unrelated changes and credential leakage.

## Required brief completion format
```
Goal: ...
Scope: ... (files/modules)
Behavior/contracts: preserved / explicitly changed ...
Checks: baseline [command → result], final [command → result]
New tests: ...
Unverified/risks: ...
Rollback: ... (revert only this patch / specific migration procedure)
```
