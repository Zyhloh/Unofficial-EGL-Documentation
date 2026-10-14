## Emerald Service - SDK: Upload Recording

Second step of a party voice report. The EOS SDK (`FRTCAudioLogicRecord::UploadReportArchive`) streams the archived voice recording (signed audio frames plus the participant list, `RTCAudioRealRecord GetArchives`) to the single URL from [Initialize Upload](SOInit.md). Progress is published to the overlay as `voice-moderation.reportUploadProgress`.

URL: `chunkUrls[0]` from [Initialize Upload](SOInit.md) \
Method: PUT \
Auth Required: No SDK auth header is set (the URL is expected to carry its own authorization; inferred)

## Headers
`Content-Type`: application/octet-stream <br/>

## Body

Raw archive bytes, streamed from the recording buffer. Format is SDK-internal.

---

No response fields are read; on success the SDK calls [Complete Upload](SOComplete.md).
