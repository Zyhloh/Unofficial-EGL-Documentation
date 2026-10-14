# Voice Reference Client

Minimal standalone party voice client in [`Examples/VoiceClient`](../../Examples/VoiceClient). Tested against the Epic Games Launcher `0.95.2+gfa9ad49` in both directions: EGL hears the client, the client records EGL. Python, [aiortc](https://github.com/aiortc/aiortc) for ICE / DTLS-SRTP / Opus.

It does every step of the [Voice Chat flow](../Flows/VoiceChat.md) without the EOS SDK:

1. Sign in with an authorization code (`launcherAppClient2`)
2. Open [Epic Connect](../Social/Connect.md) and take the `connectionId`
3. Leave any current party, create a new one, publish presence
4. Invite an account and wait for it to join (optional)
5. Request voice credentials, claim voice in member meta
6. Register an Ed25519 key, join the signaling websocket moderated
7. Build the server SDP from `join_res`, run ICE + DTLS, send [signed](AudioSigning.md) Opus
8. Subscribe to every participant, strip the signature trailer, record their audio

## Files

| File | Contents |
| --- | --- |
| `config.json` | Settings (no environment variables) |
| `auth.py` | Authorization code / refresh token grant, token cache |
| `epic.py` | Party, presence, voice credentials, member meta, public key |
| `connect.py` | Epic Connect STOMP client |
| `voice.py` | Signaling, SDP, DTLS cipher fix, audio signing / stripping |
| `main.py` | Runs the whole flow |

## Config

`inviteAccountId`: Account id to invite (empty = solo) <br/>
`inviteWaitSeconds`: How long to wait for the invite to be accepted <br/>
`durationSeconds`: How long to stay in voice <br/>
`sendAudio`: Audio file to play into the room (empty = generated 440 / 660 Hz test tone) <br/>
`recordDir`: Where received audio is written as WAV, one file per track <br/>
`tokenFile`: Token cache, outside the repository by default <br/>
`client`: OAuth client used for the token grant <br/>
`connectionMeta` / `memberMeta`: How the client presents itself in the party

## Usage

```
pip install -r requirements.txt
python main.py
```

On first run it prints the authorization code URL (`https://www.epicgames.com/id/api/redirect?clientId=34a02cf8f4414e29b15921876da36f9a&responseType=code`). Sign in on epicgames.com in the browser, open the URL and paste the `authorizationCode`. The refresh token is reused afterwards.

The invited account must be a friend. Accept the invite in the launcher or Fortnite.

## What it does not do

- Join someone else's party (only creates its own)
- Verify incoming signatures
- Push-to-talk, devices, volume (it plays a file and records)
- Handle `transfer`, token refresh after the 2 h participant token lifetime, or reconnects
- Voice reports
