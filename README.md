# Podcast API Skills

Agent Skills for podcast research and building secure applications with the [Listen Notes Podcast API](https://www.podcastapi.com/).

Published by **Listen Notes, Inc.** Questions? Contact [hello@listennotes.com](mailto:hello@listennotes.com).

## Choose a skill

| Skill | Purpose | Example |
| --- | --- | --- |
| [`podcast-mcp`](skills/podcast-mcp/SKILL.md) — Podcast Search by Listen Notes | Research using connected MCP tools: podcasts, episodes, interviews, recommendations, available producer contacts, playlists, and transcripts | "Find startup podcasts with fewer than 30 episodes and available email contacts." |
| [`podcast-api`](skills/podcast-api/SKILL.md) | Build, debug, and explain applications using REST endpoints or official SDKs | "Build a podcast search feature in Python." |

The research skill requires a connected Listen Notes MCP server. Supported MCP Apps clients can display podcast and episode cards with available source/contact links, Listen Notes listening links, and manual audio download links when the server exposes the card tools. Other clients retain text and source links. See [connection instructions](skills/podcast-mcp/references/connection.md).

The developer skill covers endpoint and SDK selection, secure credentials, pagination, mock testing, and API or billing documentation. It also covers using playlists as a headless CMS: create collections, add curator notes, edit entries, and permanently delete collections after confirmation in the application's UI. The MCP server supports playlist reads, not writes.

## Install

### Skills CLI

```bash
npx skills add PodcastAPI/skills
```

Select `podcast-mcp` for research, `podcast-api` for development, or both. To install a specific skill, use `--skill podcast-mcp` or `--skill podcast-api`.

### OpenAI Codex

From Codex, use the built-in skill installer and ask it to install the research skill:

```text
$skill-installer
Install the podcast-mcp skill from https://github.com/PodcastAPI/skills/tree/main/skills/podcast-mcp
```

Or install it non-interactively with the Skills CLI:

```bash
npx skills add https://github.com/PodcastAPI/skills \
  --skill podcast-mcp \
  --agent codex \
  --global \
  --yes
```

For the developer skill, substitute `podcast-api` in either installation method.

For a manual user-wide installation, copy the complete skill directory to `$HOME/.agents/skills/podcast-mcp` or `$HOME/.agents/skills/podcast-api`. Run `/skills` or mention `$podcast-mcp` or `$podcast-api` in a prompt to invoke it explicitly.

The research skill declares the hosted MCP dependency in `agents/openai.yaml`. Complete the client's supported OAuth connection flow before using its tools. Reuse an existing connection if one is already configured; do not add a duplicate solely because its local server label differs.

See the official [Codex Agent Skills documentation](https://developers.openai.com/codex/skills).

### Claude plugins

**Podcast Search by Listen Notes** combines the research skill with the hosted OAuth MCP connection. In Claude.ai or Claude Desktop, open **Customize → Plugins → Add → Add marketplace**, enter `https://github.com/PodcastAPI/skills`, and add the research plugin. Open its **Connectors** tab to add or connect Listen Notes, then complete OAuth. A packaged ZIP can also be installed with **Add → Upload plugin**. Installation does not authorize an account; reuse an existing working connector for the same server URL.

For Claude Code:

```text
/plugin marketplace add PodcastAPI/skills
/plugin install listennotes-podcast-search@podcastapi
```

Use `/mcp` to check the connection and complete OAuth, then invoke `/listennotes-podcast-search:podcast-mcp` or describe the research task. See the [Claude plugin documentation](plugins/podcast-search-claude/README.md) for features, account requirements, and examples. Plugin availability depends on the Claude plan and organization settings.

To build the Claude ZIP:

```bash
python scripts/build_plugin.py --target claude
```

The separate developer plugin provides the API integration skill:

```text
/plugin marketplace add podcastapi/skills
/plugin install podcast-api@podcastapi
```

The developer plugin's marketplace entry includes only `skills/podcast-api`; it does not install the research skill or connect an MCP server.

### ChatGPT plugin package

The **Podcast Search by Listen Notes** package combines the research skill with the hosted OAuth MCP connection.

Workspace admins can import the GitHub marketplace from **Admin → Plugins → Add → Import marketplace**:

| Field | Value |
| --- | --- |
| Source | `https://github.com/PodcastAPI/skills` |
| Path | Leave empty (repository root) |
| Branch, tag, or commit | `main` |

The OpenAI marketplace in `.agents/plugins/marketplace.json` provides **Podcast Search by Listen Notes** for research and the separate **podcast-api** skill for API development. Select the research plugin and complete OAuth when prompted. Each user connects their own Listen Notes account; importing a marketplace does not authorize anyone's account.

GitHub imports manage workspace plugins and do not publish them to the public directory. Imported MCP plugins may be marked **Desktop only**, even when the server is remote. Check the import results and the client's supported surfaces. See [OpenAI's marketplace import documentation](https://learn.chatgpt.com/docs/enterprise/plugin-management).

To build the research plugin's ZIP:

```bash
python scripts/build_plugin.py
uv run --with PyYAML==6.0.3 python scripts/validate.py
```

The build refreshes the plugin's bundled research skill from `skills/podcast-mcp`, then writes a versioned archive to `dist/` with the hosted MCP connection and light and dark theme logos. Commit the refreshed skill files with any canonical skill changes so GitHub imports and ZIP installs receive the same content. See the [plugin documentation](plugins/podcast-search-openai/README.md) for features, account setup, and package contents.

### Manual Installation

Clone the repository and copy the complete `skills/podcast-mcp` or `skills/podcast-api` folder into the appropriate global skill directory:

| Agent | Global skill directory |
| --- | --- |
| OpenAI Codex | `$HOME/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Compatible agents can install the same folder in their documented Agent Skills directory. Keep `references/` and, when present, `agents/` with `SKILL.md`.

## Sources

For research, current MCP tool schemas and `getWorkflowGuide` are the sources of truth for supported arguments and task recipes. The guide is free and makes no Podcast API request. Returned metadata and exact Listen Notes links provide evidence for the answer. The MCP server uses the Production API and the selected API app's existing billing.

For development, the skill keeps procedural guidance local while treating these live resources as authoritative:

- [OpenAPI YAML](https://listen-api.listennotes.com/api/v2/openapi.yaml) for endpoint contracts
- [API tutorials](https://www.listennotes.com/api/tutorials/) for application workflows
- [API FAQ](https://www.listennotes.com/api/faq/) and [billing FAQ](https://www.listennotes.com/api/billing-faq/) for common questions
- [Pricing](https://www.listennotes.com/api/pricing/) and [terms](https://www.listennotes.com/api/terms/) for current plan and policy details

Exact request and response schemas are intentionally not copied into this repository.

## Development

CI validates both skills against the [Agent Skills specification](https://agentskills.io/specification), checks metadata and documentation links, and smoke-tests each skill's installation for Codex, Claude Code, and Cursor. Repository contract checks also verify the developer plugin's skill selection and the research skill's MCP dependency.

Example evaluation scenarios live in `evals/cases.json` for API integrations and `evals/podcast-mcp.json` for research workflows. They describe expected skill activation, tool selection, pagination, and error handling. Repository checks validate their structure without requiring production credentials.
