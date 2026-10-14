## Party Service - Join Requests: Decline Join Request

Rejects a received join request (`decline-join-party-request`).

URL: https://api.epicgames.dev/epic/party/internal/v2/users/:accountId/joinRequests/:requesterId \
Method: DELETE \
Auth Required: Yes (Bearer elevated EG1 access token, from `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`accountId`: The signed-in account id <br/>
`requesterId`: Account id that requested to join <br/>

No body.
