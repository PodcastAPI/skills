# Podcast Search by Listen Notes for Devin

Find podcast episodes, research guest interviews, and discover potential PR leads using the Listen Notes podcast database. The plugin also supports on-demand searches for brand mentions and can retrieve transcripts when available.

## Install and connect

1. In Devin Cloud, go to **Customize → Plugins → Add plugin** and upload the plugin ZIP. For local development with the Devin CLI, run `devin plugins install --local ./plugins/podcast-search-devin` from the repository root.
2. In Devin Cloud, open **Customize → MCPs**, select the plugin's `listen-notes` server, and choose **Connect**. In the CLI, run `devin mcp login` and select the same server.
3. Sign in to Listen Notes and select a Podcast API app. You can use an app from your own API account or one available through your API team.
4. Start a new Devin session and ask a podcast research question.

The MCP connection is free. Lookup requests use the selected app's existing Podcast API permissions, quota, and billing. See [Podcast API access information](https://www.listennotes.com/api/mcp/access/).

## Try it

- Find three podcast interviews with Patrick Collison and link to each episode.
- Find podcasts about developer tools with fewer than 30 published episodes and list any available producer contacts.
- Find episodes published in the last 30 days that mention Cloudflare in the title or description.

## Build from source

Run `python scripts/build_plugin.py --target devin` from the repository root. The command refreshes the bundled research skill and writes the versioned ZIP to `dist/`.

Published by Listen Notes, Inc. [Support](https://www.listennotes.com/contact/) · [Privacy Policy](https://www.listennotes.com/privacy/) · [Terms of Service](https://www.listennotes.com/terms/)
