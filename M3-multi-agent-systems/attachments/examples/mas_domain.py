"""Учебный домен и инструменты для примеров Модуля III (маркетплейс «ШопБот»).

Общий модуль для всех ноутбуков модуля: детерминированные mock-инструменты
и их описания в формате OpenAI (JSON Schema). Один и тот же набор инструментов
используется и одиночным агентом, и мультиагентными системами — это обеспечивает
корректную сравнимость архитектур.
"""
from __future__ import annotations
import json

# --- Мок-«база данных» предметной области -----------------------------------
PRODUCTS = {
    "P-100": {"name": "Wireless Headphones", "price": 4990, "stock": 7},
    "P-200": {"name": "Laptop Stand", "price": 1990, "stock": 0},
    "P-300": {"name": "USB-C Hub", "price": 2490, "stock": 15},
    "P-400": {"name": "Mechanical Keyboard", "price": 6490, "stock": 3},
}
ORDERS = {
    "ORD-1001": {"items": [{"sku": "P-100", "qty": 1}], "total": 4990,
                 "status": "delivered", "date": "2026-07-01"},
    "ORD-1002": {"items": [{"sku": "P-300", "qty": 2}], "total": 4980,
                 "status": "shipped", "date": "2026-07-15"},
}
POLICIES = {
    "refund": "Возврат в течение 14 дней с момента доставки, товар без следов "
              "использования. Комиссия за возврат — 0 ₽.",
    "shipping": "Стандартная доставка 3–5 дней; экспресс 1–2 дня (+300 ₽).",
    "warranty": "Гарантия 12 месяцев на электронику.",
}
SHIPPING = {"ORD-1002": {"carrier": "CDEK", "state": "in_transit", "eta_days": 2}}


# --- Инструменты (типизированный вход/выход, структурированный результат) -----
def search_products(query: str, max_price: float | None = None) -> list[dict]:
    """Поиск товаров по подстроке названия (каталог на английском)."""
    res = []
    for sku, p in PRODUCTS.items():
        if query.lower() in p["name"].lower() and (max_price is None or p["price"] <= max_price):
            res.append({"sku": sku, **p})
    return res


def get_order(order_id: str) -> dict:
    """Информация о заказе по идентификатору."""
    o = ORDERS.get(order_id)
    return {"order_id": order_id, **o} if o else {"error": "order_not_found", "order_id": order_id}


def get_policy(topic: str) -> dict:
    """Текст политики магазина по теме: refund | shipping | warranty."""
    return {"topic": topic, "text": POLICIES.get(topic, "Политика не найдена.")}


def calc_refund(order_id: str) -> dict:
    """Расчёт возможности и суммы возврата по заказу (учитывает статус и политику)."""
    o = ORDERS.get(order_id)
    if not o:
        return {"error": "order_not_found", "order_id": order_id}
    if o["status"] != "delivered":
        return {"refundable": False, "reason": f"статус '{o['status']}' — возврат только после доставки"}
    return {"refundable": True, "amount": o["total"], "reason": "в пределах политики возврата (14 дней)"}


def check_shipping(order_id: str) -> dict:
    """Статус доставки заказа по трек-данным."""
    s = SHIPPING.get(order_id)
    return {"order_id": order_id, **s} if s else {"order_id": order_id, "state": "no_tracking"}


# Реестр «имя инструмента -> функция»
TOOL_FUNCS = {
    "search_products": search_products,
    "get_order": get_order,
    "get_policy": get_policy,
    "calc_refund": calc_refund,
    "check_shipping": check_shipping,
}

# Описания инструментов в формате OpenAI (JSON Schema)
TOOLS_SPEC = [
    {"type": "function", "function": {
        "name": "search_products",
        "description": "Найти товары по ключевому слову в названии (каталог на английском).",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string"}, "max_price": {"type": "number"}}, "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "get_order", "description": "Получить информацию о заказе по идентификатору.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}},
                       "required": ["order_id"]}}},
    {"type": "function", "function": {
        "name": "get_policy",
        "description": "Текст политики магазина: refund, shipping или warranty.",
        "parameters": {"type": "object", "properties": {
            "topic": {"type": "string", "enum": ["refund", "shipping", "warranty"]}},
            "required": ["topic"]}}},
    {"type": "function", "function": {
        "name": "calc_refund", "description": "Рассчитать возможность и сумму возврата по заказу.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}},
                       "required": ["order_id"]}}},
    {"type": "function", "function": {
        "name": "check_shipping", "description": "Статус доставки заказа.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}},
                       "required": ["order_id"]}}},
]


def run_tool(name: str, args: dict) -> dict:
    """Исполнить инструмент по имени с аргументами; вернуть структурированный результат."""
    if name not in TOOL_FUNCS:
        return {"error": "unknown_tool", "name": name}
    return TOOL_FUNCS[name](**args)


def tools_subset(names: list[str]) -> list[dict]:
    """Подмножество схем инструментов (для специалистов с ограниченным набором)."""
    return [t for t in TOOLS_SPEC if t["function"]["name"] in names]
