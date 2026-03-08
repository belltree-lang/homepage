# Task 20 – Improve Hero Visual Balance

## Goal

Improve the hero section visual balance.

## Changes

### index.html

Ensure hero structure contains:

- `hero-eyebrow`
- `hero-title`
- `hero-description`
- `hero-actions`
- `hero-visual`

### styles.css

```css
.hero {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
}

@media (min-width: 768px) {
  .hero {
    grid-template-columns: 1.2fr 1fr;
    align-items: center;
  }
}

.hero-title {
  font-size: clamp(32px, 4vw, 48px);
  line-height: 1.2;
}

.hero-description {
  max-width: 520px;
  font-size: 18px;
  color: var(--color-slate);
}

.hero-actions {
  margin-top: 24px;
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.hero-visual {
  background: var(--color-light-gray);
  border-radius: 16px;
  height: 260px;
}
```

## Rules

Do not add images.

