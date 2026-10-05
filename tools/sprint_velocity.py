"""Calculate sprint velocity from story point values."""

import argparse
import math


def calculate_velocity(story_points: list[float]) -> dict[str, float | int]:
    """Return sprint statistics for a set of story point values."""
    cleaned = [float(value) for value in story_points if value is not None]
    if not cleaned:
        raise ValueError('At least one story point value is required.')

    total = sum(cleaned)
    average = total / len(cleaned)
    ordered = sorted(cleaned)
    midpoint = len(ordered) // 2
    median = ordered[midpoint] if len(ordered) % 2 else (ordered[midpoint - 1] + ordered[midpoint]) / 2

    return {
        'total': total,
        'average': average,
        'median': median,
        'minimum': min(cleaned),
        'maximum': max(cleaned),
        'count': len(cleaned),
    }


def parse_arguments() -> argparse.Namespace:
    """Parse sprint velocity input values from the command line."""
    parser = argparse.ArgumentParser(description='Calculate sprint velocity from story point values.')
    parser.add_argument(
        '--story-points',
        nargs='+',
        default=[],
        help='Story point values such as 5 8 13 8 5. You may also provide a comma-separated list in one argument.',
    )
    return parser.parse_args()


def _normalize_points(raw_values: list[str]) -> list[float]:
    """Normalize comma-delimited or whitespace-delimited point values."""
    flattened: list[float] = []
    for item in raw_values:
        for part in item.split(','):
            stripped = part.strip()
            if stripped:
                flattened.append(float(stripped))
    return flattened


def main() -> None:
    """Compute and print sprint velocity summary values."""
    args = parse_arguments()
    values = _normalize_points(args.story_points)
    if not values:
        raise SystemExit('Provide at least one story point value with --story-points.')

    stats = calculate_velocity(values)
    print(f"Total story points: {stats['total']:.2f}")
    print(f"Average velocity: {stats['average']:.2f}")
    print(f"Median velocity: {stats['median']:.2f}")
    print(f"Minimum: {stats['minimum']:.2f}")
    print(f"Maximum: {stats['maximum']:.2f}")
    print(f"Sprint count: {stats['count']}")


if __name__ == '__main__':
    main()
