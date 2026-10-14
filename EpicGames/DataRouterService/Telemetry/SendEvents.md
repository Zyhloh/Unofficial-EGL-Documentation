## Data Router Service - Telemetry: Send Events

EOS telemetry endpoint. Used by two clients:

- the launcher exe (`epic_dev` + `/telemetry/data`, sink `telemetry::sinks::eos_datarouter`, gated by `telemetry-eos-datarouter-sample-rate`)
- the social overlay web app (`AppID=egs-launcher-social`, batched every 2000 ms)

URL: https://api.epicgames.dev/telemetry/data \
Method: POST \
Auth Required: Yes (Bearer EOS client token; the overlay gets it from `window.ue.social.getclienttoken`)

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer token <br/>
`x-routing-x-epic-operational`: true (social overlay) <br/>

## Query Parameters
`AppID`: e.g. `egs-launcher-social` <br/>
`AppVersion`: Build hash, e.g. `48a8a998c785c6c7358b56ddc82474ca23ae565f` <br/>
`AppEnvironment`: `prod` <br/>
`UploadType`: `eteventstream` <br/>
`SessionID`: Optional <br/>
`UserID`: Optional, account id <br/>

## Body
```json
{
  "Events": [
    {}
  ]
}
```

The overlay sends `{ Events: [...] }` with `referrerPolicy: no-referrer` (and `keepalive` on unload). The exe's EOS sink is keyed by `app_id` and logs `EOS Data Router batch sent` / `batch rejected`; its exact query set was not recovered.
