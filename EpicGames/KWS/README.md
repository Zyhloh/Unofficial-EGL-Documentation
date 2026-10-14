# Hosts

This are some (not all) Hosts that you can access the KWS (K3S settings) Service from

- api.kws.ol.epicgames.com

<br/>

Recommended Hosts:

- api.kws.ol.epicgames.com

Plain EG1 bearer token from any client.

| Method | Path | Page |
| --- | --- | --- |
| GET | `/v1/epic-settings/public/users/:accountId/values` | [Get Setting Values](Settings/GetValues.md) |
| PATCH | `/v1/epic-settings/public/users/:accountId/values` | [Update Setting Values](Settings/UpdateValues.md) (incl. voice reporting toggle) |

Realtime changes: `k3s.v1.PARENT_LIMITS_CHANGED` and `k3s.v1.EFFECTIVE_VALUES_CHANGED` over [Epic Connect](../../Launcher/Social/Connect.md) (only applied when `productIds` contains `prod-fn`). Parental controls page: `https://accounts.epicgames.com/account/parental-controls`.
