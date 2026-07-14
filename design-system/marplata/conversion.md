# Conversion Strategy and CTA Patterns

> **INHERITS FROM:** `MASTER.md`
> Conversion optimization strategies and CTA placement patterns.

## Conversion Strategy

### Single CTA Focus
- One primary action per page
- Reduce cognitive load
- Clear visual hierarchy

### Large Typography
- Headlines should be bold and clear
- Communicate value proposition immediately
- Use Playfair Display for editorial feel

### Lots of Whitespace
- Generous padding around elements
- Clear visual separation
- Focus on key content

### No Nav Clutter
- Minimal navigation on landing pages
- Remove distractions
- Guide user to conversion point

### Mobile-First
- Design for mobile screens first
- Progressive enhancement
- Touch-friendly targets

## CTA Placement

### Center, Large CTA Button
- Primary action centered on page
- Large enough to be easily tappable
- Contrasting color for visibility

### Section Order
1. **Hero Headline** - Compelling value proposition
2. **Short Description** - Brief explanation
3. **Benefit Bullets (3 max)** - Key value points
4. **Primary CTA** - Clear call to action
5. **Footer** - Supporting information

## CTA Button Styles

### Primary CTA
```css
.cta-primary {
  background: var(--color-primary);
  color: white;
  padding: 16px 32px;
  border-radius: 8px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 200ms ease;
}

.cta-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

### Secondary CTA
```css
.cta-secondary {
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  padding: 16px 32px;
  border-radius: 8px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
}
```

## Conversion Best Practices

### Above the Fold
- Clear value proposition
- Primary CTA visible without scrolling
- Hero image or visual

### Social Proof
- Testimonials
- Trust badges
- User counts

### Urgency
- Limited time offers
- Scarcity indicators
- Clear deadlines

### Form Optimization
- Minimize required fields
- Clear labels
- Inline validation
- Progress indicators
