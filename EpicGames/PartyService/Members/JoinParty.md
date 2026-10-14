## Party Service - Members: Join Party

Joins a party (`accept-party-invite`, accepted join request, join from presence). The client leaves a different current party first, then calls [Get Party](../Parties/GetParty.md) with the returned id.

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/join \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: the invite correlation id when joining from an invite, else random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: The signed-in account id <br/>

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
