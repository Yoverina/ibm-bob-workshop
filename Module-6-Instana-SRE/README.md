# 🔧 Lab: AI-Powered Incident Analysis with IBM Instana and Bob

> **Difficulty**: Beginner–Intermediate  
> **Duration**: ~30–45 minutes  
> **Mode**: Bob SRE Agent (`🔧 SRE`)

In this lab, you will use **Bob** — an AI Site Reliability Engineer — to connect to the IBM Instana monitoring API, fetch live incidents, and generate a deep root cause analysis report. By the end, you will have a working incident-fetching script and a structured analysis report generated entirely by AI.

---

## 📋 Table of Contents

1. [What You Will Learn](#-what-you-will-learn)
2. [Prerequisites](#-prerequisites)
3. [Project Structure](#-project-structure)
4. [Step 1 – Clone & Set Up Environment](#-step-1--clone--set-up-environment)
5. [Step 2 – Configure Instana Credentials](#-step-2--configure-instana-credentials)
6. [Step 3 – Install Dependencies](#-step-3--install-dependencies)
7. [Step 4 – Fetch Incidents from Instana](#-step-4--fetch-incidents-from-instana)
8. [Step 5 – Analyze Incidents with Bob SRE Mode](#-step-5--analyze-incidents-with-bob-sre-mode)
9. [Step 6 – Review the Analysis Report](#-step-6--review-the-analysis-report)
10. [Sample Output](#-sample-output)
11. [Troubleshooting](#-troubleshooting)
12. [What's Next](#-whats-next)

---

## 🎯 What You Will Learn

- How to authenticate and query the **Instana REST API** to retrieve incident events
- How to save and work with structured incident data in JSON format
- How to use **Bob's SRE mode** to perform AI-driven root cause analysis on real monitoring data
- How to interpret **cascading failure patterns** across distributed infrastructure components (Etcd, Kafka, ACE Integration Servers)
- SRE best practices: severity triage, blast radius estimation, and prioritized remediation

---

## ✅ Prerequisites

| Requirement | Details |
|-------------|---------|
| Python | 3.8 or higher |
| pip | Included with Python 3.8+ |
| Instana account | Access to an Instana tenant (trial or production) |
| Instana API key | Generate from **Settings → API Tokens** in your Instana UI |
| Bob AI agent | Installed and available in your editor |

> 💡 **No Instana account?** You can still complete Steps 1–4 by using the sample data files (`incidents.json`, `latest_5_open_incidents.json`) already included in the repository.

---

## 📁 Project Structure

```
bob-instana/
├── .env                          # Your credentials (create this — not committed)
├── .bob/
│   └── custom_modes.yaml         # Bob SRE mode definition
├── fetch_instana_incidents.py    # Script to pull incidents from Instana API
├── requirements.txt              # Python dependencies
├── incidents.json                # Output: all fetched incidents (raw)
├── latest_5_open_incidents.json  # Output: top 5 open incidents
└── instana_incident_analysis_report.md  # Output: AI-generated analysis report
```

---

## 🚀 Step 1 – Clone & Set Up Environment

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

---

## 🔑 Step 2 – Configure Instana Credentials

Create a `.env` file in the project root with your Instana credentials:

```bash
touch .env
```

Open `.env` and add the following — **replace the placeholder values**:

```dotenv
INSTANA_HOST=https://your-tenant.instana.io
INSTANA_API_KEY=your_api_token_here
```

### How to find your credentials

1. Log in to your Instana UI
2. Navigate to **Settings** → **API Tokens**
3. Click **Add API Token**, give it a name (e.g., `bob-lab`), and copy the token
4. Your `INSTANA_HOST` is the base URL of your Instana UI (e.g., `https://mycompany.instana.io`)

> ⚠️ **Security**: The `.env` file is intentionally excluded from version control. Never commit API keys to Git.

---

## 📦 Step 3 – Install Dependencies

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

## ⚡ Step 4 – Fetch Incidents from Instana

Run the incident fetcher script:

```bash
python fetch_instana_incidents.py
```

### What the script does

1. **Loads** `INSTANA_HOST` and `INSTANA_API_KEY` from `.env`
2. **Calls** the Instana `/api/events` endpoint with a 24-hour time window
3. **Filters** for incident-type events and fetches the latest 5
4. **Saves** the results to `incidents.json`

### Expected output

```
2026-03-09 03:04:50,123 - __main__ - INFO - Starting Instana incident fetch process
2026-03-09 03:04:50,124 - __main__ - INFO - Initialized Instana API client for host: https://your-tenant.instana.io
2026-03-09 03:04:50,125 - __main__ - INFO - Fetching open incidents from: https://your-tenant.instana.io/api/events
2026-03-09 03:04:51,432 - __main__ - INFO - API Response Status: 200
2026-03-09 03:04:51,435 - __main__ - INFO - Successfully fetched 5 open incidents
2026-03-09 03:04:51,436 - __main__ - INFO - Successfully saved 5 incidents to incidents.json
2026-03-09 03:04:51,437 - __main__ - INFO - Incident fetch process completed successfully
```

After running, `incidents.json` will contain the structured incident data:

```json
{
  "metadata": {
    "fetch_timestamp": "2026-03-09T03:04:56Z",
    "incident_count": 5,
    "status": "OPEN"
  },
  "incidents": [ ... ]
}
```

> 💡 **No live Instana instance?** The file `latest_5_open_incidents.json` in this repo contains real sample data you can use in the next step.

---

## 🤖 Step 5 – Analyze Incidents with Bob SRE Mode

This is where the AI-powered analysis happens.

### 5a. Open Bob in SRE Mode

In your editor with Bob, **switch to the SRE mode** (`🔧 SRE`). This mode is pre-configured in `.bob/custom_modes.yaml` and equips Bob with:

- Instana API knowledge and link generation
- SRE methodology (detection → triage → root cause → remediation)
- Kubernetes, Kafka, Etcd, and ACE domain expertise
- Incident management best practices

### 5b. Ask Bob to Analyze the Incidents

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

### 5c. Explore Further (Optional)

Try these additional prompts in SRE mode:

```
What is the blast radius of the storage failure detected in the incidents?
```

```
Generate a post-mortem template for the Etcd fsync duration incidents.
```

```
What SLO violations should I expect from these incidents?
```

---

## 📊 Step 6 – Review the Analysis Report

Open `instana_incident_analysis_report.md` to review the generated report. The report structure includes:

### Executive Summary
High-level findings, root cause identification, and priority actions sorted by urgency (🔴 P0 → 🟡 P1 → 🟢 P2).

### Incident-by-Incident Analysis
Each incident contains:
- Instana deep-link for one-click navigation to the event UI
- Symptom description with metric evidence
- Root cause hypotheses ranked by probability
- Suggested fix commands

### Pattern Analysis
Cross-incident correlation revealing systemic issues — for example, the shared storage infrastructure failure that simultaneously triggered Etcd, Kafka, and ACE incidents within a 6-minute window.

### Remediation Roadmap
Time-boxed action plan:

| Window | Actions |
|--------|---------|
| **Next 15 min (P0)** | Escalate to storage team, identify IOPS bottleneck |
| **Next 2 hours (P1)** | Bottom-up service recovery: Storage → Etcd → Kafka → ACE |
| **Next 24 hours (P2)** | Architecture review, storage isolation, monitoring fixes |

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

## 🛠️ Troubleshooting

### `INSTANA_HOST not found in environment variables`
Ensure `.env` exists in the project root and contains `INSTANA_HOST=...`. Run:
```bash
cat .env
```

### `401 Unauthorized` from the API
Your API key may be invalid or expired. Regenerate it in **Instana → Settings → API Tokens**.

### `0 incidents returned`
This is normal if no incidents occurred in the past 24 hours. Try increasing the time window in `fetch_instana_incidents.py`:
```python
'windowSize': 604800000,  # 7 days in milliseconds
```

### `ModuleNotFoundError: No module named 'dotenv'`
Run `pip install -r requirements.txt` and ensure your virtual environment is activated.

### Bob SRE mode not available
Ensure `.bob/custom_modes.yaml` is present and reload your editor. The custom mode is defined at the project level and loaded automatically by Bob.

---

## 🔭 What's Next

Once you complete this lab, explore these follow-on exercises:

- **Automate the workflow**: Schedule `fetch_instana_incidents.py` as a cron job and have Bob generate a daily report
- **Extend the fetcher**: Modify the script to also fetch application performance metrics using the `/api/application-monitoring/analyze/call-groups` endpoint
- **Build alert rules**: Use the incident patterns found in this lab to define smarter Instana alert specifications
- **Post-mortem practice**: Use Bob's SRE mode to generate a full post-mortem for the storage failure incident
- **SLO definition**: Ask Bob to define SLIs and SLOs based on the incidents analyzed

---

## 📚 References

- [Instana REST API Documentation](https://www.ibm.com/docs/en/instana-observability/current?topic=apis-rest-api)
- [Instana Events API](https://www.ibm.com/docs/en/instana-observability/current?topic=apis-rest-api#events)
- [IBM ACE (App Connect Enterprise)](https://www.ibm.com/docs/en/app-connect/12.0)
- [Etcd Operations Guide](https://etcd.io/docs/v3.5/op-guide/)
- [SRE Book — Google](https://sre.google/sre-book/table-of-contents/)

---

*Made with Bob 🤖*
