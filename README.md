# BellTree Corporate Website & Recruitment Platform

This repository contains the static web source code for `bellmfit.com`, maintained by human and AI contributors.

## 🏗️ Architecture Overview

The site is built strictly using **Static HTML/CSS** to ensure maximal speed, simplicity, and ease of automated editing by AI agents (Antigravity/Codex).
There is no backend framework (like WordPress) or complex build steps (like Webpack or Vite). 

### Repository Structure
- `.github/workflows/`: CI/CD automation rules for FTPS deployment.
- `assets/`: Static resources for styling and media.
  - `css/variables.css`: **The cornerstone of the design system**. Contains all colors, typography, and spacing tokens.
  - `css/style.css`: The main stylesheet.
  - `css/reset.css`: Browser normalization.
  - `images/`: Images and illustrations.
- `pages/`: 
  - `recruit/`: The recruitment platform and specific job postings.
  - `services/`: Detailed pages for the various healthcare & fitness services offered.
- `governance/`: The authoritative ruleset that both human and AI editors must follow (`AI_RULES.md`, `design-system.md`).

## 🚀 Deployment Workflow (GitHub Actions → Lolipop)

Deployments are entirely automated. 

1. **Local Editing**: Edits are made locally via VSCode or AI agents.
2. **Review**: All diffs MUST be reviewed locally in the browser before pushing.
3. **Push to GitHub**: Code is committed and pushed to the `main` branch.
4. **Automated FTPS Sync**: The GitHub Action (`.github/workflows/deploy.yml`) calculates the diff and pushes *only changed files* to the Lolipop server via secure FTPS.
5. **Live**: The site updates within seconds.

*(Note: Requires `FTP_SERVER`, `FTP_USERNAME`, and `FTP_PASSWORD` secrets configured in GitHub.)*

## 🤖 AI Editing Rules

This repository is optimized for autonomous or semi-autonomous AI editors.
For the complete list of constraints, review `governance/AI_RULES.md`.

**Key directives:**
1. **Never commit directly** without presenting a diff to the user.
2. **Never inline CSS styles**. Always leverage existing classes and the tokens found in `assets/css/variables.css`.
3. **Respect folder hierarchy**. Any new pages should be nested correctly under the domain-driven folders (`pages/`).
