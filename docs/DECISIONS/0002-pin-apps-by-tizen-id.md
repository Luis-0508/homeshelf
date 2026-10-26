# 0002. Pin apps by Tizen app ID

- Status: Accepted
- Date: 2026-10-25

## Context
The first version pinned apps by name. On the reference TV `getAppsInfo()`
returns about 200 entries, several with the same name ("Netflix" ×3,
"Apple TV" ×2, "YouTube" and an internal "Youtube"), and names that differ
from Smart Hub. The name match picked the internal native Netflix player, and
reading the whole list took about 3 s.

## Decision
`PINNED` lists Tizen app IDs — the store-level IDs Smart Hub itself launches,
matched to store IDs by version through the TV's REST API. Pinned apps are
read with synchronous `getAppInfo(id)`.

## Alternatives considered
- Names plus de-duplication: still ambiguous, and names are localised and
  differ from the visible Smart Hub names.
- Full `getAppsInfo()` with filters: slow, and `show` is `true` for services.

## Consequences
Correct app and ~0.3 s start. Users must look up IDs (`sdb shell 0 applist`)
to change the shelf; an uninstalled pinned app is skipped and logged.
