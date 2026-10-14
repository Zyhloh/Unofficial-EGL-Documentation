## Launcher Service - Installer: Linux Manifest

Pinned Proton runtime and Linux installer metadata. Fetched by the Linux build before running Windows games through Proton (`install_proton_runtime`, `proton-runtime-required-event`); the launcher can override the pin with `EGL_PROTON_PIN`.

URL: https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/linux-manifest.txt \
Method: GET \
Auth Required: No

Responds `303 See Other` to a versioned file on `epicgames-download1.akamaized.net`, e.g. `https://epicgames-download1.akamaized.net/Builds/UnrealEngineLauncher/Installers/Linux/linux-manifest-Prod-20.3.3.txt?launcherfilename=linux-manifest-Prod-20.3.3.txt`.

---

_Example Response_

`text/plain`, `key=value` lines (captured 2026-10-14):

```
# Author-controlled fields. script_url/script_sha512/egl_installer_url/egl_installer_sha512
# are generated per-tier at publish time by EpicGamesLauncher_PromoteLinuxScript.
proton_version=GE-Proton10-34
proton_url=https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton10-34/GE-Proton10-34.tar.gz
proton_sha512=9fd0b2cfbd501c0b5c892239c392c7283a029b5e5d5a77d3f85b0ce190d555456241a18eebca16b53f094b403499201c13550a3f0b9b365e1a5eb5737cbb7303

script_url=https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/install_linux.sh
script_sha512=e1a2eb32d6de0feba3c04e7dd3c2694bbd84d5d76cce820ab4aaa002f0848bbaff7ccecbac6be20b406177dfd4c2bba993c22156e0560540e5ecaa19371a6056
egl_installer_url=https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.exe
egl_installer_sha512=0893e9d57fe0ce49f94449f5830adfa6b7e369a06db75e653815564331f8c168d5aa283dca4fcc6aff3d1eef22c76a2a3b1648778a094cd50d020d892ff1e1bb
```
