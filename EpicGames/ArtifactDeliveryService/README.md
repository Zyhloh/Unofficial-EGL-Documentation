# Hosts

This are some (not all) Hosts that you can access the Artifact Delivery Service (build CDN) from

- epicgames-download1.akamaized.net
- egdownload.fastly-edge.com
- content-download-egs.distro.on.epicgames.com

<br/>

Recommended Hosts:

- Whatever [Get Asset (v2)](../LauncherService/Assets/GetAssetV2.md) returns in `manifests[].uri` / `cdnBaseUrls`

<br/>

Game build hosts are not hardcoded in the launcher: manifest URLs and CDN base URLs come from the assets response and are tried in order (mirror fallback). `epicgames-download1.akamaized.net` and `egdownload.fastly-edge.com` are the only download hosts named in the binary (the Fab download redirect allow-list) and `epicgames-download1.akamaized.net` is where the [Linux Manifest](../LauncherService/Installer/LinuxManifest.md) redirects. `content-download-egs.distro.on.epicgames.com` serves the launcher's own files under `/Builds/EGLv2/` (`stable-target.json`, Fortnite deployment registry).
