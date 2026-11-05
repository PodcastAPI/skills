# Podcast Search by Listen Notes

A plugin for ChatGPT and Codex for podcast research, PR lead discovery, and on-demand media monitoring, powered by the [Listen Notes Podcast API](https://www.podcastapi.com/).

Published by **Listen Notes, Inc.** Contact: [hello@listennotes.com](mailto:hello@listennotes.com).

## Features

- Search podcasts and episodes by topic, person, or keyword.
- Find relevant podcasts and available producer contacts for PR outreach planning.
- Check recent podcast episode titles and descriptions for mentions of a brand, company, competitor, or person, with dates and source links. Run a new search to check for later coverage; the plugin does not schedule alerts.
- Filter results by publication date, episode count, and other supported criteria.
- Explore recommendations, read playlists, and retrieve available transcripts.
- View podcast cards with artwork, publisher details, episode counts, and available Web, RSS, Apple Podcasts, and Email buttons. Email opens a contact dialog with a copy action.
- View episode cards with publication dates, duration, **Listen on Listen Notes**, and **Download audio** links when an audio URL is available. The download link opens the original audio URL so users can save the file manually in their browser. The browser may display its own player before saving.
- Both card types show available Listen Score and global-rank badges beside the podcast name. Unavailable scores are omitted.
- Restricted Email/RSS buttons show a neutral access notice and an informational link. They do not reveal restricted data or change the API account.

Cards require an MCP Apps-capable client and the connected server's card tools. Displaying cards from previously fetched results makes no additional Podcast API request.

## Connect your account

When the client requests authorization, sign in to Listen Notes and select an existing Podcast API app. API account owners can also create an app during consent; team members select an existing app. The client can reuse an existing authorized connection.

You need Podcast API access through your own API account or an API team. See [API access information](https://www.listennotes.com/api/mcp/access/) for account and field requirements. Complete authorization through Listen Notes; keep API keys and access tokens out of chat.

The MCP service is free. Production API requests use the selected API app's existing plan and billing.

The tools read accessible playlists but do not edit them, send outreach, or transcribe uploaded audio. [Privacy Policy](https://www.listennotes.com/privacy/) and [Terms of Service](https://www.listennotes.com/terms/) apply.

## Example requests

- "Find podcast interviews about bootstrapping a startup."
- "Find PR leads: technology podcasts with fewer than 30 episodes and available producer contacts."
- "Find podcast episodes mentioning Cloudflare in the past 30 days for media monitoring."
- "Pick a random podcast episode I can listen to."

The bundled [podcast-mcp skill](skills/podcast-mcp/SKILL.md) provides research workflows, source-link guidance, and handling for pagination and unavailable data.

## Install from a GitHub marketplace

In ChatGPT's **Admin → Plugins → Add → Import marketplace**, use `https://github.com/PodcastAPI/skills` as Source, leave Path empty, and select `main` as the branch. The repository's OpenAI marketplace lists this plugin as `podcast-search` alongside the separate API development skill.

After importing, make the plugin available to the intended workspace members and complete account authorization when prompted. GitHub marketplace import does not publish a public directory listing. Imported MCP plugins may be marked **Desktop only**; see [OpenAI's supported import behavior](https://learn.chatgpt.com/docs/enterprise/plugin-management).

## Build the package

From the repository root:

```bash
python scripts/build_plugin.py
uv run --with PyYAML==6.0.3 python scripts/validate.py
```

The build refreshes the bundled skill, writes `dist/podcast-search-<version>.zip` using the version in `plugin.json`, and prints its path and SHA-256 checksum. The plugin directory is also self-contained for GitHub imports.

The package contains:

| Source | Purpose |
| --- | --- |
| `plugin.json` | Plugin identity, listing metadata, and starter prompts |
| `mcp.json` | Connection to `https://mcp.listennotes.com/mcp/` using Streamable HTTP and server-advertised OAuth discovery |
| `assets/` | Light and dark theme logos |
| `skills/podcast-mcp/` | Research skill, copied from the repository's canonical skill directory during the build |

Edit the canonical skill in the repository's `skills/podcast-mcp/` directory, then run the build and validation commands. Include the refreshed plugin skill files in the same commit. Validation checks that the canonical and bundled skills match, including their supporting references and agent configuration.

The MCP server and card UI are hosted by Listen Notes and maintained separately from this package.

## Support

Visit [Podcast Search by Listen Notes](https://www.listennotes.com/api/mcp/) or contact [hello@listennotes.com](mailto:hello@listennotes.com).
