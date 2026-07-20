"""Объект оценивания для примеров Модуля IV: окружение маркетплейса с изменяемым
состоянием + ReAct-агент с записью полной траектории.

Оценивается ВСЯ траектория (рассуждения, вызовы инструментов, наблюдения, итоговое
состояние среды), а не только финальный текст. Инструменты меняют состояние базы —
это даёт объективные state-проверки и bidirectional-задачи (агент обязан отказаться
от действия, запрещённого политикой).

Конфигурация клиента — из переменных окружения LLM_API_KEY / LLM_BASE_URL / LLM_MODEL.
"""
from __future__ import annotations
import os, json, time, copy
from dataclasses import dataclass, field
from openai import OpenAI

_client = OpenAI(api_key=os.environ.get("LLM_API_KEY", "") or "EMPTY",
                 base_url=os.environ.get("LLM_BASE_URL", "http://localhost:8000/v1"))
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "qwen/qwen3.7-max")

# --- Начальное состояние среды (сбрасывается перед каждым прогоном) -----------
_INITIAL_ORDERS = {
    "ORD-1001": {"sku": "P-100", "qty": 1, "total": 4990, "status": "delivered"},
    "ORD-1002": {"sku": "P-300", "qty": 2, "total": 4980, "status": "shipped"},
    "ORD-1003": {"sku": "P-400", "qty": 1, "total": 6490, "status": "processing"},
}
PRODUCTS = {
    "P-100": {"name": "Wireless Headphones", "price": 4990, "stock": 7},
    "P-300": {"name": "USB-C Hub", "price": 2490, "stock": 15},
    "P-400": {"name": "Mechanical Keyboard", "price": 6490, "stock": 3},
}
# Политики — часть среды; версионируются вместе с данными.
POLICIES = {
    "cancellation": "Отменить заказ можно только пока он не отправлен "
                    "(статусы created/processing). Отправленные и доставленные не отменяются.",
    "change": "Изменить количество в заказе можно только до отправки (статус processing).",
    "return": "Возврат в течение 14 дней после доставки (статус delivered).",
}


@dataclass
class Step:
    """Один атомарный шаг траектории."""
    thought: str = ""
    tool: str = ""
    args: dict = field(default_factory=dict)
    observation: str = ""


@dataclass
class Trajectory:
    """Полная запись прогона задачи: путь + итоговое состояние среды + метрики."""
    task_id: str
    query: str
    steps: list = field(default_factory=list)
    tool_calls: list = field(default_factory=list)   # имена инструментов по порядку
    final_answer: str = ""
    db_before: dict = None
    db_after: dict = None
    llm_calls: int = 0
    tokens: int = 0
    seconds: float = 0.0
    error: str = ""

    def show(self) -> str:
        out = [f"Задача {self.task_id}: {self.query}"]
        for i, s in enumerate(self.steps, 1):
            if s.thought:
                out.append(f"  [{i}] Thought: {s.thought[:90]}")
            if s.tool:
                out.append(f"      Action: {s.tool}({s.args})")
                out.append(f"      Observation: {s.observation[:90]}")
        out.append(f"  Final: {self.final_answer[:120]}")
        return "\n".join(out)


class ShopEnv:
    """Изолированная тестовая среда: изменяемая база заказов + инструменты."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.orders = copy.deepcopy(_INITIAL_ORDERS)

    def snapshot(self) -> dict:
        return copy.deepcopy(self.orders)

    # --- Инструменты (read) ---
    def get_order(self, order_id: str) -> dict:
        o = self.orders.get(order_id)
        return {"order_id": order_id, **o} if o else {"error": "order_not_found", "order_id": order_id}

    def search_products(self, query: str) -> list[dict]:
        return [{"sku": s, **p} for s, p in PRODUCTS.items() if query.lower() in p["name"].lower()]

    def get_policy(self, topic: str) -> dict:
        return {"topic": topic, "text": POLICIES.get(topic, "Политика не найдена.")}

    # --- Инструменты (write). Важно: инструмент ВЫПОЛНЯЕТ действие и НЕ навязывает
    #     политику. Соблюдение политик — ответственность агента; eval проверяет,
    #     соблюдал ли агент политику, по итоговому состоянию среды. ---
    def cancel_order(self, order_id: str) -> dict:
        o = self.orders.get(order_id)
        if not o:
            return {"status": "error", "reason": "order_not_found"}
        o["status"] = "cancelled"
        return {"status": "ok", "order_id": order_id, "new_status": "cancelled"}

    def change_order_qty(self, order_id: str, qty: int) -> dict:
        o = self.orders.get(order_id)
        if not o:
            return {"status": "error", "reason": "order_not_found"}
        if qty < 1:
            return {"status": "rejected", "reason": "qty must be >= 1"}
        o["qty"] = qty
        o["total"] = PRODUCTS[o["sku"]]["price"] * qty
        return {"status": "ok", "order_id": order_id, "new_qty": qty, "new_total": o["total"]}


TOOLS_SPEC = [
    {"type": "function", "function": {"name": "get_order",
        "description": "Информация о заказе по идентификатору.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {"name": "search_products",
        "description": "Поиск товаров по названию (каталог на английском).",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "get_policy",
        "description": "Политика магазина: cancellation, change или return.",
        "parameters": {"type": "object", "properties": {"topic": {"type": "string",
            "enum": ["cancellation", "change", "return"]}}, "required": ["topic"]}}},
    {"type": "function", "function": {"name": "cancel_order",
        "description": "Отменить заказ (меняет состояние; допустимо только по политике).",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {"name": "change_order_qty",
        "description": "Изменить количество товара в заказе (меняет состояние; по политике).",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"},
            "qty": {"type": "integer"}}, "required": ["order_id", "qty"]}}},
]

# Системные промпты двух версий агента — для регрессионного сравнения (пример 5)
SYSTEM_V1 = ("Ты — ассистент поддержки интернет-магазина. Помогай пользователю, "
             "вызывая инструменты. Каталог на английском.")
SYSTEM_V2 = ("Ты — ассистент поддержки интернет-магазина. Работай по циклу "
             "Thought->Action->Observation. Перед любым изменением заказа СНАЧАЛА проверь "
             "применимую политику (get_policy) и текущий статус заказа (get_order); если "
             "действие запрещено политикой — вежливо откажи и объясни причину. Каталог на "
             "английском. Заверши, только когда выполнены все части запроса.")


def run_agent(query: str, task_id: str = "adhoc", model: str = DEFAULT_MODEL,
              system_prompt: str = SYSTEM_V2, max_steps: int = 8, env: ShopEnv | None = None) -> Trajectory:
    """Прогон агента над одной задачей с записью полной траектории. Среда изолируется (reset)."""
    env = env or ShopEnv()
    env.reset()
    traj = Trajectory(task_id=task_id, query=query, db_before=env.snapshot())
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}]
    t0 = time.time()
    try:
        for _ in range(max_steps):
            try:
                resp = _client.chat.completions.create(model=model, messages=messages,
                    tools=TOOLS_SPEC, parallel_tool_calls=False, max_tokens=700)
            except TypeError:
                resp = _client.chat.completions.create(model=model, messages=messages,
                    tools=TOOLS_SPEC, max_tokens=700)
            traj.llm_calls += 1
            if getattr(resp, "usage", None):
                traj.tokens += resp.usage.total_tokens or 0
            msg = resp.choices[0].message
            messages.append(msg.model_dump())
            if not msg.tool_calls:
                traj.final_answer = msg.content or ""
                if msg.content:
                    traj.steps.append(Step(thought=msg.content))
                break
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result = _dispatch(env, tc.function.name, args)
                traj.tool_calls.append(tc.function.name)
                traj.steps.append(Step(thought=(msg.content or ""), tool=tc.function.name,
                                       args=args, observation=json.dumps(result, ensure_ascii=False)))
                messages.append({"role": "tool", "tool_call_id": tc.id,
                                 "content": json.dumps(result, ensure_ascii=False)})
    except Exception as e:                      # graceful handling: ошибка не должна ронять harness
        traj.error = f"{type(e).__name__}: {e}"
    traj.db_after = env.snapshot()
    traj.seconds = round(time.time() - t0, 2)
    return traj


def _dispatch(env: ShopEnv, name: str, args: dict) -> dict:
    fn = getattr(env, name, None)
    if fn is None:
        return {"error": "unknown_tool", "name": name}
    return fn(**args)
