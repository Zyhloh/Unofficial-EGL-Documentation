## Library Service - Playtime: Publish Bulk

Publishes a batch of play intervals recorded locally in the playtime journal (`playtimejournal.json`). On success the launcher emits `playtime-published-event` with the accepted artifact ids. Disabled by `EGL_DISABLE_PLAYTIME_REPORTING`.

URL: https://library-service.live.use1a.on.epicgames.com/library/api/public/playtime/account/:accountId/bulk \
Method: PUT \
Auth Required: Yes (Bearer access token)

## Headers
`Content-Type`: application/json <br/>

## Path Parameters
`accountId`: The account id

## Body
```json
{
  "playtimeAddList": [
    {
      "artifactId": "Daisy",
      "machineId": "94b1569506b04f9f8557af611e8c5e47",
      "startTime": "2026-10-15T11:38:00.000Z",
      "endTime": "2026-10-15T11:40:00.000Z",
      "startSegment": 0,
      "endSegment": 0
    }
  ]
}
```

`artifactId`: App name of the game <br/>
`machineId`: Id of the machine the time was played on (required) <br/>
`startTime`, `endTime`: ISO 8601 UTC; the interval is added to the game's total <br/>
`startSegment`, `endSegment`: Segment counters of the local journal

---

_Example Response_

`204 No Content`. The example body above (2 minutes) raised the game's `totalTime` in [Get Playtime](GetAll.md) by exactly 120 seconds. An interval whose `endTime` is before `startTime` is also answered with 204 but adds nothing.

_Example Response (`playtimeAddList` empty or missing)_

```json
{
  "errorCode": "errors.com.epicgames.library.missing_argument",
  "errorMessage": "playtimeAddList must be supplied with the request.",
  "messageVars": [],
  "numericErrorCode": 53001,
  "originatingService": "library-service",
  "intent": "prod"
}
```

A missing `machineId` gives the same error with `machineId must be supplied with the request.`
