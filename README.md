# codex-memory-skill

`project-memory-md` is a Codex skill for maintaining durable project memory in Markdown.

It supports:
- A main `memory.md` for project-wide context
- Named custom memory files for topic-specific reusable context
- Helper scripts to initialize both kinds of memory files

## Repository Layout

- `SKILL.md`: skill instructions
- `agents/openai.yaml`: UI metadata
- `scripts/init_memory.py`: initialize a main project memory file
- `scripts/init_named_memory.py`: initialize a named custom memory file
- `references/`: Markdown templates for memory files

## Example

Initialize a main memory file:

```powershell
py scripts/init_memory.py D:\path\to\project\memory.md --project "Project Name"
```

Initialize a named memory file:

```powershell
py scripts/init_named_memory.py D:\path\to\project\memory\remote-setup.md --title "Remote Setup" --purpose "Remember remote workflow and conventions"
```
