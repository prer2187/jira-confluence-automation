"""Format a list of Jira issues into a Markdown status report."""

import argparse
import json
from collections import defaultdict
from datetime import date
from typing import Iterable


def parse_issue(raw_issue: str) -> dict[str, str]:
    """Parse an issue entry from a CLI argument.

    Supported formats:
      - KEY|STATUS|ASSIGNEE|SUMMARY
      - {"key": "PROJ-1", "status": "In Progress", "assignee": "Alice", "summary": "API work"}
    """
    value = raw_issue.strip()
    if not value:
        raise ValueError('Issue entry is empty')

    if value.startswith('{'):
        payload = json.loads(value)
        return {
            'key': str(payload.get('key', 'UNKNOWN')),
            'status': str(payload.get('status', 'Unknown')),
            'assignee': str(payload.get('assignee', 'Unassigned')),
            'summary': str(payload.get('summary', 'No summary')),
        }

    parts = [part.strip() for part in value.split('|')]
    if len(parts) < 4:
        raise ValueError(
            'Issue entries must use KEY|STATUS|ASSIGNEE|SUMMARY or a JSON object string.'
        )

    return {
        'key': parts[0],
        'status': parts[1],
        'assignee': parts[2],
        'summary': '|'.join(parts[3:]),
    }


def _status_bucket(status: str) -> str:
    value = status.lower()
    if 'done' in value or 'closed' in value or 'resolved' in value:
        return 'completed'
    if 'block' in value or 'blocked' in value or 'waiting' in value:
        return 'blocked'
    return 'active'


def format_status_report(title: str, issues: Iterable[str], generated_on: str | None = None) -> str:
    """Return a Markdown status report string for the supplied issues."""
    issue_records = [parse_issue(issue) for issue in issues]
    if not issue_records:
        return '# No issues found\n\n- No Jira issues were provided.'

    if generated_on is None:
        generated_on = date.today().isoformat()

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in issue_records:
        grouped[_status_bucket(record['status'])].append(record)

    lines: list[str] = [f'# {title}', '', f'Generated: {generated_on}', '']
    lines.extend([
        '## Summary',
        f'- Total issues: {len(issue_records)}',
        f'- Active issues: {len(grouped["active"])}',
        f'- Completed: {len(grouped["completed"])}',
        f'- Blocked: {len(grouped["blocked"])}',
        '',
        '## Active Issues',
    ])

    if grouped['active']:
        for record in grouped['active']:
            lines.append(f'- {record["key"]} | {record["status"]} | {record["assignee"]} | {record["summary"]}')
    else:
        lines.append('- None')

    lines.extend(['', '## Completed Issues'])
    if grouped['completed']:
        for record in grouped['completed']:
            lines.append(f'- {record["key"]} | {record["status"]} | {record["assignee"]} | {record["summary"]}')
    else:
        lines.append('- None')

    lines.extend(['', '## Blocked Issues'])
    if grouped['blocked']:
        for record in grouped['blocked']:
            lines.append(f'- {record["key"]} | {record["status"]} | {record["assignee"]} | {record["summary"]}')
    else:
        lines.append('- None')

    return '\n'.join(lines) + '\n'


def parse_arguments() -> argparse.Namespace:
    """Parse arguments for the Markdown report formatter."""
    parser = argparse.ArgumentParser(description='Format Jira issues into a Markdown status report.')
    parser.add_argument('--title', default='Jira Status Report', help='Report title')
    parser.add_argument(
        '--issue',
        dest='issues',
        action='append',
        default=[],
        help='Issue in KEY|STATUS|ASSIGNEE|SUMMARY format, or a JSON object string. Repeat for multiple issues.',
    )
    parser.add_argument('--generated-on', help='Date for the report header in YYYY-MM-DD format')
    return parser.parse_args()


def main() -> None:
    """Print a Markdown Jira status report."""
    args = parse_arguments()
    report = format_status_report(args.title, args.issues, args.generated_on)
    print(report)


if __name__ == '__main__':
    main()
