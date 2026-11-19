# Podcast Search by Listen Notes for Cursor

Research podcasts and episodes, find available producer contacts for PR outreach, and check podcast titles and descriptions for mentions of a brand, company, or person. The plugin combines the `podcast-mcp` skill with the hosted Listen Notes MCP server.

## Connect your account

Install the plugin in Cursor and connect its Listen Notes MCP server when prompted. Sign in through Listen Notes and choose a Podcast API app. An API account owner can create an app during authorization; team members can select an existing app available to their team. Do not paste API keys or access tokens into chat.

The MCP service is free. Podcast API requests use the selected app's existing plan and billing. Some fields require a PRO or ENTERPRISE API plan. See [API access information](https://www.listennotes.com/api/mcp/access/), the [privacy policy](https://www.listennotes.com/privacy/), and the [terms of service](https://www.listennotes.com/terms/).

## Try it

- Find podcast interviews about bootstrapping a startup.
- Find technology podcasts with fewer than 30 episodes and available producer contacts.
- Find podcast episodes mentioning Cloudflare in the past 30 days.
- Find the latest episodes in my largest playlist.

The tools are read-only. They can retrieve available transcripts and playlist data, but do not send outreach, change playlists, schedule alerts, or transcribe uploaded audio. Media monitoring is an on-demand search, not a scheduled alert. Results and supported interactive cards depend on the connected account, the server, and the Cursor client.

## Local development

From the repository root, run `python scripts/build_plugin.py --target cursor` to synchronize the bundled research skill and build a ZIP. To test the plugin in Cursor, copy this entire plugin directory to `~/.cursor/plugins/local/podcast-search-by-listen-notes`, reload Cursor, and check **Customize** for the skill and MCP server. Connect the server through Cursor's OAuth flow. See [Cursor's plugin documentation](https://cursor.com/docs/plugins) for local plugin settings and installation.

The repository's `skills/podcast-mcp/` directory is the source for the bundled skill. After changing it, rebuild the Cursor package and commit the synchronized files. For support, contact [hello@listennotes.com](mailto:hello@listennotes.com).
