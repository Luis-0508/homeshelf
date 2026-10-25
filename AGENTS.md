# Project agent guidance

Rules for anyone changing this repository: human contributors and coding agents
alike. They are tool-independent; tool-specific workflow lives in separate files
(for example `CLAUDE.md`) and never overrides these rules.

## Language and collaboration

- Treat this repository as a public open-source project with external contributors.
- Use English for code, identifiers, documentation, README content, filenames, folder names, code comments, configuration comments, branch names, commit messages, pull request titles/descriptions, and issue text.
- Do not force a conversation language. Follow the contributor's or user's language for discussion.
- User-facing product text may use the product's current language. Repository language and product language are separate concerns.
- When i18n exists, keep all supported locales complete and consistent.

## Project knowledge

The repository is the source of truth. Short documents in `docs/` record what the code alone cannot tell:

| File | Purpose |
|---|---|
| `docs/PROJECT_STATE.md` | What exists, active work, blockers, next priorities. A snapshot that may be stale. |
| `docs/ARCHITECTURE.md` | Modules, boundaries and data flow a maintainer needs to change the code safely. |
| `docs/DECISIONS/` | Numbered decision records: context, decision, consequences. |

- Read `PROJECT_STATE.md` before larger work, and the architecture or decision records only when the task touches that area.
- When a document disagrees with git or the code, trust the repository and correct the document.
- Update `ARCHITECTURE.md` when modules, boundaries or data flow change. Add a decision record when choosing between real alternatives a future maintainer might question (new dependency, architecture boundary, data format, workflow). Do not rewrite accepted records; supersede them with a new one.
- Keep these documents short and factual. Do not document unimplemented features.
- `docs/WORKFLOW.md` explains how these documents, the maintainer's task board (not required for contributors) and the workflow checks fit together.

## Engineering

- Preserve the current architecture unless the task requires a deliberate change. Keep clear boundaries between domain logic, I/O, and presentation; dependencies point inward.
- Make the smallest complete, maintainable change. Avoid unrelated refactors, formatting churn, speculative abstractions, duplicate documentation, and unnecessary configuration.
- Reuse existing patterns, types, utilities, components, and tooling before adding new ones.
- Handle errors and edge cases at the boundaries where they occur. Fail loudly on programmer errors; never swallow failures silently.
- Preserve existing behavior unless a change is requested, and preserve accessibility, responsiveness, and visual consistency in user interfaces.

## Testing

- Add or update automated tests when behavior changes, at the lowest level that proves it (unit before integration before end-to-end).
- Fix the cause of a failing test rather than weakening or deleting the test.
- Run the most relevant checks for the changed area (lint, type check, tests, build). Never claim a check passed unless it actually ran successfully, and report checks that were skipped.

## Security and dependencies

- Keep secrets, credentials, personal data, and private infrastructure details out of source, logs, fixtures, screenshots, and documentation. Use `.env.example` for configuration shape only.
- Validate untrusted input at system boundaries and use parameterized APIs instead of string-built queries or shell commands.
- Add a dependency only when it removes real complexity. Prefer maintained, widely used packages with a compatible license, commit lockfiles, and avoid unpinned or install-time-script-heavy packages without reason.
- Keep GitHub Actions pinned to immutable commit SHAs and workflow permissions minimal.
- Report vulnerabilities privately as described in `SECURITY.md`.

## Documentation and README

- Update README or contributor documentation when setup, architecture, behavior, or contributor workflow materially changes. Prefer updating existing documents over creating new ones.
- Keep the README polished rather than a plain documentation dump: a centered project mark/logo when available, project title, one-line bold tagline, a small row of meaningful badges, one strong real hero screenshot/render, then overview and feature sections.
- For visual projects, use real screenshots or renders of the current product. When several exist, prefer a compact two-column HTML table/gallery with short captions over a long vertical image list.
- Use repository-owned assets under `docs/images/` (or an existing project asset directory). Optimize large screenshots for GitHub display when practical.
- Badges must describe the real project only: CI, primary framework/runtime, language, important core technology, and license are good defaults. Avoid badge clutter.
- Never fabricate logos, screenshots, benchmarks, integrations, project status, sources, or capabilities. If no real visual exists yet, leave the visual placeholder commented out.

## Efficiency

- Start with the requested change and the nearest relevant files and tests.
- Prefer targeted searches and small file ranges over broad repository dumps.
- Do not repeatedly re-read unchanged files or preload unrelated documentation.
- Keep final reports concise: what changed, what was checked, and remaining risks or blockers.

## Git and pull requests

- Use a focused branch and pull request for every normal change; one concern per pull request.
- Write commits as coherent, descriptive units (for example `feat: add export dialog`, `fix: handle empty input`). Do not commit secrets, generated artifacts, or unrelated modifications.
- Fill in the pull request template: summary, validation actually run, risks and follow-ups. Reference related issues (`Closes #N`).
- Do not force-push or rewrite shared history unless explicitly required.
- Do not merge with failing required checks or known blockers. Merging is a maintainer decision.
- Prefer squash merging for feature/fix pull requests unless preserving individual commits has a concrete benefit.
- Treat automated review findings as suggestions to verify rather than instructions to apply blindly.

## Repository automation

- Keep automatic pull request labeling enabled and adapt `.github/labeler.yml` when project structure changes.
- Keep Dependabot enabled. Check dependencies every calendar day, including weekends, and use a high open-PR limit so updates stay visible.
- Add the relevant Dependabot package ecosystem as soon as a package manager or build ecosystem is introduced.
- Keep the repository ready for external contributors: README, contribution guidance, security guidance, and issue/PR templates should stay current.

## Before making a repository public

- Replace all template placeholders, including those in `docs/`.
- Add an appropriate open-source license.
- Add real screenshots/project imagery where they improve the README.
- Confirm secrets and private infrastructure details are absent.
- Confirm CI, Dependabot, and automatic labeling are active.
