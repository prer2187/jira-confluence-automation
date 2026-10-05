# Jira Risk Dashboard Automation Backlog

This backlog translates `project_spec.md` into actionable delivery work for one configurable Jira Cloud project and a Power BI report. It assumes an MVP-first sequence, keeps the extraction architecture open until the discovery gate, and includes notifications and capacity comparison as planned work rather than silently dropping them.

## Working Conventions

- [ ] Mark a task complete only when its deliverable and acceptance check are complete. [custom skill]
- [ ] Resolve open decisions before building the dependent feature. [custom skill]
- [ ] Keep Jira as the system of record; the solution is read-only. [custom skill]
- [ ] Never commit Jira credentials, tokens, report secrets, or personal data that is not needed for reporting. [custom skill]
- [ ] Record configuration and validation evidence with each phase. [custom skill]

## Phase 1: Setup

### 1.1 Confirm scope and delivery decisions

- [ ] Confirm Jira Cloud versus Jira Server/Data Center and record the decision. [custom skill]
- [ ] Confirm the Jira site URL, project key, project name, and target environment. [custom skill]
- [ ] Confirm the first-release issue types: stories, tasks, and bugs. [custom skill]
- [ ] Confirm sprint length, sprint naming conventions, current sprint behavior, and historical sprint retention. [custom skill]
- [ ] Confirm the daily refresh target time relative to the team's Scrum meeting. [custom skill]
- [ ] Confirm the Power BI workspace, licensing tier, report audience, and whether row-level security is needed. [custom skill]
- [ ] Confirm whether Teams or email notifications are required for the first production release. [custom skill]
- [ ] Confirm the capacity source, capacity unit, owner, and update process for workload comparison. [custom skill]
- [ ] Write the accepted decisions and unresolved assumptions into the project configuration documentation. [custom skill]

### 1.2 Select the integration architecture

- [ ] Compare Power BI connector-only, scheduled Python job, and Azure Function options against authentication, refresh, API limits, hosting, licensing, and operational support requirements. [custom skill]
- [ ] Choose the extraction runtime and document the rationale. [custom skill]
- [ ] Choose the staging destination from the approved options, such as Azure SQL, SharePoint, or controlled file/data lake storage. [MCP]
- [ ] Define the deployment environments and configuration boundaries for development, test, and production. [custom skill]
- [ ] Define the minimum Jira permissions required by the integration identity. [MCP]
- [ ] Define data retention for issue history, sprint snapshots, risk records, and refresh logs. [custom skill]
- [ ] Create an architecture decision record with the selected option, rejected options, and known tradeoffs. [custom skill]

### 1.3 Establish the repository and runtime

- [ ] Create the extraction project structure, dependency manifest, configuration template, and entry point. [custom skill]
- [ ] Pin supported runtime and dependency versions. [custom skill]
- [ ] Add a safe local configuration mechanism using environment variables or an approved local secret store. [MCP]
- [ ] Add a configuration schema for Jira site, project key, issue types, sprint scope, custom field IDs, thresholds, and destination settings. [custom skill]
- [ ] Add configuration validation that fails before extraction when required values are missing or invalid. [custom skill]
- [ ] Add formatting, linting, and unit-test commands to the project workflow. [custom skill]
- [ ] Add `.gitignore` entries for secrets, local settings, generated exports, caches, and runtime logs. [custom skill]
- [ ] Add a sample configuration containing placeholders only. [custom skill]

### 1.4 Establish security and access

- [ ] Create or obtain the approved Jira OAuth 2.0 integration or service account/API token. [MCP]
- [ ] Store credentials in the approved secret manager or Power BI-managed credential store. [MCP]
- [ ] Verify the identity can read the selected project, issues, sprints, links, and required custom fields. [MCP]
- [ ] Verify credentials are absent from source, logs, report files, browser code, and generated artifacts. [custom skill]
- [ ] Define secret rotation and access review procedures. [MCP]
- [ ] Confirm Power BI workspace access for builders, operators, and report consumers. [MCP]

## Phase 2: Core Features

### 2.1 Build the Jira client and extraction layer

- [ ] Implement Jira authentication using the selected approved method. [MCP]
- [ ] Implement paginated issue retrieval for the configured project and issue types. [MCP]
- [ ] Implement sprint retrieval for current, historical, and future sprints where Jira provides them. [MCP]
- [ ] Implement retrieval of all required issue fields: key, URL, summary, type, status, status category, priority, assignee, reporter, sprint, story points, dates, labels, components, parent, links, and activity data where available. [MCP]
- [ ] Map configured custom field identifiers instead of hard-coding organization-specific field names. [custom skill]
- [ ] Normalize missing, null, malformed, and unsupported Jira fields without aborting the complete load. [custom skill]
- [ ] Respect Jira pagination and API rate limits. [MCP]
- [ ] Add bounded retries and backoff for transient authentication, network, and Jira API failures. [custom skill]
- [ ] Return structured extraction results with records, warnings, pagination statistics, and failure details. [custom skill]
- [ ] Add request correlation or run identifiers to logs. [custom skill]

### 2.2 Implement load state and incremental processing

- [ ] Define the initial-load and incremental-load behavior for the selected destination. [custom skill]
- [ ] Persist the last successful extraction timestamp and source project. [MCP]
- [ ] Retrieve only changed or new records when the selected source supports incremental processing. [MCP]
- [ ] Ensure a failed or partial run cannot advance the last successful extraction marker. [custom skill]
- [ ] Define deduplication keys for issues, sprint snapshots, risks, and extraction runs. [custom skill]
- [ ] Preserve enough history to calculate scope growth, spillover, and recent sprint trends. [MCP]
- [ ] Add a controlled full-reload option for recovery and schema changes. [custom skill]

### 2.3 Create normalized reporting data

- [ ] Implement `FactIssue` with issue identity, project, sprint, workflow, ownership, priority, estimate, dates, URL, and extraction metadata. [custom skill]
- [ ] Implement `FactSprintSnapshot` with sprint dates, scope, completed work, issue counts, story points, and scope-change measures. [custom skill]
- [ ] Implement `FactRisk` with issue-risk pairs, type, severity, explanation, detection time, and resolution state. [custom skill]
- [ ] Implement dimensions for project, sprint, issue type, status, priority, assignee, and date. [custom skill]
- [ ] Define and enforce relationships, keys, data types, and null handling. [custom skill]
- [ ] Add load metadata containing extraction start, completion, source project, record count, status, and error details. [custom skill]
- [ ] Validate that every issue and risk record can be traced to a project, sprint where applicable, and extraction timestamp. [custom skill]

### 2.4 Implement configurable risk rules

- [ ] Create a configuration model for statuses, priority values, activity threshold, defect thresholds, sprint timing, and severity rules. [custom skill]
- [ ] Detect blocked or on-hold issues from configured statuses and blocking relationships. [custom skill]
- [ ] Detect overdue unresolved issues based on due date and resolution state. [custom skill]
- [ ] Detect high-priority unresolved issues near sprint end. [custom skill]
- [ ] Detect stale issues with no meaningful activity beyond the configured business-day threshold. [custom skill]
- [ ] Detect sprint scope growth after sprint start. [custom skill]
- [ ] Detect active unassigned issues. [custom skill]
- [ ] Detect spillover risk from incomplete work at sprint end or repeated carryover. [custom skill]
- [ ] Detect excessive open bugs using configurable count or percentage thresholds. [custom skill]
- [ ] Assign High, Medium, or Low severity using documented configurable rules. [custom skill]
- [ ] Generate a human-readable reason for every risk, including the rule and relevant values. [custom skill]
- [ ] Ensure one issue can produce multiple independent risk records. [custom skill]
- [ ] Add risk resolution or inactive-state handling when a later load no longer meets a rule. [custom skill]

### 2.5 Deliver the MVP Power BI semantic model

- [ ] Load the normalized source into a Power BI dataset or semantic model using the selected staging architecture. [MCP]
- [ ] Configure relationships and date handling for issue, sprint, risk, and refresh data. [custom skill]
- [ ] Add measures for issue-count completion, story-point completion, remaining work, active work, risk counts, and days remaining. [custom skill]
- [ ] Add measures for unassigned work, open bugs, scope change, spillover, and recent sprint throughput. [custom skill]
- [ ] Add calculated fields or measures needed for risk severity and overall risk status. [custom skill]
- [ ] Add report filters for project, sprint, status, priority, issue type, and assignee. [custom skill]
- [ ] Add Jira URL fields as Web URL categories or equivalent clickable links. [custom skill]
- [ ] Add refresh metadata and a visible last-successful-refresh indicator. [custom skill]

### 2.6 Build the initial report experience

- [ ] Build the executive risk summary with overall status, High/Medium/Low counts, sprint completion, days remaining, scope change, top five risks, and refresh timestamp. [custom skill]
- [ ] Build the sprint health page with issue-count and story-point completion, remaining work, trend or burndown, recent sprint comparison, spillover, and scope change. [custom skill]
- [ ] Build the team workload page with active issues, story points, unassigned work, high-priority work, and assignee distribution. [custom skill]
- [ ] Build the risk register with filtering, issue identity, Jira link, risk type, severity, assignee, status, priority, sprint, age, and explanation. [custom skill]
- [ ] Add drill-through or issue-detail navigation where it improves investigation. [custom skill]
- [ ] Add configurable capacity comparison once the capacity source and ownership are confirmed. [custom skill]
- [ ] Use accessible labels, readable contrast, non-color-only risk indicators, and tablet-compatible layouts. [custom skill]

### 2.7 Add refresh and notification behavior

- [ ] Configure the daily Power BI refresh or scheduled extraction according to the approved architecture. [MCP]
- [ ] Add a documented manual refresh or rerun path. [custom skill]
- [ ] Ensure partial and failed loads are visible and cannot appear current. [custom skill]
- [ ] Define notification criteria for newly detected High risks. [custom skill]
- [ ] Implement the approved Teams or email notification path, including affected issue keys and a dashboard link. [MCP]
- [ ] Prevent duplicate notifications for the same risk unless it is newly detected or materially changed. [custom skill]

## Phase 3: Integration

### 3.1 Connect the end-to-end pipeline

- [ ] Connect the Jira extractor to the selected staging destination. [MCP]
- [ ] Connect the staging destination to the Power BI semantic model. [MCP]
- [ ] Configure production credentials and environment-specific settings without embedding secrets in files. [MCP]
- [ ] Configure scheduled execution, time zone, timeout, retry, and concurrency behavior. [MCP]
- [ ] Verify the pipeline can run from a clean environment using only documented setup steps. [custom skill]
- [ ] Verify a successful run updates issue data, sprint snapshots, risks, and refresh metadata. [custom skill]
- [ ] Verify a failed run preserves the last known successful state and exposes the failure. [custom skill]

### 3.2 Validate source-to-report traceability

- [ ] Select representative Jira issues for stories, tasks, bugs, blocked work, overdue work, unassigned work, and missing optional fields. [MCP]
- [ ] Trace each representative issue from Jira through extraction, staging, semantic model, risk record, and report. [custom skill]
- [ ] Verify every displayed issue URL opens the matching Jira issue. [custom skill]
- [ ] Verify sprint, assignee, priority, status, story points, and dates match Jira for the selected samples. [custom skill]
- [ ] Verify the report shows the correct project and extraction timestamp. [custom skill]

### 3.3 Configure operations and access

- [ ] Configure monitoring for extraction failures, refresh failures, partial loads, and stale data. [MCP]
- [ ] Configure actionable error logging without exposing secrets or unnecessary personal data. [custom skill]
- [ ] Apply least-privilege access to the runtime, staging source, secret store, and Power BI workspace. [MCP]
- [ ] Configure report sharing for the Scrum Master, team, stakeholders, and leadership according to the approved audience. [MCP]
- [ ] Apply row-level security only if the confirmed audience model requires it. [MCP]
- [ ] Configure retention and cleanup for logs and historical extracts. [MCP]

## Phase 4: Testing

### 4.1 Unit and contract tests

- [ ] Test configuration validation for missing, invalid, and valid settings. [custom skill]
- [ ] Test Jira pagination, rate-limit handling, transient retries, and permanent API failures. [custom skill]
- [ ] Test field mapping for standard fields, custom fields, null values, malformed values, and renamed statuses. [custom skill]
- [ ] Test issue, sprint, and relationship normalization. [custom skill]
- [ ] Test incremental watermark behavior for success, failure, retry, and full reload. [custom skill]
- [ ] Test each risk rule with positive, negative, boundary, and missing-data cases. [custom skill]
- [ ] Test severity assignment and human-readable risk explanations. [custom skill]
- [ ] Test deduplication and preservation of historical snapshots. [custom skill]
- [ ] Test notification deduplication and High-risk filtering if notifications are implemented. [custom skill]

### 4.2 Integration and data-quality tests

- [ ] Run the extractor against a controlled Jira project or approved test fixture. [MCP]
- [ ] Verify pagination returns all expected records without duplicates. [custom skill]
- [ ] Compare extracted counts and representative field values with Jira. [custom skill]
- [ ] Verify missing custom fields do not fail the entire load. [custom skill]
- [ ] Verify partial loads are marked partial and are not promoted as current. [custom skill]
- [ ] Verify refresh metadata records start time, completion time, project, record count, status, and error details. [custom skill]
- [ ] Verify incremental extraction returns changed records and leaves unchanged records stable. [custom skill]
- [ ] Verify full reload produces the expected normalized result. [custom skill]

### 4.3 Power BI validation

- [ ] Verify filters work for sprint, status, priority, issue type, and assignee. [custom skill]
- [ ] Reconcile issue-count completion and story-point completion with independently calculated values. [custom skill]
- [ ] Reconcile risk counts and severity totals with the risk-rule test data. [custom skill]
- [ ] Verify current sprint, days remaining, scope growth, throughput, and spillover indicators. [custom skill]
- [ ] Verify workload, unassigned work, open bugs, and capacity comparison calculations. [custom skill]
- [ ] Verify every report issue link opens Jira. [custom skill]
- [ ] Verify failed or stale refresh state is visible to report users or operators. [custom skill]
- [ ] Test desktop and standard tablet layouts for readability, clipping, and usable navigation. [custom skill]
- [ ] Perform an accessibility review for contrast, labels, keyboard navigation where supported, and color-independent risk meaning. [custom skill]

### 4.4 Operational and acceptance testing

- [ ] Test a scheduled successful run before the daily Scrum meeting. [custom skill]
- [ ] Test manual rerun instructions from a clean operator context. [custom skill]
- [ ] Simulate Jira authentication failure, API rate limiting, unavailable staging, and Power BI refresh failure. [custom skill]
- [ ] Confirm bounded retries and useful error messages for each failure mode. [custom skill]
- [ ] Confirm the last successful data remains clearly identified after failure. [custom skill]
- [ ] Conduct Scrum Master user acceptance testing using real or approved representative scenarios. [custom skill]
- [ ] Obtain acceptance for the risk rules, report layout, refresh timing, permissions, and runbook. [custom skill]

## Phase 5: Documentation

### 5.1 User and operator documentation

- [ ] Document the solution purpose, scope, supported issue types, and known limitations. [custom skill]
- [ ] Document configuration for Jira site, project, issue types, sprint scope, custom fields, statuses, thresholds, capacity, and refresh time. [custom skill]
- [ ] Document the normal daily workflow for reviewing the executive summary, sprint health, workload, and risk register. [custom skill]
- [ ] Document how to open and investigate a Jira issue from Power BI. [custom skill]
- [ ] Document the manual refresh or rerun procedure. [custom skill]
- [ ] Document how to interpret each risk type, severity, and explanation. [custom skill]
- [ ] Document the notification behavior and how to follow up on a High risk. [custom skill]

### 5.2 Technical and operational runbook

- [ ] Document the selected architecture, components, data flow, and environment configuration. [custom skill]
- [ ] Document authentication, secret storage, rotation, least-privilege access, and access review. [custom skill]
- [ ] Document deployment and rollback steps for the extractor, staging layer, and Power BI model. [custom skill]
- [ ] Document scheduled refresh configuration, time zones, retry behavior, and timeout settings. [custom skill]
- [ ] Document troubleshooting for credentials, Jira schema changes, missing fields, rate limits, partial loads, and Power BI refresh failures. [custom skill]
- [ ] Document how to perform a controlled full reload and how to verify recovery. [custom skill]
- [ ] Document monitoring, alert ownership, log locations, retention, and escalation contacts. [custom skill]
- [ ] Document data lineage from Jira through the report and the retention policy for historical data. [custom skill]

### 5.3 Final release evidence

- [ ] Publish the confirmed risk-rule table and configuration reference. [custom skill]
- [ ] Publish test results, representative reconciliation evidence, and known limitations. [custom skill]
- [ ] Record open decisions that remain deferred after release. [custom skill]
- [ ] Record the production deployment date, report URL, owner, support contact, and next review date. [custom skill]
- [ ] Obtain final sign-off from the Scrum Master, technical owner, and Power BI workspace owner. [custom skill]
- [ ] Create a post-release backlog for enhancements such as higher refresh frequency, multi-project support, predictive scoring, or Jira write-back, keeping them outside version 1. [custom skill]
