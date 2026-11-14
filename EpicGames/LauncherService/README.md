# Hosts

This are some (not all) Hosts that you can access the Launcher Service from

- launcher-public-service-prod06.ol.epicgames.com
- launcher-public-service-gamedev.aeee.dev.use1a.on.epicgames.com

<br/>

Recommended Hosts:

- launcher-public-service-prod06.ol.epicgames.com

The prod host answers through Cloudflare (`server: cloudflare`, `cf-ray`). A quick burst of requests (about 15 [Get Asset (v2)](Assets/GetAssetV2.md) calls within a few seconds) got a `530` HTML challenge page instead of JSON; it cleared within a minute, and requests a few seconds apart were fine. The User-Agent made no difference.
