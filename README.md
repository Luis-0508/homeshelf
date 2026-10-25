<div align="center">

# HomeShelf

**A fast, remote-first app shelf for 2018 Samsung Tizen 4.0 TVs — plus measured notes on what such a TV really allows.**

[![CI](https://github.com/Luis-0508/homeshelf/actions/workflows/ci.yml/badge.svg)](https://github.com/Luis-0508/homeshelf/actions/workflows/ci.yml)
[![Tizen](https://img.shields.io/badge/Tizen-4.0%20TV-1428a0)](https://developer.samsung.com/smarttv/develop)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES5-f7df1e?logo=javascript&logoColor=black)](app/index.html)
[![License](https://img.shields.io/badge/license-AGPL--3.0-4d6b2f)](LICENSE)

<!-- No screenshot yet: the TV's DevTools endpoint cannot capture the page, and
photos of the screen are still to be taken. Add a real one as docs/images/hero.webp. -->

</div>

## Overview

HomeShelf is a small Tizen web app that opens to a clock and a row of your
favourite streaming apps. It runs as an ordinary app installed in Developer
Mode; it does **not** replace Samsung's Home button (and on this TV generation
nothing documented can — see [docs/HOME_REPLACEMENT.md](docs/HOME_REPLACEMENT.md)).

It was built and verified on a Samsung UE43NU7099 (2018, Tizen 4.0, basic
model group). Along the way the project measured the platform's real limits —
app lifecycle, key handling, app IDs, TV window, Smart Hub Preview, SDB access
— and recorded them in [docs/PLATFORM.md](docs/PLATFORM.md). Those notes are
probably the most useful part for anyone building for these TVs.

## Features

**Unambiguous app pinning.** Apps are pinned by Tizen app ID, because names
from `getAppsInfo()` are duplicated and differ from Smart Hub's. Pinned apps
load with `getAppInfo()` in about 0.3 s instead of ~3 s for the full list.

**Safe OK handling.** OK launches on `keyup`, and only after HomeShelf saw the
matching `keydown`, so the press that opened HomeShelf cannot start a tile.

**Remembers your place.** The launcher is terminated whenever it starts an app
on this TV, so the focused tile is stored and restored on every cold start.

**Colour-key direct launch.** Red, green, yellow and blue start the first four
pinned apps without moving focus.

**On-device tooling.** [`tools/tv_inspect.py`](tools/tv_inspect.py) evaluates
JavaScript inside the running app over the DevTools protocol;
[`tools/tv_control.py`](tools/tv_control.py) sends remote keys and queries apps
through Samsung's local network API; [`tools/discover.py`](tools/discover.py)
finds the TV read-only.

## Quick start

```bash
git clone https://github.com/Luis-0508/homeshelf.git
cd homeshelf
python -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
```

Then follow [docs/INSTALL.md](docs/INSTALL.md): Developer Mode, SDB connection,
Samsung certificate, `tizen package` and `tizen install`.

## Development

```bash
tizen package -t wgt -s <certificate-profile> -- app
tizen install -n HomeShelf.wgt -s <tv-ip>:26101 -- app
python -I tools/tv_inspect.py --port <port> "window.__homeshelfLog"
```

The web engine is Chromium M56: write ES5 and plain CSS. CI checks the Python
tools and the app script's syntax; app behaviour is verified on a real TV.

## Architecture

```text
app/     Tizen web app (config.xml, index.html, icon.png)
tools/   Python helpers for SDB/DevTools inspection and remote control
docs/    Platform measurements, Home-replacement study, install guide
```

Details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Project status

Works today on the reference TV: pinned tiles, focus restore, colour keys,
Back to exit. Present but switched off (`SHOW_INPUTS = false`): live TV/HDMI
picture and input tiles, unverified with a real signal. Not possible on this
TV with documented means: replacing the Home button, background services,
Smart Hub Preview tiles. Other models are untested.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Issues, pull requests, commit messages, documentation, filenames, and repository-facing technical text are written in English so contributors can collaborate consistently.

## Security

Please do not report security-sensitive issues publicly. See [SECURITY.md](SECURITY.md).

## License

[GNU Affero General Public License v3.0](LICENSE).

Samsung, Tizen and the app names shown in HomeShelf are trademarks of their
respective owners. This project is not affiliated with Samsung.
