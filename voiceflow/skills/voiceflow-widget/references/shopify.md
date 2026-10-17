# Shopify storefront

Use the [shared checks](installation.md). This guide covers an Online Store
theme. A headless React storefront uses the [React guide](react-nextjs.md).

1. Inspect theme code, app embeds, and tag-manager installs for Voiceflow.
   Keep one owner. If an existing integration is adequate, configure it.
2. Duplicate the theme for review when appropriate. In **Online Store → Themes**,
   open the intended theme's **Edit code** action, checking its name/live status.
3. Add the generated snippet once before the closing body tag in
   `layout/theme.liquid`, or place it in a named theme snippet rendered once
   there. Preserve `content_for_header`, `content_for_layout`, and other scripts.
4. Test the preview theme. Publishing that theme is a separate action from
   saving its code; edits to the live theme may take effect immediately.

Use [customization](customization.md) for brand, launcher spacing, or product-page
context. Serialize Liquid values safely into JavaScript; do not interpolate raw
customer strings or private tokens. A browser-provided customer ID is not proof
of identity for an order lookup.

Verify product, collection, and cart pages, including mobile cart drawers. Theme
installation does not establish checkout or customer-account coverage; those
surfaces have separate extension rules. Do not recommend legacy checkout script
injection. Roll back the named snippet/render call or integration entry, not the
entire theme and unrelated changes.

Sources: [Shopify theme editing](https://help.shopify.com/en/manual/online-store/themes/customizing-themes/edit-code/edit-theme-code),
[Theme layouts and checkout limits](https://shopify.dev/docs/storefronts/themes/architecture/layouts).
