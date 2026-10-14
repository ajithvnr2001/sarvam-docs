---
url: https://docs.sarvam.ai/_mcp/server/
title: https://docs.sarvam.ai/_mcp/server/
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:33.455156+00:00
---

# https://docs.sarvam.ai/_mcp/server/

> Source: https://docs.sarvam.ai/_mcp/server/

{"name":"fern-docs-mcp-server","version":"1.0.0","description":"MCP server for https://docs.sarvam.ai documentation. Provides AI-powered search over the documentation.","transport":"streamable-http","tools":[{"name":"searchDocs","description":"Search the documentation at https://docs.sarvam.ai. Returns relevant doc passages with source URLs.","annotations":{"title":"Search docs.sarvam.ai Docs","readOnlyHint":true},"inputSchema":{"type":"object","properties":{"query":{"type":"string","description":"The search query to run against the docs"},"topK":{"type":"integer","description":"How many results to return (default 8, max 20)"}},"required":["query"]}}],"usage":{"claudeCode":"claude mcp add --transport http fern_mcp_docs-sarvam-ai https://docs.sarvam.ai/_mcp/server","cursor":"Add \"https://docs.sarvam.ai/_mcp/server\" to your MCP server configuration","generic":"POST JSON-RPC 2.0 messages to this URL"}}
