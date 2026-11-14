# Hosts

This are some (not all) Hosts that you can access the Deck (feature flag relay) from

- distro-gateway-prod.ol.epicgames.com (base path `/deck`)
- distro-gateway-private-gamedev.ol.epicgames.net
- distro-gateway-private-ci.ol.epicgames.net

<br/>

Recommended Hosts:

- distro-gateway-prod.ol.epicgames.com

Epic's server-side relay for the launcher's LaunchDarkly flags. The client sends the flag keys with their defaults and gets the served values back, without talking to LaunchDarkly itself. Launcher 0.115 uses it instead of the LaunchDarkly mobile SDK, see [Feature flags](../../Launcher/Architecture.md#feature-flags).

- [Evaluate Features](Features/Evaluate.md)
