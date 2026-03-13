# Architecture

## Scope

This document is the authority for page architecture, navigation, page shells, and the minimal reusable content schema.

## Site Model

The repository implements a static multi-page corporate site.

Primary routes:

- `/`
- `/services/`
- `/services/fitness`
- `/services/acupuncture`
- `/services/home-care`
- `/services/legal`
- `/services/community`
- `/about`
- `/contact`

Anchors are secondary for in-page jumps inside a route.

## Shared Layout

Every page shell uses the same top-level frame:

1. Site Header
2. Main Content
3. Trust Block
4. CTA Section
5. Footer

Shared structural rules:

- Header navigation is page-based.
- Footer contains route links and secondary anchor links where useful.
- Content uses the shared container, spacing, card, and grid primitives from `governance/design-system.md`.

## Homepage Shell

Purpose:

- Introduce the company
- Establish credibility
- Explain the support model
- Route visitors toward services, company context, and contact

Required sections:

- Hero
- Metrics or achievements
- Mission or philosophy
- Support model
- Representative or company trust content
- Service overview
- Partnerships or proof
- Timeline or history
- Trust Block
- CTA Section
- Footer

## ServicePage Shell

Purpose:

- Explain one service clearly
- Show service fit, support flow, and trust evidence
- End with a direct CTA

Required sections:

- Page Hero
- Service Summary
- Detail Sections
- Trust Block
- CTA Section
- Footer

## CompanyPage Shell

Purpose:

- Explain mission, operating structure, timeline, and organizational trust

Required sections:

- Page Hero
- Company Overview
- Mission or philosophy sections
- Timeline or profile sections
- Trust Block
- CTA Section
- Footer

## Navigation Architecture

Primary navigation must point to routes first:

- `/`
- `/services/`
- `/about`
- `/contact`

Secondary navigation may link to:

- section anchors inside the same page
- service detail routes inside `/services/`

## Page Shell Notes

- All pages must include a visible page title.
- Breadcrumbs are allowed on non-home pages.
- Trust Blocks may surface metrics, partnerships, or reassurance points.
- CTA sections must be present but concise.

## Minimal Content Schema

The repository keeps a lightweight structured content layer in `siteData.json`.

Required schema keys:

- `services`
- `metrics`
- `partners`
- `timeline`
- `cta`

Schema purpose:

- centralize reusable copy and labels
- support later progressive enhancement
- avoid full JSON-driven rendering at this stage

The HTML remains the primary renderer.

