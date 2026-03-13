# Task Status

## Purpose

Track the authoritative task execution state.

## Status Directories

- `_active`: executable now
- `_planned`: queued work
- `_blocked`: waiting on dependencies
- `_completed`: finished work
- `_superseded`: archived obsolete work

## Current Execution Model

Cluster A:

- design-system tasks

Cluster B:

- component tasks

Cluster C:

- navigation and content tasks

Tasks may run in parallel only if file scopes do not conflict.

## Current Active Set

- `task-007-services-index-page-shell.md`
- `task-008-card-component-variants.md`
- `task-009-cta-system-standardization.md`
- `task-010-trust-block-system.md`

