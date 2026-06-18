# PodcastAPI Skills

Agent Skills for building secure applications with the [Listen Notes Podcast API](https://www.podcastapi.com/).

The `podcast-api` skill helps coding agents inspect an existing project, select the right endpoint, keep credentials server-side, implement pagination and error handling, test against the mock server, and answer API or billing questions from authoritative sources.

## Install

### Skills CLI

```bash
npx skills add https://github.com/PodcastAPI/skills
```

### OpenAI Codex

From Codex, use the built-in skill installer and ask it to install this repository's `podcast-api` skill:

```text
$skill-installer
Install the podcast-api skill from https://github.com/PodcastAPI/skills/tree/main/skills/podcast-api
```

Or install it non-interactively with the Skills CLI:

```bash
npx skills add https://github.com/PodcastAPI/skills \
  --skill podcast-api \
  --agent codex \
  --global \
  --yes
```

For a manual user-wide installation, copy the skill directory to `$HOME/.agents/skills/podcast-api`. Codex detects skill changes automatically; restart Codex if the skill does not appear. Run `/skills` or mention `$podcast-api` in a prompt to invoke it explicitly.

See the official [Codex Agent Skills documentation](https://developers.openai.com/codex/skills).

### Claude Code Plugin

```text
/plugin marketplace add podcastapi/skills
/plugin install podcast-api@podcastapi
```

### Manual Installation

Clone the repository and copy `skills/podcast-api` into the appropriate global skill directory:

| Agent | Global skill directory |
| --- | --- |
| OpenAI Codex | `$HOME/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Compatible agents can install the same folder in their documented Agent Skills directory.

## Sources

The skill keeps procedural guidance local while treating these live resources as authoritative:

- [OpenAPI YAML](https://listen-api.listennotes.com/api/v2/openapi.yaml) for endpoint contracts
- [API tutorials](https://www.listennotes.com/api/tutorials/) for application workflows
- [API FAQ](https://www.listennotes.com/api/faq/) and [billing FAQ](https://www.listennotes.com/api/billing-faq/) for common questions
- [Pricing](https://www.listennotes.com/api/pricing/) and [terms](https://www.listennotes.com/api/terms/) for current plan and policy details

Exact request and response schemas are intentionally not copied into this repository.

## Development

CI validates the skill against the [Agent Skills specification](https://agentskills.io/specification), checks documentation links, and smoke-tests installation for Codex, Claude Code, and Cursor. Representative prompts and expected safety invariants live in `evals/cases.json`; they require no production API key or model secret.
