# Lab 001: Authorization breaks across identity, objects, and functions

**Original fictional laboratory. No real target, tokens, victims, or proprietary details.**
Standard-library Python 3.9+. Binds to 127.0.0.1 ONLY.

## Attack-surface map

| Boundary | Invariant | Vulnerable implementation | Correct implementation |
| --- | --- | --- | --- |
| Deleted identity | Deleted account must not authorize requests | Checks token existence only | Rechecks user active state |
| Object ownership (BOLA) | Alice cannot read Bob's order | Checks token but not owner | Checks owner/explicit admin |
| Function-level authorization (BFLA) | Normal member cannot create admin invitations | Authenticated implies allowed | Checks admin role |

## Run the local API

Open terminal 1:

```bash
python3 server.py --mode vulnerable
```

Open terminal 2:

### Case A: Deleted account token remains effective

```bash
curl -i -H 'Authorization: Bearer alice-demo-token' http://127.0.0.1:8765/api/me

curl -i -X DELETE -H 'Authorization: Bearer alice-demo-token' http://127.0.0.1:8765/api/me

curl -i -H 'Authorization: Bearer alice-demo-token' http://127.0.0.1:8765/api/me
```

**Expected vulnerable observation:** after deletion, `GET /api/me` still returns HTTP 200 with a JSON user where `deleted: true`. In fixed mode it returns:

```http
HTTP/1.0 401 Unauthorized
Content-Type: application/json

{"error": "UNAUTHENTICATED"}
```

### Case B: Cross-account data access (BOLA)

```http
GET /api/orders/4002 HTTP/1.1
Host: 127.0.0.1:8765
Authorization: Bearer alice-demo-token
```

**Vulnerable response** (Alice reads Bob's order):

```http
HTTP/1.0 200 OK
Content-Type: application/json

{"order": {"id": "4002", "owner": "bob", "item": "Keyboard", "total": 60}}
```

In fixed mode the identical request returns **404** with `{"error":"NOT_FOUND"}`.

### Case C: Admin invitation from unprivileged member (BFLA)

```bash
curl -i -X POST http://127.0.0.1:8765/api/admin/invitations \
  -H 'Authorization: Bearer alice-demo-token' \
  -H 'Content-Type: application/json' \
  --data '{"email":"new-admin@lab.invalid"}'
```

**Vulnerable:** HTTP 201 with an invitation containing `"role":"admin"`. **Fixed:** HTTP 403 `{"error":"FORBIDDEN"}`.

## Compare the fix

Stop terminal 1 (`Ctrl+C`) and restart:

```bash
python3 server.py --mode fixed
```

Replay the identical requests. Observe **401, 404 and 403**, respectively.

## Automated regression

```bash
python3 -m unittest -v test_lab.py
```

The suite spins up its own ephemeral localhost server, tests **both modes** using real HTTP requests, and shuts down automatically. No internet connection needed.

## Root cause and test methodology

The recurring design error is treating a valid-looking identity token as sufficient proof of authorization. Secure checks must bind authorization to **current account state**, **resource ownership**, and **action-specific privileges**, respectively.

The test sequence documents initial state, exact principal, HTTP request, response, persistence and expected vs actual outcome. For the deleted-account test, do **not** claim an externally exploitable ATO: token acquisition by an outside attacker is a separate condition.

This is intentionally simplified educational code, **not** production authentication. A real implementation additionally requires cryptographically verified token signatures, expiry, audience/scope, revocation across instances, race-condition handling, and CSRF protection where relevant.
