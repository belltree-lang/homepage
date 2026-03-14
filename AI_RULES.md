# AI Development Rules

## Purpose

Define AI behavioral constraints for this repository.

## Behavioral Constraints

- Execute work from the authoritative Task OS only.
- Treat `tasks/_active` as executable work and `tasks/_planned` as queued work.
- Move blocked tasks to `tasks/_blocked` when dependencies are not satisfied.
- Move finished tasks to `tasks/_completed` after implementation and verification.
- Treat `tasks/_superseded` as non-executable archive.
- Modify only files explicitly allowed by the active task scope.
- Preserve existing user changes outside task scope.
- Do not introduce frameworks, bundlers, or backend services.
- Keep the site deployable as static files.
- Do not rewrite task content during implementation unless the task explicitly asks for it.
- Prefer safe, local refactors over speculative architectural changes.

## Governance References

- Architecture authority: `governance/ARCHITECTURE.md`
- Design authority: `governance/design-system.md`
- Project overview: `governance/PROJECT.md`

## Execution Model

Default loop:

`read task -> implement scoped change -> verify -> move task state`
