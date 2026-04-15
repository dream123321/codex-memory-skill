#!/usr/bin/env python3
"""Manage Markdown reminder state for project-memory-md."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re
import sys


TEMPLATE = """# Memory Reminder State

Last updated: {today}

## State
- Interval days: {interval_days}
- Last prompted: {last_prompted}
- Last synced: {last_synced}

## Policy
- Ask whether to sync memory when the workflow is active and the interval has elapsed.
- Do not auto-write memory without user confirmation unless the user directly requests sync.
- After a successful sync, refresh `Last synced`.
- If the user declines the prompt, refresh `Last prompted` only.
"""


@dataclass
class ReminderState:
    interval_days: int = 1
    last_prompted: str = ""
    last_synced: str = ""
    last_updated: str = ""


def parse_iso_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def today_from_arg(raw: str | None) -> date:
    if raw:
        parsed = parse_iso_date(raw)
        if parsed is None:
            raise ValueError("today must use YYYY-MM-DD")
        return parsed
    return date.today()


def load_state(path: Path) -> ReminderState:
    if not path.exists():
        return ReminderState()

    text = path.read_text(encoding="utf-8")
    interval_match = re.search(r"^- Interval days:\s*(\d+)\s*$", text, re.MULTILINE)
    prompted_match = re.search(r"^- Last prompted:[ \t]*([^\r\n]*)$", text, re.MULTILINE)
    synced_match = re.search(r"^- Last synced:[ \t]*([^\r\n]*)$", text, re.MULTILINE)
    updated_match = re.search(r"^Last updated:[ \t]*([^\r\n]*)$", text, re.MULTILINE)

    return ReminderState(
        interval_days=int(interval_match.group(1)) if interval_match else 1,
        last_prompted=prompted_match.group(1).strip() if prompted_match else "",
        last_synced=synced_match.group(1).strip() if synced_match else "",
        last_updated=updated_match.group(1).strip() if updated_match else "",
    )


def write_state(path: Path, state: ReminderState, today: date) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = TEMPLATE.format(
        today=today.isoformat(),
        interval_days=state.interval_days,
        last_prompted=state.last_prompted,
        last_synced=state.last_synced,
    )
    path.write_text(content, encoding="utf-8")


def most_recent_marker(state: ReminderState) -> date | None:
    markers = [parse_iso_date(value) for value in (state.last_prompted, state.last_synced)]
    values = [item for item in markers if item is not None]
    return max(values) if values else None


def should_prompt(state: ReminderState, today: date) -> bool:
    anchor = most_recent_marker(state)
    if anchor is None:
        return True
    return (today - anchor).days >= state.interval_days


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage the once-per-day reminder state for project memory sync prompts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a reminder-state.md file")
    init_parser.add_argument("path", help="Path to reminder-state.md")
    init_parser.add_argument("--interval-days", type=int, default=1, help="Reminder interval in days")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    init_parser.add_argument("--today", default="", help="Override date in YYYY-MM-DD format")

    check_parser = subparsers.add_parser("should-prompt", help="Print whether a prompt is due")
    check_parser.add_argument("path", help="Path to reminder-state.md")
    check_parser.add_argument("--today", default="", help="Override date in YYYY-MM-DD format")

    mark_prompted_parser = subparsers.add_parser("mark-prompted", help="Record that a reminder was shown")
    mark_prompted_parser.add_argument("path", help="Path to reminder-state.md")
    mark_prompted_parser.add_argument("--today", default="", help="Override date in YYYY-MM-DD format")

    mark_synced_parser = subparsers.add_parser("mark-synced", help="Record that memory was synced")
    mark_synced_parser.add_argument("path", help="Path to reminder-state.md")
    mark_synced_parser.add_argument("--today", default="", help="Override date in YYYY-MM-DD format")

    return parser


def cmd_init(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser().resolve()
    if path.exists() and not args.force:
        print(f"Refusing to overwrite existing file: {path}")
        print("Use --force only when you explicitly want to reset the reminder state.")
        return 1

    today = today_from_arg(args.today or None)
    state = ReminderState(interval_days=max(1, args.interval_days))
    write_state(path, state, today)
    print(f"Initialized reminder state at {path}")
    return 0


def cmd_should_prompt(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser().resolve()
    today = today_from_arg(args.today or None)
    state = load_state(path)
    print("PROMPT" if should_prompt(state, today) else "SKIP")
    return 0


def cmd_mark_prompted(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser().resolve()
    today = today_from_arg(args.today or None)
    state = load_state(path)
    state.last_prompted = today.isoformat()
    write_state(path, state, today)
    print(f"Marked reminder as prompted on {today.isoformat()} at {path}")
    return 0


def cmd_mark_synced(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser().resolve()
    today = today_from_arg(args.today or None)
    state = load_state(path)
    marker = today.isoformat()
    state.last_prompted = marker
    state.last_synced = marker
    write_state(path, state, today)
    print(f"Marked reminder as synced on {marker} at {path}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "init":
            return cmd_init(args)
        if args.command == "should-prompt":
            return cmd_should_prompt(args)
        if args.command == "mark-prompted":
            return cmd_mark_prompted(args)
        if args.command == "mark-synced":
            return cmd_mark_synced(args)
    except ValueError as exc:
        print(str(exc))
        return 1

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
