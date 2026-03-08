# AI Rules

## Purpose

Define AI behavior only. Design, architecture, and task numbering authority live in other governance files.

## Repository Constraints

- Keep the project static HTML and CSS.
- Do not introduce frameworks, bundlers, or backend services.
- Do not modify files outside the active task scope unless the user explicitly broadens scope.
- Preserve user changes that are unrelated to the active task.

## Task Execution Rules

- Execute tasks only from `tasks/_active`.
- Read `templates/TASK_TEMPLATE.md` before writing or normalizing tasks.
- Move blocked tasks to `tasks/_blocked`.
- Move finished tasks to `tasks/_completed`.
- Treat `tasks/_planned` as queued work and `tasks/_superseded` as archive.
- Category folders under `tasks/00-*` through `tasks/90-*` are non-executable archives.

## Collaboration Rules

- Prefer small, scoped changes.
- Keep architecture, design system, and project notes synchronized with their authoritative governance files.
- Verify relative paths after page or navigation changes.

