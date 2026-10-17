# Customize without creating a second source of truth

Read current widget settings and the site's existing `chat.load()` options.
Choose the smallest supported layer that owns the requested change.

| Need | Preferred layer |
| --- | --- |
| Shared brand, title, icons, launcher, interface, placeholder | Saved Voiceflow widget settings, using CLI/MCP or Widget UI |
| Appearance that intentionally differs on one site/page | Documented browser `assistant` overrides |
| Open from a site button, persistence, visitor context | Browser widget API |
| Styling beyond supported settings | `assistant.stylesheet` and documented CSS classes |
| Custom cards/forms/actions inside chat | Widget extensions; read the current extension guide first |

The settings API uses `chat`, `voice`, `common`, and `security`; browser options
use a different shape. Read [merge rules](tools.md#patch-only-the-intended-settings)
before patching. Browser overrides take priority over published settings, so a
stale local override can hide a successful remote update. Prefer shared settings
unless the user wants a site-specific difference.

## Match the site

Inspect the site's actual colors, typography, assets, and mobile layout. Choose
launcher placement that does not cover navigation, a cart control, or an existing
consent banner. Check text contrast and focus visibility. Reuse a public image
URL or the site's asset pipeline; a local filesystem path will not load for
visitors. Do not hide Voiceflow branding or disable restrictions to work around
an entitlement error.

For site-specific customization, merge a fragment like this into the **existing**
load options; it is not a complete snippet:

```js
assistant: {
  color: '#245D58',
  side: 'right',
  spacing: { side: '24', bottom: '24' }
}
```

These spacing values are pixel counts encoded as strings, without `px`.
Keep unrelated options. For exact palette, header/banner, launcher, or font
fields, read the current [customization reference](https://www.voiceflow.com/docs/documentation/deploy/widget/custom-web-chat-styling).

## Floating, popover, or embedded

Use a floating launcher for ordinary site-wide support unless the user chose a
different presentation. Embedded chat needs a real, mounted target with usable
height and width. Get the current render configuration from Voiceflow's snippet
or docs; do not guess an iframe URL or turn a floating widget into an embedded
one by shrinking its parent. An embedded target must survive or be remounted
correctly during client-side navigation. Overlay `open()`/`close()` methods do
not control embedded mode.

For a custom site button, initialize the widget first and then call
`window.voiceflow.chat.open()` from that button's interaction. Do not insert a
second widget or call `load()` on every click. Account for a user clicking
before the SDK is ready; keep one initialization path and a visible failure
state if loading fails. Do not auto-open the conversation on every page visit
unless requested.

## Persistence and visitor context

Choose session behavior deliberately. Follow the current
[widget API](https://www.voiceflow.com/docs/documentation/deploy/widget/web-chat-api)
for `assistant.persistence`, `userID`, `launch.event.payload`, and `user` metadata.
Browser identity is user-controlled; it is not proof of authorization to fetch
private records. Keep authorization checks server-side.

Launch payload values arrive in `last_event`; they do not automatically assign
arbitrary project variables. Capture needed values early into existing declared
variables. Transcript `user` metadata labels the conversation and is not input
to agent logic. On account switch/logout, verify the next person cannot inherit
the previous person's conversation. Do not reset every anonymous conversation
merely to fix a mounting bug.

## CSS and extensions

Prefer the documented `assistant.stylesheet` hook with a reachable HTTPS CSS
file and supported `.vfrc-` selectors. Page CSS may not reach widget internals;
avoid brittle generated class names. Test CSS in the widget itself on mobile
and desktop, including long responses, focus, and loading/error states.

For custom UI/actions, use [extensions](https://www.voiceflow.com/docs/documentation/deploy/widget/web-chat-extensions).
Do not enable `allowDangerousHTML` just to install or style the widget. Voice
and file uploads are optional capabilities with their own configuration and
usage effects; only enable them when requested and verify those features
separately.
