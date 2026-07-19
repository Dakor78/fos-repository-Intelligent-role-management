"""Общий eval-harness для примеров Модуля IV: параллельный прогон корзины с изоляцией
и программные грейдеры. Используется в примерах 4 и 5 (в примере 3 то же реализовано
пошагово для наглядности).
"""
from __future__ import annotations
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import eval_env as E


def run_suite(tasks, system_prompt, model=E.DEFAULT_MODEL, workers=4):
    """Прогнать агента по корзине: свой ShopEnv на каждую задачу (изоляция) + параллельность."""
    def one(t):
        return t["id"], E.run_agent(t["query"], task_id=t["id"], model=model,
                                    system_prompt=system_prompt, env=E.ShopEnv())
    out = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fut in as_completed([ex.submit(one, t) for t in tasks]):
            tid, traj = fut.result()
            out[tid] = traj
    return out


def grade_state(task, traj) -> bool:
    exp = task.get("expected_state") or {}
    if not exp:                                  # refuse / read-only: изменений быть не должно
        return traj.db_before == traj.db_after
    for oid, fields in exp.items():
        if not isinstance(fields, dict):         # устойчивость к «грязным» сгенерированным задачам
            continue
        after = traj.db_after.get(oid, {})
        if any(after.get(k) != v for k, v in fields.items()):
            return False
    return True


def grade_tools(task, traj) -> bool:
    return set(task.get("expected_tools") or []).issubset(set(traj.tool_calls))


def grade_safety(task, traj) -> bool:
    return traj.error == ""


def success(task, traj) -> bool:
    """Совокупный успех прогона: корректное состояние среды И отсутствие ошибок."""
    return grade_state(task, traj) and grade_safety(task, traj)
