# Platform limits on a 2018 Samsung TV (Tizen 4.0)

What a signed web app can and cannot do on the reference TV, measured in
Developer Mode with [`tools/tv_inspect.py`](../tools/tv_inspect.py) and SDB.
**measured** = observed on the device; **documented** = Samsung or Tizen
documentation only.

## Reference device

| Item | Value |
|---|---|
| Model / group | UE43NU7099, `18_KANTSU_UHD_BASIC` (REST `:8001/api/v2/`) |
| Platform build | `TIZEN-4.0-TRUNK2018-KantSU-HOTFIX-RELEASE_20260402.1` (`systeminfo` BUILD) |
| CPU | SDP1404, ARMv7 32-bit; native and web API version 3.0 |
| Web engine | UA `Tizen 4.0 … TV Safari/537.36` (Chromium M56 per Samsung): ES5 and plain CSS only |
| SDB | sdbd 2.2.31, plugin `3.4.1_TV_REL`; `sdbd_rootperm`, `rootonoff_support`, `intershell_support`, `appcmd_support` all disabled |
| SDB shell | only `0 applist`, `0 debug <appId>`, `0 kill <pkgId>`; anything else (`0 help`, `id`, `ls`, `vconftool get`) returns `closed` |

The Samsung software version (`T-KTSU…`) is not readable without extra
privileges: REST reports `Unknown`, the UPnP descriptions omit it, and
`webapis.productinfo` needs the `productinfo` privilege. Read it on the TV
under Settings › Support › About This TV.

## Application API

| Topic | Result |
|---|---|
| `getAppsInfo()` | measured: ~206 entries, ~3 s. `show` is `true` even for services and test apps; names are ambiguous ("Netflix" ×3, "Apple TV" ×2, "YouTube" plus the internal Cobalt "Youtube") and differ from Smart Hub names |
| `getAppInfo(id)` | measured: synchronous, four apps in ~0.3 s |
| Which ID to launch | measured: the store-level IDs Smart Hub starts, matched by version via REST `GET /api/v2/applications/<id>` (which also accepts Tizen IDs): YouTube `9Ur5IzDKqV.TizenYouTube`, Netflix `RN1MCdNq8t.Netflix`, Joyn `cg2m3QSB89.7tv`, Disney+ `MCmYXNxgcu.DisneyPlus`. All IDs: `sdb shell 0 applist` |
| Lifecycle | measured: launching another app **terminates** the launcher; every return is a cold start. Samsung documents multitasking for 2018 only on `18TV_PREMIUM` |
| `addAppStatusChangeListener` | measured: registers (Tizen 4.0 API) |
| `exit()` | measured: no hidden background app is brought to the front |

## Input

| Topic | Result |
|---|---|
| Registrable keys | measured: 47 via `tvinputdevice.getSupportedKeys()` — digits, colours (403–406), media, Source, Menu, Tools, Info, Exit, Guide, ChannelList and more. **Home and Smart Hub are not registrable** |
| Key events | measured: remote OK arrives as `keydown`/`keyup` 13 with `repeat=false`; the Home overlay delivers no keys and fires no `visibilitychange` |

## TV picture and inputs

| Topic | Result |
|---|---|
| `tizen.tvwindow` | measured: `show()`/`getRect()` report the requested rectangle; `tv.pip = true`. The picture is composed **behind** the page, so the page must be transparent there |
| `VIDEOSOURCE` | measured: unreliable — an HDMI input in use was listed under `disconnected` |
| Without reception | measured: tuner reports 720×576, aspect `UNKNOWN`; HDMI without a picture 720×480, aspect `UNKNOWN`; window stays black |
| `Page.captureScreenshot` (DevTools) | measured: the TV's inspector drops the connection |

## Background work and Smart Hub

| Topic | Result |
|---|---|
| Web service app | measured: `feature/web.service = false`; Samsung's Smart Hub Preview Q&A says to check this capability before starting a service |
| `webapis.preview` (Personal Preview) | measured: absent |
| Public Preview (`use.preview` + JSON URL) | measured: installed metadata is correct and the TV can reach the host, yet Smart Hub never requested the JSON — not after adding the app to the Home bar, not after a cold boot. Cause unknown (store-only, or fetched through Samsung's servers) |
| `webapis.productinfo`, `webapis.network` | measured: `SecurityError` without their privileges; `webapis.js` must be loaded from `$WEBAPIS/webapis/webapis.js` |

## Consequences for a launcher

- The Home button stays with Samsung (see [HOME_REPLACEMENT.md](HOME_REPLACEMENT.md)).
- Start fast and keep state yourself: HomeShelf uses `getAppInfo()` for its
  pinned apps and stores the focused tile in `localStorage`.
- Launch on `keyup` only after a matching `keydown` was seen, so the OK press
  that opened the launcher cannot start a tile.

## Sources

Samsung Developers: [Application API](https://developer.samsung.com/smarttv/develop/api-references/tizen-web-device-api-references/application-api.html),
[Remote Control](https://developer.samsung.com/smarttv/develop/guides/user-interaction/remote-control.html),
[Multitasking](https://developer.samsung.com/smarttv/develop/guides/fundamentals/multitasking.html),
[TVWindow API](https://developer.samsung.com/smarttv/develop/api-references/tizen-web-device-api-references/tvwindow-api.html),
[Smart Hub Preview](https://developer.samsung.com/smarttv/develop/guides/smart-hub-preview/smart-hub-preview.html),
[Public Preview](https://developer.samsung.com/smarttv/develop/guides/smart-hub-preview/implementing-public-preview.html),
[Smart Hub Preview Q&A](https://developer.samsung.com/smarttv/develop/faq/smart-hub-preview.html).
