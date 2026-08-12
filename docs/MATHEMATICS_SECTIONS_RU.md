# Разделы математики и рамки NAMM — справочник для людей

**Roman Kuznetsov · NAMM research program**

Этот документ отвечает на вопрос: *что здесь — классическая математика, что — инструмент NAMM, а что — метафора или философия?*

**Для агентов и технического каталога** (модули, frame ladder, dispatch) → [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md).

---

## Как читать статусы

| Статус | Значение |
|--------|----------|
| **✅ действует** | Есть код в репозитории **и** эксперименты с результатами |
| **🔧 заготовка** | Stub в коде, экспериментов нет |
| **📋 запланировано** | В roadmap, кода нет |
| **— не подключено** | Классический раздел; NAMM пока не трогает |

---

## Часть A — Классические разделы математики (то, что знает человечество)

Это **университетские / учебниковые** области. NAMM может использовать их как *субстрат* поиска, но не переименовывает их в «свои разделы».

| Раздел | Пример subfields | Есть в NAMM? | Статус | Эксперимент | Библиотека |
|--------|------------------|--------------|--------|-------------|------------|
| **Алгебра** | кольца, поля, многочлены, символьные выражения | частично (слой поддержки) | **✅ действует** (support) | поддерживает 001, 003 | `sympy` |
| **Комбинаторика** | перечисления, формулы над инвариантами | да | **✅ действует** | 001 | `networkx` |
| **Теория графов** | связность, пути, атласы малых графов | да | **✅ действует** | 001, 003, 005, 006, 008 | `networkx` |
| **Топология** | гомотопия, комплексы (дискретные прокси) | да (scaffold) | **✅ действует** | 006 (null-калибровка) | `gudhi` `[nd]` |
| **TDA** | persistent homology, фильтрации | да (scaffold) | **✅ действует** | 006 | `gudhi` `[nd]` |
| **Теория чисел** | делители, конгруэнции, Goldbach-тени | нет (только план) | **📋 запланировано** | — | TBD (`sympy`, `gmpy2`) |
| **Математический анализ** | пределы, интегралы, ряды | нет | **— не подключено** | — | — |
| **Дифференциальная геометрия** | многообразия, кривизна (дискретные тени) | нет (только план) | **📋 запланировано** | — | TBD |
| **Теория категорий** | категории, функторы, морфизмы | stub | **🔧 заготовка** | — | pure Python + `networkx` |
| **Математическая логика / SMT** | доказуемость, SAT/SMT | stub | **🔧 заготовка** | — | `z3-solver`, `python-sat` |
| **Квантовая механика** (физика + мат. формализм) | кубиты, запутанность, операторы плотности | stub | **🔧 заготовка** | — | `qutip` `[nd]` |
| **Геометрия (классическая)** | евклидова, проективная | нет | **— не подключено** | — | — |
| **Теория вероятностей** | распределения, стохастика | нет | **— не подключено** | — | — |
| **Теория групп** | группы, представления | нет | **— не подключено** | — | — |
| **Теория множеств / основания** | аксиomatics, ordinals | нет | **— не подключено** | — | — |
| **Математическая физика** (общая) | поля, струны (кроме QM-stub) | нет | **— не подключено** | — | — |
| **Proof assistants** | Lean, Mathlib | нет (вне репо) | **📋 запланировано** | — | Lean 4 (external) |

> **Важно:** «✅ действует» для топологии/TDA (006) и комбинаторики (001) означает *код + прогон с результатом* — в том числе **честный null**, когда сигнал не найден. Это не «открытие», а калибровка рамки.

---

## Часть B — NAMM-специфичные рамки (НЕ названия разделов университетского курса)

Это **операционные или концептуальные рамки проекта**. Их нельзя искать в оглавлении классического курса матанализа — но у каждой есть понятная роль в NAMM.

| Название | Что это | Метка | Frame | Эксперимент | Классическая база (если есть) |
|----------|---------|-------|-------|-------------|-------------------------------|
| **Теория переписывания (rewriting)** | Инструмент NAMM: поиск confluent TRS на строках `{a,b}` с certificate-first gates | `NAMM frame` | F3b | **002** (null — 0 кандидатов) | universal algebra / term rewriting |
| **Математическая ткань (mathematical fabric)** | Research ontology: bundle B, fibers, fuzzy μ_F_H; гипотезы H-F001…050 | `метафора/PI` | F1→F∞ (cross-cutting) | trail 006→007→009; не отдельный adapter | метафора из видео Anthemium + [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) |
| **Raw tensor layer** | Machine-native frame: 12 «сырых» листьев (spectrum + heat kernel), без именованных человеческих инвариантов | `NAMM frame` | F3g | **007** (первый tested-signal) | **не** «tensor analysis» учебника |
| **Config shadow / AMFW** | Operational moduli: 11D grid → 4D κ-projection; fiber degeneracy как witness | `NAMM frame` | F3h | **009**, **010** (signal + κ-sweep) | метафора compactification (M-theory **metaphor**, не физика) |
| **Trans-level Θ** | Semantic transition algebra: морфизмы между raw structures без named vocabulary | `NAMM frame` | F∞ (planned) | **011** (planned) | — |
| **Open problem shadows** | Метод атаки: конечные тени классических open problems (Kotzig, Graceful Tree) | `метод атаки` | F3e, F3e₂ | **005**, **008** | классические задачи → finite shadow search |
| **Мета-вычисление** | Поиск fixed points E ≈ F(E) на малых графах; «AI thinking topology» | `NAMM frame` | F3d, F∞ partial | **004** | частично recursion theory / fixed-point ideas |
| **Программный синтез (Graph→Int AST)** | Evolutionary search над AST-программами, не «алгоритмы» как раздел математики | `NAMM frame` | F3c | **003** | genetic programming + symbolic check |

### Три метки — что они значат

| Метка | Простыми словами |
|-------|------------------|
| **`NAMM frame`** | Можно запустить эксперимент; есть `domain_id`, модуль в `src/namm/domains/` |
| **`метафора/PI`** | Философская / визуальная рамка; **не evidential**; мотивирует эскалацию рамок |
| **`метод атаки`** | Способ формулировать falsifier для известной open problem, не новый раздел математики |

---

## Часть C — Что уже работает сегодня

**8 операционных вещей**, которые можно запустить **прямо сейчас** (`python -m namm.cli run-experiment --id …`):

| # | Что | domain_id | Эксперимент | Результат (кратко) |
|---|-----|-----------|-------------|-------------------|
| 1 | Формулы над инвариантами графов | `finite_graphs` | NAMM-2026-001 | null-калибровка (Wiener-dominated) |
| 2 | Confluent TRS search | `rewriting` | NAMM-2026-002 | null (0 кандидатов) |
| 3 | Graph→Int AST synthesis | `program_ast` | NAMM-2026-003 | run, ECIP-8be5 |
| 4 | Meta-evaluator fixed points | `meta_evaluation` | NAMM-2026-004 | run, SREFP-414d |
| 5 | Open-problem shadows (Kotzig, Graceful Tree) | `open_problem_shadow` | NAMM-2026-005, 008 | run (T0 calibration) |
| 6 | TDA persistence на geodesic metric | `tda_frame` | NAMM-2026-006 | scaffold, null |
| 7 | Raw tensor / spectral–heat composite | `raw_tensor` | NAMM-2026-007 | **tested-signal** (SHTC-639) |
| 8 | Config shadow / AMFW moduli | `config_shadow` | NAMM-2026-009, 010 | **tested-signal** (AMFW-012e) + κ-sweep |

Установка зависимостей для TDA/quantum stubs:

```bash
pip install -e ".[dev,nd]"
```

---

## Часть D — FAQ

### «Теория переписывания» — это раздел математики в NAMM?

**Для пользователя — нет.** В классическом смысле это *term rewriting* (универсальная алгебра). В NAMM это **инструмент F3b**: bounded search за confluent системами с certificate gates.

- Код: `src/namm/domains/rewriting/`
- Эксперимент 002: **честный null** — ни одна система не прошла gates
- Это **не** заявление «NAMM открыл новую область математики»

### «Математическая ткань» — это раздел математики?

**Нет.** Это **метафора/PI** из видео Anthemium и registry гипотез [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) (H-F001…050).

- Описывает bundle, fibers, fuzzy membership μ_F_H
- **Не** отдельный `domain_id` с adapter
- **Не evidential** — не заменяет Protocol v2 gates и `certificate.json`
- Связана с эскалацией 006→007→009, но сама по себе не «запускается»

### «Сырой тензорный анализ» — это анализ из учебника?

**Нет.** `raw_tensor` (F3g) — **machine-native frame**: numpy/scipy features без именованных человеческих инвариантов. Ближе к «сырым filaments» для search, чем к tensor calculus.

### «Config shadow / AMFW» — это M-theory?

**Метафора + operational frame.** F3h перечисляет 59 049 moduli vacua и смотрит fiber degeneracy при κ-projection. Это **finite shadow** и certificate witness (AMFW-012e), не физическое утверждение о 11D.

### «Open problems» — NAMM решил Graceful Tree?

**Нет.** 005 и 008 — **метод атаки**: finite shadow search + tierlist T0 calibration. Graceful Tree и Kotzig — *калибровочные* targets; beyond-anthropic targets — config_shadow (009/010).

### Где путаница в старом каталоге?

[`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) смешивает в одной таблице:

- классические поля (графы, TDA, категории),
- NAMM-frames (rewriting, raw tensor, config shadow),
- cross-cutting metaphors (mathematical fabric)

→ **этот файл** разводит их по частям A и B. Каталог остаётся для агентов.

### Что читать дальше?

| Вопрос | Документ |
|--------|----------|
| Какой frame / rung? | [`FRAME_LADDER.md`](FRAME_LADDER.md) |
| Философия (не доказательство) | [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) |
| Гипотезы ткани H-F* | [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) |
| AMFW deep dive | [`AMFW_11D_HYPOTHESIS_RESEARCH.md`](AMFW_11D_HYPOTHESIS_RESEARCH.md) |
| Технический каталог доменов | [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) |

---

Roman Kuznetsov · NAMM research program · 2026-08-12
