## Avatar Service - Avatars: Group Assignments

Avatars of the members of group chats.

URL: https://api.epicgames.dev/epic/avatar/v1/:deploymentId/assignments/groups \
Method: GET \
Auth Required: Yes (Bearer EG1 access token)

## Headers
`X-Epic-Agent`: `epic-social` <br/>

## Path Parameters
`deploymentId`: Avatars deployment, `9c9906b240c74a92a6b9100d6e4ccbd0`

## Query Parameters
`conversationId`: Comma-separated group conversation ids ([Chat](../../ChatService)) <br/>
`accountId`: Optional, comma-separated member account ids

---

_Example Response (unknown conversation)_

```json
{
  "assignments": [],
  "failedAccountIds": []
}
```

Entries in `assignments` have the same shape as in [Friends Assignments](FriendsAssignments.md).
