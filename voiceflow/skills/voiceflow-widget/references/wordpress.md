# WordPress and WordPress.com

Use the [shared checks](installation.md). Establish whether this is self-hosted
WordPress or WordPress.com, and inspect existing header/footer snippets, plugins,
theme code, and tag-manager installs first.

## Dashboard-only route

Reuse an existing trusted site-wide code-injection facility if one is installed.
Create one named **Voiceflow widget** entry in its footer/body-end HTML area;
paste the complete generated snippet, choose the intended pages, and save or
activate within the user's launch scope. Do not prescribe an unknown plugin or
ask a nontechnical user to edit PHP as the first step.

WordPress.com permits JavaScript on plugin-enabled plans with hosting features
activated. If code is stripped or the control is absent, check those capabilities
and the user's role. Do not claim a Custom HTML block will bypass restrictions.
If a new plugin is needed, explain that dependency before installing it.

## Source-managed route

Use the site's existing small integration plugin or child theme, with WordPress's
script-enqueue system. Avoid editing a parent theme that an update will replace.
If splitting the generated snippet into an external SDK and initialization code,
preserve script loading order and run `chat.load()` only after the SDK exists.
Do not enqueue the SDK and also paste its original loader.

Apply [customization](customization.md) through remote settings or this one
integration. Do not assume a page builder's CSS reaches widget internals.

Test logged out, on mobile, and on multiple page types. Check cache/minification
or delayed-JavaScript features if code differs from what was saved. Clear only
the relevant site cache when needed. Roll back the named entry or owned plugin/
child-theme change, preserving other snippets.

Sources: [WordPress.com code support](https://wordpress.com/support/code/),
[WordPress script enqueueing](https://developer.wordpress.org/reference/functions/wp_enqueue_script/).
