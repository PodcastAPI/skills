# Playlists And Media Workflows

## Application Playlists

Two supported designs serve different ownership needs:

1. Store permitted episode IDs in the application's database, then use `POST /episodes` to hydrate bounded batches.
2. Use Listen Later playlists as managed collections. Curators can edit them on ListenNotes.com or through the playlist write API; the app consumes them with `GET /playlists/{id}`.

For creation, metadata, notes, publication, permanent collection deletion, and both podcast/episode views, read [playlist-cms.md](playlist-cms.md). This works for editorial collections owned by the admin API account. An application's end-user accounts do not automatically become Listen Notes playlist owners; keep per-user authorization in the application or use the first design for application-owned libraries. Do not permanently mirror full API responses unless the applicable plan permits server-side storage.

Sources: [playlist tutorial](https://www.listennotes.help/article/45-how-to-build-a-playlist-for-episodes-in-a-podcast-app) and [human curation tutorial](https://www.listennotes.help/article/34-whats-the-easiest-way-for-our-human-content-curators-to-handpick-specific-podcasts-episodes-into-our-app-using-podcast-api).

## Transcripts

### Existing episode transcripts

Existing transcripts on Listen Notes include transcripts supplied by podcast producers. About 12% of new episodes and over 3% of all episodes have one. With `GET /episodes/{id}?show_transcript=1`, PRO and ENTERPRISE receive sanitized HTML in `transcript` or `null` if unavailable. FREE receives a plan-upgrade message. Use `GET /search` with `type=episode` and `only_in=audio` to search indexed transcript content.

Source: [transcript tutorial](https://www.listennotes.help/article/35-how-to-get-transcripts-of-any-podcast-episodes-using-podcast-api).

### On-demand transcription

If an episode has no existing transcript, use its Listen Notes episode ID to generate one. Transcription is available on FREE, PRO, and ENTERPRISE. Enable Transcription in the API dashboard and add a payment method or use an eligible invoicing arrangement. Use direct HTTP requests from your backend for these operations.

1. **Estimate** with `GET /episodes/{id}/transcript/estimate`. The estimate uses episode duration metadata and can be `null` when duration is unavailable. It does not reserve included minutes.
2. **Request** with `POST /episodes/{id}/transcript`. HTTP `202` means queued or processing. HTTP `200` means a completed transcript already exists for your API account. Repeating a pending or completed request for the same episode and account reuses it without another transcription charge.
3. **Poll** with `GET /episodes/{id}/transcript`. Follow `Retry-After` while pending. A completed job returns signed links in `download_urls` for TXT, SRT, VTT, and word-level JSON. A failed job returns `error.code`.
4. **List** completed transcripts with `GET /transcripts`. Pass each `next_cursor` into `cursor` until `next_cursor` is `null`. Follow an item's `transcript_url` to poll and obtain fresh download links.

For example, estimate transcription from the backend with an existing `EPISODE_ID`:

```bash
curl -fsS -H "X-ListenAPI-Key: ${LISTEN_API_KEY}" \
  "https://listen-api.listennotes.com/api/v2/episodes/${EPISODE_ID}/transcript/estimate"
```

Cache the transcript text generated for your API account. Use signed links for immediate downloads. They expire after 15 minutes, and polling returns fresh links. Direct downloads use no request quota. Successful API calls, including polling, follow normal request accounting. [Transcription API FAQ](https://www.listennotes.com/api/faq/#faq20) · [Billing FAQ](https://www.listennotes.com/api/billing-faq/#faq17)

## Audio And Clips

Use the episode audio URL from the API response for playback or downstream processing. Listen Notes audio URLs redirect to the podcast's current media URL; preserve redirect support in the HTTP player or downloader.

Clip creation is not a Podcast API endpoint. Download the audio only when the use case and applicable rights allow it, then use an audio tool such as FFmpeg to create a bounded clip. Keep media processing out of request handlers when it is slow or resource intensive.

Source: [clip tutorial](https://www.listennotes.help/article/19-how-to-create-audio-or-video-clips-for-a-specific-podcast-episode-using-podcast-api).

## Embedded Player

Derive the player URL by appending `embed/` to the response's `listennotes_url`, preserving the trailing slash. Render it in an iframe with an accessible title, lazy loading, and a responsive width. Do not expose the API key; the embedded player URL does not need it.

Source: [embedded-player tutorial](https://www.listennotes.help/article/36-do-you-provide-a-pre-built-embedded-podcast-player-that-i-can-put-on-my-website).
