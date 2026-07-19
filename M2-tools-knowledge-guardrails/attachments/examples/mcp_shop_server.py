"""MCP-сервер магазина «ШопБот» (Тема 5).

Публикует инструменты магазина по протоколу MCP через транспорт stdio.
Запуск вручную:  python mcp_shop_server.py   (ждёт JSON-RPC на stdin).
Обычно запускается клиентом как подпроцесс — см. notebook 02_mcp_protocol.ipynb.
"""
import logging
logging.getLogger().setLevel(logging.WARNING)  # тише лог, чтобы не засорять вывод

import pandas as pd
from mcp.server.fastmcp import FastMCP

CATALOG = pd.read_csv("data/products.csv")
ORDERS = {
    "ORD-1001": {"sku": "85123A", "name": "White Hanging Heart T-Light Holder",
                 "quantity": 2, "status": "shipped"},
}

mcp = FastMCP("shop", log_level="WARNING")


@mcp.tool()
def search_products(query: str, max_price: float | None = None, limit: int = 5) -> list[dict]:
    """Найти товары по ключевому слову в названии (каталог на английском)."""
    df = CATALOG[CATALOG["name"].str.contains(query, case=False, na=False)]
    if max_price is not None:
        df = df[df["price"] <= max_price]
    df = df.sort_values("sold", ascending=False).head(limit)
    return df[["sku", "name", "price"]].to_dict("records")


@mcp.tool()
def get_order(order_id: str) -> dict:
    """Получить статус заказа по его идентификатору."""
    return ORDERS.get(order_id, {"error": "order_not_found", "order_id": order_id})


if __name__ == "__main__":
    mcp.run(transport="stdio")
