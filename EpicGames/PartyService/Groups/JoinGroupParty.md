## Party Service - Groups: Join Group Party

Joins the current party of a group chat (`accept-group-party-invite`).

URL: https://api.epicgames.dev/epic/party/internal/v2/groups/:groupId/parties/current/join \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

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
    "id": "b1e2c3d4a5f60718293a4b5c6d7e8f90",
    "deployment_id": "d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f",
    "meta": {
      "osName": "Windows",
      "platformName": "egs",
      "productName": "Epic Games Launcher"
    }
  }
}
```

---

_Example Response (shape from client)_

```json
{
  "party_id": "a3f6c2d1e9b84f7a8c5d0e1f2a3b4c5d"
}
```
