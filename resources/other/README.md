# Другие ресурсы

Материалы, не относящиеся к остальным разделам: видеокурсы, документация фреймворков, ресурсы по безопасности агентов и по краевым вычислителям.

## Видеоматериалы и курсы

| Название | Аннотация | Связанные КИМ | Доступ | Лицензия / условия | Дата проверки |
|---|---|---|---|---|---|
| Agents Week (Yandex) — лекция и семинар по инструментам и защите | Разбор механизма вызова инструментов, протокола MCP, памяти и RAG, защитного контура агента. | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://vkvideo.ru/video-84793390_456240034 · https://vkvideo.ru/video-84793390_456240035 | свободный доступ | 2026-07-23 |
| Agents Week (Yandex) — лекция и семинар по мультиагентным системам | Архитектуры координации, типы взаимодействия агентов, протоколы. | [M3/kim-01-practical-work-cloud.md](../../M3-multi-agent-systems/kim-01-practical-work-cloud.md) | https://vkvideo.ru/video-84793390_456240036 · https://vkvideo.ru/video-84793390_456240038 | свободный доступ | 2026-07-23 |
| Репозиторий курса Agents Week 2026 | Сопроводительные материалы и ноутбуки курса. | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://github.com/mephistophellles/Agents-Week-2026/tree/main | см. репозиторий | 2026-07-23 |
| A. Karpathy. Intro to Large Language Models | Вводная лекция об устройстве БЯМ: токены, обучение, ограничения. Рекомендуется перед лабораторной работой по исследованию поведения модели. | [M1/kim-lab-02.md](../../M1-Intelligent-agent/kim-lab-02.md) | https://www.youtube.com/watch?v=zjkBMFhNj_g | свободный доступ | 2026-07-23 |
| Microsoft. AI Agents for Beginners | Учебный курс по разработке агентов; рекомендуется для самостоятельного изучения. | [M3/kim-01-practical-work-cloud.md](../../M3-multi-agent-systems/kim-01-practical-work-cloud.md) | https://github.com/microsoft/ai-agents-for-beginners | MIT | 2026-07-23 |

## Документация и методические руководства

| Название | Аннотация | Связанные КИМ | Доступ | Лицензия / условия | Дата проверки |
|---|---|---|---|---|---|
| LangGraph — документация | Официальное руководство по графам исполнения: вершины, рёбра, состояние, checkpointer. Основной каркас курса. | [M1/kim-lab-03.md](../../M1-Intelligent-agent/kim-lab-03.md), [M3/kim-01-practical-work-cloud.md](../../M3-multi-agent-systems/kim-01-practical-work-cloud.md) | https://langchain-ai.github.io/langgraph/ | MIT | 2026-07-23 |
| OpenAI. A Practical Guide to Building AI Agents | Отраслевое руководство по проектированию агентов: когда агент оправдан, как выделять роли и ограничивать полномочия. | [M1/kim-lab-01.md](../../M1-Intelligent-agent/kim-lab-01.md), [M3/kim-01-practical-work-cloud.md](../../M3-multi-agent-systems/kim-01-practical-work-cloud.md) | https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ | свободный доступ | 2026-07-23 |
| L. Weng. LLM Powered Autonomous Agents | Опорная статья по компонентной схеме агента (память, планирование, использование инструментов). Источник рабочего определения агента. | [M1/kim-lab-01.md](../../M1-Intelligent-agent/kim-lab-01.md) | https://lilianweng.github.io/posts/2023-06-23-agent/ | свободный доступ | 2026-07-23 |
| awesome-agent-learning | Подборка материалов и дорожная карта изучения агентных систем. | [M3/kim-01-practical-work-cloud.md](../../M3-multi-agent-systems/kim-01-practical-work-cloud.md) | https://github.com/artnitolog/awesome-agent-learning | см. репозиторий | 2026-07-23 |
| CrewAI · AutoGen | Альтернативные каркасы мультиагентных систем с иными моделями взаимодействия; привлекаются для сравнения с LangGraph. | [M3/kim-01-practical-work-cloud.md](../../M3-multi-agent-systems/kim-01-practical-work-cloud.md) | https://github.com/crewAIInc/crewAI · https://github.com/microsoft/autogen | MIT / CC BY 4.0 | 2026-07-23 |
| Как координировать несколько ИИ-агентов | Обзорная статья о схемах координации. | [M3/kim-01-practical-work-cloud.md](../../M3-multi-agent-systems/kim-01-practical-work-cloud.md) | https://www.developersdigest.tech/blog/how-to-coordinate-multiple-ai-agents | свободный доступ | 2026-07-23 |

## Безопасность агентных систем

| Название | Аннотация | Связанные КИМ | Доступ | Лицензия / условия | Дата проверки |
|---|---|---|---|---|---|
| OWASP AI Agent Security Cheat Sheet | Практический перечень мер защиты агентов: разграничение полномочий, изоляция инструментов, подтверждение критичных действий. | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html | CC BY-SA | 2026-07-23 |
| OWASP GenAI. Memory is a Feature. It Is Also an Attack Surface | Разбор атак на подсистему памяти агента (отравление памяти). | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/ | CC BY-SA | 2026-07-23 |
| LLAMATOR | Инструментарий тестирования безопасности агентных систем. | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://github.com/LLAMATOR-Core/ai-agents-security | см. репозиторий | 2026-07-23 |
| Awesome AI Agents Security | Подборка исследований и инструментов по безопасности агентов. | [M2/kim-01-practical-work.md](../../M2-tools-knowledge-guardrails/kim-01-practical-work.md) | https://github.com/ProjectRecon/awesome-ai-agents-security | см. репозиторий | 2026-07-23 |

## Краевые вычислители

| Название | Аннотация | Связанные КИМ | Доступ | Лицензия / условия | Дата проверки |
|---|---|---|---|---|---|
| CIX Tech — документация разработчика | Материалы по платформе CIX P1 (Orange Pi 6 Plus): инференс на GPU Mali-G720, оценка производительности. | [M3/kim-02-practical-work-edge.md](../../M3-multi-agent-systems/kim-02-practical-work-edge.md) | https://developer.cixtech.com | см. сайт | 2026-07-23 |
| ModelScope — cix/ai_model_hub | Репозиторий готовых моделей и примеров запуска для платформы CIX. | [M3/kim-02-practical-work-edge.md](../../M3-multi-agent-systems/kim-02-practical-work-edge.md) | https://www.modelscope.cn/models/cix/ai_model_hub | см. репозиторий | 2026-07-23 |

## Требования к добавлению

Размещайте здесь только материалы, которые нельзя содержательно отнести к другим разделам.
