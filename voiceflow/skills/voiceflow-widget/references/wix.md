# Wix

Use the [shared checks](installation.md). For a floating launcher, use page-level
custom code in the site dashboard rather than an HTML Embed iframe that traps
the launcher inside a small rectangle.

1. Open the site's **Settings → Custom Code** under Development & integrations.
2. Choose **Add Custom Code**, paste the generated snippet, and name it
   **Voiceflow widget**.
3. Select all intended pages or specific pages. For a persistent site-wide
   launcher, start with loading once per visit, not a fresh loader on every page.
4. Set placement to **Body – end** and apply within the authorized launch scope.
   If the control is unavailable, check the account's custom-code eligibility,
   site/domain status, and editing role in the current Wix documentation.

Verify the visitor-facing site, then navigate between pages and Back. If page
scope/navigation changes remove the widget, fix lifecycle ownership instead of
installing a duplicate. For an intentionally embedded panel, establish whether
the chosen Wix element runs in its own document before deciding target/layout.

Use [customization](customization.md) for Voiceflow appearance; Wix element styling
does not establish the inner widget's styles. Check mobile overlap and the site's
existing consent category for this code. To roll back, disable/remove the named
custom-code entry and verify it no longer loads.

Source: [Wix custom code](https://support.wix.com/en/article/embedding-custom-code-on-your-site).
