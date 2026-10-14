## Chat Service - Users: Get Conversations Summary

Unread counters for the badge. Requested when text chat is enabled and after deleted messages. Intent `get-conversations-summary-intent`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/users/:accountId/summary \
Method: GET \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>
`accountId`: Your account id <br/>

---

_Example Response_

```json
{
  "conversationCount": 1,
  "unreadMessages": 1,
  "unreadPendingInvites": 0,
  "hasMoreUnreadMessages": false,
  "hasMoreUnreadPendingInvites": false
}
```

With no conversations every counter is `0`.
