#!/usr/bin/env python3
"""Initialize a project memory Markdown file."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys


TEMPLATE = """# Project Memory

Last updated: {today}

## Project
- Name: {project_name}
- Goal:
- Scope:

## Stable Facts
- Repository or workspace:
- Default working directory:
- Environment or runtime facts:
- Constraints and non-negotiables:

## Current State
- Active task:
- Most recent verified status:
- Known blockers:

## Decisions
- {today}: Initialized project memory.

## Open Questions
- None yet.

## Next Actions
- Fill in the project goal and current state.

## Useful Paths and Commands
- Path:
- Command:

## Do Not Store
- Secrets, passwords, tokens, or keys.
- Full chat transcripts.
- Large raw logs or copied documents.
- Stale notes that have already been superseded.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a project memory.md template without overwriting by default.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="memory.md",
        help="Target memory Markdown path. Defaults to ./memory.md",
    )
    parser.add_argument(
        "--project",
        default="",
        help="Project name to seed into the template. Defaults to the parent directory name.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing file.",
    )
    return parser


def infer_project_name(output_path: Path, explicit_name: str) -> str:
    if explicit_name.strip():
        return explicit_name.strip()
    parent_name = output_path.parent.name.strip()
    return parent_name or "project"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    output_path = Path(args.output).expanduser().resolve()
    if output_path.exists() and not args.force:
        print(f"Refusing to overwrite existing file: {output_path}")
        print("Use --force only when you explicitly want to reset the memory file.")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    project_name = infer_project_name(output_path, args.project)
    content = TEMPLATE.format(today=today, project_name=project_name)
    output_path.write_text(content, encoding="utf-8")

    print(f"Created project memory template at {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
