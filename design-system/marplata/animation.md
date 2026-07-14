# Animation and Interaction Guidelines

> **INHERITS FROM:** `MASTER.md`
> Animation principles and interaction patterns.

## Animation Principles

### Timing Functions
- **Fast (150ms)**: Hover states, button presses
- **Medium (200-300ms)**: State changes, transitions
- **Slow (400-600ms)**: Page transitions, complex animations

### Easing
- **Default**: `ease` or `ease-in-out`
- **Entrances**: `ease-out` (decelerate)
- **Exits**: `ease-in` (accelerate)

## Key Effects

### Morphing Elements
- SVG/CSS shape transitions
- 400-600ms curves
- Smooth property changes

### Fluid Animations
- Use `transform` and `opacity` for performance
- Avoid animating `width`, `height`, `top`, `left`

### Dynamic Blur
- `backdrop-filter: blur()` for glass effects
- Use sparingly for performance

### Color Transitions
- 200-300ms for color changes
- Use `transition: color, background-color, border-color`

## Interaction Patterns

### Hover States
```css
.interactive {
  transition: all 200ms ease;
  cursor: pointer;
}

.interactive:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}
```

### Focus States
```css
.interactive:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

### Active/Pressed States
```css
.interactive:active {
  transform: translateY(0);
  opacity: 0.8;
}
```

## Loading States

### Spinner
- Use CSS animations for performance
- Keep duration under 2 seconds
- Provide visual feedback

### Skeleton Screens
- Use for content loading
- Maintain layout stability
- Subtle pulse animation

## Reduced Motion

Always respect `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Performance Guidelines

- Use `transform` and `opacity` for 60fps animations
- Avoid layout thrashing
- Use `will-change` sparingly
- Prefer CSS over JS animations
