## Party Service - Parties: Update Party Config

Changes party privacy (`update-party-config`, Open / Invite only toggle).

URL: https://api.epicgames.dev/epic/party/internal/v2/parties/:partyId \
Method: PATCH \
Auth Required: Yes (Bearer EG1 access token, any client; the overlay uses `window.ue.common.getsignedinuser().accesstoken`)

## Headers
`Content-Type`: application/json <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`partyId`: The party id <br/>

## Body
```json
{
  "config": {
    "joinability": "INVITE_ONLY"
  },
  "revision": 1
}
```

`config` is the client's config object with `joinability` replaced, `revision` the party revision. Only the status is checked.
