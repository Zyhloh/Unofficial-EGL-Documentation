## Fab - Pages: EGL Plugin

Fab web app loaded into the `fab-webview` (`fab_create_webview`). The launcher injects `window.ue.fab` (Fab bridge) so the page can drive downloads, exports and DCC plugins through the `fab_egl_*` / `fab_ue_*` commands. See [IPC Store and Fab](../../../../Launcher/IPC/StoreFab.md).

URL: https://www.fab.com/plugins/egl \
Method: GET \
Auth Required: Yes (signed in through the injected bridge)

Related static file: `https://quixel-megascans-static.s3.us-west-2.amazonaws.com/fab/manifest/prod/plugins_v1.json` (DCC plugin catalogue: `plugins.<name>.windows|mac.{version, downloadUrl, port, installationWorkflowVersion, normalMapConvention, supportedFormats, supportedVersions}`). Fab's in-page legacy checkout uses `fab.com/payment/web/purchase?offers=...`.
