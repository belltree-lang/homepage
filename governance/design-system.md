# Design System

## Scope

Authority for tokens, typography, spacing, color system, and component primitives under the new "Consultation-First Premium" direction.

## Token Catalog

### Color Tokens

- `--color-primary: #1A365D` (Deep slate blue - Trust, stability, corporate presence)
- `--color-primary-light: #2A4A7F`
- `--color-background: #FCFCFA` (Warm off-white - Humane, premium, approachable)
- `--color-background-alt: #F4EFEB` (Soft beige/sand - Section contrast, warmth)
- `--color-background-soft: #F9F8F6`
- `--color-accent: #C27A65` (Muted terracotta - Warm highlight for CTAs and focus)
- `--color-accent-hover: #A86550`
- `--color-surface: #FFFFFF`
- `--color-text: #2C2C2C` (Soft black, avoiding harsh contrasts)
- `--color-text-muted: #666666`
- `--color-border: #E5E0D8`
- `--color-border-strong: #C4BCB3`

### Typography Tokens

- `--font-family-base: "Noto Sans JP", sans-serif`
- `--font-size-sm: 0.875rem`
- `--font-size-body: 1rem`
- `--font-size-lead: 1.125rem`
- `--font-size-heading-sm: 1.25rem`
- `--font-size-heading-md: 1.75rem`
- `--font-size-heading-lg: clamp(2rem, 4vw, 2.75rem)`
- `--font-size-heading-xl: clamp(2.5rem, 5vw, 3.5rem)`
- `--font-weight-regular: 400`
- `--font-weight-medium: 500`
- `--font-weight-semibold: 600`
- `--font-weight-bold: 700`
- `--line-height-tight: 1.4`
- `--line-height-base: 1.8`
- `--line-height-loose: 2.0`
- `--letter-spacing-base: 0.03em`
- `--letter-spacing-heading: 0.05em`

### Spacing Tokens

- `--space-xs: 0.5rem`
- `--space-sm: 1rem`
- `--space-md: 1.5rem`
- `--space-lg: 2rem`
- `--space-xl: 3rem`
- `--space-2xl: 4.5rem`
- `--space-3xl: 6rem`
- `--space-4xl: 8rem`

### Container Tokens

- `--container-base: 1200px`
- `--container-narrow: 800px`
- `--container-wide: 1400px`
- `--container-padding: clamp(1.5rem, 4vw, 3rem)`

### Radius Tokens

- `--radius-sm: 8px`
- `--radius-md: 16px`
- `--radius-lg: 24px`
- `--radius-pill: 9999px`
- `--radius-sharp: 0px` (Used selectively for editorial contrast)

### Shadow Tokens

- `--shadow-sm: 0 4px 12px rgba(26, 54, 93, 0.04)`
- `--shadow-md: 0 8px 24px rgba(26, 54, 93, 0.08)`
- `--shadow-lg: 0 16px 48px rgba(26, 54, 93, 0.12)`

## Component Primitives

### Layouts
- **Editorial Grid:** Allows overlapping media and text blocks.
- **Consultation CTA Banner:** A prominent sticky or bottom-heavy layout acting as the ultimate conversion point.

### Buttons
- **Primary:** Terracotta background (`--color-accent`), white text, rounded pill or large radius (`--radius-md`).
- **Secondary:** Transparent background with `--color-primary` border and text.

### Typography Rules
- Emphasize line-height (`1.8` minimum for body) and ample letter-spacing to generate readability and a deliberate, calm pace.

### Surfaces
- Soft, rounded surfaces on cards to contrast against sharp photography. Alternatively, sharp photography bleeding over rounded cards. Very soft, diffused shadows.
