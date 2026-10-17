# Framer

Use the [shared checks](installation.md). Inspect existing custom-code entries
and components before adding a loader.

1. Open **Project Settings → Custom Code → Add Script** (or **+**).
2. Name the entry **Voiceflow widget**, paste the generated snippet, choose the
   body-end insertion position and the intended pages.
3. For a persistent floating widget, choose **Once** as the starting strategy.
   Do not use **Run on every page visit** to inject a second SDK/launcher.
4. Save and publish to the intended URL when authorized. Check in the browser;
   the canvas is not proof that custom code runs.

Test page navigation, not just the initial load. If the selected page scope or
site navigation removes the widget, reconcile its lifecycle rather than blindly
rerunning the loader. Page-owned embedded chat needs a mounted target and
teardown/remount handling; use the [React lifecycle guide](react-nextjs.md) for a
code component instead of assuming an Embed iframe controls the outer page.

Use remote Voiceflow settings for shared branding or a single site's load
overrides for differences; see [customization](customization.md). Verify mobile
spacing against Framer overlays and sticky controls. Disable/remove the named
entry or component to roll back, then deploy that change when authorized.

Source: [Framer custom code](https://www.framer.com/help/articles/how-to-add-custom-code/).
