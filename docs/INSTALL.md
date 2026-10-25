# Install HomeShelf in Developer Mode

HomeShelf installs as an ordinary app. It does not replace Samsung's Home
button. Every step is reversible (see "Remove").

## 1. Tools on the computer

- Tizen SDK CLI (Tizen Studio or the stand-alone CLI) with the **TV
  Extensions** and **Samsung Certificate Extension** from the Package Manager.
  On Windows, install outside *Program Files* and run the installer and the
  Package Manager with administrator rights; never run the GUI and CLI
  Package Manager at the same time.
- Python 3.10+ for the helper tools: `pip install -r tools/requirements.txt`.

## 2. TV: Developer Mode

1. Open **Apps** on the TV and enter `1 2 3 4 5` on the remote.
2. Developer Mode **On**, Host PC IP = your computer's address, OK.
3. Restart the TV (hold Power for about five seconds).

## 3. Connect

```
sdb connect <tv-ip>:26101
sdb devices
```

The TV should be listed with its model name.

## 4. Samsung certificate

Create a **Samsung** TV author and distributor certificate in the Certificate
Manager and add the TV's DUID (read over the SDB connection). You sign in to
your Samsung account yourself. Keep the certificate files and passwords out of
this repository.

## 5. Package and install

Use paths without spaces. Without `install-permit` (which copies the device
profile to the TV), `install` fails with `118012`.

```
tizen install-permit -s <tv-ip>:26101
tizen package -t wgt -s <certificate-profile> -- app
tizen install -n HomeShelf.wgt -s <tv-ip>:26101 -- app
tizen run -p HmShlf0001.HomeShelf -s <tv-ip>:26101
```

Check on the TV: clock, four tiles (YouTube, Joyn, Netflix, Disney+), arrow
keys move focus, OK starts the app, the colour keys start the four apps
directly, Back closes HomeShelf. Adapt `PINNED` in `app/index.html` to your
apps; list the IDs with `sdb shell 0 applist`.

## 6. Debug on the device

```
sdb -s <tv-ip>:26101 shell 0 kill HmShlf0001
sdb -s <tv-ip>:26101 shell 0 debug HmShlf0001.HomeShelf
sdb -s <tv-ip>:26101 forward tcp:<port> tcp:<port>
python -I tools/tv_inspect.py --port <port> "window.__homeshelfLog"
```

`0 debug` blocks while the app is already running, hence the `kill` first.
You can also open `http://127.0.0.1:<port>` in Chrome for DevTools.

## Remove

1. `tizen uninstall -p HmShlf0001.HomeShelf -s <tv-ip>:26101`, or on the TV:
   Apps › Settings › HomeShelf › Delete.
2. Set Developer Mode back to its previous value or **Off**, then restart.
3. Revoke remote-control pairing (if you used `tools/tv_control.py pair`):
   Settings › General › External Device Manager › Device Connection Manager ›
   Device List, then delete `tools/tv-token.txt`.

Developer certificates expire; the app then needs to be re-signed and
reinstalled.
