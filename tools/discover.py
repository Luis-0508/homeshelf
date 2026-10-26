"""Read-only discovery of Samsung Tizen TVs on the local network.

Sends an SSDP M-SEARCH, then queries the unauthenticated REST endpoint
http://<ip>:8001/api/v2/ for each responder. This never opens the remote
websocket, so the TV shows no "Allow" prompt and nothing on the TV changes.

Usage: python -I tools/discover.py [--timeout 4] [--ip <tv-ip>]
"""
import argparse
import json
import socket
import time
import urllib.request

SSDP_ADDR = ("239.255.255.250", 1900)
SEARCH_TARGETS = [
    "urn:samsung.com:device:RemoteControlReceiver:1",
    "urn:dial-multiscreen-org:service:dial:1",
    "ssdp:all",
]


def ssdp_search(timeout):
    found = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.settimeout(0.5)
    for st in SEARCH_TARGETS:
        msg = (
            "M-SEARCH * HTTP/1.1\r\n"
            f"HOST: {SSDP_ADDR[0]}:{SSDP_ADDR[1]}\r\n"
            'MAN: "ssdp:discover"\r\n'
            "MX: 2\r\n"
            f"ST: {st}\r\n\r\n"
        )
        sock.sendto(msg.encode(), SSDP_ADDR)
    end = time.time() + timeout
    while time.time() < end:
        try:
            data, (ip, _) = sock.recvfrom(4096)
        except socket.timeout:
            continue
        text = data.decode(errors="replace")
        headers = {}
        for line in text.split("\r\n")[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().upper()] = v.strip()
        entry = found.setdefault(ip, {"server": set(), "st": set()})
        if "SERVER" in headers:
            entry["server"].add(headers["SERVER"])
        if "ST" in headers:
            entry["st"].add(headers["ST"])
    sock.close()
    return found


def rest_info(ip):
    try:
        with urllib.request.urlopen(f"http://{ip}:8001/api/v2/", timeout=3) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=float, default=4.0)
    ap.add_argument("--ip", help="skip SSDP and query this IP only")
    args = ap.parse_args()

    if args.ip:
        candidates = {args.ip: {"server": set(), "st": set()}}
    else:
        candidates = ssdp_search(args.timeout)
        print(f"SSDP responders: {len(candidates)}")

    for ip, meta in sorted(candidates.items()):
        samsungish = any("samsung" in s.lower() or "tizen" in s.lower() for s in meta["server"] | meta["st"])
        if not samsungish and not args.ip:
            continue
        info = rest_info(ip)
        print(f"\n== {ip}")
        for s in sorted(meta["server"]):
            print(f"  SSDP server: {s}")
        if not info:
            print("  REST :8001/api/v2/ not reachable")
            continue
        d = info.get("device", {})
        keys = ["name", "modelName", "model", "OS", "firmwareVersion", "PowerState",
                "TokenAuthSupport", "networkType", "developerMode", "developerIP",
                "VoiceSupport", "FrameTVSupport", "GamePadSupport", "resolution"]
        for k in keys:
            if k in d:
                print(f"  {k}: {d[k]}")
        print(f"  api version: {info.get('version')}")


if __name__ == "__main__":
    main()
