# Accessibility checks for Vanilla Web interfaces

Treat accessibility as part of implementation, not a later visual audit.

## Semantics

- Use `<button>` for actions and `<a href>` for navigation.
- Use landmarks such as `<header>`, `<nav>`, `<main>`, and `<footer>` where they match the content.
- Keep heading levels logical and descriptive.
- Associate every form control with a visible label or an appropriate accessible name.

## Keyboard and focus

- Every interactive feature must be operable without a mouse.
- Preserve visible focus indicators; do not remove `outline` without an accessible replacement.
- When opening overlays/drawers, keep focus behavior understandable and expose expanded state when relevant.
- Escape-to-close and focus trapping are appropriate for modal dialogs; do not apply modal behavior to ordinary inline regions.

## ARIA

Prefer native semantics. Add ARIA only when it communicates state or relationships the native element does not already provide. Keep values synchronized with JavaScript state.

Examples include `aria-expanded`, `aria-controls`, `aria-current`, and dialog labeling.

## Images and icons

- Informative images need concise `alt` text.
- Decorative images should generally use empty `alt=""` when rendered with `<img>`.
- A control whose icon is decorative still needs an accessible name on the control.
- Avoid duplicating the same accessible name in both the control and nested image alt text.

## Motion and responsive UI

Respect `prefers-reduced-motion` for non-essential motion when animations are substantial. Verify that zoom, narrower viewports, and longer text do not hide controls or make content unreachable.

## Forms

Communicate errors in text, associate them with the field when possible, and do not rely on color alone. Keep validation messages specific enough for the user to correct the input.
