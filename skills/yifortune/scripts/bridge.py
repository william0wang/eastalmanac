#!/usr/bin/env python3
"""EastAlmanac local loopback bridge (pure Python standard library).

Starts a one-shot HTTP server on 127.0.0.1 (ephemeral port), opens the
EastAlmanac tool page in the user's default browser with a callback URL,
prints the JSON the page posts back to stdout, and exits 0. Works with
any preinstalled Python 3 — no pip dependencies.

Usage:
    python3 scripts/bridge.py cast --question="所问之事"
    python3 scripts/bridge.py chart --date="YYYY-MM-DD" --time="HH:MM" \
        --gender="male|female" --calendar="solar|lunar" --question="关注领域"
    python3 scripts/bridge.py bridge --date="YYYY-MM-DD" --time="HH:MM" \
        --gender="male|female" --lat=39.9042 --lon=116.4074 --tz=8 \
        [--city=beijing] --question="关注领域"

Any action also accepts --lang=en|zh|zh-tw|es|pt|de|ja (default en). The
page opens under the locale's URL prefix (/zh/tools/chart/ etc.), so the
names, essence text, and returned prompt come back in that language — pick
the one matching the user's conversation language.
"""

import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlencode

# The callback payload is UTF-8 JSON; a piped Windows console may default to
# a legacy code page, so pin both streams to UTF-8 when possible.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

TIMEOUT_SECONDS = 300

SITE_ORIGIN = "https://eastalmanac.com"

# Site locales (astro.config i18n); 'en' is the unprefixed default.
LANGS = ("en", "zh", "zh-tw", "es", "pt", "de", "ja")

# Per-action URL query whitelists; every action also carries q + callback.
ACTIONS = {
    # I Ching casting — the user draws/casts interactively on the page.
    "cast": (),
    # BaZi four pillars.
    "chart": ("date", "time", "gender", "calendar"),
    # Western natal chart + BaZi side by side (astrology-bridge tool).
    "bridge": ("date", "time", "gender", "city", "lat", "lon", "tz"),
}

received = threading.Event()
timed_out = threading.Event()


def parse_args(argv):
    """Parse the CLI: an optional leading action, then `--key=value` /
    `--key value` options; any bare positional becomes the question."""
    action = "cast"
    params = {}
    i = 0
    if argv and not argv[0].startswith("--") and argv[0].lower() in ACTIONS:
        action = argv[0].lower()
        i = 1
    while i < len(argv):
        arg = argv[i]
        if arg.startswith("--"):
            key, eq, value = arg[2:].partition("=")
            if eq:
                params[key] = value
            elif i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                params[key] = argv[i + 1]
                i += 1
            else:
                params[key] = "true"
        elif "question" not in params:
            params["question"] = arg
        i += 1
    return action, params


class BridgeHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        # Private Network Access: Chrome/Edge block a public HTTPS page from
        # POSTing to 127.0.0.1 unless the local server grants it explicitly.
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Access-Control-Request-Private-Network",
        )
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length).decode("utf-8", "replace")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

        # Emit the page's structured payload for the agent, then stop serving.
        print(body, flush=True)
        received.set()
        self.server.shutdown()

    def do_GET(self):
        self.send_response(404)
        self._cors()
        self.end_headers()

    def log_message(self, format, *args):
        pass  # keep stdout clean: only the JSON payload is printed


def main():
    action, params = parse_args(sys.argv[1:])
    question = params.get("question") or params.get("q", "")

    server = ThreadingHTTPServer(("127.0.0.1", 0), BridgeHandler)
    server.daemon_threads = True
    callback_url = "http://127.0.0.1:%d/callback" % server.server_address[1]

    query = {k: params[k] for k in ACTIONS[action] if params.get(k)}
    if question:
        query["q"] = question
    query["callback"] = callback_url
    # Locale decides the page language and the language of names/essence/prompt
    # in the returned payload; unknown values fall back to the en default.
    lang = params.get("lang", "").lower()
    if lang not in LANGS:
        lang = "en"
    origin = SITE_ORIGIN if lang == "en" else "%s/%s" % (SITE_ORIGIN, lang)
    # cast/chart live under /tools/; the astrology bridge has its own section.
    path = "astrology-bridge/" if action == "bridge" else "tools/%s/" % action
    target_url = "%s/%s?%s" % (origin, path, urlencode(query))

    print("[EastAlmanac] 正在为您打开网页进行交互: %s" % target_url, file=sys.stderr, flush=True)

    def open_browser():
        if not webbrowser.open(target_url):
            print(
                "[EastAlmanac] 无法自动打开浏览器，请手动访问: %s" % target_url,
                file=sys.stderr,
                flush=True,
            )

    # webbrowser.open() can block until the launcher subprocess returns on some
    # platforms; the main thread needs to keep serving, so open from a helper.
    threading.Thread(target=open_browser, daemon=True).start()

    def on_timeout():
        timed_out.set()
        print(
            "[EastAlmanac] 等待网页操作超时 (5分钟)。如已在网页生成结果，可复制提示词直接粘贴。",
            file=sys.stderr,
            flush=True,
        )
        server.shutdown()

    timer = threading.Timer(TIMEOUT_SECONDS, on_timeout)
    timer.daemon = True
    timer.start()

    try:
        server.serve_forever(poll_interval=0.5)
    finally:
        server.server_close()
        timer.cancel()

    sys.exit(0 if received.is_set() else 1)


if __name__ == "__main__":
    main()
