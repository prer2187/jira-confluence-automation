# Technical Specification: Jira Risk Dashboard Automation for Power BI

## 1. Overview

### 1.1 Project name

Jira Risk Data Automation for Power BI

### 1.2 Purpose

Automate the extraction, transformation, and delivery of Jira project data to Power BI so a Scrum Master can monitor delivery risks for a 10-person UI project team without manually preparing data.

This specification is based on the interview responses provided in this conversation and AI-recommended implementation assumptions where details were not specified.

### 1.3 Problem statement

Jira information is currently extracted manually. This is time-consuming, can introduce errors, and delays visibility into blockers, overdue work, workload imbalance, stale tickets, and sprint delivery risk.

### 1.4 Primary user

The primary user is the Scrum Master. Secondary users are the UI project team, project stakeholders, project managers, and leadership.

## 2. Goals and Success Criteria

### 2.1 Goals

- Remove recurring manual Jira data extraction.
- Provide a reliable Power BI risk dashboard.
- Surface actionable sprint and delivery risks early.
- Give the team and leadership a shared view of project health.
- Preserve links to Jira issues for investigation.

### 2.2 Success criteria

- Jira data is refreshed automatically at least once per day.
- The Scrum Master can see current sprint health without manually exporting Jira data.
- Risk indicators are calculated consistently from documented rules.
- Users can open the source Jira issue from Power BI.
- Data preparation time is reduced to near zero for routine reporting.
- Dashboard data is traceable to a Jira project, sprint, and extraction timestamp.

## 3. Scope

### 3.1 In scope

- Jira Cloud data extraction for one configurable Jira project.
- Stories, tasks, and bugs in the first release.
- Current, historical, and future sprint data where available.
- Data transformation and risk classification.
- Power BI dataset or semantic model and dashboard.
- Scheduled refresh and a manual refresh path where supported.
- Drill-through or hyperlinks from dashboard records to Jira.
- Documentation for configuration, operation, and troubleshooting.

### 3.2 Out of scope for version 1

- Editing Jira issues from Power BI.
- Replacing Jira as the system of record.
- Predictive machine-learning risk scoring.
- Automated reassignment or workflow changes in Jira.
- Multi-project portfolio reporting.
- External or public access.

## 4. Proposed Solution

1. Authenticate securely to Jira Cloud.
2. Query the configured Jira project and relevant sprint issues through the Jira REST API or an approved Jira Power BI connector.
3. Store or stage the extracted data in a refreshable data source.
4. Transform the data into reporting tables and calculated risk fields.
5. Refresh the Power BI semantic model on a schedule.
6. Present sprint health, workload, delivery risks, and trends in Power BI.
7. Link each issue row to its Jira source record.
8. Optionally send a Teams or email summary when material risks are detected.

### 4.1 Recommended implementation

Use a server-side extraction process, preferably a scheduled Python job or Azure Function, with Jira credentials stored in an approved secret store. Publish normalized data to a Power BI-accessible source such as Azure SQL, SharePoint, or a controlled file/data lake location. The final choice depends on the organization's existing Microsoft licensing and hosting standards.

For a low-infrastructure first release, Power BI Power Query using an approved Jira connector may be used if it meets authentication, refresh, and API-rate-limit requirements. Credentials must not be embedded in browser code or committed to the repository.

## 5. Functional Requirements

### FR-01: Jira configuration

The solution shall support configuration of the Jira site, project key, issue types, sprint scope, and relevant custom field identifiers without changing business logic.

### FR-02: Data extraction

The solution shall retrieve, at minimum:

- Issue key and URL
- Summary
- Issue type
- Status and status category
- Priority
- Assignee and reporter
- Sprint
- Story points, when available
- Created, updated, due, and resolved dates
- Labels and components, when available
- Parent, linked, and blocked-by relationships, when available
- Status transition or activity information, when available

### FR-03: Incremental processing

The solution should retrieve only new or changed Jira records after the initial load when the selected connector and source support incremental refresh. It shall retain the last successful extraction timestamp and record failures for review.

### FR-04: Sprint dashboard

Power BI shall display:

- Current sprint and project filters
- Completion percentage by issue count and story points
- Completed versus remaining work
- Days remaining in the sprint
- Sprint scope changes
- Throughput and completion trends across recent sprints

### FR-05: Team workload

Power BI shall display active issues, story points, unassigned work, and workload distribution by assignee. Capacity comparisons shall remain configurable because team capacity data was not provided during the interview.

### FR-06: Risk detection

The solution shall identify and classify at least the following risks:

- Blocked or on-hold issues
- Overdue issues
- High-priority unresolved issues
- Issues with no meaningful activity beyond a configurable threshold
- Sprint scope growth after sprint start
- Unassigned active issues
- Work likely to spill into the next sprint
- Excessive open bugs or unresolved defects

### FR-07: Risk severity

Each risk shall have a severity of High, Medium, or Low based on configurable rules. The dashboard shall show the rule or reason behind each risk so users can distinguish an alert from a judgment.

### FR-08: Issue investigation

Users shall be able to select an issue and open its Jira URL. Power BI shall show enough identifying information to trace every dashboard record back to Jira.

### FR-09: Refresh

The default refresh schedule shall be daily, with the exact time configurable around the team's Scrum schedule. The implementation should allow a higher frequency if Power BI licensing, Jira limits, and the selected architecture support it. A manual refresh or rerun procedure shall be documented.

### FR-10: Notifications

Version 1 should define, but may defer implementation of, a Teams or email notification containing newly detected High risks, affected issue keys, and a link to the dashboard.

### FR-11: Auditability

Each load shall record extraction start time, completion time, source project, record count, status, and error details when applicable.

## 6. Risk Rules

The following initial rules are recommended and shall be confirmed during implementation:

| Risk | Initial rule | Default severity |
|---|---|---|
| Blocked work | Issue is in a blocked/on-hold status or has a blocking relationship | High |
| Overdue work | Due date is before today and issue is unresolved | High |
| High-priority open work | High or critical priority issue is unresolved near sprint end | High |
| Stale issue | No update or meaningful activity for 3 business days | Medium |
| Scope growth | Sprint estimate increases after the sprint start date | Medium |
| Unassigned work | Active issue has no assignee | Medium |
| Spillover risk | Issue remains incomplete at sprint end or is repeatedly carried over | Medium |
| Defect concentration | Open bugs exceed a configurable count or percentage threshold | Medium |

Rules shall account for Jira statuses and field names configured by the organization rather than assuming standard names.

## 7. Data Model

### 7.1 FactIssue

One row per Jira issue snapshot or current issue record, including issue key, project, sprint, status, assignee, priority, story points, dates, URL, and extraction timestamp.

### 7.2 FactSprintSnapshot

One row per project and sprint extraction, including sprint dates, total scope, completed scope, issue counts, story points, and scope-change measures.

### 7.3 FactRisk

One row per issue-risk combination, including risk type, severity, explanation, detection timestamp, and resolution state where available.

### 7.4 Dimensions

- `DimProject`
- `DimSprint`
- `DimIssueType`
- `DimStatus`
- `DimPriority`
- `DimAssignee`
- `DimDate`

## 8. Power BI Report Design

### Page 1: Executive risk summary

- Overall risk status
- High, Medium, and Low risk counts
- Sprint completion and days remaining
- Scope change indicator
- Top five risks requiring attention
- Last successful refresh timestamp

### Page 2: Sprint health

- Completed versus remaining story points
- Completed versus remaining issue count
- Sprint burndown or completion trend
- Current sprint compared with recent sprints
- Spillover and scope-change indicators

### Page 3: Team workload

- Active issues by assignee
- Story points by assignee
- Unassigned work
- High-priority work by assignee
- Configurable capacity comparison when capacity data becomes available

### Page 4: Risk register

- Filterable risk table
- Issue key and Jira link
- Risk type and severity
- Assignee, status, priority, sprint, and age
- Explanation of why the issue was flagged

## 9. Security and Compliance

- Use Jira OAuth 2.0 or an organization-approved service account/API token.
- Store secrets in an approved secret manager or Power BI-managed credential store.
- Keep credentials out of source code, report files, logs, and client-side JavaScript.
- Apply least-privilege Jira permissions.
- Restrict Power BI workspace and report access to authorized internal users.
- Use row-level security only if different audiences require different project or team visibility.
- Avoid importing unnecessary personal or sensitive Jira fields.
- Define retention for extracted historical data and refresh logs.

## 10. Reliability and Operations

- Retry transient Jira and Power BI failures with bounded backoff.
- Respect Jira API rate limits and pagination.
- Handle missing custom fields and incomplete issue data without failing the entire load.
- Mark partial or failed loads clearly so stale data is not mistaken for current data.
- Monitor refresh failures and record actionable error messages.
- Provide a runbook covering credentials, project configuration, refresh failures, and Jira schema changes.

## 11. Assumptions

- Jira is Jira Cloud unless confirmed otherwise.
- The first release covers one UI project.
- The team has approximately 10 people.
- Power BI is the required reporting and visualization platform.
- Daily refresh is sufficient for the first release.
- Jira remains the authoritative source of delivery data.
- The organization can provide an approved Jira integration method and Power BI workspace.
- Sprint length, capacity method, exact Jira statuses, and custom field identifiers remain to be confirmed.

## 12. Acceptance Criteria

- A configured Jira project loads successfully without manual spreadsheet extraction.
- The Power BI report displays the current sprint and refresh timestamp.
- Users can filter by sprint, status, priority, issue type, and assignee.
- Story-point and issue-count completion are both visible.
- Blocked, overdue, high-priority, stale, unassigned, and spillover risks are surfaced using documented rules.
- Every displayed issue can be opened in Jira.
- A failed or partial extraction is visible to the operator and does not silently appear current.
- The report supports desktop use and remains readable on a standard tablet viewport.
- A non-technical Scrum Master can operate the normal refresh and review workflow using the runbook.

## 13. Delivery Plan

### Phase 1: Discovery and connection

Confirm Jira site, project key, authentication, issue types, custom fields, statuses, sprint conventions, Power BI licensing, and approved hosting.

### Phase 2: Extraction prototype

Implement a read-only Jira extraction for one project, validate pagination and field mappings, and capture extraction logs.

### Phase 3: Data model and risk logic

Create normalized reporting tables, implement configurable risk rules, and validate results against manually reviewed Jira examples.

### Phase 4: Power BI report

Build the four report pages, filters, drill-through links, refresh metadata, and accessibility-friendly risk indicators.

### Phase 5: Operational hardening

Configure scheduled refresh, error handling, permissions, monitoring, documentation, and user acceptance testing.

## 14. Open Decisions

1. Confirm Jira Cloud versus Jira Server/Data Center.
2. Confirm the Jira project key and site URL.
3. Choose Power BI connector-only, Python/Azure Function, or another approved extraction architecture.
4. Confirm the approved authentication method.
5. Confirm sprint length and refresh time.
6. Confirm the Jira fields for story points, sprint, blocked state, and capacity.
7. Confirm stale-activity threshold and risk severity thresholds.
8. Decide whether Teams/email alerts are required in version 1.
9. Decide whether historical data must be retained beyond the current and recent sprints.
10. Confirm the Power BI workspace, licensing, and audience permissions.
