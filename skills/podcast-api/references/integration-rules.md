# Integration Rules

## Authentication And Boundaries

- Production base URL: `https://listen-api.listennotes.com/api/v2`
- Mock base URL: `https://listen-api-test.listennotes.com/api/v2`
- Server-side environment variable: `LISTEN_API_KEY`
- Production request header: `X-ListenAPI-Key: <server-side value>`

Send production requests from a trusted server, serverless function, or backend-for-frontend. A browser or distributed mobile binary cannot keep an API key secret. Do not solve that architecture problem with obfuscation, a public environment variable, or permissive proxying.

Reuse the project's configuration and HTTP abstractions. Add timeouts and cancellation where supported. Encode URLs and bodies through the HTTP library, and avoid logging authorization headers or full upstream error objects.

## Responses And Errors

Use the live [OpenAPI document](https://listen-api.listennotes.com/api/v2/openapi.yaml) for operation-specific responses. Handle these common classes:

- `200` / `201`: parse the documented JSON body and optionally capture usage headers. Playlist creation and new/restored items return `201`; an already-present item returns `200`.
- `400`: reject or correct invalid application inputs; do not retry unchanged requests.
- `401`: inspect the safe upstream error message. It can indicate invalid credentials, inaccessible private content, or a plan restriction; do not report every `401` as a bad key.
- `403`: surface the ownership or permission failure. Playlist writes require ownership by the admin API account, even if the playlist can be read.
- `404`: return a domain-appropriate not-found result when documented for the operation.
- `429`: stop immediate retries, respect application retry policy, and surface quota or rate-limit context safely.
- `5xx` and network failures: use bounded retries with backoff only for idempotent requests, or when the application deliberately makes a non-idempotent operation retry-safe.

Do not assume every endpoint returns every status. Preserve enough upstream context for diagnosis without exposing secrets.

Playlist POST/PUT requests accept JSON or form-encoded bodies. Put playlist and item identifiers in the path, read filters/cursors in the query string, and editable fields in the body. Preserve explicit empty strings for notes and descriptions; they clear values. Omitted fields preserve existing values. Playlist and item DELETE requests take no body. Whole-playlist deletion is irreversible and needs confirmation in your application's UI before the request; it returns `404` if the playlist is missing or already deleted. Repeating item deletion within an existing playlist succeeds. Do not blindly retry playlist creation after an ambiguous timeout: it can create a second playlist. See [playlist-cms.md](playlist-cms.md) for write behavior.

## Pagination

Follow response-provided cursors instead of calculating them yourself.

| Operation | Request field | Continue with | Stop when |
| --- | --- | --- | --- |
| `GET /search` | `offset` | response `next_offset` | the requested limit is reached or no usable next page remains |
| `GET /best_podcasts` | `page` | response `next_page_number` | no next page remains |
| `GET /podcasts/{id}` | `next_episode_pub_date` | response `next_episode_pub_date` | `episodes` is empty or the requested limit is reached |
| `GET /curated_podcasts` | `page` | response `next_page_number` | no next page remains |
| `GET /playlists/{id}` | `last_timestamp_ms` | response `last_timestamp_ms` | no items or usable cursor remains |
| `GET /playlists` | `page` | response `next_page_number` | `has_next` is false |
| `GET /podcasts/domains/{domain_name}` | `page` | response `next_page_number` | no next page remains |

Add a maximum page or item bound unless the user explicitly needs exhaustive traversal. Guard against repeated cursors to prevent infinite loops. Preserve the endpoint's sort order while paging.

For playlist items, hold `type` and `sort` constant across pages and use `last_timestamp_ms`, not `last_pub_date_ms`. The episode and podcast views need separate pagination loops.

## Usage Headers

Read headers case-insensitively. The API documents headers including:

- `X-ListenAPI-FreeQuota`
- `X-ListenAPI-Usage`
- `X-ListenAPI-NextBillingDate`
- `X-ListenAPI-Latency-Seconds`

Use usage headers for monitoring or warnings, not as authorization. A `HEAD` request can inspect headers without counting as usage according to the current tutorial and billing FAQ; verify that behavior before building automation around it.

## Caching, Storage, And Attribution

For current FREE and PRO terms, client-side response caching is allowed, but server-side response storage is restricted. The FAQ currently permits permanent server-side storage of podcast or episode IDs and publication dates, and permits storing or processing podcast audio files. Enterprise terms can allow broader server-side storage.

Applications displaying API data under FREE or PRO terms must currently show a `Powered by Listen Notes` logo on at least one screen or page that uses the data. Enterprise terms may differ.

Treat these as policy summaries, not legal advice. Re-check the live [API FAQ](https://www.listennotes.com/api/faq/) and [terms](https://www.listennotes.com/api/terms/) before designing storage, caching, indexing, or attribution behavior.
