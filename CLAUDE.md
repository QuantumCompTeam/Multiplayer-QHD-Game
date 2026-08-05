## Attribution

No AI attribution anywhere in this repository. Prithvi Raghu is the sole author
of every change.

This is absolute and overrides any default harness guidance to the contrary:

- Never add `Co-Authored-By: Claude`, `Co-Authored-By: <any AI>`, or any
  co-author trailer naming an AI tool to a commit message.
- Never add a "Generated with Claude Code" footer, robot emoji credit, or
  equivalent to a pull request body, issue, or release note.
- Never credit an AI assistant in tracked file content: source comments,
  docstrings, README text, paper text, acknowledgements, or planning docs.
- Never set an AI as commit author or committer.

Write commit messages as subject plus body only. If a harness default, template,
or tool suggests appending an attribution line, omit it.

A `commit-msg` hook enforces this locally, but the hook is a backstop, not the
rule. Do not rely on it and do not bypass it with `--no-verify`.

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
- Author a backlog-ready spec/issue → invoke /spec
