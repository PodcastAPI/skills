# Connect Listen Notes MCP

Use this reference only when the Listen Notes tools are unavailable, authorization needs renewal, or the user asks how to connect. Reuse a working connection, including a user-selected local server, rather than adding another one.

## Connection details

| Setting | Value |
| --- | --- |
| Display name | Podcast Search by Listen Notes |
| Remote server URL | `https://mcp.listennotes.com/mcp/` |
| Transport | Streamable HTTP |
| Authentication | OAuth |
| Publisher | Listen Notes, Inc. |
| Contact | hello@listennotes.com |

1. Use the client's supported custom remote MCP connection flow. If the client can act on the skill's declared MCP dependency, follow its connection prompt. Otherwise add the remote server in the client's MCP/connector settings. A skill installation alone does not guarantee tool availability.
2. Let the user complete sign-in and consent on Listen Notes. They select an existing API app or create a new API app there. Never ask them to paste API keys, OAuth codes, passwords, or tokens into chat or skill files.
3. The MCP server uses the Production API and the selected app's existing billing; the consent screen has no environment selector. Users without an API account can get an API key through [Podcast API pricing](https://www.listennotes.com/api/pricing/).
4. Return to the client, refresh its tool list or reopen the conversation if required by that client, and confirm the tools are available. When permitted by the user's environment, call `get_profile` to check the connection; this makes no Podcast API request. Do not claim success until the call succeeds.

## Troubleshooting

- **No tools:** confirm the server is connected and enabled for the current client, mode, workspace, and conversation. Follow that client's current setup documentation; do not assume all surfaces support custom MCP servers.
- **OAuth failed or expired:** restart Connect from the client using its supported reconnect flow. Do not reuse an old authorization URL or extract tokens from local files.
- **Profile works but an API tool fails:** profile is a connection check, not an API entitlement check. Report the returned error. For an authorization error, reconnect and let the user verify the selected API app. A plan restriction or missing transcript is a separate issue.

The exact client settings and available connection flows can change. Use the client's own current documentation for UI-specific steps. For account-specific issues, contact [hello@listennotes.com](mailto:hello@listennotes.com).
