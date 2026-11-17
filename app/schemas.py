from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    cart_id: str
    promo_code: str | None = Field(default=None, max_length=32)


class PromoInfo(BaseModel):
    """Typed promo descriptor returned by the catalog.

    NOTE: this used to be a plain ``dict``. A recent refactor converted it to
    this typed model — but one caller (the checkout service) was never updated.
    """

    code: str
    discount_rate: float  # e.g. 0.20 = 20% off
    expires_at: str | None = None


class OrderResponse(BaseModel):
    order_id: str
    total_cents: int
    discount_cents: int
    applied_promo: str | None = None
