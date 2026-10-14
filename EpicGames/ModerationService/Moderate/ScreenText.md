## Moderation Service - Moderate: Screen Text

Client-side chat filtering. Outgoing messages, incoming `NEW_MESSAGE` events and conversation `lastMessage` are replaced with `filtered_text` when either filter is enabled.

URL: https://moderation-ingest-service-prod-external.ecbc.live.use1a.on.epicgames.com/v4/moderate/screen/:workloadId \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>

## Path Parameters
`workloadId`: `social_overlay_text_chat_toxicity`, `social_overlay_text_chat_personal_information` or `social_overlay_text_chat_toxicity_and_personal_information`, chosen from the user's `filter-out-mature-language` / `filter-out-pii` KWS settings <br/>

## Body
```json
{
  "text": "message text"
}
```

---

_Example Response (shape from client; only `text_response.filtered_text` is read)_

```json
{
  "text_response": { "filtered_text": "message ****" }
}
```
