# codex-memory-skill

`project-memory-md` is a Codex skill for maintaining durable project memory in Markdown.

It supports:
- A main `memory.md` for project-wide context
- Named custom memory files for topic-specific reusable context
- A once-per-day reminder policy for asking whether to sync the current thread into memory
- Truth-filtered memory updates that keep only correct, verified, and key points
- Manual sync at any time when the user explicitly asks for it
- Helper scripts to initialize both kinds of memory files and the reminder state

## Repository Layout

- `SKILL.md`: skill instructions
- `agents/openai.yaml`: UI metadata
- `scripts/init_memory.py`: initialize a main project memory file
- `scripts/init_named_memory.py`: initialize a named custom memory file
- `scripts/reminder_state.py`: initialize and update the once-per-day reminder state
- `references/`: Markdown templates for memory files and reminder state

## Behavior

- When this memory workflow is active and more than 1 day has passed since the last reminder or sync, the skill should ask whether the current thread should be synced into memory.
- If the user says yes, the skill classifies and compresses the thread into the right memory file.
- If the user says no, the skill continues without writing memory.
- The user can always say `sync memory now` to bypass the reminder cadence.
- Incorrect claims, stale guesses, and disproved conclusions should not be written into memory. If something important is still unresolved, it should be kept as an open question instead of a false fact.

## Example

Initialize a main memory file:

```powershell
py scripts/init_memory.py D:\path\to\project\memory.md --project "Project Name"
```

Initialize a named memory file:

```powershell
py scripts/init_named_memory.py D:\path\to\project\memory\remote-setup.md --title "Remote Setup" --purpose "Remember remote workflow and conventions"
```

Initialize reminder state:

```powershell
py scripts/reminder_state.py init D:\path\to\project\memory\reminder-state.md --interval-days 1
```

Check whether a prompt is due:

```powershell
py scripts/reminder_state.py should-prompt D:\path\to\project\memory\reminder-state.md
```
