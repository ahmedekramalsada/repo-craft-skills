# Generated skill contract (not a rigid template)

## Output location
Default repo path: `.agents/skills/project-maintainer/SKILL.md`.
Use `.opencode/skills/project-maintainer/SKILL.md` if this project standardizes on OpenCode-only skills. Do **not** create both for the same ID. Project-specific skill remains checked in alongside application code.

## Example outline (fill with **real** discovered facts, not placeholders)
```
---
name: project-maintainer
description: Implements and debugs [verified project domain] features using [specific workflow]; use for [tasks], not for [unrelated tasks].
---

# Project Maintainer
## When to use / not use
## Load context in this order
1. Root AGENTS.md; consult docs/code-map.md only for relevant feature.
2. Read exact target modules and adjacent contracts/tests; don't read whole repo.
## Task routing (links to current source)
| Task | First look | Contract to preserve | Test |
## Make a change
1. Establish behavior and affected files; pick smallest edit.
2. Make the change; check boundary, auth/data assumptions.
3. Test affected flow and check related contracts.
4. Update docs only if behavior/paths/decisions changed.
## Project-specific failure traps
## Verification by change type
## Completion report
```

## Review gate before saving
- Does the description allow the agent to select this for actual **coding tasks**, not every project question?
- Is every path real, and does each relevant task point to **specific** files or existing docs?
- Are commands verified, or clearly marked `UNVERIFIED` with blockers?
- Could a normal dev follow at least two task playbooks without guessing?
- Does it tell the agent where auth, migrations, data ownership, generated code, and interfaces live **if relevant**?
- Is the skill shorter than the docs it links to, and does it add procedural guidance?
- Would reading it again after 3 months still be accurate? Remove brittle line numbers and ephemeral branch references.
- Is it safe: no real `.env`, deploy token, production data, destructive commands?
- Does it comply with the Agent Skills frontmatter rules? No nested `SKILL.md` within this skill folder.
