# Contributor Workflow

## Purpose

Shared operating guide for Cursor and Codex contributors working on this repository.

## Read Order

Read in this order before editing:

1. `AGENTS.md`
2. `governance/PROJECT.md`
3. `governance/ARCHITECTURE.md`
4. `governance/design-system.md`
5. `governance/AI_RULES.md`
6. `governance/TASK_STATUS.md`
7. `templates/TASK_TEMPLATE.md`
8. the active task in `tasks/_active/`

## Authority Order

When sources conflict, use this order:

1. Direct user instruction for the current task
2. `AGENTS.md`
3. `governance/PROJECT.md`
4. `governance/ARCHITECTURE.md`
5. `governance/design-system.md`
6. `governance/AI_RULES.md`
7. `governance/TASK_STATUS.md`
8. the active task file in `tasks/_active/`
9. committed runtime files such as route `index.html`, `styles.css`, and `siteData.json`
10. `lolipop_staging/`, `output/`, `tmp/`, and `reports/` as reference only

`reports/` is date-sensitive and must never outrank committed runtime files or governance documents.

## Task Operating Rule

- Execute work only from `tasks/_active/`.
- Treat `tasks/_planned/` as queued work, not executable work.
- If a documentation/governance task is broad but not active yet, normalize it into `tasks/_active/` before starting.
- Read `templates/TASK_TEMPLATE.md` before writing or normalizing tasks.

## Cursor

### Open the Repository

From a terminal already positioned at the repo root:

```powershell
cursor .
```

Or open the explicit path:

```powershell
cursor "<repo-root>"
```

### Cursor Rule Reference

Cursor-side lightweight repo notes live at [../.cursor/repo-rules.md](../.cursor/repo-rules.md). Treat that file as a convenience summary only; the canonical rules remain `AGENTS.md` and `governance/`.

## WSL

### Basic Path Into the Repo

If you start from Windows and want to continue inside WSL:

```powershell
wsl
cd "$(wslpath '<windows-path-to-repo>')"
```

Example pattern:

```bash
cd "$(wslpath 'C:\path\to\repo')"
```

Use WSL when you want a Unix shell or Linux tooling, but keep the same authority order and task flow.

## Codex CLI

### Start From Repo Root

If you are already in the repository root:

```powershell
codex -m gpt-5.4 -c model_reasoning_effort="high"
```

### Start With an Explicit Repo Path

```powershell
codex -C "<repo-root>" -m gpt-5.4 -c model_reasoning_effort="high"
```

### Resume the Most Recent Session

```powershell
codex resume --last -C "<repo-root>" -m gpt-5.4 -c model_reasoning_effort="high"
```

### Fork the Most Recent Session

```powershell
codex fork --last -C "<repo-root>" -m gpt-5.4 -c model_reasoning_effort="high"
```

## Recommended Model Profiles

Choose models in the launch command, not by telling the model to switch inside the prompt.

- `gpt-5.4` + `high`
  - Use for governance changes, documentation cleanup, cross-file reconciliation, and route/runtime alignment work
- `gpt-5.3-codex` + `medium`
  - Use for day-to-day HTML/CSS page work and smaller scoped edits

Example daily HTML/CSS launch:

```powershell
codex -C "<repo-root>" -m gpt-5.3-codex -c model_reasoning_effort="medium"
```

## Static Site Verification

There is no package-based dev server at the repository root. Verify changes as a static site.

### Recommended Preview Command

```powershell
python -m http.server 8000
```

Open:

- `http://127.0.0.1:8000/`
- each edited route directly, such as `/services/`, `/community/`, or `/recruit/`

### Verification Expectations

- Check the edited route renders as a static file with correct relative links
- Check the page still loads `styles.css`
- Check route assumptions against committed directories, not against `reports/` or `lolipop_staging/`
- Record exactly what you verified

## Runtime Notes

- The live stylesheet is `/styles.css`
- `assets/css/*` are support/reference files, not the current runtime entry point
- `/community/` is the current committed public route
- `/services/community/` is not a committed route and must not be documented as live unless a real directory is added
