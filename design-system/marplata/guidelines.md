# Anti-Patterns and Accessibility Guidelines

> **INHERITS FROM:** `MASTER.md`
> Guidelines to follow and patterns to avoid.

## Anti-Patterns to AVOID

### Visual Anti-Patterns
- ❌ Vibrant & Block-based designs
- ❌ Playful colors
- ❌ Emojis as icons — Use SVG icons (Heroicons, Lucide, Simple Icons)
- ❌ Missing `cursor:pointer` — All clickable elements must have cursor:pointer
- ❌ Layout-shifting hovers — Avoid scale transforms that shift layout
- ❌ Low contrast text — Maintain 4.5:1 minimum contrast ratio
- ❌ Instant state changes — Always use transitions (150-300ms)
- ❌ Invisible focus states — Focus state must be visible for a11y

### Interaction Anti-Patterns
- ❌ Inconsistent button styles across pages
- ❌ Missing hover/active states
- ❌ Clickable elements without visual feedback
- ❌ Forms without validation feedback

## Accessibility Guidelines

### Focus States
- All interactive elements must have visible focus indicators
- Use `outline` or `box-shadow` for focus
- Maintain WCAG 2.1 AA compliance

### Color Contrast
- Text: 4.5:1 minimum
- Large text: 3:1 minimum
- Interactive elements: 3:1 minimum

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Logical tab order
- Skip links for main content

### Screen Readers
- Use semantic HTML
- ARIA labels where needed
- Alt text for images

### Motion
- Respect `prefers-reduced-motion`
- Provide alternatives for motion-based interactions
- No essential information conveyed only through motion
