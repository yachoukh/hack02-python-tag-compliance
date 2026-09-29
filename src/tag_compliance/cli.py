"""Command-line interface for tag compliance checks."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="Check Azure resource tag compliance")
    parser.add_argument("--policy", required=True, help="Path to tag-policy.yaml")
    parser.add_argument("--subscription", help="Azure subscription id")
    parser.add_argument("--resource-group", help="Optional Azure resource group filter")
    parser.add_argument("--input", help="Offline JSON resource fixture path")
    parser.add_argument("--format", choices=["table", "csv", "json", "md"], default="table")
    parser.add_argument("--output", help="Optional output file")
    parser.add_argument(
        "--fail-on-violations", dest="fail_on_violations", action="store_true", default=True
    )
    parser.add_argument("--no-fail", dest="fail_on_violations", action="store_false")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI."""
    build_parser().parse_args(argv)
    raise NotImplementedError("Complete the challenges to implement the CLI")
