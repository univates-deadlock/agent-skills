# CSS architecture for Vanilla Web projects

Follow the repository's existing organization first. When the project already separates tokens, globals, components, and pages, preserve that boundary.

## Recommended responsibilities

### Tokens / variables

Use custom properties for reusable design decisions:

```css
:root {
  --color-primary: #2457f5;
  --spacing-md: 1rem;
  --radius-md: 0.75rem;
  --transition-fast: 150ms ease;
}
```

Before adding a token, search for an equivalent. Prefer semantic aliases when a raw palette value acquires a stable UI meaning.

### Global styles

Global CSS should contain resets, typography defaults, document-level layout, and a small set of genuinely universal utilities. A component-specific visual rule does not belong globally merely because several pages currently use it.

### Components

Component CSS owns the block's appearance and internal layout. It should not depend on a particular page container unless that dependency is part of the component's contract.

### Pages

Page CSS owns composition unique to a route: section arrangement, page-specific hero layout, and adaptations that should not affect the shared component everywhere else.

## Responsive behavior

- Reuse existing breakpoints before inventing new ones.
- Prefer fluid sizing (`min()`, `max()`, `clamp()`, flexible grid/flex layouts) when it reduces breakpoint-specific overrides.
- Test content growth, not only ideal text lengths.
- Avoid device-name breakpoints such as "iPhone" or "tablet" in the code; base rules on layout needs.
- Keep the mobile/desktop direction consistent with the existing codebase rather than mixing strategies in adjacent files.

## Specificity

Prefer single-class component selectors and shallow relationships. Reach for `!important` only after understanding the cascade problem; it should not compensate for unclear architecture.

## Literal values

A literal is acceptable for a value that is truly local and unlikely to represent a shared design decision. Repeated or semantic visual values should normally become or reuse tokens.
