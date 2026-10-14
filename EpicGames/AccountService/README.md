# Hosts

This are some (not all) Hosts that you can access the Account Service from

- account-public-service-prod03.ol.epicgames.com (`prod`)
- account-public-service-common-gamedev.ol.epicgames.net (`gamedev` / `ci`)

<br/>

Recommended Hosts:

- account-public-service-prod03.ol.epicgames.com

The launcher picks the host from its environment table (`account_service`), selected by `-epicenv` / the `environment` setting. Every call made by the launcher carries `User-Agent` and, on token requests, an optional `DPoP` proof (see [DPoP](../../Launcher/Auth/DPoP.md)). Clients are listed in [Clients](../../Launcher/Auth/Clients.md).

Endpoints used by eglv2:

- [OAuth/Token](OAuth/Token.md) - `POST /account/api/oauth/token`
- [OAuth/Exchange](OAuth/Exchange.md) - `GET /account/api/oauth/exchange`
- [Account/GetAccount](Account/GetAccount.md) - `GET /account/api/public/account/:accountId`
- [Account/ExternalAuths](Account/ExternalAuths.md) - `GET /account/api/public/account/:accountId/externalAuths`
