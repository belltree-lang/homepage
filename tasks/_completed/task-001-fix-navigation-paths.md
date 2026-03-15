# Task 001: Fix Navigation Paths Site-wide

## Title
Fix navigation link path inconsistencies across all site directories.

## Problem
Links to `/community/index.html` and other shared pages use inconsistent relative paths in different directory depths, causing 404 errors in specific sub-pages.

## Target Files
- All `.html` files in the repository (approx. 25+ files).

## Implementation
- Normalize all header and footer links.
- Use a standardized relative path approach based on directory depth.
- Specifically fix the `/community/` link in `/pages/services/` index and sub-pages.

## Acceptance Criteria
- [ ] No 404 errors when navigating from any page to any other page linked in header/footer.
- [ ] Relative paths match the directory depth (e.g., `../../` for nested pages).

## Dependencies
- None.

## Priority
HIGH
