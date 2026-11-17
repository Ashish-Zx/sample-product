"""In-memory order repository (stand-in for Postgres/SQLAlchemy)."""

from datetime import datetime, timezone

from app.schemas import OrderResponse


class OrderRepository:
    """Very thin, realistic repository that stores completed orders."""

    def __init__(self) -> None:
        self._orders: dict[str, OrderResponse] = {}

    def save(self, order: OrderResponse) -> OrderResponse:
        self._orders[order.order_id] = order
        return order

    def get(self, order_id: str) -> OrderResponse | None:
        return self._orders.get(order_id)

    def count(self) -> int:
        return len(self._orders)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
