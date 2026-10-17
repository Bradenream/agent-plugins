# Webflow

Use the [shared checks](installation.md). Inspect site-wide code, page code,
and existing embeds for an earlier Voiceflow installation.

1. Open **Site settings → Custom code → Footer code** for a site-wide launcher.
   For selected pages, use **Page settings → Custom code → Before `</body>`**
   instead; do not install in both.
2. Add the complete generated snippet alongside existing code. Save changes.
   Custom code requires an eligible plan and editing role; check the actual
   account if the controls are missing.
3. Preview, then publish to the intended domain when authorized. Saving custom
   code does not itself publish the website. Test the visitor URL; expand-canvas
   view does not execute this code.

For embedded chat, place a target element in the intended design and initialize
after it exists; use current Voiceflow render options. For branding, change
remote settings or the single load configuration using
[customization](customization.md). The page's typography/CSS need not reach the
widget's internals.

Verify the home page, a CMS/detail page if included, and mobile. Check that page
code did not duplicate the site-level installation. Remove only this snippet
and publish the site change when authorized to roll back.

Source: [Webflow custom code](https://help.webflow.com/hc/en-us/articles/33961357265299-Custom-code-in-head-and-body-tags).
