## IGDB - Games: Search

Metadata (summary, release date, genres, developer, publisher) for external library titles (Steam / Xbox) shown in the launcher. Backs `get_external_game_metadata` (`{ source, title }`), cached by `external_library::metadata::cache`.

URL: https://api.igdb.com/v4/games \
Method: POST \
Auth Required: Yes (Bearer token from [Token](../Auth/Token.md))

## Headers
`Client-ID`: Twitch client id <br/>
`Authorization`: Bearer access token <br/>

## Body
```
fields name,summary,first_release_date,genres.name,involved_companies.company.name,involved_companies.developer,involved_companies.publisher; where name ~ *"<title>"*; limit <n>;
```

The title is escaped (`\"`) before being put in the query. `first_release_date` is formatted as `%Y-%m-%d`.

---

_Example Response (shape from client, `IgdbGame`)_

```json
[
  {
    "name": "...",
    "summary": "...",
    "first_release_date": 1700000000,
    "genres": [{ "name": "Adventure" }],
    "involved_companies": [
      { "company": { "name": "..." }, "developer": true, "publisher": false }
    ]
  }
]
```
