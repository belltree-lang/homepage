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

