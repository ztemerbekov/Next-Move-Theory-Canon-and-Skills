# Next Move Theory Canon & Skills

**Read this in:** [English](#english) · [Русский](#русский)

## English

Next Move Theory Canon & Skills is a user-global Plugin for Codex and Claude Code that helps founders and product managers decide what to build, for whom, and what to test before spending months on the wrong build. It combines an open canon with skills that start from a product conversation and route from market research to a value proposition, a build-ready product requirements document, and go-to-market work; every decision is anchored in the customer’s desired task (Job), concrete success criteria, target segment, and riskiest assumption.

### At a glance

- **For product builders.** Founders, indie hackers, product managers, senior product leaders, and product marketers.
- **Start with `nmt-chat`.** It is the conversational entry point and router: paste an idea, notes, research, or a live product situation; it separates evidence from assumptions and points to the next concrete move.
- **Use the customer’s real task.** A Job is the transition a person wants to make from a current situation to an expected outcome. A segment is a group of people with similar Jobs and similar success criteria.
- **Make value concrete.** Value means helping a segment reach its outcome with better results and less total cost—money, time, effort, mental effort, negative emotion, or rework—against its success criteria.
- **Test the dangerous assumption first.** The riskiest assumption (RAT) is the assumption most likely to sink the initiative; test it cheaply before building.
- **License and author.** The canon and skills are by Ivan Zamesin and licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### A tiny example

Suppose a founder says: “I want to build an AI planner for freelancers.” The useful starting point is not the feature. It is the decision underneath it:

> **Job:** “I want to turn a messy client request into a clear next step by tomorrow.”
>
> **Segment:** Freelancers who perform that same main task and judge success by speed and reduced uncertainty.
>
> **Value hypothesis:** Help them reach that outcome with less time and mental effort than their current option.
>
> **Riskiest assumption:** This segment will pay at the planned price. Test it with people who have already paid for similar help and a small demand test before building.

The sequence is deliberate: name the desired transition, choose the people with similar Jobs and criteria, define the value to deliver, then test the assumption most likely to kill the idea.

### Getting started

Install the suite globally:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills -g
```

Then:

1. Start with [`nmt-chat`](skills/nmt-chat/), the conversational entry point and router.
2. Paste whatever you have: a half-formed idea, messy notes, interview material, a product brief, or a live product problem.
3. Ask for the next move. The conversation can stay focused on a decision, or route to the producer skill that creates the artifact you need.

### The path from idea to build or launch

For a new idea, follow the producer path in this order:

```text
nmt-market-research
        ↓
nmt-craft-value-proposition
       ↙ ↘
nmt-product-requirements   nmt-craft-go-to-market
```

1. **`nmt-market-research`** — research the market, map and score segments, identify their Jobs, and decide whether to proceed, narrow, or pivot.
2. **`nmt-craft-value-proposition`** — turn a chosen segment and its Jobs into a concrete value proposition and implementation direction.
3. **`nmt-product-requirements`** — turn the chosen segment and value into a build-ready product requirements document: what to build and which edge cases matter.
4. **`nmt-craft-go-to-market`** — turn the value proposition into landing-page copy, ads, and a go-to-market communication plan: how to sell it.

The last two paths can run in either order, or both can be used. If you already have a live product, start with [`nmt-diagnose`](skills/nmt-diagnose/). If you have interviews, sales calls, support calls, or open-ended survey answers, use [`nmt-analyze-interviews`](skills/nmt-analyze-interviews/) to extract Jobs, success criteria, and value hypotheses.

### Skill map

| Skill | Use it for |
| --- | --- |
| [`nmt-chat`](skills/nmt-chat/) | Advice, explanation, pressure-testing, and routing to the next skill. |
| [`nmt-diagnose`](skills/nmt-diagnose/) | Finding where a live product or metric is breaking before prescribing a fix. |
| [`nmt-analyze-interviews`](skills/nmt-analyze-interviews/) | Turning interviews, notes, sales or support calls, and survey open-ends into Jobs, criteria, and value hypotheses. |
| [`nmt-market-research`](skills/nmt-market-research/) | Researching the market and choosing which segment and Jobs to compete for first. |
| [`nmt-craft-value-proposition`](skills/nmt-craft-value-proposition/) | Defining how the chosen segment will receive value and why it should choose this option. |
| [`nmt-product-requirements`](skills/nmt-product-requirements/) | Creating the build-ready product requirements document. |
| [`nmt-craft-go-to-market`](skills/nmt-craft-go-to-market/) | Creating landing-page copy, ads, and a go-to-market communication plan. |

### The decision model

The methodology follows one causal chain:

```text
Market with money
  → Segment + Job
  → Added Value
  → Unit economics + demand + ability to scale
  → Conversion + retention + repeat
  → Profit
```

The order matters. A market is defined by what people already spend to perform Jobs, not only by a category name. A segment is chosen by similarity of Jobs and success criteria, with economics and reachable demand attached. Value is the customer’s outcome over the costs of reaching it; a feature is only the delivery format. Aha Moments signal that the delivered result beat the customer’s prediction, while a Problem signals under-delivery. When a downstream metric breaks, investigate the upstream segment, Job, and value before optimizing the funnel.

Next Move Theory combines Advanced Jobs To Be Done (AJTBD), Unit Economics, the Riskiest Assumption Test (RAT), ABCDX Segmentation, and Theory of Constraints into one system for product decisions. Objectives and Key Results (OKR) are a supporting goal-setting methodology in the canon.

### Read the canon

For a short route through the public foundation, read:

1. [`nmt-key-theses.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Next-Move-Theory/nmt-key-theses.md) — how Jobs, value, economics, demand, and validation fit into one chain.
2. [`ajtbd-key-theses.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md) — Jobs, Job Graphs, segments, success criteria, value, and behavior change.
3. [`communication.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/communication.md) — how to communicate value in the language of Jobs and criteria.

The canon is also available in a more readable form at [nextmovetheory.com/library/canon](https://nextmovetheory.com/library/canon?utm_source=canon&utm_medium=github). The broader methodology, books, and related materials are at [nextmovetheory.com](http://nextmovetheory.com/?utm_source=canon&utm_medium=github).

### The book

[*The Nature of Product*](https://nextmovetheory.com/library/the-nature-of-product?utm_source=canon&utm_medium=github) is free to read on the site. It introduces the Advanced Jobs To Be Done foundation for founders, indie hackers, product managers, marketers, and designers who make product decisions with incomplete evidence.

### License and attribution

The canon and skills are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md) for the license, attribution, and repository-specific notices. When sharing or adapting the material, credit Ivan Zamesin, link back to this repository and the license, and keep the same license for adaptations.

Methodology and text by **Ivan Zamesin** — [nextmovetheory.com](http://nextmovetheory.com/?utm_source=canon&utm_medium=github) · [X](https://x.com/zamesin) · [LinkedIn](https://www.linkedin.com/in/ivan-zamesin/).

---

## Русский

Next Move Theory Canon & Skills — это устанавливаемый для пользователя Plugin для Codex и Claude Code, который помогает основателям и продакт-менеджерам решить, что создавать, для кого и что проверить, прежде чем потратить месяцы на неверную разработку. В него входят открытый канон и навыки, которые начинают с разговора о продукте и проводят вас от исследования рынка к ценностному предложению, готовому документу требований к продукту и выходу на рынок; каждое решение опирается на задачу клиента (Job), конкретные критерии успеха, целевой сегмент и самое рискованное предположение.

### Коротко

- **Для тех, кто создаёт продукты.** Основатели, инди-хакеры, продакт-менеджеры, руководители продуктовых команд и продуктовые маркетологи.
- **Начните с `nmt-chat`.** Это разговорная точка входа и маршрутизатор: вставьте идею, заметки, исследование или описание действующего продукта — навык отделит факты от предположений и подскажет следующий конкретный шаг.
- **Начинайте с реальной задачи клиента.** Job — это переход, который человек хочет совершить: из текущей ситуации в ожидаемый результат. Сегмент — это группа людей с похожими задачами и похожими критериями успеха.
- **Описывайте ценность конкретно.** Ценность — помочь сегменту получить нужный результат лучше и с меньшими совокупными затратами: денег, времени, усилий, умственной нагрузки, отрицательных эмоций или переделок — с учётом его критериев успеха.
- **Сначала проверяйте опасное предположение.** Самое рискованное предположение (RAT) — то, которое с наибольшей вероятностью погубит инициативу; его нужно дёшево проверить до разработки.
- **Лицензия и автор.** Канон и навыки созданы Иваном Замесиным и распространяются по лицензии [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### Маленький пример

Представим, что основатель говорит: «Я хочу сделать AI-планировщик для фрилансеров». Полезная отправная точка — не функция, а решение, которое за ней стоит:

> **Задача:** «Я хочу превратить хаотичный запрос клиента в понятный следующий шаг к завтрашнему дню».
>
> **Сегмент:** Фрилансеры, которые выполняют ту же основную задачу и оценивают успех по скорости и снижению неопределённости.
>
> **Гипотеза ценности:** Помочь им получить этот результат с меньшими затратами времени и умственных усилий, чем с помощью текущего варианта.
>
> **Самое рискованное предположение:** Этот сегмент будет платить запланированную цену. До разработки проверьте это на людях, которые уже платили за похожую помощь, и небольшим тестом спроса.

Последовательность намеренная: назвать желаемый переход, выбрать людей с похожими задачами и критериями, определить создаваемую ценность и проверить предположение, которое с наибольшей вероятностью погубит идею.

### Как начать

Установите набор глобально:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills -g
```

Затем:

1. Начните с [`nmt-chat`](skills/nmt-chat/) — разговорной точки входа и маршрутизатора.
2. Вставьте всё, что у вас есть: сырую идею, беспорядочные заметки, материалы интервью, описание продукта или проблему действующего продукта.
3. Спросите о следующем шаге. Разговор может остаться сфокусированным на решении, а может направить вас к навыку, который подготовит нужный результат.

### Путь от идеи к разработке или запуску

Для новой идеи используйте такой путь:

```text
nmt-market-research
        ↓
nmt-craft-value-proposition
       ↙ ↘
nmt-product-requirements   nmt-craft-go-to-market
```

1. **`nmt-market-research`** — исследовать рынок, составить и оценить карту сегментов, определить их задачи и решить, двигаться дальше, сузить фокус или изменить направление.
2. **`nmt-craft-value-proposition`** — превратить выбранный сегмент и его задачи в конкретное ценностное предложение и направление реализации.
3. **`nmt-product-requirements`** — превратить выбранный сегмент и ценность в готовый документ требований к продукту: что создавать и какие крайние случаи учесть.
4. **`nmt-craft-go-to-market`** — превратить ценностное предложение в текст лендинга, рекламу и план коммуникации для выхода на рынок: как продавать.

Последние два направления можно использовать в любом порядке или оба сразу. Если продукт уже работает, начните с [`nmt-diagnose`](skills/nmt-diagnose/). Если у вас есть интервью, звонки продаж или поддержки либо открытые ответы опросов, используйте [`nmt-analyze-interviews`](skills/nmt-analyze-interviews/), чтобы извлечь задачи, критерии успеха и гипотезы ценности.

### Карта навыков

| Навык | Для чего он нужен |
| --- | --- |
| [`nmt-chat`](skills/nmt-chat/) | Советы, объяснения, проверка гипотез и переход к следующему навыку. |
| [`nmt-diagnose`](skills/nmt-diagnose/) | Найти, где ломается действующий продукт или метрика, прежде чем назначать исправление. |
| [`nmt-analyze-interviews`](skills/nmt-analyze-interviews/) | Превратить интервью, заметки, звонки продаж или поддержки и открытые ответы опросов в задачи, критерии и гипотезы ценности. |
| [`nmt-market-research`](skills/nmt-market-research/) | Исследовать рынок и выбрать, за какой сегмент и какие задачи конкурировать в первую очередь. |
| [`nmt-craft-value-proposition`](skills/nmt-craft-value-proposition/) | Определить, какую ценность получит выбранный сегмент и почему ему стоит выбрать этот вариант. |
| [`nmt-product-requirements`](skills/nmt-product-requirements/) | Создать готовый документ требований к продукту. |
| [`nmt-craft-go-to-market`](skills/nmt-craft-go-to-market/) | Создать текст лендинга, рекламу и план коммуникации для выхода на рынок. |

### Модель принятия решений

Методология следует одной причинно-следственной цепочке:

```text
Рынок с деньгами
  → Сегмент + задача
  → Созданная ценность
  → Юнит-экономика + спрос + возможность масштабирования
  → Конверсия + удержание + повторные покупки
  → Прибыль
```

Порядок важен. Рынок определяется тем, на что люди уже тратят деньги, выполняя задачи, а не только названием категории. Сегмент выбирают по сходству задач и критериев успеха, добавляя экономику и достижимость спроса. Ценность — это результат клиента по отношению к затратам на его получение; функция — лишь способ эту ценность доставить. Момент Aha (Aha Moment) показывает, что полученный результат превзошёл ожидания клиента, а проблема (Problem) — что результат оказался хуже ожидаемого. Если ломается метрика внизу цепочки, сначала проверяйте сегмент, задачу и ценность выше по цепочке, а уже потом оптимизируйте воронку.

Next Move Theory объединяет Advanced Jobs To Be Done (AJTBD), юнит-экономику, тест самого рискованного предположения (RAT), сегментацию ABCDX и теорию ограничений в единую систему принятия продуктовых решений. Objectives and Key Results (OKR) в каноне выступает поддерживающей методологией постановки целей.

### Как читать канон

Для короткого маршрута по открытой основе прочитайте:

1. [`nmt-key-theses.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Next-Move-Theory/nmt-key-theses.md) — как задачи, ценность, экономика, спрос и проверка соединяются в одну цепочку.
2. [`ajtbd-key-theses.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md) — задачи, граф задач, сегменты, критерии успеха, ценность и изменение поведения.
3. [`communication.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/communication.md) — как говорить о ценности на языке задач и критериев.

Канон также доступен в более удобном для чтения виде на странице [nextmovetheory.com/library/canon](https://nextmovetheory.com/library/canon?utm_source=canon&utm_medium=github). Более широкая методология, книги и связанные материалы находятся на [nextmovetheory.com](http://nextmovetheory.com/?utm_source=canon&utm_medium=github).

### Книга

Книгу [*The Nature of Product*](https://nextmovetheory.com/library/the-nature-of-product?utm_source=canon&utm_medium=github) можно бесплатно прочитать на сайте. Она знакомит с основой Advanced Jobs To Be Done и предназначена для основателей, инди-хакеров, продакт-менеджеров, маркетологов и дизайнеров, которые принимают продуктовые решения при неполных данных.

### Лицензия и атрибуция

Канон и навыки распространяются по лицензии [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Лицензия, атрибуция и специальные уведомления о репозитории указаны в [`LICENSE`](LICENSE) и [`NOTICE.md`](NOTICE.md). При распространении или адаптации материала указывайте Ивана Замесина как автора, ссылайтесь на этот репозиторий и лицензию и сохраняйте ту же лицензию для адаптаций.

Методология и текст — **Иван Замесин**: [nextmovetheory.com](http://nextmovetheory.com/?utm_source=canon&utm_medium=github) · [X](https://x.com/zamesin) · [LinkedIn](https://www.linkedin.com/in/ivan-zamesin/).
