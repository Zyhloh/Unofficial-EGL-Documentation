## Feedback Service - Reports: Request Slot

First step of the in-app "Send feedback" flow (`eglv2_lib::feedback`, `src\feedback\mod.rs`), IPC command `submit_feedback` (`{ input: { description, includeLogs, screenshotPath, screenshotBase64, locale, consentVersion } }`, frontend `consentVersion` is `2026-10`). The menu item only exists while the `feedback-enabled` flag is on. The launcher sends the report metadata, gets back a report id and a presigned upload, then uploads the bundle with [Upload Report](UploadReport.md).

URL: https://77m13yhhad.execute-api.us-east-1.amazonaws.com/prod/api/v2/reports \
Method: POST \
Auth Required: Optional (Bearer access token, sent when signed in)

The URL is the `feedback_ingest` endpoint key plus `/api/v2/reports`. It can be replaced by `EGL_FEEDBACK_INGEST_HOST` or, on prod, by the `feedback-ingest-url` flag (full URL used verbatim). It must start with `https://` (`Feedback endpoint must be https`). Gamedev / ci use `https://qv4w0ux1dl.execute-api.us-east-1.amazonaws.com/ci/api/v2/reports`.

## Headers
`Content-Type`: application/json <br/>
`Authorization`: Bearer <access token> (only when signed in) <br/>

## Body
```json
{
  "launcherVersion": "0.95.1+ge288862",
  "os": "windows x86_64",
  "includeLogs": true,
  "screenshotAttached": false,
  "includedFiles": [
    "<file name>"
  ],
  "note": "Description typed by the user",
  "consent": {
    "version": "2026-10",
    "locale": "en",
    "timestamp": "2026-10-14T12:00:00Z"
  },
  "eosSdkVersion": "<version or null>",
  "overlayVersion": "<version or null>",
  "overlayOwner": "v2"
}
```

Field names and order from the `SlotRequest` and `Consent` serializers.

- `os` is formatted as `<os> <arch>` (`windows`, `x86_64`).
- `screenshot` (string) is added after `consent` only when a screenshot is attached; its content was not recovered.
- `eosSdkVersion`, `overlayVersion` are always sent, `null` when unknown.
- `overlayOwner` is one of the table values below, or `null`.
- `includedFiles` presumably lists the files packed into `logs.zip` (inferred from the name and the `Feedback.Uploaded` `file_count` field).
- Mapping `description` -> `note` and the `timestamp` format are inferred.
- Client-side checks: `A description is required`, `Description is too long (max .. characters)`, `Feedback metadata is too long`.

`overlayOwner` values: `v2`, `v1`, `eosh`, `other`, `none`. They describe who registered the EOS social overlay on the machine (inferred from the overlay registration logs, e.g. `EOSH owns overlay installation on this machine`).

Logs are scrubbed before packing (`src\feedback\scrub.rs`: user profile paths become `<USER>`, `USERNAME` / `USER` values removed).

---

_Example Response (shape from client)_

```json
{
  "reportId": "94b1569506b04f9f8557af611e8c5e47",
  "upload": {
    "url": "https://<bucket>.s3.amazonaws.com/",
    "fields": {
      "<form field>": "<value>"
    }
  }
}
```

Field names from `SlotResponse` (`reportId`, `upload`) and `PresignedPost` (`url`, `fields`). `fields` is a name -> value map copied into the upload form as is; its keys and the bucket URL are not in the client. A response that does not parse fails with `Malformed slot response`.

The value returned to the frontend is `FeedbackResult { referenceCode }`; the reference code shown to the user is presumably the `reportId` (inferred from `feedback report uploaded reference_code=`). Each submission is kept locally in `feedback\history-<env>.json` as `{ code, submittedAt }` entries (`FeedbackHistoryEntry`), read back with `get_feedback_history` (no network call).

## Errors

| Status | Client message |
| --- | --- |
| 401 | `Feedback upload was rejected (token rejected)` (when a token was sent) |
| 403 with `{ "reason": "moderation" }` | `Feedback content was refused by moderation` |
| 403 | `Feedback upload was refused by the service (403)` |
| 429 | `Too many feedback reports, try again later.` |
| 5xx | `Feedback service error (..)` |
| other | `Feedback slot request failed (..)` |
