---
name: developing-vanilla-web-interfaces
description: Use when creating, modifying, reviewing, or refactoring framework-free web interfaces built with HTML, CSS, and vanilla JavaScript, especially when BEM naming, design tokens, reusable components, responsive behavior, accessibility, or CSS architecture must stay consistent.
---

# Developing Vanilla Web Interfaces

## Core principle

Preserve the project's existing architecture first. Build semantic, accessible interfaces with the smallest reusable structure that removes real duplication. Do not introduce a framework, design system, abstraction, or naming convention that conflicts with the repository unless the task explicitly requires it.

## Before changing code

Inspect the repository instructions and nearby implementation before deciding how to build the change:

1. Read `AGENTS.md`, `CLAUDE.md`, or equivalent project instructions when present.
2. Find existing design tokens, global styles, components, page styles, breakpoints, and JavaScript conventions.
3. Find the closest existing UI pattern and extend it instead of creating a parallel convention.
4. Identify whether the change is reusable across pages or specific to one page.

## Implementation contract

### HTML

- Prefer semantic elements (`header`, `nav`, `main`, `section`, `article`, `footer`, `button`, `form`) over generic containers.
- Keep heading hierarchy meaningful.
- Use native interactive elements before recreating their behavior with JavaScript.
- Keep markup readable and avoid wrappers that exist only without a layout or semantic purpose.

### CSS

- Use the project's tokens for colors, spacing, typography, radii, shadows, transitions, and layout values before adding literals.
- When BEM is the project convention, use `block`, `block__element`, and `block--modifier` consistently. Use state classes such as `.is-open` for transient behavior rather than encoding state as a BEM modifier.
- Put reusable component styling with components and page-specific composition with page styles.
- Prefer the repository's established breakpoints and responsive strategy.
- Avoid high-specificity selectors, deep descendant chains, `!important`, and duplicated declarations unless an existing constraint requires them.

### Components

- Reuse an existing component when its semantics and behavior match.
- Extract a new reusable component when a pattern is repeated or clearly shared and has a stable responsibility.
- Keep one-off page composition local; do not abstract only to reduce a few lines.
- If the project already uses Web Components or custom elements, follow that pattern for shared markup/behavior. Do not introduce them solely because this skill mentions them.

### JavaScript

- Keep JavaScript focused on behavior and state, not duplicated presentation rules.
- Scope DOM queries and event handling to the component when possible.
- Preserve keyboard behavior, focus management, and native semantics for interactive UI.
- Prefer small explicit modules over global mutable state.

## Quality gate

Before considering frontend work complete, verify:

- the new code follows existing repository conventions;
- reusable patterns were reused rather than duplicated;
- BEM/state naming is coherent where applicable;
- visual values use existing tokens where appropriate;
- the layout behaves at the project's relevant viewport ranges;
- keyboard interaction and visible focus still work;
- images and controls have appropriate accessible text;
- no unnecessary framework, dependency, or abstraction was added.

## References

Read only the references relevant to the task:

- `references/bem.md` — BEM naming, state classes, and common naming mistakes.
- `references/css-architecture.md` — tokens, global/component/page style boundaries, responsive CSS.
- `references/components.md` — deciding when and how to reuse or extract Vanilla Web components.
- `references/accessibility.md` — practical semantic, keyboard, form, focus, and media checks.
