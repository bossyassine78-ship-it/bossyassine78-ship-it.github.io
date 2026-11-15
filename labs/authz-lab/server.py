#!/usr/bin/env python3
"""SHEMKAR Lab: three deliberately broken authorization boundaries.

Synthetic data only. Localhost only. Standard library only.
Run with --mode vulnerable or --mode fixed to compare outcomes.
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

TOKENS = {
    "alice-demo-token": "alice",
    "bob-demo-token": "bob",
    "admin-demo-token": "admin",
}


def initial_state():
    return {
        "users": {
            "alice": {"id": "u1", "name": "Alice", "email": "alice@lab.invalid",
                      "role": "member", "deleted": False},
            "bob": {"id": "u2", "name": "Bob", "email": "bob@lab.invalid",
                    "role": "member", "deleted": False},
            "admin": {"id": "u3", "name": "Admin", "email": "admin@lab.invalid",
                      "role": "admin", "deleted": False},
        },
        "orders": {
            "4001": {"id": "4001", "owner": "alice", "item": "Notebook", "total": 42},
            "4002": {"id": "4002", "owner": "bob", "item": "Keyboard", "total": 60},
        },
        "invitations": [],
    }


def make_server(mode="vulnerable", port=8765):
    if mode not in ("vulnerable", "fixed"):
        raise ValueError("mode must be vulnerable or fixed")
    state = initial_state()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            print("[%s] %s" % (mode, fmt % args))

        def respond(self, status, payload=None):
            raw = b"" if payload is None else json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Lab-Mode", mode)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            if raw:
                self.wfile.write(raw)

        def current_user(self):
            # Deliberately simple, fixed test tokens; not a real login mechanism.
            header = self.headers.get("Authorization", "")
            username = TOKENS.get(header.removeprefix("Bearer "))
            if not username:
                return None
            user = state["users"][username]
            # BUG 1 in vulnerable mode: a deleted principal stays authorized.
            if mode == "fixed" and user["deleted"]:
                return None
            return username, user

        def read_json(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 <= length <= 4096:
                    return None
                return json.loads(self.rfile.read(length) or b"{}")
            except (ValueError, json.JSONDecodeError):
                return None

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/health":
                return self.respond(200, {"lab": "shemkar-authz", "mode": mode})
            principal = self.current_user()
            if principal is None:
                return self.respond(401, {"error": "UNAUTHENTICATED"})
            username, user = principal
            if path == "/api/me":
                return self.respond(200, {"user": user})
            if path.startswith("/api/orders/"):
                order = state["orders"].get(path.rsplit("/", 1)[-1])
                if order is None:
                    return self.respond(404, {"error": "NOT_FOUND"})
                # BUG 2: authentication is checked, ownership is not.
                if mode == "fixed" and order["owner"] != username and user["role"] != "admin":
                    return self.respond(404, {"error": "NOT_FOUND"})
                return self.respond(200, {"order": order})
            return self.respond(404, {"error": "NOT_FOUND"})

        def do_DELETE(self):
            if urlsplit(self.path).path != "/api/me":
                return self.respond(404, {"error": "NOT_FOUND"})
            principal = self.current_user()
            if principal is None:
                return self.respond(401, {"error": "UNAUTHENTICATED"})
            username, user = principal
            user["deleted"] = True
            # Real systems should revoke all credentials here, not just set a flag.
            return self.respond(200, {"deleted": username})

        def do_POST(self):
            if urlsplit(self.path).path != "/api/admin/invitations":
                return self.respond(404, {"error": "NOT_FOUND"})
            principal = self.current_user()
            if principal is None:
                return self.respond(401, {"error": "UNAUTHENTICATED"})
            username, user = principal
            # BUG 3: valid session was mistaken for admin authority.
            if mode == "fixed" and user["role"] != "admin":
                return self.respond(403, {"error": "FORBIDDEN"})
            data = self.read_json()
            if not isinstance(data, dict) or not isinstance(data.get("email"), str) \
                    or not data["email"].endswith("@lab.invalid"):
                return self.respond(400, {"error": "USE_A_LAB_INVALID_EMAIL"})
            invitation = {"email": data["email"], "created_by": username,
                          "role": "admin", "id": len(state["invitations"]) + 1}
            state["invitations"].append(invitation)
            return self.respond(201, {"invitation": invitation})

    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    httpd.lab_state = state
    return httpd


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fictional local-only authorization API lab")
    parser.add_argument("--mode", choices=["vulnerable", "fixed"], default="vulnerable")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    httpd = make_server(args.mode, args.port)
    print(f"Local lab on http://127.0.0.1:{httpd.server_port} [{args.mode}]", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
