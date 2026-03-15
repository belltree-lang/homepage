# Task 002: Local SEO & Condition Blocks (Visiting Acupuncture)

## Title
Implement Local SEO-focused content and condition blocks for the Visiting Acupuncture & Massage service.

## Problem
The current acupuncture service page is generic and doesn't target local-intent keywords (南大沢, 町田, etc.) or specific long-tail condition queries, which is critical for attracting the right users in the service area.

## Target Files
- `pages/services/acupuncture/index.html` (Main landing page)
- `solutions/stroke/index.html` [NEW]
- `solutions/parkinson/index.html` [NEW]
- `solutions/lower-back-pain/index.html` [MODIFY]
- `solutions/knee-pain/index.html` [MODIFY]

## Implementation

### 1. Main Service Page Refinement
- Update **H1** to: "南大沢・町田エリアの訪問鍼灸マッサージ"
- Ensure natural inclusion of: 訪問鍼灸, 訪問マッサージ, 訪問鍼灸マッサージ, and area names (南大沢, 町田, 八王子, 日野).
- Add a new section: **H2: 訪問鍼灸マッサージで対応している主な症状**
    - Implement 4 condition blocks: 腰痛, 膝痛, 脳梗塞後遺症, パーキンソン病.
    - Each block connects condition + visiting care + local area + link to solution page.

### 2. Solution Pages (Supporting SEO entry points)
- Create new pages for **Stroke** and **Parkinson** using the standard solution hierarchy.
- Titles:
    - Stroke: "南大沢・町田で脳梗塞後遺症の訪問鍼灸マッサージをお探しの方へ"
    - Parkinson: "町田・八王子エリアのパーキンソン病向け訪問マッサージ・リハビリ支援"
- Update existing **Lower back pain** and **Knee pain** pages to strengthen the link back to the local visiting service.

### 3. Internal Linking
- Establish two-way links between the main service page and individual condition pages.
- Ensure all condition pages have a clear CTA to the contact page.

## Acceptance Criteria
- [ ] Acupuncture H1/H2 reflects local SEO strategy.
- [ ] 4 condition blocks implemented with local context.
- [ ] Stroke and Parkinson solution pages created and linked.
- [ ] No keyword cannibalization (main service page remains canonical for service intent).

## Dependencies
- Task 001 (Completed).

## Priority
HIGH
