## Data Router Service - Data Router: Send Data

Analytics + log sink of the launcher (`eglv2_lib::telemetry::sinks::datarouter`). Events are spooled to `telemetry/spool/*.jsonl` and sent in batches; a live session logged `Data Router batch sent status=204 count=12 app_id="LauncherV2"`. Gated by the `telemetry-datarouter-sample-rate` and `telemetry-datarouter-log-levels` flags and `-disable-telemetry` / `EGL_DISABLE_TELEMETRY`.

URL: https://datarouter.ol.epicgames.com/datarouter/api/v1/public/data \
Method: POST \
Auth Required: No

## Headers
`Content-Type`: application/json <br/>
`User-Agent`: `<AppID>/<AppVersion> ...` <br/>

## Query Parameters
`SessionID`: Launcher session id (uuid) <br/>
`AppID`: `LauncherV2` (release builds), `LauncherV2.Dev` (others) <br/>
`AppVersion`: `0.95.1+ge288862` <br/>
`UserID`: Account id, empty when signed out <br/>
`AppEnvironment`: Environment string; the exe also holds the template `UnrealEngineLauncher{env}.{kind}` (`{env}` empty for prod, `_GD` otherwise; `{kind}` `Release` / `Dev`) next to this code, its use as `AppEnvironment` is inferred <br/>
`UploadType`: `eteventstream` <br/>

## Body
```json
{
  "Events": [
    {
      "EventName": "Launcher.Log",
      "DateOffset": "+00:00:00.000",
      "event_id": "94b1569506b04f9f8557af611e8c5e47",
      "level": "...",
      "origin": "...",
      "session_time_ms": 1234,
      "sample_rate": 1,
      "schema_version": 1
    }
  ]
}
```

`Events`, `EventName`, `DateOffset` and the snake_case keys are from the binary; values are placeholders. Other events (`Settings.Snapshot`, `Store.PurchaseCompleted`, ...) carry their own props next to the common ones (`wall_ms`, `account_id`, `device_id`, `session_id`, `release_type`, `release_channel`, `launcher_version`).

---

_Example Response_

`204 No Content`
