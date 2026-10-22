---
name: project-refactor
description: Safely reorganizes and refactors codebases into simple, maintainable, well-bounded modules with the smallest behavior-preserving changes. Use for tangled monoliths, feature isolation, duplicate logic, hard-to-edit architecture, or requested clean-code/OOP/design-pattern improvements; requires regression checks and risk gates.
license: MIT
---

# Project Refactor

Make **future changes cheaper and safer**, not architecture more impressive. Prefer the smallest clear fix; keep existing working behavior and contracts. No directory layout, OOP pattern, framework, or abstraction is automatically best.

## When to apply
- User requests refactoring, restructuring, separating concerns, reducing coupling, or making a codebase easier for people and AI to maintain.
- Avoid structural refactoring for a narrow bug or feature when a small local edit is sufficient. Do not silently convert a monolith to microservices or rewrite to a different stack.

## Principles (priority order)
1. **Correctness → clarity → simplicity → change isolation → performance (measured).** Preserve behavior during pure refactoring. Fix defects in **separate** changes with explicit tests and user intent.
2. **Simplest thing that works:** a clear one-liner is better than a class; a small function is better than ceremony; an interface is justified only by a genuine seam/need. Don't force SOLID, OOP, Clean Architecture, DDD, CQRS, repositories, dependency injection, or design patterns without concrete benefit.
3. **Localize change:** minimize touched files and diff size. Group related code, keep public interfaces stable, avoid incidental renames/reformatting and unrelated dependency upgrades.
4. **Vertical slice when useful:** feature-centric organization for sufficiently large apps; keep a small app flat when it is easier. Platform/shared code only for real cross-feature responsibilities; no speculative `utils` dump.
5. **State/integration are high risk:** APIs, DB schema, persistence semantics, auth, permissions, migrations, cache keys, queues, events, cron, and deployment contracts require explicit protection.
6. **Never fake safety:** passing tests increases confidence, not a mathematical guarantee of no bugs. If tests are absent, introduce characterization/contract tests before risky changes or stop with a bounded plan.

## 0 — Preconditions (read-only)
- Inspect repo instructions/docs and source of truth; `git status --short` and current branch. Preserve user modifications; never hard reset, force push, or silently revert unrelated files.
- Trace one affected behavior end-to-end. Identify real responsibilities, imports and runtime dependencies, boundaries, source-of-truth state, and adjacent consumers.
- Record known existing failures and unrun checks. Inspect test scripts before execution; no production DB/services, privileged scripts, network install, or destructive commands without explicit authorization.
- Establish a **baseline**: existing relevant unit/integration/e2e/contract tests and build/typecheck/lint if safe; record passing/failing/skipped and exact environment. Read [safety gates](references/safety-gates.md) for risk-based verification.

## 1 — Choose the *minimum* design change
- List the observed pain (e.g. cycle, N+1 coupling, 12 files for one edit, duplicate business rule), its evidence and impact.
- Define **one clear success criterion** (e.g. `feature A no longer imports feature B's private implementation`; behavior tests stay green).
- Evaluate options: (A) leave as-is, (B) local extraction/rename, (C) move a coherent slice, (D) larger boundary change. Choose the **least intrusive option** that satisfies the user goal.
- Follow the language/framework's idioms; respect current working package layout. Example `features/<feature>` + `platform` + `shared` is a **possible pattern, not a mandate**. For nontrivial design choices, consult [the lean design guide](references/lean-design.md).
- Design patterns are tools: Strategy for real branching policy, Adapter for external dependency seams, Factory for complex construction. Do not create interfaces for one trivial concrete class, deep inheritance, or wrappers that only forward one call.
- Favor composition, cohesion, explicit contracts and limited dependencies; choose duplication over the wrong abstraction. Extract shared behavior when meaning and reuse justify it, **not** after an arbitrary fixed duplicate count.

## 2 — Present a bounded plan / approval gate
State: affected files, before/after boundaries, *why*, behavior/contracts to preserve, tests, risks, rollback and estimated change size.
- For cross-module moves, shared contracts, schema/infrastructure changes, or broad edits: **propose first and obtain explicit approval** before implementation, unless the user already explicitly approved that specific plan.
- For a narrowly requested local refactor with tests and no public contract changes: proceed within scope without an extra approval question, if permissions allow.
- If expected regressions cannot be measured (missing environment/tests), reduce scope, establish safety nets, or report that execution is blocked; do not claim safe completion. For larger approved work, suggest an isolated branch/worktree when supported, but do not change the user's branch or worktree without permission.

## 3 — Refactor in reversible increments
1. Add or strengthen a **behavior/characterization/contract test** at the seam when necessary (record intended existing behavior, including quirks; do not enshrine sensitive data).
2. Make **one conceptual, behavior-preserving edit**: move one function/module/slice, narrow a dependency, rename coherently, or extract a boundary.
3. Update imports/configuration/registration exactly where needed, preserve exported names/routes/message formats/DB behavior unless separately authorized.
4. Run the **smallest relevant checks immediately**; compare to baseline. At the end run broader checks proportionate to risk. For frontend validate key user flows; for API test request/response/error codes; for DB test migrations on disposable data.
5. If a new failure occurs: stop, isolate the last change, fix within scope or revert **your own** edit only. Never bury regressions under snapshots, skipped tests, lint suppressions, silent catch blocks, or wider rewrites.
6. Update existing `AGENTS.md`, code map and architecture notes **only for actually changed boundaries**; no doc flood. Keep generated repo skill links current if present.

## 4 — Prove what you can and hand off
Use [completion report](references/safety-gates.md): initial vs final checks; added/updated tests; preserved contracts; modified files; unresolved risks; any skipped check and why; rollback action. Claim “verified against the checks run,” never “bug-free.”

## Stop immediately when
- Unexpected secret exposure or destructive operation is requested; a test would touch production; uncontrolled external effects; conflicting ongoing edits; risky migration without backout; inability to preserve a public contract; or tests newly fail with unknown cause.
- Architectural beauty is the only benefit and the existing code is clearer without the proposed abstraction.
