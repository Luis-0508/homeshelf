"""Evaluate JavaScript inside a Tizen web app on the TV via the Chrome DevTools
protocol. Debug-only and read-only by itself: it runs whatever expression you
pass, so keep expressions side-effect free unless you mean otherwise.

Prerequisite (launches the app in debug mode and forwards the inspector port):
  sdb -s <tv>:26101 shell 0 debug HmShlf0001.HomeShelf   -> "... port: NNNNN"
  sdb -s <tv>:26101 forward tcp:NNNNN tcp:NNNNN

Usage:
  .venv/Scripts/python -I tools/tv_inspect.py --port NNNNN "document.title"
  .venv/Scripts/python -I tools/tv_inspect.py --port NNNNN --await "new Promise(...)"
  .venv/Scripts/python -I tools/tv_inspect.py --port NNNNN --file probe.js
  .venv/Scripts/python -I tools/tv_inspect.py --port NNNNN --console 20

"0 debug" blocks while the app is already running; stop it first with
  sdb -s <tv>:26101 shell 0 kill HmShlf0001
"""
import argparse
import json
import time
import urllib.request

import websocket


def page_ws(port):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=10) as r:
        targets = json.loads(r.read().decode())
    return targets[0]["webSocketDebuggerUrl"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--await", dest="await_promise", action="store_true")
    ap.add_argument("--console", type=float, metavar="SECONDS",
                    help="print console messages for this many seconds instead of evaluating")
    ap.add_argument("--file", help="read the expression from this file")
    ap.add_argument("expression", nargs="?")
    args = ap.parse_args()
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            args.expression = f.read()

    ws = websocket.create_connection(page_ws(args.port), timeout=30)
    if args.console:
        ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
        end = time.time() + args.console
        ws.settimeout(1)
        while time.time() < end:
            try:
                msg = json.loads(ws.recv())
            except websocket.WebSocketTimeoutException:
                continue
            if msg.get("method") == "Runtime.consoleAPICalled":
                p = msg["params"]
                print(p["type"], " ".join(str(a.get("value", a.get("description"))) for a in p["args"]))
            elif msg.get("method") == "Runtime.exceptionThrown":
                print("exception", msg["params"]["exceptionDetails"].get("text"))
        ws.close()
        return

    ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {
        "expression": args.expression, "returnByValue": True,
        "awaitPromise": args.await_promise}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == 1:
            break
    ws.close()
    result = msg.get("result", {})
    if "exceptionDetails" in result:
        print("ERROR:", json.dumps(result["exceptionDetails"], indent=2))
    else:
        print(json.dumps(result.get("result", {}).get("value"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
