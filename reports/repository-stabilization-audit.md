# Repository Stabilization Audit

## Repository Structure

Present and authoritative:

- `governance/`
- `templates/`
- `tasks/`
- `tasks/_active`
- `tasks/_planned`
- `tasks/_blocked`
- `tasks/_completed`
- `tasks/_superseded`
- `agents/`
- `reports/`

Archive-only task folders remain present under `tasks/00-*` through `tasks/90-*`, but contain no executable task files.

## Task OS State

- `_active`: 4
- `_planned`: 24
- `_completed`: 0
- `_blocked`: 0
- `_superseded`: 64

Initial active set:

- `task-007-services-index-page-shell.md`
- `task-008-card-component-variants.md`
- `task-009-cta-system-standardization.md`
- `task-010-trust-block-system.md`

## Governance Authority Map

- `governance/ARCHITECTURE.md`: page architecture, navigation, page shells, content schema
- `governance/design-system.md`: tokens, typography, spacing, color, primitives, component catalog
- `governance/AI_RULES.md`: AI behavior constraints only
- `governance/PROJECT.md`: repository overview
- `governance/DECISIONS.md`: architecture decisions
- `governance/TASK_INDEX.md`: task number ranges
- `governance/TASK_STATUS.md`: execution model and active state

Root governance files now act as pointers to the canonical files in `governance/`.

## Design System Token Coverage

Implemented token groups in `styles.css`:

- color
- typography
- spacing
- container widths
- breakpoints
- border radius
- shadow system
- icon sizes

Literal values remain only where browser behavior or one-off media query syntax still requires them.

## Component Catalog Completeness

Documented in `governance/design-system.md`:

- Hero
- SectionHeader
- Card
- CTA Panel
- Grid
- TwoColumnLayout
- TrustBlocks
- Footer

Each component includes purpose, allowed variants, layout rules, and usage rules.

## Page Architecture Readiness

Implemented route shells:

- `/`
- `/services/`
- `/services/fitness`
- `/services/acupuncture`
- `/services/home-care`
- `/services/legal`
- `/services/community`
- `/about`
- `/contact`

Shell coverage:

- Homepage shell: ready
- ServicePage shell: ready
- CompanyPage shell: ready

## Navigation Readiness

Primary navigation is page-based:

- `/`
- `/services/`
- `/about`
- `/contact`

Anchors remain secondary on the homepage footer and local route navigation.

## Parallel Execution Readiness

Cluster model installed:

- Cluster A: design-system tasks
- Cluster B: component tasks
- Cluster C: navigation and content tasks

Parallel execution rule:

Tasks may run in parallel only when file scopes do not conflict.

## Final Task Lists

### tasks in `_active`

- `task-007-services-index-page-shell.md`
- `task-008-card-component-variants.md`
- `task-009-cta-system-standardization.md`
- `task-010-trust-block-system.md`

### tasks in `_planned`

- `task-001-governance-authority-model.md`
- `task-002-design-token-freeze.md`
- `task-005-navigation-architecture.md`
- `task-006-content-schema.md`
- `task-011-services-page-template.md`
- `task-012-footer-system.md`
- `task-013-icon-system.md`
- `task-014-grid-system-cleanup.md`
- `task-015-responsive-layout-audit.md`
- `task-016-accessibility-improvements.md`
- `task-017-seo-improvements.md`
- `task-018-align-governance-docs.md`
- `task-019-localize-navigation-copy.md`
- `task-020-hero-visual-balance.md`
- `task-021-section-contrast.md`
- `task-022-icon-system.md`
- `task-023-support-model-visualization.md`
- `task-024-footer-trust-layer.md`
- `task-025-structure-analysis.md`
- `task-026-governance-unification.md`
- `task-027-card-system.md`
- `task-028-token-cleanup.md`
- `task-029-task-template-standardization.md`
- `task-030-hero-visual-depth.md`

### tasks in `_completed`

- none

### tasks in `_blocked`

- none

### tasks in `_superseded`

- legacy task files and number-colliding archive tasks

