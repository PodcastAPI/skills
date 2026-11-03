# Podcast API Skills

Agent Skills for podcast research and building secure applications with the [Listen Notes Podcast API](https://www.podcastapi.com/).

Published by **Listen Notes, Inc.** Questions? Contact [hello@listennotes.com](mailto:hello@listennotes.com).

## Choose a skill

| Skill | Purpose | Example |
| --- | --- | --- |
| [`podcast-mcp`](skills/podcast-mcp/SKILL.md) — Podcast Search by Listen Notes | Research using connected MCP tools: podcasts, episodes, interviews, recommendations, available producer contacts, playlists, and transcripts | "Find startup podcasts with fewer than 30 episodes and available email contacts." |
| [`podcast-api`](skills/podcast-api/SKILL.md) | Build, debug, and explain applications using REST endpoints or official SDKs | "Build a podcast search feature in Python." |

The research skill requires a connected Listen Notes MCP server. It guides tool use; it does not provide a new card UI or audio player. See [connection instructions](skills/podcast-mcp/references/connection.md).

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

### Claude Code Plugin

The existing developer plugin remains a separate, developer-only install:

```text
/plugin marketplace add podcastapi/skills
/plugin install podcast-api@podcastapi
```

The marketplace entry explicitly selects `skills/podcast-api`, so adding the standalone research skill does not add it to this plugin. A separate research plugin and public marketplace submissions are planned for later milestones. To use `podcast-mcp` now, install it as a standalone skill and connect the remote MCP server through the client's supported flow.

### Manual Installation

Clone the repository and copy the complete `skills/podcast-mcp` or `skills/podcast-api` folder into the appropriate global skill directory:

| Agent | Global skill directory |
| --- | --- |
| OpenAI Codex | `$HOME/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Compatible agents can install the same folder in their documented Agent Skills directory. Keep `references/` and, when present, `agents/` with `SKILL.md`.

## Sources

For research, current MCP tool schemas and `getWorkflowGuide` are the sources of truth for supported arguments and task recipes. The guide is free and makes no Podcast API request. Returned metadata and exact Listen Notes links provide evidence for the answer. Mock mode returns fixed sample data without API quota usage; Production uses the selected API app's existing billing.

For development, the skill keeps procedural guidance local while treating these live resources as authoritative:

- [OpenAPI YAML](https://listen-api.listennotes.com/api/v2/openapi.yaml) for endpoint contracts
- [API tutorials](https://www.listennotes.com/api/tutorials/) for application workflows
- [API FAQ](https://www.listennotes.com/api/faq/) and [billing FAQ](https://www.listennotes.com/api/billing-faq/) for common questions
- [Pricing](https://www.listennotes.com/api/pricing/) and [terms](https://www.listennotes.com/api/terms/) for current plan and policy details

Exact request and response schemas are intentionally not copied into this repository.

## Development

CI validates both skills against the [Agent Skills specification](https://agentskills.io/specification), checks metadata and documentation links, and smoke-tests each skill's installation for Codex, Claude Code, and Cursor. Repository contract checks also verify the developer plugin's skill selection and the research skill's MCP dependency.

Representative development cases live in `evals/cases.json`; research activation and workflow cases live in `evals/podcast-mcp.json`. These are review scenarios with expected behavior, not automatically measured model results. They require no production API key or model secret. Validate actual client activation separately; a valid package does not guarantee tool selection.
