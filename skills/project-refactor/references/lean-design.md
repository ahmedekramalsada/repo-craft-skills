# Lean design decisions (use only for nontrivial architectural choices)

This is a **decision aid**, not a checklist that forces added layers. Optimize for local comprehensibility and the ability to make a future change safely.

## First diagnose the real problem
- **High coupling:** a feature reaches into another feature's internals → encapsulate the *specific* shared contract; don't make a service for each function.
- **Low cohesion:** unrelated concepts changed together → move code near the behavior/data it owns.
- **Repeated business rule:** two copies diverge → consolidate where ownership is clear; duplicating tiny syntax is sometimes simpler.
- **Too many dependencies:** an edit affects unrelated files → first remove unnecessary import/state knowledge, then consider modules.
- **Hard to test:** a unit calls external systems directly → isolate the I/O boundary with a seam, not a global DI container by default.
- **Big function/class:** split only where named responsibilities or effects make understanding easier; length is a signal, not a rule.
- **Premature abstraction:** abstractions outnumber meaningful behaviors → inline/remove instead of layering further.

## Practical coding principles (calibrated)

| Principle | Apply when it helps | Don't turn it into |
| --- | --- | --- |
| KISS / YAGNI | Prefer existing language idioms and straightforward code | Hidden complexity from ultra-compressed code |
| DRY | Repeated **knowledge or policy** must change together | A generic helper for two coincidentally similar expressions |
| Single responsibility | A module has one coherent reason to change | One file/class per tiny function |
| Encapsulation | Protect invariants and hide volatile internals | Getters/setters wrapping every field |
| Interface segregation | Consumers need meaningfully different contracts | Many one-method interfaces for one implementation |
| Dependency inversion | Independent business logic needs a seam to unstable I/O | Universal DI or abstract repositories |
| Open/closed | Multiple *real* algorithms/providers vary independently | Strategy objects for one fixed `if` branch |
| Liskov/composition | Subtypes must honor behavior; prefer composition for shared behavior | Deep inheritance for superficial reuse |
| Testability | Key logic can be exercised with deterministic inputs | Mocking all internals and testing implementation details |

## Pattern selection: require an actual need
- **Strategy:** several interchangeable policies exist and more changes are likely; else a clear conditional.
- **Adapter:** upstream API or external provider shape differs from your domain; else call it directly.
- **Factory:** construction has meaningful invariants/variation; else constructor or direct function.
- **Repository / data access:** persistence is complex enough to isolate queries or substitution matters; else existing framework data idiom.
- **Events:** decoupled side effects and delivery semantics are intentional; else direct call.
- **State machine:** transitions/permissions are complicated enough that valid states need explicit modeling; else simple enum + checks.

## Always examine relevant correctness dimensions
- Input validation and error semantics; safe defaults; fail-closed authorization.
- Data ownership, transactional boundaries, concurrent writes, retries and idempotence.
- Resource bounds/timeouts, I/O use, memory/performance **when measured**.
- Stable API/wire format, storage schema and compatibility with consumers.
- Accessibility/user feedback for interface changes.

Choose the smallest design with fewer independent concepts, fewer changed files, and fewer surprising dependencies **while preserving clear naming and correctness**.
