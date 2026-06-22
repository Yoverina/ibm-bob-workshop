# 🚀 Quick Setup: Instana MCP Server with Bob

> **Duration**: ~5 minutes  
> **For**: Workshop participants who want to use Instana MCP tools in Bob IDE

## Prerequisites

- Python 3.8+ installed
- Bob IDE installed
- Node.js installed (for npx command)
- Instana credentials (provided in workshop)

---

## Step 1: Install Instana MCP Server

Open your terminal and run:

```bash
pip install mcp-instana
```

Verify installation:
```bash
mcp-instana --help
```

---

## Step 2: Configure Bob to Auto-Start MCP

### Option A: Project-Level (Recommended for Workshop)

1. Create `.bob` folder in your project root (if not exists)
2. Create/edit `.bob/bob_config.json`:

```json
{
  "mcpServers": {
    "Instana MCP Server": {
      "command": "mcp-instana",
      "args": ["--transport", "stdio"],
      "env": {
        "INSTANA_BASE_URL": "https://instana.example.com",
        "INSTANA_API_TOKEN": "your_instana_api_token",
      }
    }
  }
}
```

### Option B: Global (All Projects)

Go to settings/MCP/Global MCPs and click open. Configure themcp_settings.json`  
Use the same JSON content as above.

---

## Step 3: Restart Bob

1. Close Bob IDE completely
2. Reopen Bob IDE
3. Click the MCP dropdown (top-right corner)
4. Verify "Instana MCP Server" shows a **green dot** ✅

---

## Step 4: Test It

In Bob chat, try:

```
List all applications from Instana in the last 24 hours
```

or

```
Show me critical incidents from the last 6 hours
```

---

## Troubleshooting

### ❌ "command not found: mcp-instana"

Find the full path:
```bash
which mcp-instana
```

Update config with full path:
```json
"command": "/full/path/to/mcp-instana"
```

### ❌ Red dot in MCP dropdown

1. Check credentials in config
2. Verify `pip install mcp-instana` succeeded
3. Restart Bob IDE
4. Check Bob logs: Help → Toggle Developer Tools → Console

### ❌ "Connection refused"

Ensure you're using `stdio` transport mode (not HTTP mode).

---

## What You Can Do Now

With Instana MCP configured, Bob can:

- ✅ Query infrastructure metrics (JVM, Kubernetes, Docker)
- ✅ Analyze incidents and events
- ✅ Fetch application performance data
- ✅ Generate root cause analysis reports
- ✅ Access custom dashboards
- ✅ Monitor website beacons

**Example prompts:**
- "Analyze the top 5 critical incidents"
- "Show me JVM heap usage for host galactica1"
- "List all Kubernetes pods with high CPU"
- "Generate an incident report for the last 24 hours"

---

## Next Steps

- Switch to **SRE mode** in Bob for advanced incident analysis
- Try the main workshop lab: [README.md](./README.md)
- Explore full MCP capabilities: [INSTANA-MCP.md](./INSTANA-MCP.md)

---

*Made with Bob 🤖*