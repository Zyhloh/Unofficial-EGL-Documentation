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

_Example Response (shape from client, `EngineAgreement`)_

```json
{
  "key": "unreal_engine2",
  "version": 3,
  "title": "Unreal Engine End User License Agreement",
  "body": "<EULA.Header>...</>"
}
```

`body` is Unreal Slate rich text (`<EULA.Header>`, `</>`, `<a href="...">`, `\n`). The launcher converts it to a small HTML subset and runs it through DOMPurify before showing it. What the service returns once the account is up to date was not captured.
