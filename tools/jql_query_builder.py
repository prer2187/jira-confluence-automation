"""Build Jira JQL queries from command-line search parameters."""

import argparse


def _quote(value: str) -> str:
    """Return a Jira-safe quoted string."""
    return f'"{value.strip()}"'


def build_jql(
    project: str | None = None,
    status: list[str] | None = None,
    assignee: list[str] | None = None,
    reporter: list[str] | None = None,
    issue_type: list[str] | None = None,
    labels: list[str] | None = None,
    created_after: str | None = None,
    created_before: str | None = None,
    updated_after: str | None = None,
    due_before: str | None = None,
    extra_filter: str | None = None,
) -> str:
    """Construct a JQL query from common Jira filters."""
    clauses: list[str] = []

    if project:
        clauses.append(f'project = {_quote(project)}')

    if status:
        values = [item.strip() for item in status if item and item.strip()]
        if values:
            if len(values) == 1:
                clauses.append(f'status = {_quote(values[0])}')
            else:
                clauses.append(f'status in ({", ".join(_quote(v) for v in values)})')

    if assignee:
        values = [item.strip() for item in assignee if item and item.strip()]
        if values:
            if len(values) == 1:
                clauses.append(f'assignee = {_quote(values[0])}')
            else:
                clauses.append(f'assignee in ({", ".join(_quote(v) for v in values)})')

    if reporter:
        values = [item.strip() for item in reporter if item and item.strip()]
        if values:
            if len(values) == 1:
                clauses.append(f'reporter = {_quote(values[0])}')
            else:
                clauses.append(f'reporter in ({", ".join(_quote(v) for v in values)})')

    if issue_type:
        values = [item.strip() for item in issue_type if item and item.strip()]
        if values:
            if len(values) == 1:
                clauses.append(f'issuetype = {_quote(values[0])}')
            else:
                clauses.append(f'issuetype in ({", ".join(_quote(v) for v in values)})')

    if labels:
        values = [item.strip() for item in labels if item and item.strip()]
        if values:
            if len(values) == 1:
                clauses.append(f'labels = {_quote(values[0])}')
            else:
                clauses.append(f'labels in ({", ".join(_quote(v) for v in values)})')

    if created_after:
        clauses.append(f'created >= {_quote(created_after)}')
    if created_before:
        clauses.append(f'created <= {_quote(created_before)}')
    if updated_after:
        clauses.append(f'updated >= {_quote(updated_after)}')
    if due_before:
        clauses.append(f'due <= {_quote(due_before)}')

    if extra_filter:
        clauses.append(extra_filter.strip())

    return ' AND '.join(clauses) if clauses else 'ORDER BY created DESC'


def parse_arguments() -> argparse.Namespace:
    """Parse JQL builder arguments from the command line."""
    parser = argparse.ArgumentParser(description='Build a Jira JQL string from common filters.')
    parser.add_argument('--project', help='Project key such as PROJ')
    parser.add_argument('--status', nargs='*', default=[], help='One or more issue statuses')
    parser.add_argument('--assignee', nargs='*', default=[], help='One or more assignee names')
    parser.add_argument('--reporter', nargs='*', default=[], help='One or more reporter names')
    parser.add_argument('--issue-type', nargs='*', default=[], help='One or more issue type names')
    parser.add_argument('--labels', nargs='*', default=[], help='One or more labels')
    parser.add_argument('--created-after', help='Lower bound date such as 2026-01-01')
    parser.add_argument('--created-before', help='Upper bound date such as 2026-01-31')
    parser.add_argument('--updated-after', help='Updated since date such as 2026-01-15')
    parser.add_argument('--due-before', help='Due date upper bound such as 2026-02-01')
    parser.add_argument('--extra-filter', help='Additional raw JQL filter text to append')
    return parser.parse_args()


def main() -> None:
    """Build and print a JQL query string."""
    args = parse_arguments()
    query = build_jql(
        project=args.project,
        status=args.status,
        assignee=args.assignee,
        reporter=args.reporter,
        issue_type=args.issue_type,
        labels=args.labels,
        created_after=args.created_after,
        created_before=args.created_before,
        updated_after=args.updated_after,
        due_before=args.due_before,
        extra_filter=args.extra_filter,
    )
    print(query)


if __name__ == '__main__':
    main()
