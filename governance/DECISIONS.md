# Decisions

## 2026-03-08

Decision:

The repository uses the Task OS in `tasks/_active`, `_planned`, `_blocked`, `_completed`, and `_superseded` as the only executable workflow.

Reason:

Eliminate ambiguity between archived category folders and live execution queues.

Impact:

Archived category folders are no longer task sources.

## 2026-03-08

Decision:

Governance authority moves to `/governance`.

Reason:

Root-level documents had drifted and mixed responsibilities.

Impact:

Root documents are entry pointers. Canonical guidance lives in `/governance`.

## 2026-03-08

Decision:

Navigation becomes page-based with anchors as secondary support only.

Reason:

Parallel work on multiple page shells requires stable route boundaries.

Impact:

Static route pages exist for services, company information, and contact.

## 2026-03-08

Decision:

The site remains static HTML and shared CSS.

Reason:

The repository goal is low-friction AI parallel delivery without framework overhead.

Impact:

No framework or build tool may be introduced by default.


## 2026-08-31

Decision:

Header and footer are edited directly in each page. The sync script `scripts/sync_components.py` and the templates `templates/header.html` / `templates/footer.html` are retired to `_archive/2026-08-31/`.

Reason:

The templates still held the old BellTree corporate navigation (about / model / news / cases / solutions), while the live pages had moved to the BellFit layout with the tokushoho link added on 2026-08-31. Running the script would have wiped those page edits across the site.

Impact:

Site-wide header or footer changes are applied per page by hand (the FOOTER_START / FOOTER_END markers remain as grep anchors). `templates/**` and `_archive/**` are excluded from FTP deploys.
