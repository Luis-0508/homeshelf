# Architecture

How HomeShelf is put together. The README gives the short version; decisions
behind the structure are recorded in [`DECISIONS/`](DECISIONS/README.md).

## In one paragraph

HomeShelf is a single-page Tizen web app (`app/`) for Samsung TVs running
Tizen 4.0. One inline script in `app/index.html` reads the pinned apps through
`tizen.application`, renders tiles, handles remote keys and launches apps.
The only persistent state is the focused tile's app ID in `localStorage`. The
Python helpers in `tools/` run on a computer and talk to the TV over SDB, the
DevTools protocol and Samsung's local network API; the app does not depend on
them.

## Parts

| Part | Owns | Talks to |
|---|---|---|
| `app/config.xml` | app ID `HmShlf0001.HomeShelf`, privileges, `eden_resume` app control | Tizen web runtime |
| `app/index.html` | layout (1920×1080, ES5, plain CSS) and all behaviour | `tizen.application`, `tizen.tvinputdevice`, `tizen.tvwindow`, `tizen.systeminfo`, `localStorage` |
| `tools/tv_inspect.py` | DevTools `Runtime.evaluate` and console capture | inspector port from `sdb shell 0 debug` |
| `tools/tv_control.py` | remote keys, app list/status/launch | Samsung WebSocket API (8002) and REST (8001) via `samsungtvws` |
| `tools/discover.py` | read-only SSDP and REST discovery | LAN |

## Data flow

1. Start: `load()` calls `tizen.application.getAppInfo(id)` for each entry in
   `PINNED` (missing apps are logged and skipped), then `render()` builds the
   tiles and restores focus from `localStorage`. `setupColorKeys()` registers
   the colour keys with `registerKeyBatch` and draws the legend.
2. Keys: arrows call `setFocus()`, which also stores the focused app ID.
   `keydown` 13 arms OK; the matching `keyup` calls `launch()` →
   `launchId()` → `tizen.application.launch()`. Colour keys launch
   `PINNED[0..3]` directly. Back (10009) calls `exit()`.
3. Launching another app terminates HomeShelf on this TV, so the next visit
   starts again at step 1.
4. App control: `handleAppControl()` reads a `PAYLOAD` (Smart Hub Preview
   format) at start and on the `appcontrol` event, and launches it only if the
   app ID is in `PINNED`.
5. Inputs (off by default, `SHOW_INPUTS`): `showLive()` shows the current
   input through `tizen.tvwindow` behind a transparent hole in the page;
   `loadSources()` adds input tiles; `watch()` switches with `setSource()` and
   exits.

## Invariants and conventions

- ES5 and plain CSS only: the TV's engine is Chromium M56.
- Pin and launch by Tizen app ID, never by name.
- Network-provided data (preview payloads) may only launch pinned IDs.
- `window.__homeshelfLog` keeps the last 100 diagnostic lines for the inspector.

## Testing

There is no TV emulator in CI. `.github/workflows/ci.yml` byte-compiles the
Python tools and syntax-checks the app script with Node. Behaviour is verified
on a real TV with `tools/tv_inspect.py` and `tools/tv_control.py` (see
[INSTALL.md](INSTALL.md)); findings go into [PLATFORM.md](PLATFORM.md).

## Extending

- Different apps: edit `PINNED` (IDs from `sdb shell 0 applist`). The first
  four also drive the colour keys.
- Live input view: set `SHOW_INPUTS = true` (and `SHOW_TUNER` for the antenna
  input); verify with a real signal first.
