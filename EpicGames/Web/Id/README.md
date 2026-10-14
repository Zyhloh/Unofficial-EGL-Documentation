# Hosts

This are some (not all) Hosts that you can access the Epic Games Id (web sign-in) pages from

- www.epicgames.com (`prod`)
- epicgames-gamedev.ol.epicgames.net (`gamedev` / `ci`)

<br/>

Recommended Hosts:

- www.epicgames.com

These are browser pages, not APIs. eglv2 never renders them in a webview; it opens them in the system browser (`ShellExecuteW`). Paths come from the launcher's environment table (`website` base):

- [Authorize](Authorize.md) - `/id/authorize`
- [Register](Register.md) - `/id/register`
- [Exchange](Exchange.md) - `/id/exchange`
- [Link](Link.md) - `/id/link`

Other `www.epicgames.com` pages opened by `open_account_link` are listed in [Account Links](../../../Launcher/Auth/AccountLinks.md).
