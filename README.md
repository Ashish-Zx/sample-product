# Sample Product API (SentinelSRE test target)

A tiny but realistically-structured FastAPI checkout service. Use it to demo
SentinelSRE end-to-end: **green → push a bug → red CI → paste error → SRE
fixes it with a draft PR**.

## Endpoints
| Method | Path | Description |
|---|---|---|
| GET | `/health` | liveness |
| POST | `/api/checkout` | create an order (applies promo codes) |
| GET | `/api/orders/{order_id}` | fetch an order |

## The demo sequence

### 1. FIRST WORKING (green)
The repo currently contains the **working** code. Push it and confirm CI is green:
```bash
git init && git add -A && git commit -m "checkout v2: typed promo catalog"
git branch -M main
git remote add origin git@github.com:<you>/sample-product.git
git push -u origin main
```
CI runs `pytest` → **all 4 tests pass** (green check).

### 2. THEN WRONG (introduce the bug)
Apply this one-line regression and push — CI will go **red**:
```diff
# app/services/checkout_service.py (inside the `else:` branch)
-                rate = promo_info.discount_rate
+                rate = promo_info["discount_rate"]   # TypeError: 'PromoInfo' object is not subscriptable
```
```bash
git add -A && git commit -m "checkout: read promo as dict (regression)" && git push
```
Now the **valid-promo test fails** with `TypeError: 'PromoInfo' object is not subscriptable`.

### 3. GIVE SRE THE ERROR
Deploy on Render (free) and reproduce the runtime failure:
```bash
curl -X POST https://<your-app>.onrender.com/api/checkout \
  -H 'Content-Type: application/json' \
  -d '{"cart_id":"c_1","promo_code":"SAVE20"}'
```
→ HTTP 500 with a traceback through `app/services/checkout_service.py:38`.
Copy that log. (Or use the failing CI log — both work.)

### 4. LET SRE FIX IT
In SentinelSRE → **New Incident**:
- Title: `TypeError: 'PromoInfo' object is not subscriptable in POST /api/checkout`
- Repo: select `you/sample-product` (connected GitHub), pick the commit
- Paste the stack trace from step 3
- **Investigate** → watch agents → **Approve** → SRE opens a **draft PR**
  that reverts the line back to `promo_info.discount_rate`.

## Local checks
```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt pytest
.venv/bin/pytest -q        # working = 4 passed; after bug = 1 failed / 3 passed
```
