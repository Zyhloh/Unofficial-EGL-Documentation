# Voice - Audio Signing

In a moderated party voice room (`signed_audio` option, see [RTC Signaling](RTCSignaling.md#join)) every outgoing Opus RTP payload carries a counter and an Ed25519 signature. The format was read from the EOS SDK (`AudioPacker_v1::Sign`, `SigningAssistant_Outgoing::PatchPayload`), the inputs were confirmed by hooking EGL's signer, and a standalone client using it was heard by EGL (2026-10-14).

## Key

The signing key is the Ed25519 private key whose public half was registered with [Register Public Key](../../EpicGames/PublicKeyService/PublicKey/Register.md); the returned JWT is the `signed_public_key` in `join`. Generate one key per session; see [Moderation](Moderation.md#voice-moderation-key).

## Format (version 1)

Applied to each Opus payload before SRTP:

```
message   = opus || u32be(counter) || room_name
signature = Ed25519(private key, message)
payload   = opus || u32be(counter) || signature || 00 00 00 01
```

| Part | Size | Notes |
| --- | --- | --- |
| `opus` | variable | the encoded frame as it would be sent unsigned |
| `counter` | 4 | big-endian, starts at `0` for the room session, `+1` per packet, never goes backwards (the verifier rejects a lower counter) |
| `room_name` | | ASCII `pv2-<partyId>` from [Get Voice Room Connection](../../EpicGames/PartyService/Conferences/ConnectVoiceRoom.md); signed but not sent |
| `signature` | 64 | Ed25519 over `message` |
| version | 4 | `00 00 00 01` |

The trailer adds 72 bytes per packet. Version 0 (unsigned) is `opus || 00 00 00 00`.

EGL hook output, first packets of a session: counter `0`, `1`, `2`, ... with Opus payloads of 2-276 bytes (TOC `0x7b`: 3 x 20ms frames per packet) and a 36-byte context = the room name.

## Test vector

Private key seed (RFC 8032 test 1) `9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60`, public key `11qYAYKxCrfVS/7TyWQHOg7hcvPapiMlrwIaaPcHURo=`, room `pv2-2f1f0a5e3c8b4b6f9d7e1a2b3c4d5e6f`, Opus payload `f8fffe`, counter `0`:

```
message   f8fffe 00000000 7076322d3266316630613565336338623462366639643765316132623363346435653666
signature 90bee74ef1a1aedbad5b94920862bcda586c2b329db14294e19fb5a7f588f817a0fe081603599caf85b162ef6e008b550f612068a4416fd3b522140fa873990a
payload   f8fffe 00000000 90bee74ef1a1aedbad5b94920862bcda586c2b329db14294e19fb5a7f588f817a0fe081603599caf85b162ef6e008b550f612068a4416fd3b522140fa873990a 00000001
```

## Receiving

Packets forwarded from moderated participants keep the trailer (incoming sizes in [Media](Media.md#rtp)). Before Opus decoding:

- last 4 bytes `00 00 00 01`: drop the last 72 bytes; `opus = payload[:-72]`, `counter = payload[-72:-68]`, `signature = payload[-68:-4]`.
- last 4 bytes `00 00 00 00`: drop the last 4 bytes.

To verify (`AudioPacker_v1::Verify`):

1. Take the participant's `signed_public_key` from `user_joined` (or the parsed `join_res.users` string).
2. Verify that JWT with Epic's signing key: the header has no `kid`, read `kid` from the payload, pick that key from [Get Signing Keys](../../EpicGames/PublicKeyService/PublicKey/SigningKeys.md#verifying-a-key-jwt) and check the EdDSA signature over `header.payload` (confirmed working). Check `account_id` = the participant's `user_token` and `expiration`.
3. Map the incoming packet to the participant by its CSRC (= their `ssrc.audio`, [Media](Media.md#rtp)).
4. Rebuild `message` with the room name and check the packet signature against the JWT's `key` claim.

Step 2 was confirmed live; per-packet verification (step 4) was not run by the standalone client.

libopus does not reject a payload with the trailer still attached: the standalone client fed unstripped EGL payloads to aiortc's decoder and the recording was audible. Decoding real EGL Opus frames offline with and without an appended 72-byte trailer gave clearly different PCM (difference RMS larger than the signal RMS), so the trailer corrupts the end of each frame; strip it.

## SDK functions

| Function | Role |
| --- | --- |
| `Moderation::GenerateKeys` / `CryptoKeyGeneratorOpenSSL::GenerateEd25519` | key pair |
| `PublicKey::CreatePublicKeyV2` | public key registration (`/publickey/v2/` routes) |
| `RTCAudio::RegisterOwnSigningAlgorithm` / `RegisterParticipantSigningAlgorithm` | own signer, per-participant verifiers |
| `AudioSigner::CreateSignContext` | binds the room name as context |
| `AudioPacker::Pack` / `Unpack`, `AudioPacker_v1::Sign` / `Verify`, `AudioPacker_v0::Verify` | trailer format (`Signature Version is not supported: %zu`, `Null Version Verifier expects %zu zeros bytes`) |
| `SigningAssistant_Outgoing::PatchPayload` | patches the outgoing RTP payload |
| `RTCRoom::JoinRoom` | refuses to join moderated without a signer (`A sending signature was missed`) |
