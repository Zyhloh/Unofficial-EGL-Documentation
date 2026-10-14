## Party Service - Groups: Join Group Party

Joins the current party of a group chat (`accept-group-party-invite`).

URL: https://api.epicgames.dev/epic/party/internal/v2/groups/:groupId/parties/current/join \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: the invite correlation id or random UUID v4 <br/>

## Path Parameters
`groupId`: Group chat id <br/>

## Query Parameters
`joinerId`: The signed-in account id <br/>

## Body
```json
{
  "connection": {
    "id": "3a9c51fffe7d2e48-00000001-0007c2d4-5b1e9f0a7c3d2b6e-4f8a1c2d",
    "deployment_id": "_",
    "meta": {
      "osName": "Windows",
      "platformName": "egs",
      "productName": "Epic Games Launcher"
    }
  }
}
```

Body not captured; `connection` is built by the same code as [Create Party](../Parties/CreateParty.md) `join_info.connection`, which EGL was captured sending with `deployment_id: "_"`.

---

_Example Response (shape from client)_

```json
{
  "party_id": "2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f"
}
```
