## Avatar Service - Avatars: Friends Assignments

Avatars of the signed-in account's friends.

URL: https://api.epicgames.dev/epic/avatar/v1/:deploymentId/assignments/friends \
Method: GET \
Auth Required: Yes (Bearer EG1 access token)

## Headers
`X-Epic-Agent`: `epic-social` <br/>

## Path Parameters
`deploymentId`: Avatars deployment, `9c9906b240c74a92a6b9100d6e4ccbd0`

## Query Parameters
`accountId`: Optional, comma-separated friend account ids. Without it every friend is returned (18 of 18 in a live test)

---

_Example Response (shortened)_

```json
{
  "assignments": [
    {
      "accountId": "94b1569506b04f9f8557af611e8c5e47",
      "avatar": {
        "avatarId": "AthenaCharacter:cid_defaultoutfit[2,13]",
        "url": "https://cosmo.fdeb.live.use1a.on.epicgames.com/cdn-cgi/image/height={},format=png/v1/item/WER5RlAYhxo-8yifvRDInC-Q2XrexQd5yOUDL4gAPA4/png"
      }
    }
  ]
}
```
