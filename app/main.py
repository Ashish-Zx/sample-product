import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.config import settings
from app.schemas import OrderRequest, OrderResponse
from app.services.checkout_service import CheckoutService

app = FastAPI(title="Sample Product API", version="2.0.0")

# One shared service instance (DI stand-in).
service = CheckoutService()

_INDEX = Path(__file__).resolve().parent / "static" / "index.html"


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """Serve the demo storefront UI."""
    return FileResponse(_INDEX)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}


@app.post("/api/checkout", response_model=OrderResponse)
def create_order(payload: OrderRequest) -> OrderResponse:
    """Create an order from a cart, optionally applying a promo code."""
    if not payload.cart_id:
        raise HTTPException(status_code=400, detail="cart_id is required")

    try:
        return service.create_order(payload.cart_id, payload.promo_code)
    except Exception as exc:  # surface real tracebacks to the error log
        raise HTTPException(status_code=500, detail=f"checkout failed: {exc}") from exc


@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str) -> OrderResponse:
    order = service.order_repo.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    return order
