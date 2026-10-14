## Moderation Service - Moderate: Screen Text Batch

Bulk variant used for message history pages. The result array must have the same length and order as the input.

URL: https://moderation-ingest-service-prod-external.ecbc.live.use1a.on.epicgames.com/v4/moderate/screen_batch/:workloadId \
Method: POST \
Auth Required: Yes (Bearer elevated EG1 access token)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer {token} <br/>

## Path Parameters
`workloadId`: `social_overlay_text_chat_toxicity`, `social_overlay_text_chat_personal_information` or `social_overlay_text_chat_toxicity_and_personal_information`, chosen from the user's `filter-out-mature-language` / `filter-out-pii` KWS settings <br/>

## Body
```json
[
  { "text": "first" },
  { "text": "second" }
]
```

---

_Example Response (shape from client)_

```json
[
  { "text_response": { "filtered_text": "first" } },
  { "text_response": { "filtered_text": "second" } }
]
```
