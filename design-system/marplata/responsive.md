# Responsive Design Breakpoints

> **INHERITS FROM:** `MASTER.md`
> Breakpoint definitions and responsive design guidelines.

## Breakpoints

| Breakpoint | Min Width | Target Devices |
|------------|-----------|----------------|
| `xs` | `375px` | Small phones |
| `sm` | `640px` | Large phones |
| `md` | `768px` | Tablets |
| `lg` | `1024px` | Laptops |
| `xl` | `1280px` | Desktops |
| `2xl` | `1536px` | Large screens |

## Mobile-First Approach

All styles should be written mobile-first, with progressive enhancement for larger screens.

```css
/* Base styles (mobile) */
.container {
  padding: 16px;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
  }
}
```

## Layout Guidelines

### Mobile (< 768px)
- Single column layout
- Full-width cards
- Stacked navigation
- Touch-friendly tap targets (44x44px minimum)

### Tablet (768px - 1023px)
- 2-column grids
- Sidebar navigation
- Comfortable spacing

### Desktop (≥ 1024px)
- Multi-column layouts
- Persistent navigation
- Hover states enabled

## Common Patterns

### Responsive Grid
```css
.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
  }
}
```

### Responsive Typography
```css
.heading {
  font-size: 24px;
}

@media (min-width: 768px) {
  .heading {
    font-size: 32px;
  }
}

@media (min-width: 1024px) {
  .heading {
    font-size: 48px;
  }
}
```
