## Party Service - Invites: Send Party Invite

Invites a friend to the caller's current party (`send-party-invite`, `send-bulk-party-invite`, second half of `create-and-send-*`).

URL: https://api.epicgames.dev/epic/party/internal/v2/users/:accountId/invites/:inviterId \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4, kept as the invite `correlationId` <br/>

## Path Parameters
`accountId`: Invitee account id <br/>
`inviterId`: The signed-in account id <br/>

## Query Parameters
`auto`: `true` for auto-invites, else `false` <br/>

No body.

---

_Example Response (shape from client)_

```json
{
  "sent_by": "94b1569506b04f9f8557af611e8c5e47",
  "sent_to": "1b8b8b2f4f3a4e6c9d0e5a7f2c4b6d81",
  "party_id": "a3f6c2d1e9b84f7a8c5d0e1f2a3b4c5d",
  "expires_at": "2026-10-15T16:00:00.000Z"
}
```
