"""Simulated catalog & promo lookups (stand-in for a real downstream service)."""

from app.schemas import PromoInfo

# Base catalog price per cart (cents).
BASE_PRICE_CENTS = 10000  # $100.00

# Promo table keyed by code.
_PROMOS = {
    "SAVE20": PromoInfo(code="SAVE20", discount_rate=0.20),
    "WELCOME10": PromoInfo(code="WELCOME10", discount_rate=0.10),
}


def base_price_cents() -> int:
    return BASE_PRICE_CENTS


def lookup_promo(code: str) -> PromoInfo | None:
    """Return the promo descriptor or None if the code is unknown/expired."""
    promo = _PROMOS.get(code)
    if promo is None:
        return None
    return promo
