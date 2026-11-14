## Avatar Service - Avatars: Party Assignments

Avatars of the members of a party.

URL: https://api.epicgames.dev/epic/avatar/v1/:deploymentId/assignments/party/:partyId \
Method: GET \
Auth Required: Yes (Bearer EG1 access token)

## Headers
`X-Epic-Agent`: `epic-social` <br/>

## Path Parameters
`deploymentId`: Avatars deployment, `9c9906b240c74a92a6b9100d6e4ccbd0` <br/>
`partyId`: Party id ([Party V2](../../PartyService/V2))

## Query Parameters
`accountId`: Optional, comma-separated member account ids

---

_Example Response (unknown party)_

```json
{
  "assignments": [],
  "failedAccountIds": []
}
```

Entries in `assignments` have the same shape as in [Friends Assignments](FriendsAssignments.md). `failedAccountIds` lists members whose avatar could not be resolved.
