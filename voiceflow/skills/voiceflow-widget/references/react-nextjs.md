# React and Next.js

Use the [shared installation checks](installation.md). Keep the actual generated
configuration; adapt the loader to the app's existing script lifecycle rather
than pasting script tags into a component's returned markup.

## Choose one lifecycle owner

For a persistent floating widget, mount one client-side owner in the shared app
shell/layout. Load the SDK once and initialize the widget once for that owner.
Separate **SDK available** from **widget mounted**: `window.voiceflow` can still
exist after `destroy()` or after an embedded target disappeared.

For page-owned embedded chat, initialize only after its target mounts and call
`destroy()` when that owner really unmounts. Dispose owned listeners. Prevent a
late script-load callback from initializing against an unmounted target. If a
new owner appears while loading, it must still be able to initialize. Do not
destroy a shared widget from a child page's cleanup.

React development Strict Mode deliberately repeats setup/cleanup. Exercise
that cycle; do not turn Strict Mode off or use a permanent guard that suppresses
the second mount after the first cleanup destroyed the widget. Avoid depending
on a freshly allocated configuration object that retriggers setup every render.

## Next.js

Use a Client Component for browser API access and script callbacks. A suitable
shared layout can include that component without becoming a client-only app.
`next/script` provides loading strategies; `afterInteractive` suits a readily
available launcher, while `lazyOnload` deliberately delays it. Respect the
existing site's choice rather than adding a second loader.

An inline `Script` needs a stable `id`. With an external script, remember that
`onReady` runs again on component mounts; SDK script deduplication does not
deduplicate `chat.load()` calls. A reused SDK still needs initialization after
an intentional widget teardown. Keep credentials out of public environment
variables and serialized props; only the generated browser verification belongs
in client code.

## Customize and check

Keep brand overrides beside this one configuration; use
[customization](customization.md) for remote settings and supported CSS. A custom
support button should invoke the existing ready widget, not mount another one.

Test a cold deep link, development remount, production build, route changes,
Back, and a slow SDK load followed by navigation. Confirm one widget and expected
conversation persistence. For authenticated sites, also check logout/account
switch without leaking the previous conversation. Roll back the integration
component and its imports/listeners, retaining unrelated layout code.

Sources: [React effects](https://react.dev/reference/react/useEffect),
[Next.js scripts](https://nextjs.org/docs/app/guides/scripts).
