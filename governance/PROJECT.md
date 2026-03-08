# Project Overview

## Purpose

BellTree corporate site repository for static, page-based healthcare and community support communication.

## Repository Model

- Static HTML pages with shared CSS
- No framework, no bundler, no backend dependency
- Page-based navigation with optional in-page anchors
- AI task execution through the Task OS in `tasks/`

## Root Structure

- `governance/` authority documents
- `templates/` reusable templates
- `tasks/` task operating system
- `agents/` role notes for AI contributors
- `reports/` audit and review outputs
- `assets/` shared images and icons

## Runtime Surface

- `/index.html` homepage
- `/services/` service index
- `/services/*` service detail shells
- `/about/` company page
- `/contact/` contact page
- `/styles.css` shared design implementation
- `/siteData.json` minimal reusable content schema

## Delivery Goal

Provide a stable AI parallel development environment that can scale to 100+ tasks without design drift or structural ambiguity.

