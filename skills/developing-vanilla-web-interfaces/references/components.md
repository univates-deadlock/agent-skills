# Reusable components in Vanilla Web projects

Componentization is a tool for consistency, not a goal by itself.

## Reuse first

Before creating anything new, search for an existing component with the same semantic purpose. Prefer extending a compatible component over creating `card-v2`, `new-button`, or parallel markup.

## Extract when

A component is a strong candidate for extraction when several of these are true:

- it appears in multiple pages or repeated sections;
- it has a clear, stable responsibility;
- its markup and behavior should stay synchronized;
- it has meaningful variants rather than page-specific accidents;
- callers can use it without knowing its internal implementation.

Keep a one-off section local when extraction would only move markup to another file without creating a useful boundary.

## Web Components

If the project already uses custom elements, a shared element can encapsulate repeated markup and behavior:

```js
class SiteNotice extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <aside class="notice" role="status">
        <p class="notice__message"></p>
      </aside>
    `;
  }
}

customElements.define("site-notice", SiteNotice);
```

Do not introduce a custom element for static one-off markup or merely to imitate a framework component model.

## Behavior boundaries

- Query elements from the component root when possible.
- Attach listeners once and avoid hidden global side effects.
- Prefer native controls and events.
- Keep state names explicit (`is-open`, `is-expanded`) and synchronize relevant ARIA attributes such as `aria-expanded`.
- Clean up global listeners if the component can be disconnected and reconnected.

## Variants

Use a variant only when it represents a stable, named difference in component behavior or presentation. Page layout differences should usually be expressed by page composition rather than multiplying component modifiers.
