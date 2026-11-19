# Podcast Search by Listen Notes for Antigravity

Find podcasts and episodes, research guest interviews, find available producer contacts, and search for mentions of a person, company, or topic. This plugin combines the `podcast-mcp` research skill with the hosted Listen Notes MCP server.

## Connect your account

Connect the Listen Notes MCP server when prompted. Sign in through Listen Notes and choose a Podcast API app. API account owners can create an app during authorization; team members can select an existing app available to their team. In Antigravity CLI, use `/mcp` to select the server and authenticate. If prompted, paste the authorization code from the Antigravity callback page into the CLI prompt. Do not paste credentials or authorization codes into a conversation.

The MCP service is free. Podcast API requests use the selected app's existing plan and billing. Some fields require a PRO or ENTERPRISE API plan. See [API access information](https://www.listennotes.com/api/mcp/access/), the [privacy policy](https://www.listennotes.com/privacy/), and the [terms of service](https://www.listennotes.com/terms/).

## Try it

- Find podcast interviews about bootstrapping a startup.
- Find technology podcasts with fewer than 30 episodes and available producer contacts.
- Find podcast episodes mentioning Cloudflare in the past 30 days.

The tools are read-only. They can retrieve available transcripts and playlist data, but do not send outreach, change playlists, schedule alerts, or transcribe uploaded audio. Media monitoring is an on-demand search. Results depend on the connected account and its API access.

## Local development

From the repository root, run `python scripts/build_plugin.py --target antigravity` to synchronize the bundled research skill and build a ZIP. Run `agy plugin validate --strict plugins/podcast-search-antigravity` to validate the plugin. The canonical skill is `skills/podcast-mcp/`; commit synchronized plugin files when it changes. Contact [hello@listennotes.com](mailto:hello@listennotes.com) for support.
