# Voice - Media (SDP, ICE, DTLS, RTP)

How audio flows once [signaling](RTCSignaling.md) returned `join_res`. There is no SDP on the wire: each side builds it locally. EGL's SDK builds a remote description from `join_res` (`ServerSdp::BuildSession`, `BuildAudioSection`, `BuildCandidates`); a standalone client (aiortc) that did the same was heard by EGL and heard EGL (2026-10-14). UDP captures of EGL (STUN -> DTLS -> SRTP) confirm the details below.

## Summary

| Item | Value |
| --- | --- |
| Transport | one UDP 5-tuple to `join_res.ipv4`:`join_res.udp_port`, everything bundled, RTCP muxed |
| ICE | server ICE-lite, client is controlling, single server host candidate, no TURN / STUN servers |
| DTLS | client is the DTLS client (`a=setup:active`), server certificate is RSA |
| SRTP | `use_srtp`; server picked `SRTP_AEAD_AES_128_GCM` (`0x0007`) for EGL |
| Codec | Opus, payload type `100`, `opus/48000/2`, 60ms frames (`join_res.ptime`), DTX, in-band FEC |
| Outgoing SSRC | must be `join_res.ssrc.audio` |
| Incoming | one stream per `join_res.reserved_audio_streams[].ssrc`, CSRC = the speaking participant's `ssrc.audio` |
| Payload | Opus + signing trailer in moderated rooms ([Audio Signing](AudioSigning.md)) |

## Remote SDP

Treat the server as the offerer. One `recvonly` section (the server receives your audio) plus one `sendonly` section per reserved stream, all with the same ICE / DTLS parameters. Built from the `join_res` example on [RTC Signaling](RTCSignaling.md#join_res):

```
v=0
o=- 0 2 IN IP4 127.0.0.1
s=-
t=0 0
a=ice-lite
a=msid-semantic:WMS *
a=group:BUNDLE 0 1 2 3 4 5
m=audio 9 UDP/TLS/RTP/SAVPF 100
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:oHnpOjDxTPw
a=ice-pwd:RSGJwJCR1N+2gKgzgHmOvWcREmsCRAXC
a=fingerprint:sha-256 5C:1E:9A:7F:3D:2B:8E:4A:6F:0C:1D:2E:3B:4A:59:68:77:86:95:A4:B3:C2:D1:E0:F1:A2:B3:C4:D5:E6:F7:08
a=setup:actpass
a=mid:0
a=extmap:1 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:5 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:100 opus/48000/2
a=fmtp:100 minptime=10;useinbandfec=1;usedtx=1
a=ptime:60
a=recvonly
a=candidate:1 1 udp 2130706431 203.0.113.24 41872 typ host
a=end-of-candidates
m=audio 9 UDP/TLS/RTP/SAVPF 100
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:oHnpOjDxTPw
a=ice-pwd:RSGJwJCR1N+2gKgzgHmOvWcREmsCRAXC
a=fingerprint:sha-256 5C:1E:9A:7F:3D:2B:8E:4A:6F:0C:1D:2E:3B:4A:59:68:77:86:95:A4:B3:C2:D1:E0:F1:A2:B3:C4:D5:E6:F7:08
a=setup:actpass
a=mid:1
a=extmap:1 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:5 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:100 opus/48000/2
a=fmtp:100 minptime=10;useinbandfec=1;usedtx=1
a=ptime:60
a=sendonly
a=msid:remote audio-20
a=ssrc:20 cname:remote
a=candidate:1 1 udp 2130706431 203.0.113.24 41872 typ host
a=end-of-candidates
```

Sections `mid:2` to `mid:5` repeat `mid:1` with `ssrc` `30`, `40`, `50`, `60`. `ptime` comes from `join_res.ptime`. The `msid` / `cname` values are local labels, any value works. SDK template strings also cover `a=candidate:{0} 1 {1} {2} {3} {4} typ {5}` for `ipv6` / `tcp_port` / `ssltcp_port` and TURN entries from `ice.servers`; none were needed.

## Answer

1. Create the answer with one local audio track on `mid:0`.
2. Force the outgoing RTP SSRC to `join_res.ssrc.audio` (aiortc: set the sender's SSRC before creating the answer). The server assigned this SSRC; the working client always used it (other values not tested).
3. Send `join_update` with the answer's `a=fingerprint` (`sha-256 ...`). EGL sent it 31ms after `join_res`; the standalone client sent it before applying the local description.
4. Apply the local description and start ICE.

The answer itself is never sent; the server only needs the fingerprint and the STUN checks.

## ICE

Captured EGL STUN Binding Request to `ipv4:udp_port`:

| Attribute | Value |
| --- | --- |
| `USERNAME` (`0x0006`) | `<join_res.ice.ufrag>:<client ufrag>`, e.g. `oHnpOjDxTPw:Ab3d` |
| `GOOG-NETWORK-INFO` (`0xC057`) | `00010000` (libwebrtc, optional) |
| `ICE-CONTROLLING` (`0x802A`) | tie-breaker |
| `USE-CANDIDATE` (`0x0025`) | on the nominating check |
| `PRIORITY` (`0x0024`) | candidate priority |
| `MESSAGE-INTEGRITY` (`0x0008`) | HMAC-SHA1 keyed with `join_res.ice.pwd` |
| `FINGERPRINT` (`0x8028`) | CRC32 |

The server answers with a Binding Success Response carrying `XOR-MAPPED-ADDRESS`. It never sends its own checks (ICE-lite), so the client must be controlling and nominate.

## DTLS

The client sends the ClientHello. Server certificate is RSA, so the client must offer ECDHE-RSA suites; aiortc's default list is ECDSA-only and the server silently ignores that ClientHello (no alert, the handshake times out). Offering the SDK's list fixes it.

EGL ClientHello (record version `feff`, client version `fefd` = DTLS 1.2):

| Item | Value |
| --- | --- |
| Cipher suites | `cca9` `cca8` `ccaa` `c02b` `c02f` `009e` `c00a` `c014` `0039` `c009` `c013` `0033` `009c` `0035` `002f` (+ `00ff`) |
| OpenSSL names | `ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES128-SHA:AES128-GCM-SHA256:AES256-SHA:AES128-SHA` |
| `use_srtp` profiles | `0001` (`SRTP_AES128_CM_SHA1_80`), `0008` (`SRTP_AEAD_AES_256_GCM`), `0007` (`SRTP_AEAD_AES_128_GCM`) |
| Supported groups | x25519, secp256r1, x448, secp521r1, secp384r1 |
| Other extensions | ec_point_formats, session_ticket, encrypt_then_mac, extended_master_secret, signature_algorithms |

ServerHello for EGL: cipher `cca8` (ECDHE-RSA-CHACHA20-POLY1305), SRTP profile `0007`. The standalone client offered the same list without `ccaa`, `0039` and `0033` and connected.

## RTP

| Item | Value |
| --- | --- |
| Payload type | `100` (Opus) |
| Timestamp step | `2880` per packet (60ms at 48kHz); larger jumps during DTX silence |
| Header extensions | one-byte (`0xBEDE`): id `1` abs-send-time (3 bytes), id `5` ssrc-audio-level (1 byte). EGL packets also carry a 16-byte id `3` element of unknown meaning; not needed |
| Outgoing | SSRC `join_res.ssrc.audio`, no CSRC |
| Incoming | SSRC = a reserved stream (`20`, `30`, ...), one CSRC = the speaker's `ssrc.audio` from `user_joined` (`ras_csrc` option) |
| RTCP | sender reports (`200`) and receiver reports (`201`) both ways on the same port |

Right after DTLS, EGL sent a burst of padding-only RTP packets (P bit set, same timestamp) on its audio SSRC; inferred to be libwebrtc bandwidth probing, not required.

Incoming packet sizes show the signing trailer is forwarded unchanged: EGL's smallest outgoing and the standalone client's smallest incoming packets were both about 130 bytes, which is header + extensions + SRTP tag + a tiny DTX frame + the 72-byte trailer. Strip it before decoding ([Audio Signing](AudioSigning.md#receiving)).
