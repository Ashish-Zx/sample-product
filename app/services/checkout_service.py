"""Checkout business logic.

This is the heart of the "real product". A recent refactor changed the promo
catalog to return a typed ``PromoInfo`` model, but this service still treats it
as a ``dict`` (``promo_info["discount_rate"]``) — so every order with a promo
code crashes with ``TypeError: 'PromoInfo' object is not subscriptable``.
"""

import uuid

from app import catalog
from app.repositories import OrderRepository, now_iso
from app.schemas import OrderResponse


class CheckoutService:
    def __init__(self, order_repo: OrderRepository | None = None) -> None:
        self.order_repo = order_repo or OrderRepository()

    def _lookup_promo(self, code: str):
        """Return the promo descriptor for a code (typed, not a dict)."""
        return catalog.lookup_promo(code)

    def create_order(self, cart_id: str, promo_code: str | None) -> OrderResponse:
        base = catalog.base_price_cents()

        discount_cents = 0
        applied = None

        if promo_code:
            promo_info = self._lookup_promo(promo_code)
            if promo_info is None:
                # Unknown code: treat as no discount (real-world behaviour).
                discount_cents = 0
            else:
                # Working version: PromoInfo is a typed model, read via attribute.
                rate = promo_info.discount_rate
                discount_cents = int(base * rate)
                applied = promo_code

        order_id = str(uuid.uuid4())
        order = OrderResponse(
            order_id=order_id,
            total_cents=base - discount_cents,
            discount_cents=discount_cents,
            applied_promo=applied,
        )
        self.order_repo.save(order)
        return order
