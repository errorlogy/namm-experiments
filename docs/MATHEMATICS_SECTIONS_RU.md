# Разделы математики — три слоя (краткий указатель)

**Roman Kuznetsov · NAMM research program**

Этот файл — **краткая навигация**. Полная база класических разделов + Python libs → [`MATHEMATICS_LIBRARY_BASE.md`](MATHEMATICS_LIBRARY_BASE.md) и [`data/mathematics_library_base.yaml`](../data/mathematics_library_base.yaml).

**Для агентов** (domain_id, dispatch, frame ladder) → [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md).

---

## Три слоя — не смешивать

```
┌─────────────────────────────────────────────────────────────┐
│  Слой 1 · КЛАССИЧЕСКАЯ МАТЕМАТИКА + Python libs           │
│  MATHEMATICS_LIBRARY_BASE.md · mathematics_library_base.yaml│
│  (алгебра, топология, графы, QM, … — учебниковые разделы)  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Слой 2 · NAMM ГИПОТЕЗЫ (CONJECTURE, falsifiers)            │
│  MATH_OBJECT_HYPOTHESES.md · MATHEMATICAL_FABRIC_HYPOTHESES │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Слой 3 · МЕТАФОРЫ / PHILOSOPHICAL INFERENCE                │
│  PHILOSOPHICAL_INFERENCE.md · Anthemium video · fabric      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              NAMM_DOMAIN_UNIVERSE.md (технический каталог)
```

| Слой | Что это | Документ |
|------|---------|----------|
| **1** | Классические разделы + PyPI | [`MATHEMATICS_LIBRARY_BASE.md`](MATHEMATICS_LIBRARY_BASE.md) |
| **2** | Falsifiable гипотезы H-*, H-F* | [`MATH_OBJECT_HYPOTHESES.md`](MATH_OBJECT_HYPOTHESES.md), [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) |
| **3** | PI, метафоры, видео | [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md), [`ANTHEMIUM_VIDEO_NOTES.md`](ANTHEMIUM_VIDEO_NOTES.md) |

---

## NAMM-frames — НЕ названия разделов университета

Эти сущности живут в [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md), **не** в Library Base:

| NAMM frame | Метка | Эксперимент |
|------------|-------|-------------|
| Rewriting (F3b) | NAMM frame | 002 |
| Raw tensor (F3g) | NAMM frame | 007 |
| Config shadow / AMFW (F3h) | NAMM frame + метафора | 009, 010 |
| Mathematical fabric | метафора/PI | trail 006→007→009 |
| Open problem shadows | метод атаки | 005, 008 |

Классическая база там, где есть: rewriting → universal algebra; TDA → topology; графы → graph theory.

---

## Что читать дальше?

| Вопрос | Документ |
|--------|----------|
| Таблица всех классических разделов + libs | [`MATHEMATICS_LIBRARY_BASE.md`](MATHEMATICS_LIBRARY_BASE.md) |
| Какой frame / rung? | [`FRAME_LADDER.md`](FRAME_LADDER.md) |
| Философия (не доказательство) | [`PHILOSOPHICAL_INFERENCE.md`](PHILOSOPHICAL_INFERENCE.md) |
| Гипотезы ткани H-F* | [`MATHEMATICAL_FABRIC_HYPOTHESES.md`](MATHEMATICAL_FABRIC_HYPOTHESES.md) |
| Технический каталог доменов | [`NAMM_DOMAIN_UNIVERSE.md`](NAMM_DOMAIN_UNIVERSE.md) |

---

Roman Kuznetsov · NAMM research program · 2026-08-12
