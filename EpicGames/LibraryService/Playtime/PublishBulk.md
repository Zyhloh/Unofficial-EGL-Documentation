## Library Service - Playtime: Publish Bulk

Publishes a batch of play intervals recorded locally in the playtime journal (`playtimejournal.json`). On success the launcher emits `playtime-published-event` with the accepted artifact ids. Disabled by `EGL_DISABLE_PLAYTIME_REPORTING`.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/playtime/account/:accountId/bulk \
Method: PUT \
Auth Required: Yes (Bearer access token)

Method is taken from the request builder's `http::Method` tag (3 = PUT).

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`accountId`: The account id

## Body
```json
{
  "playtimeAddList": [
    {
      "artifactId": "Fortnite",
      "machineId": "94b1569506b04f9f8557af611e8c5e47",
      "startTime": "2026-10-14T15:00:00.000Z",
      "endTime": "2026-10-14T16:00:00.000Z",
      "startSegment": 0,
      "endSegment": 1
    }
  ]
}
```

Field names from `PlaytimeAddBulk` / `PlaytimeAdd`; value formats are not visible in the client and are placeholders.
