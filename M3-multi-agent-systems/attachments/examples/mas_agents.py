"""Эталонные реализации архитектур для бенчмарка (пример 5 Модуля III).

Собирает в одном месте одиночного ReAct-агента, иерархическую МАС и МАС с критиком,
с учётом метрик (число вызовов модели, токены, время). Конфигурация клиента — из
переменных окружения LLM_API_KEY / LLM_BASE_URL / LLM_MODEL.
"""
from __future__ import annotations
import os, json, time
from openai import OpenAI
from pydantic import BaseModel, ValidationError
import mas_domain as dom

_client = OpenAI(api_key=os.environ.get("LLM_API_KEY", "") or "EMPTY",
                 base_url=os.environ.get("LLM_BASE_URL", "http://localhost:8000/v1"))
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "qwen/qwen3.7-max")

SPECIALISTS = {
    "catalog_agent": ["search_products"],
    "orders_agent":  ["get_order", "check_shipping"],
    "policy_agent":  ["get_policy", "calc_refund"],
}


class _Meter:
    """Счётчик вызовов модели и токенов."""
    def __init__(self):
        self.calls = 0
        self.tokens = 0

    def track(self, resp):
        self.calls += 1
        if getattr(resp, "usage", None):
            self.tokens += resp.usage.total_tokens or 0
        return resp


def _complete(meter, model, **kw):
    return meter.track(_client.chat.completions.create(model=model, **kw))


# ---------------- Одиночный ReAct-агент ----------------
def react_agent(query: str, model: str = DEFAULT_MODEL, max_steps: int = 8) -> dict:
    m = _Meter()
    t0 = time.time()
    messages = [
        {"role": "system", "content":
            "Ты — ассистент поддержки магазина. Работай циклом Thought-Action-Observation, "
            "используй инструменты. Каталог на английском. Заверши, только когда покрыты ВСЕ "
            "части запроса."},
        {"role": "user", "content": query}]
    answer = "лимит шагов"
    for _ in range(max_steps):
        resp = _complete(m, model, messages=messages, tools=dom.TOOLS_SPEC, max_tokens=700)
        msg = resp.choices[0].message
        messages.append(msg.model_dump())
        if not msg.tool_calls:
            answer = msg.content
            break
        for tc in msg.tool_calls:
            out = dom.run_tool(tc.function.name, json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "content": json.dumps(out, ensure_ascii=False)})
    return {"arch": "single_react", "answer": answer, "llm_calls": m.calls,
            "tokens": m.tokens, "seconds": round(time.time() - t0, 2)}


# ---------------- Иерархическая МАС ----------------
class _SubTask(BaseModel):
    agent_role: str
    description: str
    priority: int


class _Plan(BaseModel):
    subtasks: list[_SubTask]


def _make_plan(meter, query, model):
    roles = list(SPECIALISTS)
    prompt = (f"Разбей запрос на подзадачи для специалистов {roles}. Верни ТОЛЬКО JSON "
              f'{{"subtasks":[{{"agent_role":"...","description":"...","priority":1}}]}}.\n\n{query}')
    for _ in range(2):
        raw = _complete(meter, model, max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]).choices[0].message.content
        try:
            plan = _Plan.model_validate_json(raw[raw.find("{"): raw.rfind("}") + 1])
            plan.subtasks = [s for s in plan.subtasks if s.agent_role in SPECIALISTS]
            if plan.subtasks:
                return plan
        except (ValidationError, ValueError):
            pass
    return _Plan(subtasks=[_SubTask(agent_role=r, description=query, priority=1) for r in roles])


def _run_specialist(meter, role, subtask, model, max_steps=4):
    tools = dom.tools_subset(SPECIALISTS[role])
    messages = [{"role": "system", "content":
                 f"Ты специалист '{role}'. Реши подзадачу только своими инструментами. "
                 f"Каталог на английском."},
                {"role": "user", "content": subtask}]
    for _ in range(max_steps):
        msg = _complete(meter, model, messages=messages, tools=tools, max_tokens=500).choices[0].message
        messages.append(msg.model_dump())
        if not msg.tool_calls:
            return {"role": role, "status": "success", "result": msg.content}
        for tc in msg.tool_calls:
            out = dom.run_tool(tc.function.name, json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "content": json.dumps(out, ensure_ascii=False)})
    return {"role": role, "status": "partial", "result": "лимит шагов"}


def hierarchical_mas(query, planner_model=DEFAULT_MODEL, specialist_model=DEFAULT_MODEL,
                     coordinator_model=DEFAULT_MODEL, critic_model=None) -> dict:
    """Иерархическая МАС; если critic_model задан — добавляется шаг верификации."""
    m = _Meter()
    t0 = time.time()
    plan = _make_plan(m, query, planner_model)
    results = [_run_specialist(m, s.agent_role, s.description, specialist_model)
               for s in sorted(plan.subtasks, key=lambda x: x.priority)]
    joined = "\n".join(f"[{r['role']}] {r['result']}" for r in results)
    answer = _complete(m, coordinator_model, max_tokens=500,
        messages=[{"role": "system", "content":
                   "Ты координатор. Собери единый ответ, покрывающий ВСЕ части запроса."},
                  {"role": "user", "content": f"Запрос: {query}\n\nРезультаты:\n{joined}"}]
        ).choices[0].message.content
    arch = "hierarchical_mas"
    if critic_model:
        arch = "mas_critic"
        raw = _complete(m, critic_model, max_tokens=300,
            messages=[{"role": "user", "content":
                       f'Оцени полноту ответа. Верни JSON {{"score":0-10,"issues":["..."]}}.\n\n'
                       f"Запрос: {query}\nОтвет: {answer}"}]).choices[0].message.content
        try:
            fb = json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
        except ValueError:
            fb = {"score": 7, "issues": []}
        if fb.get("score", 7) < 7:
            answer = _complete(m, coordinator_model, max_tokens=500,
                messages=[{"role": "system", "content": "Ты координатор. Исправь ответ по замечаниям."},
                          {"role": "user", "content":
                           f"Запрос: {query}\nОтвет: {answer}\nЗамечания: {fb.get('issues')}"}]
                ).choices[0].message.content
    return {"arch": arch, "answer": answer, "llm_calls": m.calls, "tokens": m.tokens,
            "seconds": round(time.time() - t0, 2)}


def quality_score(answer: str, expected_facts: list[str]) -> float:
    """Объективная (fact-based) оценка: доля ожидаемых фактов, найденных в ответе."""
    if not expected_facts:
        return 0.0
    a = (answer or "").lower()
    hit = sum(1 for f in expected_facts if f.lower() in a)
    return round(hit / len(expected_facts), 2)
