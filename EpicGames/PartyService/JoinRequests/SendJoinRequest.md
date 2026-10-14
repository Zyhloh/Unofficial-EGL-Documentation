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

No body. The parsed response is returned to the intent caller unchanged.
