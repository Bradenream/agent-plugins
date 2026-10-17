# Shared installation and verification

## Prepare one installation

Search the site's layouts, code-injection fields, tag manager, installed plugins,
and app embeds for `voiceflow`, `chat.load`, and the widget script URL. Identify
which location owns the existing install before adding another. Keep a copy or
diff of the settings/source you will change for rollback.

Get the project-specific snippet using [widget tools](tools.md). Preserve its
verification and runtime fields. A target environment must have the version
the snippet requests; saved draft settings are not evidence of live settings.
Do not publish simply to make a preview test pass.

Use one loader and one active widget per document. Install in the shared layout
for site-wide support, or scope it to requested pages. Treat a sandboxed HTML
embed/iframe as a different document, not a way to install a site-wide floating
launcher. Respect the site's existing consent and script-loading policy.

For an embedded panel, establish its target DOM element and responsive dimensions
before initialization. Use the current supported render options. On a client-
routed site, decide whether the widget persists across routes or belongs to a
page that must mount/unmount it; do not mix those ownership models.

## When the user must paste the code

Do as much as the host can do first. Return the actual snippet, fully populated
with observed values, followed by one short sequence for the chosen platform:
where to open settings, which field, selected pages, save/activation effect,
and the URL to check. If the snippet cannot be retrieved, direct the user to
Voiceflow's Widget tab and state what information remains missing.

Do not give eight platform guides or ask for a terminal when the user only
needs one paste. After they save, resume verification if browser access exists.
Otherwise give these concrete self-checks; do not claim to have observed them.

## Verify the browser, not just the setting

Use the actual preview or authorized live URL, outside the editor when it
suppresses scripts. Record the URL, target environment/version, and checks done.

1. **Mount:** one launcher/panel, correct site/page scope and brand. The script
   and settings requests succeed; no relevant console error. Check narrow/mobile
   width, keyboard access, and overlap with fixed UI.
2. **Conversation:** open the widget and send a harmless test message when
   authorized. Observe a real response from the intended agent. Do not trigger
   bookings, payments, emails, or other external actions as a smoke test.
3. **Lifecycle:** navigate to another included page, an excluded page if any,
   use Back, and reload. Check for duplicate launchers, missing targets, and
   unwanted conversation resets. Test expected persistence in a fresh session.
4. **Customization:** verify the requested color/copy/CSS and any custom opener,
   embedded layout, voice, or visitor context actually requested. Account for
   local overrides before assuming the remote patch failed.

Do not mistake HTTP 200, a snippet response, or a screenshot of a launcher for
proof of a working conversation. If testing would exceed authorization, report
the configuration/install checks and leave the runtime check explicitly pending.

## Rollback and handoff

Remove or disable only this integration's loader and local customization,
retaining unrelated site code. Restore the previous settings if needed. A
remote draft rollback still needs an authorized publish to change production.
For a source-based site, provide the file/diff; for a builder, name the code
entry. End with the observed status and the smallest remaining action.

Source: [Voiceflow installation](https://www.voiceflow.com/docs/documentation/deploy/widget/embedding-the-chat-widget).
