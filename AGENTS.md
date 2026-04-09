# AGENTS.md

## Purpose

Repository entry point for human and AI contributors.

## Authority Map

- Architecture rules: `governance/ARCHITECTURE.md`
- Design tokens and components: `governance/design-system.md`
- AI behavior constraints: `governance/AI_RULES.md`
- Repository overview: `governance/PROJECT.md`
- Architectural decisions: `governance/DECISIONS.md`
- Task number ranges: `governance/TASK_INDEX.md`
- Task execution state: `governance/TASK_STATUS.md`

## Task Operating System

Executable tasks may exist only in:
- `tasks/_active`: Execute tasks only from here.
- `tasks/_planned`: Treat as queued work.
- `tasks/_blocked`: Move tasks here if blocked by dependencies.
- `tasks/_completed`: Move finished tasks here.
- `tasks/_superseded`: Treat as archived obsolete work.

Category folders under `tasks/00-*` through `tasks/90-*` are archive-only and are not executable sources.

## Working Rules

- Read the active task file before implementation.
- Read `templates/TASK_TEMPLATE.md` before writing or normalizing new tasks.
- Modify only the files listed in the task scope unless the user explicitly expands scope.
- Do not introduce frameworks, build tooling, Webpack, Vite, Tailwind, or backend dependencies.
- Keep the repository deployable as plain static files. Use `assets/css/variables.css` and `assets/css/style.css`.
- Use the task lifecycle defined in `governance/TASK_STATUS.md`.

## Verification Rules

- Verify changed pages render as static files with correct relative paths.
- Keep implementation aligned with `governance/design-system.md`.
- Do not claim tests were run unless they were run.
