# Hosts

This are some (not all) Hosts that you can access the Entitlement Service from

- entitlement-public-service-prod08.ol.epicgames.com
- entitlement-public-service-gamedev.ol.epicgames.net

<br/>

Recommended Hosts:

- entitlement-public-service-prod08.ol.epicgames.com

<br/>

Both hosts are in the launcher's environment table (`entitlement` key), but no `/entitlement/api/...` path is present in the 0.95.1 binary. Ownership checks after a purchase or free-entitlement acquire (`src\entitlement.rs`: "Product entitlement confirmed in library", `Entitlement.NotYetVisible`) are done by re-reading the library ([Library Items](../LibraryService/Library/Items.md)), not by calling this service.
