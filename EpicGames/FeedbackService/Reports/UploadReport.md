## Feedback Service - Reports: Upload Report

Second step of `submit_feedback` (`src\feedback\upload.rs`): uploads the log bundle to the presigned POST returned by [Request Slot](RequestSlot.md). Logged as `feedback report uploaded reference_code=.. include_logs=.. logs_trimmed=..` and `Feedback.Uploaded`.

URL: `upload.url` from the slot response \
Method: POST \
Auth Required: No (the presigned `fields` carry the authorization)

`upload.url` must start with `https://` (`Upload URL must be https`).

## Headers
`Content-Type`: multipart/form-data <br/>

## Body
Multipart form:

| Part | Value |
| --- | --- |
| every `upload.fields` key | its value, as a text part |
| `file` | the report bundle, file name `logs.zip`, content type `application/zip` |

The `file` part is added after the field parts (call order). Which files go into `logs.zip` depends on `includeLogs` / the screenshot; the zip layout was not recovered.

---

| Response | Client message |
| --- | --- |
| 2xx | success |
| error body containing `EntityTooLarge` | `Report is too large to upload` |
| other | `Report upload failed (..)` |
