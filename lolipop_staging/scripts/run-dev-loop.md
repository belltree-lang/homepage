# AI Development Loop

You are the development agent for this repository.

Follow this workflow.

STEP 1 — Scan repository

List:

index.html
styles.css
tasks/
design-system.md
ARCHITECTURE.md

STEP 2 — Scan tasks

Read all files inside:

tasks/

Determine execution order.

Rules:

HTML tasks first
CSS tasks after

STEP 3 — Implement tasks

For each task:

Read the task file

Modify only the listed files

Do not introduce frameworks

Do not commit automatically

After each task record:

task name
files modified
summary
side effects

STEP 4 — Repository review

Check:

HTML structure
heading hierarchy
duplicate ids

CSS

unused selectors
color tokens
typography
responsive rules

Architecture

ARCHITECTURE.md compliance
design-system.md compliance

STEP 5 — Generate report

Create:

reports/review-latest.md

Include:

repository structure
tasks implemented
files changed
issues found
design consistency
suggested improvements
quality score (0–10)

STEP 6 — Improvement suggestions

If improvements are found:

create new tasks under

tasks/

Use naming:

task-XX-description.md

Return a summary.