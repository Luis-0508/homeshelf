# 0003. GitHub issues for planned work

- Status: Accepted
- Date: 2026-10-27

## Context

The maintainer's shared project template made a local claude-kanban board the default for planned
work. This repository never had tickets on it. The maintainer moved all projects off the board at
the same time, because the board duplicated state kept in GitHub and `docs/PROJECT_STATE.md` and
added to the context of every Claude Code session.

## Decision

- Planned work lives in GitHub issues: one issue per pull request, grouped by milestone, with goal,
  acceptance criteria and a "Depends on" list. Pull requests close their issue with `Closes #N`.
- The board merge driver and its git attribute are removed. The SessionStart hook shows open pull
  requests and issues assigned to the maintainer through `gh`, skipping that part silently when `gh`
  is unavailable.
- Priority order lives in "Next priorities" in `docs/PROJECT_STATE.md`.
- The project memory and the SessionStart hook stay unchanged otherwise.

## Alternatives considered

- Keep the board with stricter usage rules: lowers context use but keeps the duplicated state and
  the merge driver.
- A GitHub Project board: adds ordering and columns, but is another place to maintain; milestones
  and the state file are enough for now.

## Consequences

- One source for planned work; no board merges or board update pull requests.
- The hook makes two short network calls; offline sessions just lose that section.
