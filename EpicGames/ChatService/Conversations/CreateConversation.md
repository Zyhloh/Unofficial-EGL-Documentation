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

Events: the creator and every invited account receive `social.chat.v1.CONVERSATION_CREATED` and `NEW_INVITE`, followed by `REPORTABILITY_CHANGE` ([events](../README.md#realtime-events)). The history starts with `NEW_INVITE` and `REPORTABILITY_CHANGE` system entries.

`isReportable` observed: `false` for a group created with one member and one invite, `true` once a second member had joined; `true` from creation for a group created by another account with two invites.
