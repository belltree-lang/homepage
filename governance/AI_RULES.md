# AI Rules

## Purpose

Define AI behavior constraints. General workflow, architecture, and design system authority live in other governance files.

## AI Behavior Constraints

- **Scope Adherence:** Modify only the files listed in the active task scope unless the user explicitly broadens scope. Preserve user changes that are unrelated to the active task.
- **Collaboration:** Prefer small, scoped changes to avoid context window degradation or merge conflicts.
- **Safety Protocol:** AI agents MUST NOT execute `git push` directly to `main` without first showing a local diff to the user for review.
- **Verification:** Do not falsely claim tests were run. Explain exactly how verification was performed.

## Authority Delegation

For repository constraints (e.g., no build tools), task lifecycles, and workflow instructions, all AI agents must follow the rules defined in `AGENTS.md`.
