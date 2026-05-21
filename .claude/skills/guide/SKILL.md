---
name: guide
description: 'Project onboarding assistant and knowledge base backed by auto-generated wiki files. ALWAYS use this skill when the user wants to understand, explore, or look up anything about the codebase — including project structure, architecture, tech stack, conventions, KB structure, pipeline stages, or where something is located. Also triggers for onboarding new developers, refreshing/updating wiki, and answering "how does X work" or "what is X" questions. Do NOT use for creating/modifying code, adding functions, fixing bugs — those have dedicated skills.'
---

# Guide - Project Onboarding Assistant

Answer questions about the Finpath Newsroom codebase using the auto-generated wiki as the primary knowledge source, with codebase exploration as fallback.

## Wiki Files

All wiki files are in `docs/wiki/`:

| File               | Type   | Read when user asks about...                                                  |
| ------------------ | ------ | ----------------------------------------------------------------------------- |
| `architecture.md`  | Manual | System overview, directory structure, data flow, tech stack                   |
| `onboarding.md`    | Manual | New developer guide, "I'm new", getting started                               |
| `features-map.md`  | Auto   | Feature (chức năng) index, pipeline stages, workers, KB domains               |
| `skills-guide.md`  | Auto   | Available Claude skills, "what can you do"                                    |

## Workflow

1. **Classify** the question and determine which wiki file(s) to read (see table above).

   - If multiple files are relevant, read them in parallel.
   - For "how does X work" / "chức năng X" / feature level questions → read `features-map.md` first.

2. **Read wiki** file(s) and compose a clear answer in Vietnamese.

3. **Explore codebase** if wiki is insufficient:

   - Lib functions → `lib/*.py`, `lib/stages/*.py`
   - KB content → `kb/{sector}/`
   - Web frontend → `web/src/`
   - Worker → `worker/`
   - Skills → `.claude/skills/`

4. **Format response** with code blocks, tables, and file paths. Always include relevant file paths so the user can navigate directly.

## Onboarding Path

When a developer says they're new or asks for onboarding:

1. **Architecture** → Read and summarize `architecture.md`
2. **Features** → Read and summarize `features-map.md`
3. **Skills** → Read `skills-guide.md`, explain key skills
4. **KB Structure** → Walk through `kb/` directories (bank, ck, bds, oil-gas)

Present one step at a time, ask if the user wants to continue to the next step.

## Updating Wiki

When the user asks to update or refresh wiki content (e.g., "update wiki", "refresh wiki", "cập nhật wiki"):

### Auto-generated files (scan from codebase)

Run the scan scripts to regenerate auto-generated wiki files:

```bash
bash .claude/skills/guide/scripts/scan-all.sh
```

Or run individual scans:

```bash
bash .claude/skills/guide/scripts/scan-skills.sh    # docs/wiki/skills-guide.md
bash .claude/skills/guide/scripts/scan-features.sh  # docs/wiki/features-map.md
```

### Manual files (edit directly)

When the user asks to update manual wiki files (`architecture.md`, `onboarding.md`):

1. **Read** the current file from `docs/wiki/`
2. **Ask** the user what to add/change/remove (or apply if they already specified)
3. **Edit** the file directly
4. Confirm the update to the user

## Notes

- Wiki-first: always check wiki before exploring codebase
- Respond in Vietnamese
- Keep answers concise — link to specific files (e.g., `lib/pipeline_db.py:15`)
- For "where is X" questions, search wiki maps first, then grep codebase if not found
