"""Minimal, reversible remote control for a Samsung Tizen TV via the official
local network API (samsungtvws). It only sends remote-control keys and
launches/queries apps; it never installs, uninstalls or changes settings by itself.

  info                 read-only REST device info (no prompt on the TV)
  pair --yes           opens the secure websocket (port 8002); the TV shows an
                       "Allow" prompt. The token is stored in tools/tv-token.txt.
  key KEY [KEY ...]    send remote keys, e.g. KEY_HOME KEY_RIGHT KEY_ENTER
  apps                 list installed apps (needs pairing)
  status APP_ID        app status via REST
  launch APP_ID        launch an app via REST

Revoke access at any time on the TV: Settings > General > External Device
Manager > Device Connection Manager > Device List (delete the entry), then
delete tools/tv-token.txt.

Usage: python -I tools/tv_control.py --host <tv-ip> info
"""
import argparse
import json
import os
import sys

from samsungtvws import SamsungTVWS

TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tv-token.txt")
CLIENT_NAME = "TVCleanup"


def tv(host, secure):
    if secure:
        return SamsungTVWS(host=host, port=8002, token_file=TOKEN_FILE, timeout=30, name=CLIENT_NAME)
    return SamsungTVWS(host=host, port=8001, timeout=10, name=CLIENT_NAME)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info")
    p = sub.add_parser("pair")
    p.add_argument("--yes", action="store_true", help="confirm that the Allow prompt may appear")
    k = sub.add_parser("key")
    k.add_argument("keys", nargs="+")
    sub.add_parser("apps")
    for name in ("status", "launch"):
        sub.add_parser(name).add_argument("app_id")
    args = ap.parse_args()

    if args.cmd == "info":
        print(json.dumps(tv(args.host, False).rest_device_info(), indent=2))
    elif args.cmd == "pair":
        if not args.yes:
            sys.exit("Refusing: pairing shows a prompt on the TV. Re-run with --yes.")
        t = tv(args.host, True)
        t.open()
        t.close()
        print("Paired." if os.path.exists(TOKEN_FILE) else "Connected, but the TV issued no token.")
    elif args.cmd == "key":
        t = tv(args.host, True)
        for key in args.keys:
            if not key.startswith("KEY_"):
                sys.exit(f"Not a key code: {key}")
            t.send_key(key)
        t.close()
    elif args.cmd == "apps":
        t = tv(args.host, True)
        print(json.dumps(t.app_list(), indent=2))
        t.close()
    elif args.cmd == "status":
        print(json.dumps(tv(args.host, False).rest_app_status(args.app_id), indent=2))
    elif args.cmd == "launch":
        print(json.dumps(tv(args.host, False).rest_app_run(args.app_id), indent=2))


if __name__ == "__main__":
    main()
