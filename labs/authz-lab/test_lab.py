#!/usr/bin/env python3
"""End-to-end HTTP regression tests. Uses only synthetic localhost data."""
import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from server import make_server


class TestAuthzLab(unittest.TestCase):
    def call(self, path, token=None, method="GET", data=None):
        headers = {}
        if token:
            headers["Authorization"] = "Bearer " + token
        if data is not None:
            headers["Content-Type"] = "application/json"
        req = Request(self.base + path, data=json.dumps(data).encode() if data is not None else None,
                      headers=headers, method=method)
        try:
            with urlopen(req, timeout=2) as res:
                return res.status, json.load(res)
        except HTTPError as err:
            return err.code, json.load(err)

    def exercise(self, mode):
        httpd = make_server(mode, 0)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.base = "http://127.0.0.1:%d" % httpd.server_port
        try:
            status, _ = self.call("/api/orders/4002", "alice-demo-token")
            self.assertEqual(status, 200 if mode == "vulnerable" else 404,
                             "BOLA: other customer's order")
            status, _ = self.call("/api/admin/invitations", "alice-demo-token",
                                  "POST", {"email": "new-admin@lab.invalid"})
            self.assertEqual(status, 201 if mode == "vulnerable" else 403,
                             "BFLA: non-admin creates admin invitation")
            status, _ = self.call("/api/me", "alice-demo-token", "DELETE")
            self.assertEqual(status, 200)
            status, _ = self.call("/api/me", "alice-demo-token")
            self.assertEqual(status, 200 if mode == "vulnerable" else 401,
                             "Session invalidation: deleted account's token")
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=3)

    def test_expected_vulnerable_behaviour(self):
        self.exercise("vulnerable")

    def test_fixed_guards(self):
        self.exercise("fixed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
