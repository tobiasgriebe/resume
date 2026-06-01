#!/usr/bin/env python3
"""Render an HTML file to PDF via Chrome CDP — no header/footer."""

import base64, json, os, socket, struct, subprocess, sys, time, urllib.request

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT   = 9223   # separate port so it doesn't clash with any running Chrome


def ws_connect(host, port, path):
    key = base64.b64encode(os.urandom(16)).decode()
    s = socket.create_connection((host, port), timeout=10)
    s.send((
        f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
        f"Upgrade: websocket\r\nConnection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    ).encode())
    buf = b""
    while b"\r\n\r\n" not in buf:
        buf += s.recv(4096)
    assert b"101" in buf, "WebSocket upgrade failed"
    return s


def ws_send(s, text):
    data  = text.encode()
    mask  = os.urandom(4)
    n     = len(data)
    hdr   = bytes([0x81, 0x80 | n]) if n < 126 else bytes([0x81, 0xFE]) + struct.pack(">H", n)
    s.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))


def ws_recv(s, timeout=20):
    s.settimeout(timeout)
    def read(n):
        buf = b""
        while len(buf) < n:
            buf += s.recv(n - len(buf))
        return buf
    hdr  = read(2)
    n    = hdr[1] & 0x7F
    if n == 126: n = struct.unpack(">H", read(2))[0]
    elif n == 127: n = struct.unpack(">Q", read(8))[0]
    data = read(n)
    return json.loads(data) if (hdr[0] & 0x0F) == 1 else {}


def cdp(s, mid, method, params=None):
    ws_send(s, json.dumps({"id": mid, "method": method, "params": params or {}}))


def wait_for(s, pred, timeout=15):
    end = time.time() + timeout
    while time.time() < end:
        try:
            msg = ws_recv(s, timeout=max(0.5, end - time.time()))
            if pred(msg):
                return msg
        except (socket.timeout, OSError):
            break
    return None


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: html_to_pdf.py input.html output.pdf")

    html_path  = os.path.abspath(sys.argv[1])
    output     = os.path.abspath(sys.argv[2])

    proc = subprocess.Popen(
        [CHROME, "--headless", "--disable-gpu", "--no-first-run",
         "--no-sandbox", f"--remote-debugging-port={PORT}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1.5)

        resp    = urllib.request.urlopen(f"http://localhost:{PORT}/json/list", timeout=5)
        targets = json.loads(resp.read())
        pages   = [t for t in targets if t.get("type") == "page"]
        if not pages:
            sys.exit("No page target found")
        ws_url = pages[0]["webSocketDebuggerUrl"]
        path   = ws_url[ws_url.index("/devtools"):]

        s = ws_connect("localhost", PORT, path)

        mid = 0
        def cmd(method, params=None):
            nonlocal mid; mid += 1
            cdp(s, mid, method, params)
            return mid

        cmd("Page.enable")
        wait_for(s, lambda m: m.get("id") == 1)

        cmd("Page.navigate", {"url": f"file://{html_path}"})
        wait_for(s, lambda m: m.get("method") == "Page.loadEventFired", timeout=10)
        time.sleep(0.4)

        pid = cmd("Page.printToPDF", {
            "displayHeaderFooter": False,
            "printBackground":     True,
            "paperWidth":  8.2677,   # A4 in inches
            "paperHeight": 11.6929,
            "marginTop":    0,
            "marginBottom": 0,
            "marginLeft":   0,
            "marginRight":  0,
        })
        result = wait_for(s, lambda m: m.get("id") == pid, timeout=20)

        if not result or "result" not in result:
            sys.exit("CDP printToPDF returned no data")

        pdf = base64.b64decode(result["result"]["data"])
        with open(output, "wb") as f:
            f.write(pdf)
        print(f"{len(pdf)} bytes → {output}")

    finally:
        proc.kill()


if __name__ == "__main__":
    main()
