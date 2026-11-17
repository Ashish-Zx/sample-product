from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_checkout_without_promo():
    r = client.post("/api/checkout", json={"cart_id": "c_1"})
    assert r.status_code == 200
    body = r.json()
    assert body["total_cents"] == 10000
    assert body["discount_cents"] == 0
    assert body["applied_promo"] is None


def test_checkout_with_unknown_promo():
    # Unknown codes are tolerated (no discount).
    r = client.post("/api/checkout", json={"cart_id": "c_1", "promo_code": "NOPE"})
    assert r.status_code == 200
    assert r.json()["discount_cents"] == 0


def test_checkout_with_valid_promo():
    # Currently FAILS: the service reads promo_info["discount_rate"] as a dict,
    # but the catalog returns a typed PromoInfo model -> TypeError.
    r = client.post("/api/checkout", json={"cart_id": "c_1", "promo_code": "SAVE20"})
    assert r.status_code == 200
    body = r.json()
    assert body["applied_promo"] == "SAVE20"
    assert body["discount_cents"] == 2000  # 20% of $100
    assert body["total_cents"] == 8000
