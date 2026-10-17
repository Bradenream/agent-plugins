# Plain HTML, static sites, and Astro

Use the [shared installation checks](installation.md). For a conventional
multi-page site, put the returned script in the shared footer/layout before
`</body>`, once per document. If there is no shared layout, add it only to the
requested pages. Do not add it both to a template and a tag manager.

For a floating widget, the generated snippet is the starting point. For embedded
chat, create the target on each intended page before loading the widget and use
the current supported render options. Preserve responsive container dimensions.

## Astro

Inspect whether the site uses ordinary full-page navigation or `ClientRouter`.
Keep the snippet in the relevant layout. If preserving a generated inline
snippet, use Astro's `is:inline` handling deliberately; don't accidentally let
the build transform it into a second, differently owned loader.

With client-side navigation, a previously loaded script does not guarantee that
the widget's DOM survived the page swap. Use the documented navigation lifecycle
to reconcile widget ownership: either persist the mounted integration or destroy
and remount it against the new target. A simple permanent `loaded = true` guard
can leave a missing widget after a swap. Do not reinitialize on every navigation
without checking whether the existing widget is still mounted.

Put browser-only calls in browser scripts, not server frontmatter. Keep
site-specific branding in one load configuration; use [customization](customization.md)
for CSS and remote settings.

Verify a direct deep link, navigation, Back, and reload in the built preview;
inspect for duplicates or a missing widget after a swap. Remove the layout
entry and its owned listeners to roll back.

Sources: [Astro scripts](https://docs.astro.build/en/guides/client-side-scripts/),
[Astro navigation lifecycle](https://docs.astro.build/en/guides/view-transitions/).
