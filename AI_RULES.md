# AI Development Rules

## Purpose

Provide strict rules for AI agents working in this repository.

## General Rules

- Do not introduce frameworks.
- Keep the project static HTML + CSS.
- Follow `ARCHITECTURE.md` for layout structure.
- Follow `design-system.md` for visual tokens.

## File Ownership

`index.html`  
Owned by UI agent.

`styles.css`  
Owned by CSS agent.

Content text  
Owned by Content agent.

SEO metadata  
Owned by SEO agent.

`reports`  
Owned by Review agent.

## Change Rules

Agents must modify only their owned files.

Do not modify governance documents unless the task explicitly requires it.

## Design Rules

Always prefer design tokens over literal values.

## Example

Use:

`var(--border-color)`

Avoid:

`#e6e8ef`

## Development Model

`tasks -> implementation -> review -> analysis -> improvement`
