# Task 24 – Improve Footer Layout

## Changes

### styles.css

```css
.footer {
  padding: 80px 0;
  border-top: 1px solid #e6e8ef;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
}

@media (min-width: 768px) {
  .footer-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```
