# Task 23 – Add Support Model Diagram

## Changes

### index.html

```html
<div class="support-diagram">
  <div class="support-node">Fitness</div>
  <div class="support-node">Healthcare</div>
  <div class="support-node">Community</div>
  <div class="support-node">End-of-life</div>
</div>
```

### styles.css

```css
.support-diagram {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.support-node {
  padding: 20px;
  border: 1px solid #e6e8ef;
  border-radius: 12px;
  background: white;
  text-align: center;
}
```

