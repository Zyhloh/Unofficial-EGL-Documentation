## Party Service - Join Requests: Send Join Request

Asks a friend's party to let the caller in (`send-join-party-request`).

URL: https://api.epicgames.dev/epic/party/internal/v2/users/:accountId/joinRequests/:requesterId \
Method: POST \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: Friend account id <br/>
`requesterId`: The signed-in account id <br/>

## Query Parameters
`auto`: `true` for automatic requests, else `false` <br/>

No body. The parsed response is returned to the intent caller unchanged. Requests expire after one hour.

`party.v2.JOIN_REQUEST_CREATED` is pushed (captured on the requester's own connection; the requestee is notified as well, EGL showed the request). There is no separate accept route: the leader accepts by sending a normal [party invite](../Invites/SendInvite.md) to the requester. That consumes the request (`party.v2.JOIN_REQUEST_EXPIRED`), the requester gets `party.v2.INVITE_CREATED` and then calls [Join Party](../Members/JoinParty.md). Rejecting is [Decline Join Request](DeclineJoinRequest.md). Flow confirmed live with EGL as the leader (2026-10-14).

---

_Example Response_

```json
{
  "requester_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
  "requester_dn": "ExampleAlt",
  "requester_pl": "",
  "requester_pl_dn": "",
  "requestee_id": "94b1569506b04f9f8557af611e8c5e47",
  "sent_at": "2026-10-14T18:05:34.267Z",
  "expires_at": "2026-10-14T19:05:34.267Z",
  "auto": false
}
```

`requester_pl` / `requester_pl_dn`: empty for an EGL requester (inferred: platform and platform display name).

_Example `party.v2.JOIN_REQUEST_CREATED`_

```json
{
  "correlationId": "819d89cd-3e8c-47a9-a28a-4b39e2ca6895",
  "timestamp": 1792001134282,
  "id": "ZWYxYzllMzE2MWM1YTFmOQ",
  "connectionId": "6b4e20fffe8a1d57-00000001-05a3e9c1-7d2f4b6a8c0e1f35-2c9a7e4b",
  "payload": {
    "sent": "2026-10-14T18:05:34.267Z",
    "requester_id": "c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60",
    "requester_dn": "ExampleAlt",
    "requestee_id": "94b1569506b04f9f8557af611e8c5e47",
    "sent_at": "2026-10-14T18:05:34.267Z",
    "expires_at": "2026-10-14T19:05:34.267Z",
    "auto": false
  },
  "type": "party.v2.JOIN_REQUEST_CREATED"
}
```

`party.v2.JOIN_REQUEST_EXPIRED` has the identical payload. Captured order on the requester's connection after the leader accepted: `JOIN_REQUEST_EXPIRED`, `INVITE_CREATED` (inviter = the leader), then after Join Party `INVITE_EXPIRED`, `MEMBER_JOINED`.
