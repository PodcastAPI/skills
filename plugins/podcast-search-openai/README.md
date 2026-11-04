# Podcast Search by Listen Notes

A plugin for ChatGPT and Codex that uses the [Listen Notes Podcast API](https://www.podcastapi.com/) to find podcasts, episodes, guest interviews, and available producer contacts.

Published by **Listen Notes, Inc.** Contact: [hello@listennotes.com](mailto:hello@listennotes.com).

## Features

- Search podcasts and episodes by topic, person, or keyword.
- Filter results by publication date, episode count, and other supported criteria.
- Explore recommendations, read playlists, and retrieve available transcripts.
- View podcast cards with artwork, publisher details, episode counts, and available Web, RSS, Apple Podcasts, and Email buttons. Email opens a contact dialog with a copy action.
- View episode cards with publication dates, duration, source links, and audio controls. Playback starts on request; a Listen Notes link provides an alternative when playback is unavailable in the client.

Cards require an MCP Apps-capable client and the connected server's card tools. Displaying cards from previously fetched results makes no additional Podcast API request.

## Connect your account

When the client requests authorization, sign in to Listen Notes and select an existing Podcast API app or create a new one. The client can reuse an existing authorized connection.

You need a Podcast API account to connect. [Get an API key](https://www.listennotes.com/api/pricing/) if you do not have one. Complete authorization through Listen Notes; keep API keys and access tokens out of chat.

The MCP service is free. Production API requests use the selected API app's existing plan and billing.

## Example requests

- "Find podcast interviews about bootstrapping a startup."
- "Find technology podcasts with fewer than 30 episodes and available producer contacts."
- "Pick a random podcast episode I can listen to."

The bundled [podcast-mcp skill](../../skills/podcast-mcp/SKILL.md) provides research workflows, source-link guidance, and handling for pagination and unavailable data.

## Build the package

From the repository root:

```bash
uv run --with PyYAML==6.0.3 python scripts/validate.py
python scripts/build_plugin.py
```

The build writes `dist/podcast-search-<version>.zip`, using the version in `plugin.json`, and prints its path and SHA-256 checksum.

The package contains:

| Source | Purpose |
| --- | --- |
| `plugin.json` | Plugin identity, listing metadata, and starter prompts |
| `mcp.json` | Connection to `https://mcp.listennotes.com/mcp/` using Streamable HTTP and server-advertised OAuth discovery |
| `assets/` | Light and dark theme logos |
| `skills/podcast-mcp/` | Research skill, copied from the repository's canonical skill directory during the build |

The MCP server and card UI are hosted by Listen Notes and maintained separately from this package.

## Support

See the [Podcast API documentation](https://www.listennotes.com/api/) or contact [hello@listennotes.com](mailto:hello@listennotes.com).
