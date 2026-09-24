# Playlists As A Headless CMS

Use a Listen Later playlist as an editorial collection for a podcast app, topic page, newsletter, or handpicked listening feed. Listen Notes stores the collection metadata, content references, and curator notes; your app supplies the presentation. Editors can curate on ListenNotes.com or through your own backend using the playlist API.

## Ownership And Application Design

- Only playlists owned by your admin API account can be modified. Reading a public/unlisted playlist, joining it, or having contributor membership does not grant API write access.
- `GET /playlists` lists playlists the admin created or joined; do not treat every returned playlist as writable. Public/unlisted playlists can be read by ID regardless of owner; private access requires the admin's membership. Normal API authentication still applies.
- Keep the API key on your backend. Authenticate your application's editors and authorize which collection they may edit before forwarding writes. Application users do not automatically get separate Listen Notes ownership or permissions.
- Prefer one playlist per editorial collection. Keep presentation settings or custom editorial fields in the application if needed; do not turn free-text notes into an undocumented CMS schema. Follow [storage and attribution rules](integration-rules.md#caching-storage-and-attribution) for API metadata.

## Editorial Workflow

1. Discover candidates using search, podcast details, recommendations, or human selection. Keep the Listen Notes episode/podcast IDs returned by the API.
2. Create a collection with `POST /playlists`. Supply a nonblank `name` and deliberately choose `visibility` and `type`. For an unpublished editorial draft, explicitly choose `private`: creation otherwise defaults to `public`, an empty description, and `episode_list`.
3. Add each selection with `POST /playlists/{id}/items`. Send exactly one of `episode_id` or `podcast_id` and optional `notes` explaining why it belongs in the collection. Save the returned integer item `id` for later notes edits or removal.
4. Edit the collection with `PUT /playlists/{id}`. Send only the fields to change: `name`, `description`, `visibility`, or `type`. Use `PUT /playlists/{id}/items/{item_id}` for item notes and `DELETE /playlists/{id}/items/{item_id}` to remove an entry.
5. Publish intentionally: set `visibility` to `public` for discoverability on ListenNotes.com, or `unlisted` for access by anyone who knows its ID. You can also keep the collection private and serve authorized app readers through your backend. An unlisted URL is not access control. Visibility does not replace the app's own draft/publish permissions.
6. Render `GET /playlists/{id}` in your app. Display collection metadata and each entry's `data` plus curator `notes`. Use the returned `listennotes_url` for the corresponding Listen Notes view. Render notes as text, not trusted HTML. Reuse the write response to update the editor immediately.

Private is a visibility setting, not a versioned draft system. Editing a published playlist changes that collection; the API does not supply staged revisions, a review queue, or atomic publication of a batch of changes. Add those application behaviors only when requested.

## Episode And Podcast Views

A playlist can hold both episodes and podcasts. Its `type` is the saved default view, not a restriction on what can be added.

- Use `episode_list` for handpicked individual episodes; use `podcast_list` for recommended shows. Adding a show is not a request to copy all its episodes into the collection.
- Set `type` in a create/update body to change the saved default. Existing contents remain intact when it changes.
- Use the query parameter `?type=episode_list` or `?type=podcast_list` on a GET to select that view for this request only. Omitting it uses the saved default.
- The response `type` and `listennotes_url` describe the selected view. Use the returned URL rather than constructing it from the playlist name.
- For a mixed collection, fetch and paginate both views separately; a single response does not merge all content types.

Continue with response `last_timestamp_ms` in the next request, keeping `type` and `sort` constant. Stop on empty items, a missing/repeated cursor, or an application page limit. The parameter is `last_timestamp_ms`, not `last_pub_date_ms`. Supported sort values are `recent_added_first`, `oldest_added_first`, `recent_published_first`, and `oldest_published_first`; there is no arbitrary position/reorder field. Handle the documented item `type` and optional/deleted content without assuming every `data` object is a live episode.

## Write Semantics That Matter

- Paths use the 11-character playlist `id` and integer playlist-item `id`. The nested `data.id` is the episode/podcast ID, a different identifier; content IDs contain 32 hexadecimal characters.
- Create returns `201` with playlist metadata. Add returns `201` for new or restored entries and `200` if already present. The returned item ID is the authoritative editing handle.
- Re-adding the same content reuses the item. Omitted `notes` preserve its notes, including on re-addition; supplied `notes` replace them. Send `notes: ""` to clear notes, never `null` or an omitted field. Notes edits preserve the item ID and `added_at_ms` ordering timestamp.
- Metadata PUT preserves omitted fields, requires at least one supported field, and accepts `description: ""` to clear it. Names must be nonblank and cannot be `rss` (case insensitive). Name/description limits are 4,096 characters; plain-text notes are limited to 1,024 characters.
- Item DELETE takes no body and returns `200` with `{ "id": 23, "deleted": true }`. Repeating it for that same deleted entry succeeds. Removing an entry does not remove the underlying podcast/episode from the directory.
- Handle `400` validation errors, `401` authentication/access errors, `403` ownership errors, `404` missing playlist/item/content, and quota/rate-limit errors. A missing episode or podcast returns `404` with the content-specific reason; invalid content ID syntax returns `400`.
- Writes accept JSON and form encoding. Keep path identifiers out of the editable body and do not drop explicitly empty strings in a serializer. Do not blindly retry collection creation after a timeout or repeat it on every app render; keep the returned playlist ID in the app's collection configuration.

The current API does not delete an entire playlist. Do not invent `DELETE /playlists/{id}` or implement it by deleting every item. Bulk addition, arbitrary reordering, artwork editing, and custom-audio upload are also not current write operations. Add multiple selections with bounded individual requests when the user requests them.

## Node SDK Example

Backend-only helpers for `podcast-api@3.0.2` (Node 22+). These define explicit editing actions; they do not run a mutation on import. Call them only from an authorized editor action. Get `episodeId` from a search/details response; `playlistId` and `itemId` come from the create/add responses.

```js
const { Client } = require('podcast-api');

function collectionEditor() {
  const apiKey = process.env.LISTEN_API_KEY;
  if (!apiKey) throw new Error('LISTEN_API_KEY is required');
  const client = Client({ apiKey });

  return {
    async create(name, type = 'episode_list') {
      const response = await client.createPlaylist({ name, type, visibility: 'private' });
      return response.data;
    },
    async addEpisode(playlistId, episodeId, notes) {
      const params = { id: playlistId, episode_id: episodeId };
      if (notes !== undefined) params.notes = notes;
      const response = await client.addPlaylistItem(params);
      return response.data;
    },
    async setNotes(playlistId, itemId, notes) {
      const response = await client.updatePlaylistItemNotes({
        id: playlistId, item_id: itemId, notes, // '' explicitly clears notes.
      });
      return response.data;
    },
    async publish(playlistId) {
      const response = await client.updatePlaylist({ id: playlistId, visibility: 'public' });
      return response.data;
    },
    async removeItem(playlistId, itemId) {
      const response = await client.deletePlaylistItem({ id: playlistId, item_id: itemId });
      return response.data;
    },
    async readPage(playlistId, lastTimestampMs = 0) {
      const response = await client.fetchPlaylistById({
        id: playlistId, type: 'episode_list', sort: 'recent_added_first',
        last_timestamp_ms: lastTimestampMs,
      });
      return response.data;
    },
  };
}

module.exports = { collectionEditor };
```

For show curation, pass `podcast_list` when creating the collection, use `podcast_id` instead of `episode_id` when adding, and read the `podcast_list` view. Handle SDK errors at the application boundary without serializing credentials or the SDK's full request/error object.

See [official-sdks.md](official-sdks.md) for equivalent methods in the other languages. The [OpenAPI document](https://listen-api.listennotes.com/api/v2/openapi.yaml) is authoritative; the [interactive playlist docs](https://www.listennotes.com/api/docs/#post-api-v2-playlists) provide full schemas. The public mock is stateless: use [testing.md](testing.md) rather than expecting a mock create-then-fetch sequence to persist a collection.
