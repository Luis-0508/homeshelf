# Contributing

Thanks for contributing.

## Language

Repository-facing collaboration is in English: documentation, filenames, branches, commits, issues, and pull requests. Conversation may use whatever language is natural for the contributor.

## Workflow

1. Create a focused branch from the default branch.
2. Make the smallest complete change that solves the issue.
3. Add or update relevant tests.
4. Run the relevant local checks.
5. Open a pull request with a clear English summary and validation notes.

## Pull requests

Keep pull requests focused. Avoid unrelated refactors or formatting changes. Explain behavior changes, testing, and any remaining limitations.

Automated review tools such as CodeRabbit provide suggestions. Verify findings against the actual code before applying them.

## Documentation

Update README or project documentation when setup, architecture, public behavior, or contributor workflow changes. Use real screenshots and project assets; do not fabricate visuals or capabilities.

Project knowledge lives in `docs/`: `PROJECT_STATE.md` (current state and priorities), `ARCHITECTURE.md` (structure and data flow) and `DECISIONS/` (decision records). Read the relevant parts before larger changes and update them when your change makes them inaccurate. `AGENTS.md` lists the full engineering rules.

## Optional tooling

The maintainer's default workflow uses Claude Code with a local Kanban board (`CLAUDE.md`, `.claude/`, `.kanban/`). None of it is required to contribute: the board is plain JSON you can read, and these files do not affect building or testing the project. Please do not edit `.kanban/board.json` by hand; mention the related issue in your pull request instead. See [docs/WORKFLOW.md](docs/WORKFLOW.md) for how the pieces fit together.
