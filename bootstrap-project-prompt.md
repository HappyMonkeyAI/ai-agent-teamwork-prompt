# Bootstrap Project — Agent Prompt

You are initializing a brand-new project repository for multi-agent collaboration.
Do not assume prior structure. Follow this prompt to set up the project correctly before implementation begins.

## 1. Project identity

- Use the repo name as the project title everywhere.
- If a README-TEMPLATE.md exists, use it as the starting point for README.md.

## 2. Required root files

Create these files at the repo root:

- `README.md` — user-facing overview, getting started, project goals
- `CONTEXT.md` — concise operating manual covering:
  - stack and runtime assumptions
  - non-negotiable rules
  - workflow protocols (manifest mode and branch mode)
  - resolved architecture decisions
  - what not to do
- `HERMES.md` or equivalent agent guide — agent behavior rules, repo workflow expectations, coordination rules

## 3. Required folders

Create this structure:

- `docs/adr/` — one ADR per significant architecture decision, short and decision-focused
- `research/` — external references, comparisons, and notes:
  - `research/README.md`
  - `research/LINKS.md`
  - `research/templates/project-note.md`
  - `research/github-projects/` — one note per external repo
  - `research/notes/` — optional deeper notes

## 4. Coordination initialization

Initialize the multi-agent coordination system:

1. Copy the coordination skill scripts to the project:
   ```
   python3 /home/stephen/.hermes/skills/devops/multi-agent-coordination/scripts/init.py
   ```
2. If needed, seed an initial `.agent-tasks.json` with slice 1 tasks for the first build.

## 5. Rules to follow

- Work in small feature slices.
- Keep docs concise, explicit, and project-specific.
- Update docs in the same change as code/workflow changes.
- Capture architecture decisions as ADRs, not prose.
- Prefer manifest mode for rapid prototyping, branch mode when clean merge history matters.
- `.agent-manifest.json`, `.agent-status.md`, and `.agent-tasks.json` should be in `.gitignore`.
- Add coordination rules from the skill template to `AGENTS.md` if the project uses one.
- Copy or adapt `templates/AGENTS.md` from **ai-agent-teamwork-prompt** (includes CLI profile routing).
- Point agents at canonical profiles: `~/projects/ai-agent-teamwork-prompt/profiles/`.

## 6. Delivery checklist

Before finishing:

- [ ] README.md exists and reflects current project
- [ ] CONTEXT.md captures runtime, rules, and coordination protocols
- [ ] HERMES.md exists with agent behavior rules (create if none exists)
- [ ] `docs/adr/` exists and contains at least one decision or a placeholder note
- [ ] `research/` skeleton exists with README and LINKS
- [ ] Coordination system initialized (`.agent-manifest.json`, `.agent-status.md`)
- [ ] `.gitignore` excludes coordination metadata
- [ ] `AGENTS.md` includes coordination template if applicable

## 7. Output

Summarize exactly what was created or changed and where. If you chose between alternatives, explain why.
