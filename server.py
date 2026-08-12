"""Local dev server for the Northern Edge Joinery site.

Serves site/ as static files and implements POST /api/enquiry with the same
server-side validation contract as the production handler in
netlify/functions/enquiry.js — so what you test locally is what deploys.

    python server.py [port]

Enquiries are appended to enquiries.log rather than emailed; this is a dev
server, not a mail relay.
"""
import json
import re
import socket
import sys
import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

ROOT = "site"
LOG = "enquiries.log"
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")

LIMITS = {"name": 120, "email": 200, "project": 80, "message": 4000}
PROJECTS = {
    "Bespoke joinery",
    "Custom fitted wardrobes",
    "Fitted furniture",
    "Not sure yet",
}


def validate(fields):
    """Return {field: message} for everything wrong with the submission."""
    errors = {}

    for key, limit in LIMITS.items():
        if len(fields.get(key, "")) > limit:
            errors[key] = "Too long."

    if not fields.get("name", "").strip():
        errors["name"] = "Please tell us your name."

    email = fields.get("email", "").strip()
    if not email:
        errors["email"] = "We need an email address to reply to."
    elif not EMAIL_RE.match(email):
        errors["email"] = "That does not look like an email address."

    project = fields.get("project", "")
    if not project:
        errors["project"] = "Please choose the closest project type."
    elif project not in PROJECTS:
        errors["project"] = "Unrecognised project type."

    message = fields.get("message", "").strip()
    if len(message) < 10:
        errors["message"] = "Please tell us a little about the room."

    return errors


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))

    def _json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path.split("?")[0] != "/api/enquiry":
            return self._json(404, {"error": "Not found"})

        length = int(self.headers.get("Content-Length") or 0)
        if length > 64_000:
            return self._json(413, {"error": "Too large"})

        raw = self.rfile.read(length).decode("utf8", "replace")
        fields = {k: v[0] for k, v in parse_qs(raw, keep_blank_values=True).items()}

        # Honeypot: accept and discard, so the bot learns nothing.
        if fields.get("company-website", "").strip():
            return self._json(200, {"ok": True})

        errors = validate(fields)
        if errors:
            return self._json(422, {"ok": False, "errors": errors})

        stamp = datetime.datetime.now().isoformat(timespec="seconds")
        with open(LOG, "a", encoding="utf8") as f:
            f.write(f"--- {stamp}\n")
            for key in ("name", "email", "project", "message"):
                f.write(f"{key}: {fields.get(key, '')}\n")
            f.write("\n")

        print(f"  enquiry logged from {fields.get('email')} -> {LOG}")
        return self._json(200, {"ok": True})

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class DualStackServer(ThreadingHTTPServer):
    """Listen on IPv6 and IPv4.

    'localhost' resolves to ::1 first on Windows. Binding IPv4 only makes every
    request wait for that connection to fail before falling back — about two
    seconds each, which looks like the site is slow when it is not.
    """

    address_family = socket.AF_INET6
    daemon_threads = True

    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4321
    print(f"Northern Edge Joinery — serving {ROOT}/ on http://localhost:{port}")
    print(f"POST /api/enquiry is live; submissions append to {LOG}")
    DualStackServer(("::", port), Handler).serve_forever()
