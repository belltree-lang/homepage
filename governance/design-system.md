# Design System

## Scope

Authority for tokens, typography, spacing, color system, and component primitives.

## Token Catalog

### Color Tokens

- `--color-primary: #1f4e79`
- `--color-secondary: #2c3e50`
- `--color-background: #f5f7fa`
- `--color-background-alt: #eef3f8`
- `--color-background-soft: #f8fafc`
- `--color-surface: #ffffff`
- `--color-text: #222222`
- `--color-text-muted: #4f6378`
- `--color-border: #c9d6e3`
- `--color-border-strong: #9fb6cc`
- `--color-primary-rgb: 31, 78, 121`
- `--color-shadow-rgb: 15, 23, 42`

### Typography Tokens

- `--font-family-base: "Noto Sans JP", sans-serif`
- `--font-size-label: 0.875rem`
- `--font-size-body: 1rem`
- `--font-size-lead: 1.125rem`
- `--font-size-heading-sm: 1.25rem`
- `--font-size-heading-md: 1.625rem`
- `--font-size-heading-lg: clamp(2.25rem, 4vw, 3rem)`
- `--font-weight-medium: 500`
- `--font-weight-semibold: 600`
- `--font-weight-bold: 700`
- `--line-height-tight: 1.25`
- `--line-height-base: 1.9`

### Spacing Tokens

- `--space-2xs: 0.25rem`
- `--space-xs: 0.5rem`
- `--space-sm: 0.75rem`
- `--space-md: 1rem`
- `--space-lg: 1.5rem`
- `--space-xl: 2rem`
- `--space-2xl: 3rem`
- `--space-3xl: 5rem`
- `--space-4xl: 7.5rem`

### Container Tokens

- `--container-page: 60rem`
- `--container-narrow: 48rem`
- `--container-wide: 72rem`
- `--container-gutter: 1rem`

### Breakpoint Tokens

- `--breakpoint-tablet: 48rem`
- `--breakpoint-desktop: 64rem`

Note:

Media queries still use literal values for browser compatibility, but the named token values above are the design authority.

### Radius Tokens

- `--radius-sm: 0.5rem`
- `--radius-md: 0.75rem`
- `--radius-lg: 1rem`
- `--radius-xl: 1.25rem`
- `--radius-pill: 999px`

### Shadow Tokens

- `--shadow-sm: 0 0.625rem 1.5rem rgba(var(--color-shadow-rgb), 0.05)`
- `--shadow-md: 0 1rem 2rem rgba(var(--color-shadow-rgb), 0.08)`
- `--shadow-lg: 0 1.5rem 3rem rgba(var(--color-primary-rgb), 0.14)`

### Icon Tokens

- `--icon-size-sm: 1.75rem`
- `--icon-size-md: 2.5rem`
- `--icon-size-lg: 3rem`

## Component Catalog

### Hero

Purpose:

- establish page value proposition
- present the primary context and main action

Allowed variants:

- homepage hero
- page hero

Layout rules:

- one heading, one supporting lead, one primary CTA group
- optional visual support on homepage

Usage rules:

- keep copy concise
- route links are preferred over anchor-only CTAs

### SectionHeader

Purpose:

- group eyebrow, title, and short introduction

Allowed variants:

- default
- compact
- divider

Layout rules:

- vertical stack
- optional divider after the intro

Usage rules:

- use once at the start of each major section

### Card

Purpose:

- provide a shared surface for grouped content

Allowed variants:

- default
- metric
- service
- trust
- timeline

Layout rules:

- use shared padding, border, radius, and shadow tokens

Usage rules:

- extend with modifier classes instead of redefining base card styling

### CTA Panel

Purpose:

- present a trust-oriented action area near the end of a page

Allowed variants:

- inline CTA
- full-width CTA panel

Layout rules:

- lead copy, support points, and CTA actions

Usage rules:

- one primary action and one secondary action at most

### Grid

Purpose:

- arrange repeated content blocks using shared responsive patterns

Allowed variants:

- `grid-2`
- `grid-3`
- `grid-4`
- `grid-auto-fit`

Layout rules:

- mobile 1 column
- tablet 2 columns where relevant
- desktop up to 4 columns

Usage rules:

- prefer shared grid classes over section-specific grids

### TwoColumnLayout

Purpose:

- pair text and visual or paired explanatory blocks

Allowed variants:

- balanced split
- content-heavy split

Layout rules:

- stack on mobile
- split on tablet and above

Usage rules:

- use only when both columns hold meaningful content

### TrustBlocks

Purpose:

- show metrics, reassurance, partnerships, or proof points

Allowed variants:

- metric blocks
- partner blocks
- reassurance blocks

Layout rules:

- repeated card surfaces inside shared grids

Usage rules:

- keep labels short and evidence-oriented

### Footer

Purpose:

- close the page with route links, company context, contact, and copyright

Allowed variants:

- homepage footer
- internal page footer

Layout rules:

- multi-column at desktop
- stacked blocks on mobile

Usage rules:

- include primary routes first
- anchor links are secondary

