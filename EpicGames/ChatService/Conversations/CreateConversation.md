## Chat Service - Conversations: Create Conversation

Create a group chat and invite members. Intent `request-create-text-chat-conversation`.

URL: https://api.epicgames.dev/epic/chat/v1/public/:namespace/conversations \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>
`X-Epic-Agent`: epic-social <br/>
`X-EPIC-CORRELATION-ID`: random UUID v4 <br/>

## Path Parameters
`namespace`: Always `_` in the overlay <br/>

## Query Parameters
`invite`: `true` <br/>

## Body
`members` must include the requesting account.

```json
{
  "title": "Docs Test",
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "94b1569506b04f9f8557af611e8c5e47"],
  "type": "group"
}
```

---

_Example Response_

Only the creator is a member; every other account in `members` is invited and joins with [Update Invite Status](UpdateInviteStatus.md).

```json
{
  "conversationId": "07c0ExampleGroupId0001",
  "dateCreated": "2026-10-14T22:29:51.034Z",
  "isActive": true,
  "isReportable": false,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"],
  "invited": ["94b1569506b04f9f8557af611e8c5e47"]
}
```

_Example Error Response_ (400, requesting account missing from `members`)

```json
{
  "messageVars": [],
  "errorMessage": "Requesting account should be included in the members list",
  "errorCode": "errors.com.epicgames.bad_request",
  "correlationId": "5b8e2f1a-7c3d-4e6f-9a0b-1c2d3e4f5a6b",
  "numericErrorCode": 1001,
  "responseStatus": 400,
  "intent": "prod",
  "originatingService": "chat-service-api-prod"
}
```

Events (new group): the creator and every invited account receive `social.chat.v1.CONVERSATION_CREATED` and `NEW_INVITE`, followed by `REPORTABILITY_CHANGE` ([events](../README.md#realtime-events)). The history starts with `NEW_INVITE` and `REPORTABILITY_CHANGE` system entries.

### Existing group (dedup)

Creating a group whose account set (members + invited) equals an existing active group returns that group instead of a new one, with `isExisting: true`. The original title is kept; the new `title` is ignored. Any different account set creates a new group.

Request with title `Docs Report Test` and the same three accounts as an existing `Docs Reject Test` group:

```json
{
  "conversationId": "07c0ExampleGroupId0005",
  "dateCreated": "2026-10-14T22:54:12.127Z",
  "isActive": true,
  "isReportable": true,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60"],
  "invited": ["94b1569506b04f9f8557af611e8c5e47", "5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b"],
  "isExisting": true
}
```

Same request after `94b1569506b04f9f8557af611e8c5e47` accepted:

```json
{
  "conversationId": "07c0ExampleGroupId0005",
  "dateCreated": "2026-10-14T22:54:12.127Z",
  "isActive": true,
  "isReportable": true,
  "members": ["c1f0a37e2b6d4e8a9f5c7d1e3b2a4f60", "94b1569506b04f9f8557af611e8c5e47"],
  "invited": ["5e2d8c1b9a7f4e3d8c6b2a1f0e9d7c3b"],
  "isExisting": true
}
```

No events are sent for a dedup hit.

### Group size

The API accepts 2-account groups (creator + one invite). The EGL UI only offers group creation from 3 accounts, but lists and opens 2-account groups created through the API.

### isReportable

Follows the creator's KWS `chat` / `enhanced-text-reporting` value (game `fn`), changed with [KWS Update Setting Values](../../KWS/Settings/UpdateValues.md#text-reporting):

| Creator setting | Group `isReportable` | EGL label |
| --- | --- | --- |
| `prefer-not-recording` | `false` | "Text reporting is off" |
| `recording` | `true` | |

Observed: a group created with `prefer-not-recording` stayed `isReportable: false` after the invitee joined (on `MEMBERS_JOIN`, `NEW_MESSAGE`, `MEMBERS_LEFT`); after switching the creator's setting to `recording`, every new group was created `true`. In an earlier group (`07c0ExampleGroupId0001`, [Add Members](AddMembers.md)) `isReportable` went from `false` to `true` after a second member joined; what triggered that change was not isolated.
