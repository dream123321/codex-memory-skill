---
name: "project-memory-md"
description: "Maintain project-scoped memory in Markdown, including a main `memory.md` and optional custom named memory files. Use when Codex needs to initialize, read, update, compress, or sync durable context across sessions, especially when the user mentions or attaches a `memory.md`, asks to create a reusable custom memory snippet, or wants Codex to load a specific memory file before continuing."
---

# Project Memory MD

## Overview
Maintain a compact `memory.md` as the durable top-level project memory. Support additional custom memory files for reusable topic-specific context such as remote setup, experiment notes, paper outlines, or task conventions.

## Workflow
1. Locate the memory file.
   - Prefer an explicitly mentioned Markdown file.
   - If the user asks for a named memory, prefer `<project-root>/memory/<slug>.md`.
   - Otherwise prefer `<project-root>/memory.md`.
   - If no file exists, initialize one with `scripts/init_memory.py`.
2. Load memory before acting.
   - Read the full file first.
   - Treat it as compressed context, not guaranteed truth.
   - Re-check anything that can drift over time, such as paths, branch names, versions, schedules, or status.
   - If multiple custom memories exist, read `memory/index.md` first when present, then only load the relevant file or files.
3. Update memory with durable information only.
   - Keep project goals, repo paths, environment facts, decisions, conventions, active work, open questions, next actions, and useful commands.
   - Drop greetings, raw chat transcripts, speculative chains of thought, repeated dead ends, giant logs, and copied source documents.
   - For custom memories, write only the topic-specific facts that are useful to reload later.
4. Upsert instead of append-only logging.
   - Rewrite sections so the file stays short and navigable.
   - Merge duplicates.
   - Remove or rewrite stale statements when newer decisions supersede them.
   - Preserve user-authored notes unless they are clearly outdated or explicitly replaced.
5. Stamp the update.
   - Refresh `Last updated`.
   - Convert relative dates like "today" into absolute dates.
6. Reuse memory in later sessions.
   - If the user @mentions the memory file, read it first and rebuild context from it before repeating background questions.
   - If the user asks for a named memory, locate that custom `.md` and load it before continuing.

## Real-Time Limits
Do not claim that Codex can silently auto-save every turn in the background. In practice, Codex updates the file when the user asks to sync memory, when the workflow explicitly calls for an update, or when the user and agent agree on a checkpoint such as end-of-task.

## Memory Shape
Keep `memory.md` short, usually under 200 lines, with stable sections:
- `Project`
- `Stable Facts`
- `Current State`
- `Decisions`
- `Open Questions`
- `Next Actions`
- `Useful Paths and Commands`
- `Do Not Store`

Use the template in `references/memory-template.md` when creating or repairing the file.

For custom reusable memories, prefer separate files under `memory/`:
- `memory/index.md`: one-line directory of available memory files and when to load them
- `memory/<topic>.md`: one reusable memory capsule for a specific topic

Use the template in `references/custom-memory-template.md` or initialize a file with `scripts/init_named_memory.py`.

## Update Rules
- Prefer terse bullets over prose.
- Keep only information that would help a future session resume the project quickly.
- Mark uncertainty explicitly instead of presenting guesses as facts.
- Never store passwords, tokens, private keys, or copied secrets from chat, shell history, or config files.
- If a section no longer helps future work, delete it rather than preserving clutter.

## Initialization
Run the helper when a project does not already have a memory file:

```powershell
py C:\Users\27603\.codex\skills\project-memory-md\scripts\init_memory.py D:\path\to\project\memory.md --project "Project Name"
```

If the file already exists, do not overwrite it unless the user explicitly wants a reset.

To create a reusable custom memory file:

```powershell
py C:\Users\27603\.codex\skills\project-memory-md\scripts\init_named_memory.py D:\path\to\project\memory\remote-setup.md --title "Remote Setup" --purpose "Remember how this project connects to its remote environment"
```

When multiple custom memories exist, keep a lightweight `memory/index.md` so a future session can discover them quickly.

## Expected User Requests
- `Use $project-memory-md and initialize D:\repo\memory.md.`
- `Use $project-memory-md and sync the key decisions from this thread into D:\repo\memory.md.`
- `Read this @memory.md first, then continue the project.`
- `Create a custom memory file for remote setup and save it under D:\repo\memory\remote-setup.md.`
- `Load @D:\repo\memory\paper-outline.md before you continue writing.`
