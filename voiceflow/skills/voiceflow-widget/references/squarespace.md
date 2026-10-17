# Squarespace

Use the [shared checks](installation.md). Check Code Injection and page-level
blocks for an existing install before adding one.

1. Open the site's **Code Injection** panel. Availability depends on the site's
   plan; check the current help page/account rather than assuming all plans.
2. For a site-wide floating launcher, add the generated snippet to **Footer**,
   retaining existing code. This inserts it before the closing body tag.
3. Save within the user's launch scope; do not assume saving this panel creates
   an isolated draft. Check the visitor URL in a private/logged-out window.
4. For selected pages, use supported page-specific injection and verify scope.
   Do not also retain a site-wide install. Checkout pages do not support this
   custom-code route.

Use [customization](customization.md) for brand and launcher position. Do not
expect Squarespace's page CSS editor to control all widget internals; use the
documented Voiceflow stylesheet hook where needed.

Verify mobile and navigation between pages. Some editor views suppress scripts;
an empty editor preview is not proof of a failed install. A template using
client-side/Ajax navigation needs the same one-owner lifecycle check as other
client-routed sites. Roll back only this snippet and any owned customizations,
then check the visitor page again.

Source: [Squarespace Code Injection](https://support.squarespace.com/hc/en-us/articles/205815908-Customize-parts-of-your-site-with-code-injection).
