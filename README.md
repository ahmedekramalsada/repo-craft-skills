# RepoCraft Skills

**Understand the repo. Simplify the code. Teach the next agent.**

Three open, portable [Agent Skills](https://agentskills.io/specification) for making existing and new repositories easier to navigate and safer to change — without unnecessary abstraction, documentation bloat, or giant rewrites.

| Skill | Job | Does **not** do |
| --- | --- | --- |
| [`project-map`](skills/project-map/SKILL.md) | Build evidence-backed, progressive developer documentation and a useful `AGENTS.md` | Rewrite application code |
| [`project-refactor`](skills/project-refactor/SKILL.md) | Identify the smallest maintainable structural change, protect behavior with tests, refactor incrementally | Enforce one architecture or promise zero bugs |
| [`project-master`](skills/project-master/SKILL.md) | Generate or refresh a **repo-specific** skill to guide future coding tasks | Replace source/docs or copy them into a huge prompt |

## The idea

```
Any repository (tiny CLI → large monorepo)
        │
        ├── project-map         → README / AGENTS.md / minimal docs
        │                          (accurate, source-linked, on demand)
        ├── project-refactor     → smaller, test-verified changes
        │                          (only when structural change is justified)
        └── project-master       → .agents/skills/project-maintainer/SKILL.md
                                   (how future agents change THIS repo)
```

**The recommended order** for a messy project is `project-map` → `project-refactor` (if it actually needs refactoring) → `project-master`. For a clean new project, skip the refactor. Run them independently if that's all the task needs. When module locations change, update existing docs and the generated skill in the same change.

## Install

### OpenCode — user-wide (macOS / Linux / WSL)

```bash
mkdir -p ~/.config/opencode/skills
cp -R skills/project-map skills/project-refactor skills/project-master ~/.config/opencode/skills/
```

Run these commands **from the root of this downloaded/cloned repository**. Project-local alternative: copy the three folders into `<your-project>/.opencode/skills/` instead. Avoid both locations with the same skill IDs unless intentional overrides are desired.

### Codex and portable clients

For Codex, put these three folders under your user `~/.agents/skills/` or project `.agents/skills/`. OpenCode also discovers `.agents/skills/` under its current docs. Other agents vary: check their support for the Agent Skills standard. The **generated** project-specific skill normally lives at `<repo>/.agents/skills/project-maintainer/SKILL.md`.

These skills use simple `SKILL.md` files with optional just-in-time references; they do not require network access, Python, a particular programming language, MCP servers, or extra runtime packages.

## Use in OpenCode

Ask the agent explicitly to load the skill, for example:

```
Use the project-map skill to map this repository. Create only
useful, source-verified documentation. Don't edit application code.
```

```
Use the project-refactor skill to assess this repo. Show me the
smallest safe plan first; preserve behavior and public contracts.
```

```
Use the project-master skill to create a repo-local skill for
future feature work, bug fixes, and testing. Avoid duplicate docs.
```

After initialization:

```
Use the project-maintainer skill to add [feature]. Follow this
project's test and contract checks; make the smallest correct edit.
```

Skill auto-discovery depends on the agent's configuration/permissions; explicitly requesting a named skill is the most predictable way to start.

## Design promises

- **Adapt, don't mandate.** Don't force `features/core/shared`, DDD or microservices into a 100-line project; use feature modules only when boundaries pay for themselves.
- **Smallest correct change.** A clear one-line fix beats a new abstraction; never optimize line count at the expense of readability or correctness.
- **Behavior and contracts first.** Characterization/contract tests before risky refactors; baseline checks, frequent verification and explicit stops for high-risk changes.
- **One source of truth.** Code is authoritative for implementation; docs describe navigation, boundaries and rationale; AGENTS.md stores tiny standing rules; skills hold task procedures.
- **On-demand context.** Agents load only what they need; reference files stay unloaded until needed.
- **No false confidence.** No skill can guarantee zero regressions. Results must say what was and wasn't tested.
- **No surprise writes.** Docs bootstrap doesn't change code; wide refactors need approved scope; preserve unrelated work and keep secrets out of artifacts.

## Layout

```
repo-craft-skills/
├── skills/
│   ├── project-map/
│   │   ├── SKILL.md
│   │   └── references/output-contract.md
│   ├── project-refactor/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── safety-gates.md
│   │       └── lean-design.md
│   └── project-master/
│       ├── SKILL.md
│       └── references/generated-skill-contract.md
├── evals/
│   ├── README.md
│   └── scenarios.json
├── tests/validate.py
├── .github/workflows/validate.yml
├── CONTRIBUTING.md
└── LICENSE
```

## Validate

Local structural checks (Python 3.9+, stdlib only):

```bash
python3 tests/validate.py
```

The GitHub Actions workflow runs the same validator. `evals/scenarios.json` provides **behavioral test prompts and acceptance criteria** for checking actual agents on sample repositories. Static validation **does not** prove model behavior or project safety; the behavioral scenarios need to be run against real coding agents and reviewed. See [the manual evaluation protocol](evals/README.md).

Optional standard validator (if you already have `skills-ref`):

```bash
skills-ref validate skills/project-map
skills-ref validate skills/project-refactor
skills-ref validate skills/project-master
```

## Maintain and contribute

The best improvements come from reproducible examples where a skill fails: a poor module boundary suggestion, unnecessary docs, a bad code route, a missed test, or extra context consumption. See [CONTRIBUTING.md](CONTRIBUTING.md). PRs should improve one observable behavior with an evaluation scenario, not just add instructions.

## Research / grounding

- [Agent Skills specification](https://agentskills.io/specification) — portable metadata and progressive disclosure.
- [OpenCode: skills](https://dev.opencode.ai/v2/docs/skills/) and [project instructions](https://dev.opencode.ai/v2/docs/instructions/) — discovery and `AGENTS.md` behavior.
- [OpenAI: Codex customization](https://learn.chatgpt.com/docs/customization/overview) — distinction between durable guidance and task skills.
- [Anthropic: authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — descriptions, lean skill bodies and evaluation.
- [Martin Fowler: Refactoring](https://www.martinfowler.com/books/refactoring.html) — incremental, behavior-preserving edits.
- [Google engineering practices: small changes](https://github.com/google/eng-practices/blob/master/review/developer/small-cls.md) — focused reviews and separating refactors from features.

## License

MIT — see [LICENSE](LICENSE).
