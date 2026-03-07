# AGENTS.md

## Project Overview

This repository is a static corporate website.

Project: BellTree Corporate Website

The site must communicate:

- Trust
- Professionalism
- Community impact

The design system is defined in `design-system.md`.

Implementation tasks may be defined in `tasks/`.

- `index.html` is the primary entry point and contains the full page structure and most site content.
- `styles.css` contains the global design tokens, layout rules, responsive behavior, and animation styling.
- `main.js` contains lightweight progressive enhancement for scroll-triggered reveal effects.
- `siteData.json` is structured content data, but it is not currently wired into the page runtime.

There is no framework, backend, bundler, or build pipeline in the repository as it stands. Any change should preserve the ability to run the site as plain static files.

## Development Philosophy

AI agents must follow these principles.

1. **Safety First**

   Never introduce large structural changes unless explicitly instructed.

2. **Small Changes**

   Each task should modify only the files listed in the task specification.

3. **Design System Compliance**

   All UI changes must follow the design system defined in `design-system.md`.

4. **Minimalism**

   Avoid unnecessary libraries, frameworks, or dependencies.

## Architecture Description

The site is a single-page static site rendered directly by the browser.

1. The browser loads `index.html`.
2. `index.html` loads `styles.css` for all layout and visual styling.
3. `index.html` loads `main.js` at the end of the document.
4. `main.js` attaches an `IntersectionObserver` to elements with the `.fade-in` class and adds `.is-visible` when they enter the viewport.
5. CSS transitions in `styles.css` animate those elements into view.

### Architectural constraints

- Keep the site deployable as static files unless the user explicitly asks for a platform change.
- Avoid introducing a framework or build step for minor content or styling changes.
- Do not duplicate content across `index.html` and `siteData.json` without a clear reason.
- If `siteData.json` is used in the future, make it the clear source of truth for the content it owns.

## Coding Rules

### General

- Prefer small, direct changes over speculative refactors.
- Preserve the current static-site model unless a broader rewrite is explicitly requested.
- Use semantic HTML elements where possible.
- Keep JavaScript minimal and focused on progressive enhancement.
- Prefer readable, dependency-free solutions.
- Read the corresponding file in `tasks/` before implementing a task when task files are present.
- Only modify the files listed in the task unless the user explicitly broadens the scope.
- Do not change unrelated code.
- Preserve existing content unless the task explicitly allows modification.

### HTML

- Keep content structure semantic and accessible.
- Use headings in logical order.
- Use list elements only for actual lists.
- Add `aria-` attributes only when native HTML semantics are insufficient.
- Keep metadata in the `<head>` accurate when page content changes materially.
- Prefer `section`, `header`, `nav`, `article`, and `footer` where they fit naturally.
- Avoid excessive div nesting.

### CSS

- Reuse existing CSS custom properties in `:root` before adding new colors or spacing values.
- Prefer extending existing layout patterns such as `.container`, `.section`, and card styles before inventing new ones.
- Keep selectors simple and low-specificity.
- Preserve responsive behavior for mobile layouts.
- Add motion carefully and provide reduced-motion handling when introducing or changing animations.
- Follow the design token approach defined by `design-system.md`.
- Keep the core palette aligned with:
  - `#0B2E4E`
  - `#2FAF90`
  - `#F5F7F8`
  - `#222222`
  - `#FFFFFF`
- Card UI should default to:
  - `border-radius: 8px`
  - `padding: 24px`
  - `background: white`
  - subtle shadow
- Avoid introducing inconsistent one-off styles.

### JavaScript

- Treat JavaScript as enhancement, not a requirement for core content visibility.
- Avoid adding libraries for simple DOM behavior.
- Guard browser APIs when reasonable; pages should degrade gracefully if a feature is unavailable.
- Keep scripts modular and easy to remove if the site returns to fully static behavior.

### Content and Data

- Do not add the same factual content in multiple places unless one is explicitly generated from the other.
- If updating business facts, dates, staffing counts, or offerings, check for duplicate references across `index.html` and `siteData.json`.
- Prefer a single source of truth for business content.

## Commit Style

- Use short, imperative commit messages.
- Prefer formats like:
  - `feat: add partner section copy`
  - `fix: prevent fade-in content from staying hidden without js`
  - `docs: add repository agent guidance`
  - `style: refine business card spacing`
- Keep unrelated changes out of the same commit.
- If a change affects content, styling, and script behavior, group them only when they are part of one user-visible change.

## Testing Rules

This repository currently has no automated test suite. Until one is added, testing is manual.

### Required checks for most changes

- Open `index.html` in a browser and verify the page renders without console errors.
- Verify the layout at desktop width and a narrow mobile width.
- If editing `main.js` or animation-related CSS, verify sections reveal correctly on scroll.
- Confirm content remains readable if JavaScript fails or is disabled when the change touches progressive enhancement behavior.
- If changing factual content, verify consistency across `index.html` and `siteData.json`.

### Before finishing work

- Check that asset paths still resolve correctly as plain relative files.
- Check that no section is unintentionally hidden by default.
- Check for obvious HTML/CSS syntax mistakes.
- Verify that design-system-driven changes remain consistent with `design-system.md`.

## Layout System

- Use a container max width of `1200px` unless the user explicitly requests otherwise.
- Standard section spacing is `100px` top and bottom unless a task says otherwise.
- Grid behavior should follow:
  - mobile: 1 column
  - tablet: 2 columns
  - desktop: up to 4 columns

## Responsive Design Rules

- Breakpoints should follow:
  - mobile: under `768px`
  - tablet: `768px` to `1024px`
  - desktop: above `1024px`
- Layouts must adapt gracefully across these sizes.

## Accessibility Rules

- All images must include meaningful `alt` text unless purely decorative.
- Interactive elements must remain keyboard accessible.
- Color contrast must remain sufficient.
- Avoid relying solely on color to communicate meaning.

## Performance Rules

- Keep the site lightweight.
- Do not introduce heavy frameworks.
- Do not add build tools or large JavaScript bundles.
- Images should use optimized formats when added.

## Forbidden Actions

- Do not introduce new frameworks.
- Do not add build tools.
- Do not restructure the entire codebase.
- Do not remove content without explicit instruction.

## Development Workflow

When given a task:

1. Read the task specification.
2. Modify only the specified files.
3. Verify the acceptance criteria.
4. Stop.

### If tooling is added later

- Document the exact commands here.
- Run all repo-defined checks before concluding work.
- Do not claim automated testing was performed unless it actually was.

## End Goal

The final site should be:

- visually calm
- modern
- trustworthy
- easy to navigate
- responsive across devices
