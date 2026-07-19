# Модуль 2. Инструменты агента, представление знаний и защитный контур агента

Директория содержит контрольно-измерительные материалы (КИМ) модуля 2, рубрику оценивания и демонстрационные материалы. Модуль охватывает четыре темы и завершается сквозной состязательной практической работой.

## Темы модуля

| № | Тема | Ключевые понятия |
|---|------|------------------|
| 4 | Инструменты агента и механизм их вызова (tool calling) | контракт инструмента, stop-and-parse, идемпотентность, структурированный вывод |
| 5 | Model Context Protocol (MCP) | клиент-сервер, discovery, JSON-RPC, замена сервера |
| 6 | Подсистема памяти агента и технология RAG | виды памяти, entity memory, эмбеддинги + BM25, переранжирование, HyDE |
| 7 | Защитный контур агента | модель угроз, инъекции, PII, эшелонированная защита, human-in-the-loop |

## Контрольно-измерительные материалы

| КИМ | Тип | Аннотация | Файл |
|-----|-----|-----------|------|
| КИМ-2.1 | Практическая работа | Сквозная состязательная лабораторная «Дуэль оценивающих агентов»: студент отвечает на открытый вопрос, разрабатывает ИИ-агента-оценщика, атакует агента соперника и защищает своего | [kim-01-practical-work.md](kim-01-practical-work.md) |
| КИМ-2.2 | Банк открытых вопросов | 40 открытых вопросов по темам 4–7 (по 10 на тему, с уровнями сложности); используется как пул вопросов A/B в КИМ-2.1 | [kim-02-open-questions.md](kim-02-open-questions.md) |

**Рубрика оценивания:** [rubric-01.md](rubric-01.md) — шкала, балльная структура (100 б.), начисление за атаку и защиту, метрика attack success rate, штрафы.

## Демонстрационные материалы

[attachments/examples/](attachments/examples/) — четыре Python-ноутбука со сквозным примером (ассистент интернет-магазина) по одной теме каждый: инструменты и tool calling, MCP, память и RAG, защитный контур. Ноутбуки подробно комментированы и запускаются сверху вниз; зависимости зафиксированы в [attachments/examples/requirements.txt](attachments/examples/requirements.txt). Подробности — в [attachments/examples/README.md](attachments/examples/README.md).

## Источники датасетов

Демонстрационные материалы используют открытые датасеты (подготовка — `attachments/examples/data/prepare_data.py`):

| Датасет | Назначение | Ссылка |
|---------|-----------|--------|
| Online Retail II (UCI) | каталог товаров (`products.csv`) | https://archive.ics.uci.edu/dataset/502/online+retail+ii |
| SQuAD v1.1 (dev) | корпус знаний для RAG (`squad_dev.json`) | https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json |
| deepset/prompt-injections | обучение детектора инъекций (`prompt_injections.parquet`) | https://huggingface.co/datasets/deepset/prompt-injections |

## Дополнительные материалы

Курс **Agents Week** (Yandex) — лекции и семинары по теме модуля:

- Лекция: https://vkvideo.ru/video-84793390_456240034
- Семинар: https://vkvideo.ru/video-84793390_456240035
- Репозиторий курса: https://github.com/mephistophellles/Agents-Week-2026/tree/main

Безопасность AI-агентов (к теме 7 и курсовому проекту):

- LLAMATOR — инструменты тестирования безопасности агентов: https://github.com/LLAMATOR-Core/ai-agents-security
- Awesome AI Agents Security — подборка ресурсов: https://github.com/ProjectRecon/awesome-ai-agents-security
- OWASP AI Agent Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- OWASP GenAI: «Memory is a Feature. It Is Also an Attack Surface»: https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/
- Обзоры и исследования (arXiv): https://arxiv.org/abs/2504.18575 · https://arxiv.org/abs/2606.09935 · https://arxiv.org/abs/2607.05120

## Темы для дальнейшего изучения

Если хотите стать специалистом по безопасности AI-агентов, рекомендуется также самостоятельно изучить:

1. Prompt Injection
2. Indirect Prompt Injection
3. Agent Goal Hijacking
4. Tool Poisoning
5. MCP Security
6. RAG Poisoning
7. Context Poisoning
8. Memory Poisoning
9. Agent Data Injection (ADI)
10. Tool Permission Models
11. Sandboxing AI Agents
12. AI Red Teaming
13. Supply Chain Security for AI Agents
14. AI Agent Benchmarks (WASP, GitInject, AIVP)
