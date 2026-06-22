# watsonx Orchestrate ADK — Complete Guide

This guide covers how to use the **IBM watsonx Orchestrate Agent Development Kit (ADK)** — the `orchestrate` CLI — to build, deploy, and manage AI agents. Examples are based on the Telkom Indonesia demo environment.

---

## 1. What is the ADK?

The ADK (`ibm-watsonx-orchestrate`) is a Python package that provides:
- **`orchestrate` CLI** — manage environments, import tools/agents, deploy, chat
- **`@tool` decorator** — wrap Python functions as callable agent tools
- **YAML agent spec** — define agent behavior, LLM, instructions, and tool references

**Core concept:**
```
Python function (@tool decorator)
        ↓  orchestrate tools import
Tool registered in WXO cloud
        ↓  referenced in agent YAML
Agent uses tool when needed
        ↓  orchestrate agents import + deploy
Agent live in WXO instance
```

---

## 2. Installation

Requires **Python 3.11** (not 3.13 — grpcio compatibility).

```bash
# Create venv with Python 3.11
python3.11 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Install ADK
pip install ibm-watsonx-orchestrate
```

Verify:
```bash
orchestrate --version
orchestrate --help
```

---

## 3. Environment Setup

The ADK uses "environments" — named pointers to a WXO instance with an API key.

### 3.1 Create an environment

```bash
orchestrate env add \
  --name <env-name> \
  --url  <wxo-instance-url>
```

Example for this project:
```bash
orchestrate env add \
  --name telkom-demo \
  --url  https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/f3c996f2-fd0f-464b-8b9b-24f5669687a9
```

### 3.2 Activate with API key

```bash
orchestrate env activate <env-name> --api-key <api-key>
```

Example:
```bash
orchestrate env activate telkom-demo --api-key VHR3tdu2KGa-44CpaexaVC3ijostQJ2pHdNStt5Br6ln
```

### 3.3 Activate using a .env file (recommended)

Create a `.env` file:
```
WXO_URL=https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/f3c996f2-fd0f-464b-8b9b-24f5669687a9
WXO_API_KEY=VHR3tdu2KGa-44CpaexaVC3ijostQJ2pHdNStt5Br6ln
```

Then activate:
```bash
orchestrate env activate local --env-file .env
```

> `local` is a special built-in env name that reads from the `.env` file directly.

### 3.4 List / check environments

```bash
orchestrate env list
```

---

## 4. Writing Tools

A tool is a Python function decorated with `@tool`. The docstring becomes the tool's description — write it clearly because the LLM reads it to decide when to call the tool.

### 4.1 Minimal tool example

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_customer_count(region: str) -> str:
    """
    Get the total number of customers in a given region.

    :param region: The region name (e.g. 'Jakarta', 'Surabaya')
    :returns: JSON string with customer count
    """
    # your logic here
    return '{"region": "Jakarta", "count": 12450}'
```

### 4.2 Tool rules

| Rule | Detail |
|------|--------|
| **Return type** | Always return `str` — serialize dicts/lists with `json.dumps()` |
| **Docstring** | Required. First line = tool description. `:param` lines document each argument. `:returns:` documents the output. |
| **Type hints** | Required on all parameters — ADK uses them to generate the JSON schema |
| **No `*args`/`**kwargs`** | All parameters must be explicitly named |
| **Error handling** | Catch exceptions and return them as JSON strings — never raise from a tool |

### 4.3 Full tool pattern (with credentials + error handling)

```python
import os
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# Hardcode credentials as defaults — WXO cloud won't have local env vars
API_KEY = os.environ.get("MY_API_KEY", "your-default-key-here")

@tool
def query_data(sql: str, limit: int = 100) -> str:
    """
    Execute a read-only SQL query and return results.

    :param sql: A valid SELECT SQL statement
    :param limit: Maximum rows to return (default: 100)
    :returns: JSON string with query results
    """
    try:
        # your logic
        results = [{"id": 1, "name": "example"}]
        return json.dumps({"row_count": len(results), "results": results})
    except Exception as e:
        return json.dumps({"error": str(e)})
```

> **Important about credentials:** When tools run inside WXO cloud, they don't have access to your local environment variables. Hardcode credentials as default parameter values with `os.environ.get("KEY", "default-value")`.

### 4.4 Multiple tools in one file

You can define multiple `@tool` functions in a single `.py` file. All will be imported together.

```python
@tool
def list_schemas(catalog: str) -> str:
    """List all schemas in a catalog. :param catalog: catalog name :returns: JSON list"""
    ...

@tool
def list_tables(catalog: str, schema: str) -> str:
    """List all tables in a schema. :param catalog: catalog name :param schema: schema name :returns: JSON list"""
    ...
```

---

## 5. Importing Tools

```bash
orchestrate tools import \
  -f <path-to-tool-file.py> \
  -r <path-to-requirements.txt>
```

### 5.1 Requirements file

Create a separate `requirements.txt` for each tool file. Keep it minimal — heavy dependencies (torch, sentence-transformers) slow down deployment and cause failures if bundled with light tools.

```
# requirements_watsonxdata.txt
presto-python-client==0.8.4
python-dotenv==1.0.0
```

```
# requirements_milvus.txt
pymilvus==2.4.9
sentence-transformers==3.0.1
python-dotenv==1.0.0
```

### 5.2 Import example

```bash
# Light tools (Presto / SQL)
orchestrate tools import \
  -f tools/watsonxdata_tools.py \
  -r tools/requirements_watsonxdata.txt

# Heavy tools (Milvus / embeddings)
orchestrate tools import \
  -f tools/milvus_tool.py \
  -r tools/requirements_milvus.txt
```

### 5.3 List deployed tools

```bash
orchestrate tools list
orchestrate tools list -v   # verbose — shows tool descriptions
```

### 5.4 Delete a tool

```bash
orchestrate tools delete --name <tool-name>
```

---

## 6. Writing Agent YAML

Agents are defined in YAML files. The `instructions` field is the system prompt — write it in detail.

### 6.1 Full YAML spec

```yaml
spec_version: v1
kind: native
name: My_Agent_Name          # must be unique, no spaces — use underscores
llm: watsonx/ibm/granite-3-8b-instruct   # or ibm/granite-3-3b-instruct
style: default
description: |
  One-paragraph description of what this agent does.
  Shown in the WXO UI agent selector.

instructions: |
  ## IDENTITY
  You are a [role] that [purpose].

  ## WHAT YOU CAN DO
  - List capabilities here

  ## HOW TO USE YOUR TOOLS
  - tool_name_1: use when [condition]
  - tool_name_2: use when [condition]

  ## RESPONSE FORMAT
  - Always respond with [format]
  - Never do [anti-pattern]

tools:
  - tool_name_1      # must match the function name in the .py file
  - tool_name_2

hide_reasoning: false       # show chain-of-thought (good for demos)
memory_enabled: false       # true = remembers conversation history
```

### 6.2 Available LLMs

| Model ID | Notes |
|----------|-------|
| `watsonx/ibm/granite-3-8b-instruct` | Default — good balance of speed and quality |
| `watsonx/ibm/granite-3-3b-instruct` | Faster, lighter |
| `watsonx/ibm/granite-3-2b-instruct` | Smallest, fastest |
| `watsonx/meta-llama/llama-3-3-70b-instruct` | Largest, best reasoning |

### 6.3 Orchestrator agent (with collaborators)

An orchestrator agent routes to specialist agents — it has no tools of its own, only `collaborators`:

```yaml
spec_version: v1
kind: native
name: Master_Assistant
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: |
  Main entry point. Routes questions to the right specialist.

instructions: |
  You have two specialist agents:
  1. SQL_Agent — for database questions
  2. RAG_Agent — for document questions

  Route based on the user's question type.

collaborators:
  - SQL_Agent      # must match the name: field of the sub-agent
  - RAG_Agent

hide_reasoning: false
memory_enabled: true    # orchestrator keeps conversation context
```

> Collaborator agents must be imported and deployed **before** the orchestrator.

---

## 7. Importing and Deploying Agents

### 7.1 Import an agent

```bash
orchestrate agents import -f agents/my_agent.yaml
```

Import reads the YAML and registers the agent. After import it is not yet live.

### 7.2 Deploy an agent

```bash
orchestrate agents deploy --name My_Agent_Name
```

Deploy makes the agent available in the WXO UI and via API.

### 7.3 Import + deploy in sequence (recommended order)

Always deploy specialist agents before the orchestrator:

```bash
# 1. Import tools first
orchestrate tools import -f tools/my_tool.py -r tools/requirements.txt

# 2. Import and deploy specialist agents
orchestrate agents import -f agents/specialist_agent.yaml
orchestrate agents deploy --name Specialist_Agent

# 3. Import and deploy orchestrator last
orchestrate agents import -f agents/orchestrator.yaml
orchestrate agents deploy --name Master_Assistant
```

### 7.4 List agents

```bash
orchestrate agents list
orchestrate agents list -v    # verbose — shows descriptions and IDs
```

### 7.5 Delete an agent

```bash
orchestrate agents delete --name My_Agent_Name
```

### 7.6 Re-deploy after changes

After editing a `.yaml` file, re-import (import overwrites the existing definition):

```bash
orchestrate agents import -f agents/my_agent.yaml
```

After editing a `.py` tool file, re-import the tool:

```bash
orchestrate tools import -f tools/my_tool.py -r tools/requirements.txt
```

---

## 8. Testing Agents

### 8.1 Via WXO UI (recommended)

Open in browser and click **AI assistant** in the sidebar:
```
https://us-south.watson-orchestrate.cloud.ibm.com/instances/f3c996f2-fd0f-464b-8b9b-24f5669687a9
```

Select an agent from the dropdown and start chatting.

### 8.2 Via CLI (interactive terminal only)

`orchestrate chat ask` requires an interactive terminal with stdin. Run it directly in your shell — it cannot be piped or run from a script:

```bash
orchestrate chat ask --agent-name My_Agent_Name
```

You will see a `>` prompt. Type your question and press Enter. Type `exit` or Ctrl+C to quit.

> **Do not** run `orchestrate chat ask` in the background, via subprocess, or piped — it will give an EOF error.

---

## 9. Project Structure (recommended layout)

```
wxo-agentic/
├── .env                           # WXO_URL, WXO_API_KEY, and tool credentials
├── .env.example                   # template (commit this, not .env)
├── deploy.sh                      # one-shot deploy script
│
├── tools/
│   ├── my_sql_tool.py             # @tool functions for SQL queries
│   ├── my_rag_tool.py             # @tool functions for vector search
│   ├── requirements_sql.txt       # lean deps for SQL tool
│   └── requirements_rag.txt       # heavier deps for RAG tool
│
└── agents/
    ├── specialist_agent_1.yaml    # SQL specialist
    ├── specialist_agent_2.yaml    # RAG specialist
    └── orchestrator.yaml          # master agent with collaborators
```

**Key rule:** one `requirements.txt` per tool file, kept as lean as possible.

---

## 10. Deploy Script (one-shot automation)

The project's `deploy.sh` deploys everything in the right order:

```bash
cd wxo-agentic
chmod +x deploy.sh
./deploy.sh
```

What it does:
1. Loads `.env`
2. Validates required vars (`WXO_URL`, `WXO_API_KEY`, `WXD_API_KEY`)
3. Installs `ibm-watsonx-orchestrate`
4. Connects to the WXO instance
5. Imports all tools
6. Imports and deploys all agents
7. Lists deployed agents

To write your own deploy script:

```bash
#!/bin/bash
set -e

# Load env
export $(grep -v '^#' .env | xargs)

# Activate environment
orchestrate env add -n my-env -u "$WXO_URL" 2>/dev/null || true
orchestrate env activate my-env --api-key "$WXO_API_KEY"

# Deploy tools
orchestrate tools import -f tools/my_tool.py -r tools/requirements.txt

# Deploy agents (specialists first, orchestrator last)
orchestrate agents import -f agents/specialist.yaml
orchestrate agents deploy --name Specialist_Agent

orchestrate agents import -f agents/orchestrator.yaml
orchestrate agents deploy --name Master_Agent

echo "Done. Agents:"
orchestrate agents list -v
```

---

## 11. This Project's Agents (Telkom Demo)

### File locations

```
wxo-agentic/
├── .env                                   ← WXO + Presto + Milvus credentials
├── tools/watsonxdata_tools.py             ← 4 Presto tools
├── tools/milvus_tool.py                   ← 1 Milvus search tool
├── tools/requirements_watsonxdata.txt     ← presto-python-client only
├── tools/requirements_milvus.txt          ← pymilvus + sentence-transformers
├── agents/nl2sql_agent.yaml              ← NL2SQL specialist
├── agents/rag_agent.yaml                 ← RAG specialist
└── agents/telkom_assistant.yaml          ← master orchestrator
```

### Tool → agent wiring

```
watsonxdata_list_schemas    ┐
watsonxdata_list_tables     ├── NL2SQL_Data_Analyst
watsonxdata_describe_table  │
watsonxdata_execute_select  ┘

milvus_search_documents ──── Equity_Research_RAG_Agent

NL2SQL_Data_Analyst      ┐
Equity_Research_RAG_Agent┘── Telkom_Data_Assistant (orchestrator)
```

### Quick redeploy (after any change)

```bash
cd wxo-agentic
source venv/bin/activate
orchestrate env activate local --env-file .env

# Re-import only what changed:
orchestrate tools import -f tools/watsonxdata_tools.py -r tools/requirements_watsonxdata.txt
orchestrate agents import -f agents/nl2sql_agent.yaml
```

### After adding new tables to watsonx.data

Edit `agents/nl2sql_agent.yaml` — add the new schema/table to the `DATA ENVIRONMENT` and `KEYWORD MAPPING` sections in `instructions:`, then:

```bash
orchestrate agents import -f agents/nl2sql_agent.yaml
```

---

## 12. Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `uv install: exit status 1` | Heavy deps in requirements.txt (torch, grpcio) exceed install time | Split into separate lean requirements files per tool |
| `401 Malformed decoded credentials` | Tool running in WXO cloud can't read local env vars | Hardcode credentials as default values in `os.environ.get("KEY", "hardcoded-default")` |
| `EOF when reading a line` | `orchestrate chat ask` run from script/background | Must run in interactive terminal directly |
| `collaborator not found` | Orchestrator imported before specialist agents | Always import/deploy specialists first |
| `tool not found` | Agent YAML references tool name that doesn't match function name | Tool name = Python function name exactly (no class, no module prefix) |
| `grpcio build error on Python 3.13` | pymilvus requires grpcio which doesn't support Python 3.13 | Use Python 3.11 venv |

---

*Last updated: 2026-06-08 | Based on ibm-watsonx-orchestrate ADK*
