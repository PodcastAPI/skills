# Podcast Search by Listen Notes

**PR leads & media monitoring**

Research podcasts, discover guest interviews, find available producer contacts for PR outreach planning, and check recent podcast mentions of your brand, company, or competitors. Published by **Listen Notes, Inc.** Contact: [hello@listennotes.com](mailto:hello@listennotes.com).

![Podcast Search by Listen Notes](assets/logo.png)

## What you can do

- Discover podcasts by topic, language, genre, or episode count, and find guest interviews by a person's name.
- Identify potential PR leads from relevant shows and available producer email addresses. A listed contact does not guarantee that a show accepts pitches.
- Monitor media mentions with on-demand searches of episode titles and descriptions, filtered by publication date. Results include dates and source links; the plugin does not schedule alerts.
- View podcast cards with artwork, publisher details, episode counts, available Listen Score and global-rank badges, and Web, RSS, Apple Podcasts, and Email buttons. Email opens a contact dialog with a copy action.
- View episode cards with publication dates, duration, listening links, and manual audio download links when available. Audio opens externally for you to save in your browser.
- Read accessible playlists, explore recommendations, and retrieve transcripts already available for indexed episodes.

Cards appear when the connected Claude client supports MCP Apps. Text and exact Listen Notes links remain available when a card cannot be displayed. Drawing cards from cached results makes no additional Podcast API request.

## Install and connect in Claude

1. Open **Customize → Plugins → Add → Add marketplace** in Claude.ai or Claude Desktop and enter `https://github.com/PodcastAPI/skills`.
2. Add **Podcast Search by Listen Notes** from the `podcastapi` marketplace. If you have a packaged ZIP, use **Add → Upload plugin** instead.
3. Open the plugin's **Connectors** tab. Add the bundled Listen Notes connector if it is marked **Not added**, or select **Connect** if it is **Not connected**. On managed accounts, an organization owner may need to add it first.
4. Complete OAuth on Listen Notes and choose an existing Podcast API app. API account owners can also create an app during authorization; team members select an existing app available through their API account.
5. Start a conversation and ask a podcast research question. If a working connector already uses the server URL below, reuse it. Installing the skill alone does not authorize the connection.

| Connection | Value |
| --- | --- |
| Remote server | `https://mcp.listennotes.com/mcp/` |
| Transport | Streamable HTTP |
| Authentication | OAuth |

Availability of plugin installation and connector controls depends on your Claude plan and organization settings. See [Claude's plugin installation documentation](https://claude.com/docs/plugins/overview).

## Install in Claude Code

```text
/plugin marketplace add PodcastAPI/skills
/plugin install listennotes-podcast-search@podcastapi
```

Use `/mcp` to check the Listen Notes connection and complete OAuth when needed. Invoke the research skill with `/listennotes-podcast-search:podcast-mcp`, or describe the task naturally. Clients without card support receive text results and source links.

## Example requests

- "Find technology podcasts with fewer than 30 episodes and producer email contacts for my startup's PR outreach. Show podcast cards."
- "Find up to three podcast episodes mentioning Cloudflare in the past 30 days for media monitoring. Show dates, episode cards, and source links."
- "Find three podcast interviews with Patrick Collison and show the matches as cards."
- "Pick a random episode and show where I can listen to it or download its audio."
- "Show my playlists and the two most recently added episodes in the largest one."

## API access and data handling

You need Podcast API access through your own API account or an API team. Requests use the API app selected during OAuth and that account's existing plan, quota, permissions, and billing. The MCP service itself is free. Account access and available fields are described on the [API access information page](https://www.listennotes.com/api/mcp/access/).

Email and RSS require PRO or ENTERPRISE API access and can still be absent from a source. Restricted buttons show an access notice without revealing restricted values. The tools cannot send outreach, edit playlists, change accounts, or transcribe uploaded audio.

The plugin connects to Listen Notes; it does not run a local server or require credentials in its files. Research queries and identifiers go to the Listen Notes MCP server and Podcast API. Opening a publisher, RSS, Apple Podcasts, or audio link visits that destination through Claude's link controls. Listen Notes does not record chat messages. API request logs are retained unless the API account owner deletes the account; fetched results are cached for ten minutes. You can revoke a connection from [MCP connections](https://www.listennotes.com/api/mcp/connections/).

[Website](https://www.listennotes.com/api/mcp/) · [Support](https://www.listennotes.com/contact/) · [Privacy Policy](https://www.listennotes.com/privacy/) · [Terms of Service](https://www.listennotes.com/terms/)

## Build from source

From the repository root:

```bash
python scripts/build_plugin.py --target claude
uv run --with PyYAML==6.0.3 python scripts/validate.py
claude plugin validate ./plugins/podcast-search-claude --strict
```

The build refreshes the bundled skill from the canonical `skills/podcast-mcp` directory and writes `dist/listennotes-podcast-search-<version>.zip` with a SHA-256 checksum. The ZIP and this plugin directory contain the same research skill, native Claude manifest, OAuth MCP connection, license, and light and dark theme logos. Edit the canonical skill, then rebuild and include the synchronized files in the same change. The separately hosted MCP server supplies the tools and card UI.
