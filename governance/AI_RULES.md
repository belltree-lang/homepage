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

## Deployment & AI Architecture Rules

- The site is automatically deployed to Lolipop via `FTP-Deploy-Action` on push to the `main` branch.
- **Safety Protocol:** AI agents MUST NOT execute `git push` directly to `main` without first showing a local diff to the user for review.
- **CSS Modularity:** Use `assets/css/variables.css` for all design tokens. Do not hardcode hex colors or spacing values in HTML. Use `assets/css/style.css` for main styles.
- **No Build Tools:** Do not introduce Webpack, Vite, Tailwind, or complex build steps. The pipeline strictly copies static files.
