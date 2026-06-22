# 🔧 Workshop: AI-Powered SRE with IBM Bob and Instana

> **Complete Workshop Guide**  
> **Duration**: ~60–90 minutes  
> **Level**: Beginner–Intermediate  
> **Mode**: Bob SRE Agent (`🔧 SRE`)

This comprehensive workshop guide teaches you how to use **Bob** — an AI Site Reliability Engineer — with **IBM Instana** to perform intelligent incident analysis, infrastructure monitoring, and automated root cause analysis.

---

## 📋 Table of Contents

1. [Workshop Overview](#-workshop-overview)
2. [What You Will Learn](#-what-you-will-learn)
3. [Prerequisites](#-prerequisites)
4. [Part 1: Basic Setup](#-part-1-basic-setup)
5. [Part 2: Instana MCP Integration](#-part-2-instana-mcp-integration)
6. [Part 3: Incident Analysis Lab](#-part-3-incident-analysis-lab)
7. [Part 4: Advanced MCP Capabilities](#-part-4-advanced-mcp-capabilities)
8. [Example Prompts for BOB x Instana](#-example-prompts-for-bob-x-instana)
9. [Troubleshooting](#-troubleshooting)
10. [What's Next](#-whats-next)

---

## 🎯 Workshop Overview

This workshop is divided into four parts:

1. **Basic Setup**: Clone the repository and configure Instana credentials
2. **Instana MCP Integration**: Connect Bob to Instana's MCP server for real-time data access
3. **Incident Analysis Lab**: Use Bob to fetch and analyze incidents from Instana
4. **Advanced MCP Capabilities**: Explore infrastructure analysis, application monitoring, and automation

By the end, you'll have a fully functional AI-powered SRE assistant that can:
- Query live Instana data
- Analyze incidents and generate root cause analysis reports
- Monitor infrastructure metrics
- Manage application configurations
- Investigate events and changes

---

## 🎯 What You Will Learn

- How to authenticate and query the **Instana REST API** to retrieve incident events
- How to configure and use **Instana MCP Server** with Bob for real-time observability
- How to save and work with structured incident data in JSON format
- How to use **Bob's SRE mode** to perform AI-driven root cause analysis on real monitoring data
- How to interpret **cascading failure patterns** across distributed infrastructure components
- How to leverage MCP tools for infrastructure analysis, application monitoring, and event investigation
- SRE best practices: severity triage, blast radius estimation, and prioritized remediation

---

## ✅ Prerequisites

| Requirement | Details |
|-------------|---------|
| Python | 3.8 or higher |
| pip | Included with Python 3.8+ |
| Node.js | For npx command (MCP setup) |
| Instana account | Access to an Instana tenant (trial or production) |
| Instana API key | Generate from **Settings → API Tokens** in your Instana UI |
| Bob AI agent | Installed and available in your editor |

> 💡 **No Instana account?** You can still complete the basic lab using the sample data files (`incidents.json`, `latest_5_open_incidents.json`) included in the repository.

---

## 🚀 Part 1: Basic Setup

### Step 1.1 – Clone & Set Up Environment

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd bob-instana
```

Create a Python virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows
```

### Step 1.2 – Configure Instana Credentials

Create a `.env` file in the project root with your Instana credentials:

```bash
touch .env
```

Open `.env` and add the following — **replace the placeholder values**:

```dotenv
INSTANA_HOST=https://your-tenant.instana.io
INSTANA_API_KEY=your_api_token_here
```

#### How to find your credentials

1. Log in to your Instana UI
2. Navigate to **Settings** → **API Tokens**
3. Click **Add API Token**, give it a name (e.g., `bob-workshop`), and copy the token
4. Your `INSTANA_HOST` is the base URL of your Instana UI (e.g., `https://mycompany.instana.io`)

> ⚠️ **Security**: The `.env` file is intentionally excluded from version control. Never commit API keys to Git.

### Step 1.3 – Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This installs:

| Package | Purpose |
|---------|---------|
| `python-dotenv` | Loads credentials from your `.env` file |
| `requests` | Makes HTTP calls to the Instana REST API |

---

## 🔌 Part 2: Instana MCP Integration

### Step 2.1 – Install Instana MCP Server

Open your terminal and run:

```bash
pip install mcp-instana
```

Verify installation:
```bash
mcp-instana --help
```

### Step 2.2 – Configure Bob to Auto-Start MCP

#### Option A: Project-Level (Recommended for Workshop)

1. Create `.bob` folder in your project root (if not exists)
2. Create/edit `.bob/bob_config.json`:

```json
{
  "mcpServers": {
    "Instana MCP Server": {
      "command": "mcp-instana",
      "args": ["--transport", "stdio"],
      "env": {
        "INSTANA_BASE_URL": "https://your-tenant.instana.io",
        "INSTANA_API_TOKEN": "your_instana_api_token"
      }
    }
  }
}
```

#### Option B: Global (All Projects)

Go to settings/MCP/Global MCPs and click open. Configure the `mcp_settings.json` with the same JSON content as above.

### Step 2.3 – Restart Bob

1. Close Bob IDE completely
2. Reopen Bob IDE
3. Click the MCP dropdown (top-right corner)
4. Verify "Instana MCP Server" shows a **green dot** ✅

### Step 2.4 – Test MCP Connection

In Bob chat, try:

```
List all applications from Instana in the last 24 hours
```

or

```
Show me critical incidents from the last 6 hours
```

---

## 🧪 Part 3: Incident Analysis Lab

### Step 3.1 – Fetch Incidents from Instana

Run the incident fetcher script:

```bash
python fetch_instana_incidents.py
```

#### What the script does

1. **Loads** `INSTANA_HOST` and `INSTANA_API_KEY` from `.env`
2. **Calls** the Instana `/api/events` endpoint with a 24-hour time window
3. **Filters** for incident-type events and fetches the latest 5
4. **Saves** the results to `incidents.json`

#### Expected output

```
2026-03-09 03:04:50,123 - __main__ - INFO - Starting Instana incident fetch process
2026-03-09 03:04:50,124 - __main__ - INFO - Initialized Instana API client for host: https://your-tenant.instana.io
2026-03-09 03:04:50,125 - __main__ - INFO - Fetching open incidents from: https://your-tenant.instana.io/api/events
2026-03-09 03:04:51,432 - __main__ - INFO - API Response Status: 200
2026-03-09 03:04:51,435 - __main__ - INFO - Successfully fetched 5 open incidents
2026-03-09 03:04:51,436 - __main__ - INFO - Successfully saved 5 incidents to incidents.json
2026-03-09 03:04:51,437 - __main__ - INFO - Incident fetch process completed successfully
```

> 💡 **No live Instana instance?** The file `latest_5_open_incidents.json` in this repo contains real sample data you can use in the next step.

### Step 3.2 – Analyze Incidents with Bob SRE Mode

#### 3.2a. Open Bob in SRE Mode

In your editor with Bob, **switch to the SRE mode** (`🔧 SRE`). This mode is pre-configured in `.bob/custom_modes.yaml` and equips Bob with:

- Instana API knowledge and link generation
- SRE methodology (detection → triage → root cause → remediation)
- Kubernetes, Kafka, Etcd, and ACE domain expertise
- Incident management best practices

#### 3.2b. Ask Bob to Analyze the Incidents

With SRE mode active, prompt Bob with:

```
Analyze the incidents in latest_5_open_incidents.json and generate a full incident 
analysis report with root cause analysis, impact assessment, and prioritized 
remediation steps. Save the report as instana_incident_analysis_report.md
```

Bob will:

1. Read the raw JSON incident data
2. Parse each incident's severity, entity type, metrics, and timestamps
3. Identify **cross-incident patterns** (e.g., cascading storage failures)
4. Generate **clickable Instana UI links** for each incident
5. Produce a structured Markdown report with executive summary, detailed RCA, and action items

### Step 3.3 – Review the Analysis Report

Open `instana_incident_analysis_report.md` to review the generated report. The report structure includes:

#### Executive Summary
High-level findings, root cause identification, and priority actions sorted by urgency (🔴 P0 → 🟡 P1 → 🟢 P2).

#### Incident-by-Incident Analysis
Each incident contains:
- Instana deep-link for one-click navigation to the event UI
- Symptom description with metric evidence
- Root cause hypotheses ranked by probability
- Suggested fix commands

#### Pattern Analysis
Cross-incident correlation revealing systemic issues — for example, the shared storage infrastructure failure that simultaneously triggered Etcd, Kafka, and ACE incidents within a 6-minute window.

#### Remediation Roadmap
Time-boxed action plan:

| Window | Actions |
|--------|---------|
| **Next 15 min (P0)** | Escalate to storage team, identify IOPS bottleneck |
| **Next 2 hours (P1)** | Bottom-up service recovery: Storage → Etcd → Kafka → ACE |
| **Next 24 hours (P2)** | Architecture review, storage isolation, monitoring fixes |

---

## 🚀 Part 4: Advanced MCP Capabilities

Now that you have MCP connected, you can leverage Bob's full Instana integration capabilities. The following sections demonstrate practical use cases for SRE workflows.

### 4.1 Application Monitoring

Query application metrics, services, and endpoints:

```
List all services in the "robot-shop" application
```

```
Show me active alerts for application "payment-service"
```

### 4.2 Event Investigation

Fetch and analyze different event types:

```
Get the latest 10 critical incidents from the last 24 hours
```

```
Show me all change events from the last 6 hours
```

```
Analyze Kubernetes info events and identify patterns
```

### 4.3 Automation Catalog

Browse and search automation actions:

```
List all available automation actions
```

```
Find automation actions related to CPU issues
```

```
Show recent automation execution history
```

---

## 💡 Workshop Use Cases

This section contains 3 practical use cases to demonstrate Bob's SRE capabilities with Instana.

### Use Case 1: Application Endpoint Error Analysis

**Objective**: Analyze endpoints from an application to identify which endpoints have the highest error rates and determine which services they belong to.

**Prompt**:
```
Fetch the "robot-shop" application from Instana. Find the service with the highest error calls,
then from that service, identify the endpoints with the highest error calls.
Generate a report with:
1. Service name and its error call rate
2. Top 5 endpoints with highest error rates
3. Root cause analysis for the errors
4. Recommended remediation steps
```

**What Bob will do**:
1. Query Instana for the application's services
2. Calculate error call rates for each service
3. Identify the service with highest errors
4. Drill down into that service's endpoints
5. Analyze error patterns and suggest fixes

**Expected Output**: A detailed report showing the error chain from application → service → endpoint with actionable insights.

---

### Use Case 2: Service Error Rate Analysis & Reporting

**Objective**: Analyze the top N services/applications with the highest ratio of error calls to total calls and generate a comprehensive report.

**Prompt**:
```
Analyze the top 10 services/applications with the highest ratio of error calls to total calls
in the last 24 hours. Generate a detailed report including:
1. Service/application name
2. Total calls
3. Error calls
4. Error rate percentage
5. Trend analysis (increasing/decreasing)
6. Impact assessment (affected users, business impact)
7. Root cause hypotheses
8. Prioritized remediation actions

Save the report as service_error_analysis_report.md
```

**What Bob will do**:
1. Query application metrics for all services
2. Calculate error rate ratios (error calls / total calls)
3. Sort and identify top 10 worst performers
4. Analyze trends over the time window
5. Correlate with incidents and changes
6. Generate actionable remediation plan

**Expected Output**: A markdown report with executive summary, detailed service-by-service analysis, and prioritized action items.

---

### Tips for Using These Use Cases

1. **Customize the prompts**: Replace "robot-shop" with your actual application name
2. **Adjust time windows**: Change "last 24 hours" to match your needs (e.g., "last 7 days")
3. **Modify thresholds**: Adjust "top 10" to any number that makes sense for your environment
4. **Combine use cases**: Chain multiple analyses together for comprehensive investigations
5. **Save outputs**: Always ask Bob to save reports as markdown files for documentation


---

## 📁 Project Structure

```
bob-instana/
├── .env                          # Your credentials (create this — not committed)
├── .bob/
│   ├── custom_modes.yaml         # Bob SRE mode definition
│   └── bob_config.json           # MCP server configuration
├── instana-mcp/
│   ├── instana_mcp_capabilities.md   # Full MCP capabilities reference
│   └── instana-mcp-setup.md          # Quick setup guide
├── fetch_instana_incidents.py    # Script to pull incidents from Instana API
├── requirements.txt              # Python dependencies
├── incidents.json                # Output: all fetched incidents (raw)
├── latest_5_open_incidents.json  # Output: top 5 open incidents
├── instana_incident_analysis_report.md  # Output: AI-generated analysis report
└── workshop.md                   # This comprehensive workshop guide
```

---

## 🛠️ Troubleshooting

### Basic Setup Issues

#### `INSTANA_HOST not found in environment variables`
Ensure `.env` exists in the project root and contains `INSTANA_HOST=...`. Run:
```bash
cat .env
```

#### `401 Unauthorized` from the API
Your API key may be invalid or expired. Regenerate it in **Instana → Settings → API Tokens**.

#### `0 incidents returned`
This is normal if no incidents occurred in the past 24 hours. Try increasing the time window in `fetch_instana_incidents.py`:
```python
'windowSize': 604800000,  # 7 days in milliseconds
```

#### `ModuleNotFoundError: No module named 'dotenv'`
Run `pip install -r requirements.txt` and ensure your virtual environment is activated.

### MCP Setup Issues

#### ❌ "command not found: mcp-instana"

Find the full path:
```bash
which mcp-instana
```

Update config with full path:
```json
"command": "/full/path/to/mcp-instana"
```

#### ❌ Red dot in MCP dropdown

1. Check credentials in config
2. Verify `pip install mcp-instana` succeeded
3. Restart Bob IDE
4. Check Bob logs: Help → Toggle Developer Tools → Console

#### ❌ "Connection refused"

Ensure you're using `stdio` transport mode (not HTTP mode).

### Bob SRE Mode Issues

#### Bob SRE mode not available
Ensure `.bob/custom_modes.yaml` is present and reload your editor. The custom mode is defined at the project level and loaded automatically by Bob.

#### MCP tools not working
1. Verify green dot in MCP dropdown
2. Check credentials in `.bob/bob_config.json`
3. Test with simple prompt: "List applications from Instana"
4. Review Bob logs for error messages

---

## 📄 Sample Output

The following snippet is from the analysis Bob generated for the 5 open incidents found in this lab:

```
## Executive Summary

Root Cause: All incidents trace back to a shared storage backend failure causing:
- Etcd cluster: Complete unavailability (fsync >1000ms, normal <10ms)
- Kafka cluster: Message rejection (disk exhaustion or IOPS saturation)
- ACE Integration Servers: Cascading failures due to storage contention

Timeline: All incidents within a 6-minute window (10:50–10:57 HKT)
Blast Radius: Platform-wide outage affecting Kubernetes, messaging, and integrations
```

The 5 incidents analyzed:

| # | Problem | Severity | Entity | State |
|---|---------|----------|--------|-------|
| 1 | ACE Integration Server Issue | Medium (5) | ACE Integration Server | Open |
| 2 | ACE Integration Server Issue | Medium (5) | ACE Integration Server | Open |
| 3 | KafkaClusterEventRejectedBytes | Critical (10) | Kafka Cluster | Open |
| 4 | Etcd fsync duration (>1.0s) | Critical (10) | Etcd Node | Open |
| 5 | Etcd fsync duration (>1.0s) | Critical (10) | Etcd Node | Open |

---

## 🔭 What's Next

Once you complete this workshop, explore these follow-on exercises:

### Automation & Integration
- **Automate the workflow**: Schedule `fetch_instana_incidents.py` as a cron job and have Bob generate a daily report
- **Extend the fetcher**: Modify the script to also fetch application performance metrics using the `/api/application-monitoring/analyze/call-groups` endpoint
- **Build alert rules**: Use the incident patterns found in this lab to define smarter Instana alert specifications

### Advanced Analysis
- **Post-mortem practice**: Use Bob's SRE mode to generate a full post-mortem for the storage failure incident
- **SLO definition**: Ask Bob to define SLIs and SLOs based on the incidents analyzed
- **Capacity planning**: Use infrastructure metrics to generate capacity planning reports
- **Performance optimization**: Analyze distributed traces to identify and fix bottlenecks

### MCP Exploration
- **Infrastructure deep-dive**: Use the two-pass infrastructure analysis workflow for detailed metric investigation
- **Application monitoring**: Create custom application perspectives and alert configurations
- **Automation catalog**: Explore and test automation actions for common incident scenarios
- **Dashboard creation**: Build custom dashboards for your team's specific monitoring needs

### SRE Best Practices
- **Runbook generation**: Create runbooks for common incident types
- **Chaos engineering**: Design and execute chaos experiments with Bob's guidance
- **Observability improvements**: Implement observability best practices in your applications
- **Incident response**: Develop and refine incident response procedures

---

## 📚 References

### Instana Documentation
- [Instana REST API Documentation](https://www.ibm.com/docs/en/instana-observability/current?topic=apis-rest-api)
- [Instana Events API](https://www.ibm.com/docs/en/instana-observability/current?topic=apis-rest-api#events)
- [Instana MCP Server](https://github.com/instana/mcp-server)

### Technology References
- [IBM ACE (App Connect Enterprise)](https://www.ibm.com/docs/en/app-connect/12.0)
- [Etcd Operations Guide](https://etcd.io/docs/v3.5/op-guide/)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

### SRE Resources
- [SRE Book — Google](https://sre.google/sre-book/table-of-contents/)
- [SRE Workbook — Google](https://sre.google/workbook/table-of-contents/)
- [The Site Reliability Workbook](https://landing.google.com/sre/workbook/toc/)

---

## 🎓 Workshop Completion Checklist

- [ ] Cloned repository and set up Python environment
- [ ] Configured Instana credentials in `.env`
- [ ] Installed Python dependencies
- [ ] Installed and configured Instana MCP Server
- [ ] Verified MCP connection (green dot in Bob)
- [ ] Fetched incidents using Python script
- [ ] Analyzed incidents with Bob SRE mode
- [ ] Generated incident analysis report
- [ ] Tested MCP tools with example prompts
- [ ] Explored infrastructure analysis capabilities
- [ ] Tried application monitoring features
- [ ] Investigated events and automation catalog

---

## 🤝 Support & Feedback

If you encounter issues during the workshop:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review Bob logs: Help → Toggle Developer Tools → Console
3. Verify Instana credentials and API token permissions
4. Ensure all prerequisites are installed correctly

---