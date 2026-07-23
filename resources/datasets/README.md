# Датасеты

Учебные данные, используемые в демонстрационных примерах модулей. Все внешние наборы скачиваются скриптом подготовки и в репозитории хранятся в сокращённом виде.

| Название | Аннотация | Связанные КИМ | Доступ | Лицензия / условия | Дата проверки |
|---|---|---|---|---|---|
| Online Retail II (UCI) | Транзакции интернет-магазина. В курсе используется извлечённый каталог из 500 товаров (`products.csv`) как предметная область сквозного примера «ШопБот». | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://archive.ics.uci.edu/dataset/502/online+retail+ii · локально: [M2/attachments/examples/data/](../../M2-tools-knowledge-guardrails/attachments/examples/data/) | CC BY 4.0 (UCI ML Repository) | 2026-07-23 |
| SQuAD v1.1 (dev) | 2067 абзацев Википедии с вопросами и ответами. Используется как корпус знаний для построения RAG-конвейера (эмбеддинги + BM25 + переранжирование). | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json · локально: `squad_dev.json` | CC BY-SA 4.0 | 2026-07-23 |
| deepset/prompt-injections | 546 размеченных примеров вредоносных и безопасных промптов. Используется для обучения ML-детектора инъекций в защитном контуре. | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://huggingface.co/datasets/deepset/prompt-injections · локально: `prompt_injections.parquet` | MIT | 2026-07-23 |
| Кэш эмбеддингов корпуса RAG | Предрассчитанные векторы абзацев SQuAD (`rag_embeddings.npy`) — ускоряют запуск примера и снимают зависимость от доступности эмбеддинг-модели. | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | локально: [M2/attachments/examples/data/](../../M2-tools-knowledge-guardrails/attachments/examples/data/) | производный артефакт (условия SQuAD) | 2026-07-23 |
| Учебный домен МАС (in-memory) | Синтетический домен поддержки магазина: каталог, заказы, политики и инструменты к ним (`mas_domain.py`). Общий для всех архитектур модуля III, что делает их сравнимыми. Внешняя загрузка не требуется. | [M3/kim-01-practical-work-cloud.md](../../M3-multi-agent-systems/kim-01-practical-work-cloud.md) | локально: [M3/attachments/examples/](../../M3-multi-agent-systems/attachments/examples/) | материалы курса | 2026-07-23 |
| Корзина задач eval (`eval_suite.json`) | Набор тестовых задач для оценки агента: позитивные, негативные, граничные и двунаправленные случаи с ожидаемым итоговым состоянием среды. Создаётся примером 02 модуля IV. | [M4/kim-01-practical-work.md](../../M4-evaluation-and-operations/kim-01-practical-work.md) | локально: [M4/attachments/examples/data/](../../M4-evaluation-and-operations/attachments/examples/data/) | материалы курса | 2026-07-23 |
| τ²-bench: домен `retail` | Данные публичного бенчмарка: политики домена, задачи с эталонным итоговым состоянием БД, база данных и профили пользователя. Подтягиваются частичным клонированием (~33 МБ вместо ~700 МБ). | [M4/kim-01-practical-work.md](../../M4-evaluation-and-operations/kim-01-practical-work.md) | https://github.com/sierra-research/tau2-bench | MIT | 2026-07-23 |

## Подготовка данных

Внешние наборы для модуля II загружаются одной командой:

```bash
cd M2-tools-knowledge-guardrails/attachments/examples/data && python prepare_data.py
```

Скрипт скачивает исходники, извлекает используемые подмножества и сохраняет их в рабочем формате. Суммарный объём данных курса — менее 10 МБ (без кэша эмбеддингов).

## Требования к добавлению

Укажите источник, лицензию, состав признаков, целевую переменную, объем, ограничения, возможные смещения и рекомендуемое разбиение.

Дополнительно для данного курса: если набор используется в примерах, приведите способ его воспроизводимой загрузки (скрипт, а не ручное скачивание) и оценку объёма.
