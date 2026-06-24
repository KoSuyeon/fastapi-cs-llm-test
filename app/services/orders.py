# '주방' - 주문 데이터를 읽어 오는 서비스(라우터는 이걸 호출만 한다)
import csv
from app.core.config import ORDERS_CSV


def load_orders() -> dict:
    """data/orders.csv 를 {order_id: 주문dict} 로 로드(요청마다 다시 안 읽게 1회)."""
    orders = {}
    with open(ORDERS_CSV, encoding="utf-8-sig", newline="") as f:   # utf-8-sig: BOM 제거
        for row in csv.DictReader(f):
            orders[row["order_id"]] = {
                "order_id": row["order_id"],
                "product_name": row["product_name"],
                "order_amount": int(row["order_amount"]) if row["order_amount"] else 0,
                "order_status": row["order_status"],
                "courier": row["courier"],
            }
    return orders