# Website Architecture

## Project

BellTree Corporate Website

This document defines the architectural structure and design principles of the website.

All UI and structural decisions should follow this document.

---

# Core Philosophy

The website should communicate:

Trust  
Clarity  
Human warmth  
Professional healthcare quality

The design should feel:

Calm  
Structured  
Readable  
Accessible

Avoid startup-style aggressive marketing.

---

# Site Layout

The homepage follows a **single narrative flow**.

Order of sections:

1. Hero
2. Achievements
3. Mission
4. Support Model
5. Founder Message
6. Business Units
7. Partnerships
8. Company History
9. Footer

Each section must clearly communicate one idea.

---

# Container System

All sections follow a unified container layout.

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}
```

Section spacing:

```css
section {
  padding: 100px 0;
}
```

---

# Grid System

Layout uses a simple responsive grid.

Desktop:

4 columns

Tablet:

2 columns

Mobile:

1 column

No complex grid frameworks should be introduced.

---

# Card UI Pattern

Many sections use card-based layouts.

Card style:

background: white  
border-radius: 8px  
padding: 24px  
box-shadow: subtle

Cards must feel clean and readable.

---

# Typography System

Primary font:

system-ui

Scale:

h1: 40px  
h2: 32px  
h3: 24px  
body: 16px

Line height:

1.6

Avoid dense paragraphs.

---

# Color System

Primary colors:

Navy: #0B2E4E  
Emerald: #2FAF90  
Gray background: #F5F7F8  
Text: #222222  
White: #FFFFFF

Use color sparingly.

Most sections should remain neutral.

---

# Hero Section

The hero should communicate immediately:

What BellTree is  
Who it serves  
Why it matters

Structure:

headline  
subheading  
supporting text  
optional CTA

Hero must feel calm and trustworthy.

Avoid flashy animations.

---

# Achievements Section

Purpose:

Show credibility.

Use metrics such as:

years of service  
community reach  
impact statistics

Display as cards.

---

# Mission Section

Purpose:

Explain the philosophy of the organization.

Short paragraphs.

Centered layout.

Readable typography.

---

# Support Model Section

Explain how BellTree supports people through life stages.

Example flow:

Exercise  
Rehabilitation  
Home care  
Community support  
End-of-life planning

Visual flow preferred.

---

# Founder Message

Humanize the organization.

Structure:

photo  
message  
signature

Text should feel personal.

---

# Business Units

Explain each service.

Examples:

Fitness  
Home therapy  
Care management  
Community services

Use cards.

---

# Partnerships

Show collaboration with:

Universities  
Healthcare institutions  
Local community groups

Use logos or cards.

---

# Company History

Timeline format.

Milestones:

Founding  
Expansion  
Community initiatives

---

# Footer

Footer should contain:

Navigation  
Contact information  
Legal information

Avoid overly complex layouts.

---

# Responsive Behavior

Breakpoints:

< 768px mobile  
768-1024px tablet  

1024px desktop

Layout must gracefully adapt.

---

# Accessibility

All images require alt text.

Headings must follow hierarchy.

Ensure sufficient color contrast.

Navigation must remain usable via keyboard.

---

# Performance

The website should remain lightweight.

Avoid:

large JS frameworks  
complex build systems

Prefer static HTML and CSS.

---

# Development Rules

Developers and AI agents must:

Follow the design system  
Follow tasks in `/tasks`  
Avoid unnecessary refactoring

Small, safe changes are preferred.

---

# Final Goal

Create a corporate website that communicates:

Trust  
Community impact  
Professional healthcare support

while remaining:

Simple  
Readable  
Accessible
