## EULA Tracking Service - Agreements: Get Agreement For Account

Returns the agreement the account still has to accept. EGL v2 calls it from the EULA gate before installs / launches (`eglv2_lib::eula_gate`), for engine / tool entitlements (`acquire_engine_entitlement`, `acquire_tool_entitlement`) and for the EULA ids on catalog items. A pending agreement becomes an `eula-prompt-event` and is answered with `accept_eula` / `dismiss_eula`. Keys seen in a live log: `epicgames_tos`, `egstore`, `unreal_engine2`, `twin2`.

URL: https://eulatracking-public-service-prod06.ol.epicgames.com/eulatracking/api/public/agreements/:key/account/:accountId \
Method: GET \
Auth Required: Yes (Bearer access token)

## Path Parameters
`key`: Agreement key, e.g. `epicgames_tos` <br/>
`accountId`: The account id

## Query Parameters
`locale`: Body language, e.g. `en` <br/>

---

_Example Response (pending agreement, `body` shortened)_

```json
{
  "key": "uefn",
  "version": 12,
  "revision": 5,
  "title": "Unreal Editor for Fortnite Supplemental Terms to the Epic Games Terms of Service",
  "body": "<EULA.Header>1.\tIntroduction.</>\n\nUnreal Editor for Fortnite (“<EULA.Highlight>UEFN</>”) is a creation tool ...",
  "locale": "en",
  "createdTimestamp": "2026-02-27T00:03:11.840Z",
  "lastModifiedTimestamp": "2026-02-27T00:03:11.840Z",
  "status": "ACTIVE",
  "description": "EULA for Unreal Editor for Fortnite",
  "custom": false,
  "url": "https://...",
  "bodyFormat": "HTML",
  "wasDeclined": false,
  "hasResponse": false
}
```

Keys the launcher checks (0.115 logs): `epicgames_tos`, `egstore`, `emporium` (Epic Marketplace Content License Agreement, version 4) and `uefn` (UEFN supplemental terms, version 12). An account that never used the Fab / Unreal side still has `emporium` and `uefn` pending. Only `key`, `version`, `title` and `body` are read by the launcher (`EngineAgreement`).

`body` is Unreal Slate rich text (`<EULA.Header>`, `</>`, `<a href="...">`, `\n`). The launcher converts it to a small HTML subset and runs it through DOMPurify before showing it.

When nothing is pending for the key the service returns `204 No Content` with an empty body (live for `epicgames_tos` and `egstore`).
