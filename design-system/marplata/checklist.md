# Pre-Delivery Checklist

> **INHERITS FROM:** `MASTER.md`
> Quality gates to verify before delivering UI code.

## Visual Quality

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Brand logos are correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] Use theme colors directly (bg-primary) not var() wrapper

## Interaction

- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

## Light/Dark Mode

- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible in both modes
- [ ] Glass/transparent elements visible in both modes
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery

## Layout

- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

## Accessibility

- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
- [ ] Keyboard navigation works
- [ ] Screen reader compatible

## Performance

- [ ] Images optimized
- [ ] CSS/JS minified
- [ ] No render-blocking resources
- [ ] Lazy loading for images
- [ ] Critical CSS inlined

## Browser Support

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari
- [ ] Chrome Android

## Responsive Testing

- [ ] 375px (iPhone SE)
- [ ] 768px (iPad)
- [ ] 1024px (iPad Pro)
- [ ] 1440px (Desktop)
- [ ] 1920px (Large Desktop)

## Content

- [ ] All text is readable
- [ ] No placeholder content (lorem ipsum)
- [ ] All links work
- [ ] All forms submit
- [ ] Error states handled
- [ ] Loading states implemented

## Code Quality

- [ ] Consistent naming conventions
- [ ] No unused CSS/JS
- [ ] Comments where needed
- [ ] No console errors
- [ ] Valid HTML
- [ ] Valid CSS
- [ ] Valid JavaScript
