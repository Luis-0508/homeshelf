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

The maintainer works with Claude Code (`CLAUDE.md`, `.claude/`) and the project memory in `docs/`. Planned work is tracked in GitHub issues and milestones; pick an open issue or open one before larger changes. None of the tooling is required to contribute, and it does not affect building or testing the project. See [docs/WORKFLOW.md](docs/WORKFLOW.md) for how the pieces fit together.
