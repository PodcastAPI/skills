# Official SDKs

Use this version snapshot for playlist support, then check the target project's lockfile and the linked SDK documentation. Do not assume a newly generated method exists in an older installed package. Upgrade within the user's scope and check the SDK's runtime requirements; an existing HTTP client is a valid alternative when an upgrade would not fit.

## Versions And Packages

Synchronized versions as of 2026-09-24; these are a compatibility snapshot, not a promise that they remain the latest release. All listed versions support the five playlist write operations.

| Language | Package / dependency | Version | SDK documentation |
| --- | --- | --- | --- |
| JavaScript | npm `podcast-api` | `3.0.2` | [Node and Workers](https://github.com/ListenNotes/podcast-api-js) |
| Python | PyPI `podcast-api` | `3.0.0` | [Python](https://github.com/ListenNotes/podcast-api-python) |
| Ruby | RubyGems `podcast_api` | `3.0.0` | [Ruby](https://github.com/ListenNotes/podcast-api-ruby) |
| PHP | Composer `listennotes/podcast-api` | `3.0.0` | [PHP](https://github.com/ListenNotes/podcast-api-php) |
| Rust | crates.io `podcast-api` | `3.0.0` | [Rust](https://github.com/ListenNotes/podcast-api-rust) |
| Go | `github.com/ListenNotes/podcast-api-go/v3` | `v3.0.0` | [Go](https://github.com/ListenNotes/podcast-api-go) |
| Swift | SPM repository `ListenNotes/podcast-api-swift`; CocoaPods `PodcastAPI` | `3.0.0` | [Swift](https://github.com/ListenNotes/podcast-api-swift) |
| .NET | NuGet `PodcastAPI` | `3.0.0` | [.NET](https://github.com/ListenNotes/podcast-api-dotnet) |
| Java | Maven `com.listennotes:podcast-api` | `3.0.0` | [Java](https://github.com/ListenNotes/podcast-api-java) |
| Kotlin | Maven `com.listennotes:podcast-api` | `3.0.0` | [Kotlin examples](https://github.com/ListenNotes/podcast-api-kotlin) |
| Scala | Maven `com.listennotes:podcast-api` | `3.0.0` | [Scala examples](https://github.com/ListenNotes/podcast-api-scala) |

Kotlin and Scala are examples for the Java SDK, not separate Maven packages. Use the shared Java version and `com.listennotes.podcast_api` imports. Java/Kotlin/Scala require Java 17+, Node SDK v3 requires Node 22+, Python requires 3.10+, and .NET v3 requires .NET 8+. Check the other SDK READMEs for their runtime requirements. Go v3 needs `/v3` in the import path.

## Playlist Method Names

| Operation | JavaScript, Java, Kotlin, Scala, PHP, Swift | Python, Ruby, Rust | Go, .NET |
| --- | --- | --- | --- |
| Create playlist | `createPlaylist` | `create_playlist` | `CreatePlaylist` |
| Update metadata | `updatePlaylist` | `update_playlist` | `UpdatePlaylist` |
| Add item | `addPlaylistItem` | `add_playlist_item` | `AddPlaylistItem` |
| Update/clear notes | `updatePlaylistItemNotes` | `update_playlist_item_notes` | `UpdatePlaylistItemNotes` |
| Delete item | `deletePlaylistItem` | `delete_playlist_item` | `DeletePlaylistItem` |
| Read playlist | `fetchPlaylistById` | `fetch_playlist_by_id` | Go: `FetchPlaylistByID`; .NET: `FetchPlaylistById` |
| List account playlists | `fetchMyPlaylists` | `fetch_my_playlists` | `FetchMyPlaylists` |

An OpenAPI operation ID is not always the SDK method name: `getPlaylistById` maps to the read methods above. README method anchors are the lowercase function name, retaining underscores, for example [JavaScript createPlaylist](https://github.com/ListenNotes/podcast-api-js#createplaylist) and [Python update_playlist_item_notes](https://github.com/ListenNotes/podcast-api-python#update_playlist_item_notes).

Parameter and response conventions differ by SDK. Node uses a parameter object and `response.data`; Python uses keyword arguments and `response.json()`. Java and its Kotlin/Scala examples use `Map<String, String>` parameters and `response.toJSON()`. Follow each SDK's signature rather than mechanically translating one language's example. Keep explicit empty strings when clearing notes or descriptions.

For Python, `from listennotes import podcast_api` remains the import for PyPI's `podcast-api`. For Node use `Client`; Workers use `ClientForWorkers` with a secret binding. Some SDKs select the stateless mock when no API key is supplied. Require a configured key in production rather than silently treating fake mock data as real.

Use the [headless CMS workflow](playlist-cms.md) for examples and the [interactive API docs](https://www.listennotes.com/api/docs/) for operation-specific code in every language. Full request/response schemas remain in the [OpenAPI document](https://listen-api.listennotes.com/api/v2/openapi.yaml).
