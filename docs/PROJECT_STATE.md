# Project state

Narrative snapshot of where HomeShelf stands. **The repository is
authoritative:** if git, the code, the task board or GitHub disagree with this
file, trust them and correct this file.

- Last updated: 2026-10-26
- Verified against: `main` at `804e03a`

## What exists

- Tizen 4.0 web app (`app/`, version 0.2.4), verified on a UE43NU7099:
  four pinned apps by Tizen ID, ~0.3 s start, OK on keyup after a seen
  keydown, focus restored after every cold start, colour-key direct launch,
  Back exits.
- Live TV/HDMI view and input tiles in the code but off (`SHOW_INPUTS = false`).
- Smart Hub Preview `PAYLOAD` handling (pinned IDs only); the preview itself
  never appeared on the reference TV, so no `use.preview` metadata is set.
- Tools: `tv_inspect.py` (DevTools evaluate/console), `tv_control.py`
  (remote keys, app list/status/launch), `discover.py` (read-only discovery).
- Browser preview with simulated Tizen APIs (`scripts/preview/`) and the
  README screenshots rendered from it (`docs/images/`).
- Measured platform limits (`PLATFORM.md`) and the Home-replacement study
  (`HOME_REPLACEMENT.md`).

See [ARCHITECTURE.md](ARCHITECTURE.md) for how it fits together and
[DECISIONS/](DECISIONS/README.md) for why.

## Active work

- None. The initial import (#1) is merged and the repository is public.

## Blockers

- None.

## Next priorities

1. No board tickets yet. Candidate work, once the maintainer plans it:
   record the result of the *Autorun Last App* test from
   `HOME_REPLACEMENT.md`; optionally a photo of the real TV screen.

## Known limitations

- Only one TV model verified; package ID `HmShlf0001` and `PINNED` are tuned
  to it.
- No automated behaviour tests: CI checks syntax and builds the preview;
  behaviour is verified on the device. Screenshots are browser renders, not
  TV captures (no app icons, different font).
- Replacing the Home button is not possible with documented means on Tizen 4.0
  (see `HOME_REPLACEMENT.md`).
