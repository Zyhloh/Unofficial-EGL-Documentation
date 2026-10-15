## Data Router Service - Data Router: Send Data

Analytics + log sink of the launcher (`eglv2_lib::telemetry::sinks::datarouter`). Events are spooled to `telemetry/spool/*.jsonl` and sent in batches; a live session logged `Data Router batch sent status=204 count=12 app_id="LauncherV2"`. Gated by the `telemetry-datarouter-sample-rate` and `telemetry-datarouter-log-levels` flags and `-disable-telemetry` / `EGL_DISABLE_TELEMETRY`.

URL: https://datarouter.ol.epicgames.com/datarouter/api/v1/public/data \
Method: POST \
Auth Required: No

## Headers
`Content-Type`: application/json <br/>
`User-Agent`: `<AppID>/<AppVersion> Windows/10.0.<build>`, e.g. `LauncherV2/0.95.1+ge288862 Windows/10.0.<build>` (`Windows/unknown` when the OS version cannot be read) <br/>

## Query Parameters
`SessionID`: Launcher session id (uuid) <br/>
`AppID`: `LauncherV2` (release builds), `LauncherV2.Dev` (others) <br/>
`AppVersion`: `0.95.1+ge288862` <br/>
`UserID`: Account id, empty when signed out <br/>
`AppEnvironment`: Lowercased environment: `prod`, `gamedev` or `ci` <br/>
`UploadType`: `eteventstream` <br/>

## Body
```json
{
  "Events": [
    {
      "EventName": "Launcher.Log",
      "DateOffset": "+00:00:00.000",
      "event_id": "<eventId>",
      "level": "...",
      "origin": "...",
      "session_time_ms": 1234,
      "sample_rate": 1,
      "schema_version": 4
    }
  ]
}
```

`Events`, `EventName`, `DateOffset` and the snake_case keys are from the binary; values are placeholders. Other events (`Settings.Snapshot`, `Store.PurchaseCompleted`, ...) carry their own props next to the common ones (`wall_ms`, `account_id`, `device_id`, `session_id`, `release_type`, `release_channel`, `launcher_version`). `schema_version` is 4 in 0.95.2.

The `UnrealEngineLauncher{_GD|}.{Release|Dev}` template next to this code is the `AppID` of the EOS sink ([Send Events](../Telemetry/SendEvents.md)), not a Data Router value.

Each spool record has a `dests.dataRouter` entry; a subset of events (`App.Opened`, `Auth.*`, `Tab.Visited`, `UpdateCheck.Completed`, `Library.Refreshed`) also gets a `dests.mixpanel` copy sent to Mixpanel (`distinctId` = device id, `accountId` null).

---

_Example Response_

`204 No Content`
