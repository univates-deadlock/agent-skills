# BEM conventions

Use BEM when the repository has adopted it. Do not retrofit unrelated existing code unless the task includes that refactor.

## Shape

```css
.card {}
.card__title {}
.card__actions {}
.card--featured {}
.card__button--compact {}
```

- **Block**: standalone component or meaningful UI unit.
- **Element**: a part that belongs to that block.
- **Modifier**: a stable variation of a block or element.

Prefer lowercase kebab-case inside each BEM segment.

## State classes

Runtime state is separate from structural naming:

```css
.menu {}
.menu.is-open {}
.accordion__panel.is-hidden {}
```

Use `.is-*` (or the repository's existing state convention) for transient state toggled by JavaScript. Do not create `.menu--open` if `open` is only runtime state and the project already distinguishes state classes.

## Boundaries

Avoid chaining unrelated blocks into fragile selectors:

```css
/* Avoid */
.hero .card .card__title span {}

/* Prefer */
.card__title-emphasis {}
```

A nested block keeps its own namespace. Do not rename a reusable `button` into `hero__button` merely because it appears inside the hero; use the reusable button class plus a hero-specific class only when page composition needs it.

## Common mistakes

- `green_title`: describes appearance, uses snake_case, and is hard to evolve.
- `header__nav__link`: BEM elements do not form an ancestry chain. Prefer `header__link`.
- `card-title`: ambiguous if the codebase uses BEM. Prefer `card__title`.
- `card--active` for temporary JavaScript state when `.is-active` is the established convention.
- Creating a modifier for every single CSS difference instead of a meaningful component variant.
