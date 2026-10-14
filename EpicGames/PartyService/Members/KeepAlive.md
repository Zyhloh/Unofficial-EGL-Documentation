## Party Service - Members: Keep Alive

Revives the signed-in member after the service marked it `suspended`. Not on a timer: the party chat panel fires `party-keep-alive-request` whenever the local member of the active party has `suspended: true` (set from `party.v2.MEMBER_DISCONNECTED` / `MEMBER_STATE_UPDATED`).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId/members/:accountId/keep-alive \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>
`accountId`: The signed-in account id <br/>

No body. The parsed response is not read by the overlay. Also accepted while the member is not suspended (captured on a fresh solo party).

---

_Example Response_

```json
{
  "account_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "meta": {},
  "revision": 0,
  "updated_at": "2026-10-14T17:57:26.758Z",
  "joined_at": "2026-10-14T17:57:26.758Z",
  "suspended": false
}
```

The member object without `connections`.
