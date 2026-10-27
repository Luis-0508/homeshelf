# Decision records

Short records of significant technical decisions: what was decided, why, and
what it costs. They are written when a decision is made and are not rewritten
later; a changed decision gets a new record that supersedes the old one.

Name files `NNNN-short-title.md`, numbered in order, and add each record to
the table.

| # | Decision | Status |
|---|---|---|
| [0001](0001-plain-es5-tizen-web-app.md) | Plain ES5 Tizen web app without a framework or build step | Accepted |
| [0002](0002-pin-apps-by-tizen-id.md) | Pin apps by Tizen app ID | Accepted |
| [0003](0003-github-issues-for-planned-work.md) | GitHub issues for planned work | Accepted |

## Template

```markdown
# NNNN. Title

- Status: Proposed | Accepted | Superseded by NNNN
- Date: YYYY-MM-DD

## Context
What problem or force made a decision necessary.

## Decision
What we do.

## Alternatives considered
The real options that were rejected, and why.

## Consequences
What becomes easier, what becomes harder, what to watch.
```
