#!/usr/bin/env python3
"""Initialize a reusable named memory Markdown file."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys


TEMPLATE = """# Custom Memory

Last updated: {today}

## Identity
- Title: {title}
- Purpose: {purpose}
- Trigger phrases: {trigger_phrases}

## Scope
- Use this memory when:
- Do not use this memory when:

## Durable Facts
- Fact:

## Decisions or Conventions
- {today}: Initialized named memory.

## Reuse Notes
- What to load first:
- What to verify again:
- What can safely be assumed:

## Next Useful Follow-Up
- Next likely action:

## Do Not Store
- Secrets, passwords, tokens, or keys.
- Full chat transcripts.
- Temporary logs with no reuse value.
"""


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "custom-memory"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a reusable custom memory Markdown file without overwriting by default.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="memory/custom-memory.md",
        help="Target custom memory Markdown path. Defaults to ./memory/custom-memory.md",
    )
    parser.add_argument(
        "--title",
        default="",
        help="Human-readable memory title.",
    )
    parser.add_argument(
        "--purpose",
        default="Reusable context for a specific topic.",
        help="Short explanation of why this memory exists.",
    )
    parser.add_argument(
        "--trigger",
        action="append",
        default=[],
        help="Trigger phrase that should cause this memory to be loaded. Repeat as needed.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing file.",
    )
    return parser


def infer_title(output_path: Path, explicit_title: str) -> str:
    if explicit_title.strip():
        return explicit_title.strip()
    stem = output_path.stem.replace("-", " ").replace("_", " ").strip()
    return stem.title() if stem else "Custom Memory"


def normalize_output_path(output_arg: str, explicit_title: str) -> Path:
    raw_path = Path(output_arg).expanduser()
    if raw_path.suffix.lower() == ".md":
        return raw_path.resolve()

    base_dir = raw_path.resolve()
    title = explicit_title.strip() or raw_path.name
    filename = f"{slugify(title)}.md"
    return (base_dir / filename).resolve()


def format_trigger_phrases(triggers: list[str], title: str) -> str:
    values = [item.strip() for item in triggers if item.strip()]
    if not values:
        values = [title]
    return ", ".join(values)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    output_path = normalize_output_path(args.output, args.title)
    if output_path.exists() and not args.force:
        print(f"Refusing to overwrite existing file: {output_path}")
        print("Use --force only when you explicitly want to reset the named memory file.")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    title = infer_title(output_path, args.title)
    content = TEMPLATE.format(
        today=today,
        title=title,
        purpose=args.purpose.strip(),
        trigger_phrases=format_trigger_phrases(args.trigger, title),
    )
    output_path.write_text(content, encoding="utf-8")

    print(f"Created custom memory template at {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
