# Instana MCP Server Capabilities

This document explains what the connected **Instana MCP Server** can do in this workspace, based on the tools currently exposed by the server.

## Overview

The Instana MCP Server available here provides access to several major Instana capability areas:

- Infrastructure analysis
- Application monitoring and configuration
- Automation catalog and execution history
- Custom dashboard management
- Event investigation
- Website monitoring and configuration

In practice, this means the MCP server can be used to query observability data, inspect incidents and issues, review changes, analyze infrastructure metrics, browse automation actions, and manage some Instana resources directly.

---

## 1. Infrastructure Analysis

Tool: `analyze_infrastructure_elicitation`

This capability supports a two-pass workflow for infrastructure analysis.

### What it can do

It can help answer infrastructure questions such as:

- maximum heap size of a JVM
- CPU, memory, or disk-related metrics
- Kubernetes-related infrastructure metrics
- Docker/container metrics
- grouped infrastructure metric analysis
- filtered infrastructure metric analysis over time

### How it works

#### Pass 1: Intent to schema
You provide:

- a natural language intent
- an entity hint

Example intents:

- "maximum heap size of JVM on host galactica1"
- "CPU usage by Kubernetes namespace"
- "disk free space on a host"

The MCP server then returns the schema choices needed for the next step.

#### Pass 2: Selections to results
You provide exact selections such as:

- entity type
- metric names
- aggregation type
- filters
- groupings
- time range
- ordering

Then the MCP server builds the Instana API payload and returns the results.

### Typical use cases

- Investigate host CPU, memory, and disk usage
- Analyze JVM heap metrics
- Group infrastructure metrics by host, namespace, or service
- Filter infrastructure entities by tags
- Retrieve time-bounded infrastructure measurements

---

## 2. Application Monitoring and Configuration

Tool: `manage_applications`

This is a broad application-focused capability that supports multiple resource types.

### Supported resource types

- `metrics`
- `alert_config`
- `global_alert_config`
- `settings`
- `catalog`

### 2.1 Application metrics

Resource type: `metrics`

#### What it can do

- Query application metrics
- List services in an application
- List endpoints in an application
- Group and order application data
- Filter by application tags
- Include or exclude internal and synthetic traffic

#### Example use cases

- List services for an application perspective
- List endpoints for a service
- Query application call metrics
- Group by `service.name`
- Group by `endpoint.name`

### 2.2 Application alert configuration

Resource type: `alert_config`

#### What it can do

- Find active alert configurations
- Find alert versions
- Retrieve a specific alert configuration
- Create alert configurations
- Update alert configurations
- Delete alert configurations
- Enable or disable alerts
- Restore alerts
- Update alert baselines

#### Example use cases

- Find active alerts for an application
- Review alert history and versions
- Enable or disable application-specific alerts
- Update thresholds or baseline behavior

### 2.3 Global application alert configuration

Resource type: `global_alert_config`

#### What it can do

Similar to application alert configuration, but for global application alert settings:

- find active
- find versions
- find
- create
- update
- delete
- enable
- disable
- restore

### 2.4 Application settings and perspectives

Resource type: `settings`

#### What it can do

- Get all application settings
- Get a specific application setting
- Create application perspectives
- Update settings
- Delete settings
- Reorder settings
- Replace all settings

#### Supported subtypes

- `application`
- `endpoint`
- `service`
- `manual_service`

#### Example use cases

- Create a new application perspective
- Retrieve an application perspective by name
- Update endpoint or service settings
- Manage manual services

### 2.5 Application catalog access

Resource type: `catalog`

#### What it can do

- Get application tag catalog
- Get application metric catalog

#### Example use cases

- Discover valid grouping tags
- Discover valid application metrics before querying
- Build correct metric queries without guessing field names

---

## 3. Automation Catalog and Execution History

Tool: `manage_automation`

This capability is focused on Instana automation actions.

### Supported resource types

- `catalog`
- `history`

### 3.1 Automation catalog

Resource type: `catalog`

#### What it can do

- List all automation actions
- Get action details
- Search for matching actions
- Get action matches by ID and time window
- Get action types
- Get action tags

#### Example use cases

- Browse available remediation or diagnostic actions
- Search for actions related to CPU, memory, or incidents
- Inspect action metadata and supported targets

### 3.2 Automation execution history

Resource type: `history`

#### What it can do

- List action execution history
- Get details for a specific action execution

#### Example use cases

- Review recent automation runs
- Investigate failed automation executions
- Audit action history for a target snapshot or event

---

## 4. Custom Dashboard Management

Tool: `manage_custom_dashboards`

This capability manages Instana custom dashboards.

### What it can do

- Get all custom dashboards
- Get a dashboard by ID
- Create a dashboard
- Update a dashboard
- Delete a dashboard
- Get shareable users for a dashboard
- Get shareable API tokens for a dashboard

### Example use cases

- Inventory dashboards
- Create a new dashboard for a team
- Update dashboard widgets
- Remove obsolete dashboards
- Review sharing options

---

## 5. Event Investigation

Tool: `manage_events`

This is one of the most useful capabilities for operational investigation.

### What it can do

- Get a specific event by ID
- Get Kubernetes info events
- Get agent monitoring events
- Get issue events
- Get incident events
- Get change events
- Get multiple events by IDs

### Supported event-focused operations

- `get_event`
- `get_kubernetes_info_events`
- `get_agent_monitoring_events`
- `get_issues`
- `get_incidents`
- `get_changes`
- `get_events_by_ids`

### Example use cases

- Fetch recent incidents
- Fetch recent issues
- Fetch recent changes
- Investigate a specific event ID
- Review Kubernetes-related informational events
- Analyze agent monitoring events over a time range

### Filters and controls

The tool supports parameters such as:

- `from_time`
- `to_time`
- `time_range`
- `max_events`
- `filter_event_updates`
- `exclude_triggered_before`

### Practical examples already supported by this MCP

- Retrieve 10 incidents from the last 24 hours
- Retrieve critical issues from the last 24 hours
- Retrieve change events from the last 24 hours
- Inspect a single event in detail by event ID
- Summarize open versus closed events

---

## 6. Website Monitoring and Configuration

Tool: `manage_websites`

This capability covers website beacon analysis, catalog access, and configuration retrieval.

### Supported resource types

- `analyze`
- `catalog`
- `configuration`
- `advanced_config`

### 6.1 Website analysis

Resource type: `analyze`

#### What it can do

- Get grouped beacon data
- Get individual beacon data

#### Operations

- `get_beacon_groups`
- `get_beacons`

#### Example use cases

- Count beacons per page
- Analyze page load beacons
- Filter website beacons by website name
- Group by page name or other valid tags

### 6.2 Website catalog

Resource type: `catalog`

#### What it can do

- Get available website metrics
- Get valid tag catalog for website monitoring

#### Important workflow

Before running website analysis, you should first retrieve the tag catalog so you know the valid tag names.

### 6.3 Website configuration

Resource type: `configuration`

#### What it can do

- List all websites
- Get a website by ID
- Get a website by name

#### Limitation

This MCP exposure is read-only for website configuration changes. It does not provide create, update, or delete operations for websites.

### 6.4 Advanced website configuration

Resource type: `advanced_config`

#### What it can do

- Get geo-location configuration
- Get IP masking configuration
- Get geo rules

#### Limitation

These advanced configuration operations are read-only in this MCP exposure.

---

## What this MCP server is especially good for

The Instana MCP server is especially useful for:

- Incident investigation
- Issue triage
- Change review
- Infrastructure metric analysis
- Application perspective inspection
- Alert configuration lookup
- Dashboard inventory and management
- Website beacon analysis
- Automation catalog discovery

---

## Common workflows you can ask for

Here are practical things this MCP server can help with:

### Event and incident workflows

- "Fetch the latest 10 incidents"
- "Show open critical issues from the last 24 hours"
- "Get details for event ID X"
- "Fetch recent changes and summarize them"
- "List incidents in markdown"

### Infrastructure workflows

- "Analyze disk free space on a host"
- "Show JVM heap max size for a server"
- "Group CPU usage by Kubernetes namespace"
- "Find memory-related infrastructure metrics"

### Application workflows

- "List services in application X"
- "List endpoints for application X"
- "Get active alerts for application X"
- "Create an application perspective"
- "Get application metric catalog"

### Automation workflows

- "List available automation actions"
- "Find actions related to CPU"
- "Show recent automation execution history"

### Dashboard workflows

- "List all custom dashboards"
- "Get dashboard details"
- "Create or update a dashboard"

### Website workflows

- "List websites"
- "Get website tag catalog"
- "Analyze page load beacons"
- "Get website geo-location configuration"

---

## Important limitations

Based on the currently exposed tools, there are some practical limits:

- Website advanced configuration is read-only
- Website create/update/delete is not exposed here
- Infrastructure analysis requires a two-step schema-driven workflow
- Results may be truncated for performance, so large event sets often need filtering or pagination-aware follow-up
- Root cause analysis is limited to what Instana returns in the event payload and what can be inferred from related metrics and context

---

## Summary

The connected Instana MCP Server can be used to:

- investigate incidents, issues, and changes
- inspect individual events by ID
- analyze infrastructure metrics
- query application metrics and settings
- manage application alert configurations
- browse and inspect automation actions
- manage custom dashboards
- analyze website beacon data
- retrieve website and advanced website configuration details

For day-to-day operations, the most immediately useful capabilities are usually:

- [`manage_events`](instana_mcp_capabilities.md)
- [`manage_applications`](instana_mcp_capabilities.md)
- [`analyze_infrastructure_elicitation`](instana_mcp_capabilities.md)

These cover most incident response, observability triage, and operational analysis workflows.