# NAMM LLM providers — API + local

Unified access for chat completions and **typicality embeddings** (AMAT §0, experiment 030 live probes).

## Setup

1. Copy [`.env.example`](../.env.example) → `.env.local` (gitignored), **or** use central research env:
   `NAMM_ENV_FILE=C:\ai_models\mas\research\.env`
2. Fill keys (never commit). Obsidian `api_keys` should **reference** `.env`, not store secrets inline.
3. Optional local backends:
   - **Ollama** — `ollama serve` + models `llama3.2`, `nomic-embed-text`
   - **LM Studio** — OpenAI-compatible server on `:1234`
   - **sentence-transformers** — `pip install -e ".[llm-local]"`

Registry: [`data/llm_registry.yaml`](../data/llm_registry.yaml)

## CLI

```bash
namm llm status          # configured providers + auto selection
namm llm embed "text"    # test embedding
namm llm chat "prompt"   # test chat (--provider groq, --system "...")
namm llm probe           # AMAT live μ vs RPL embedding lift
```

## Auto priority (2026-08)

| Task | Order |
|------|--------|
| **Chat** | groq → openrouter → gemini → openai → deepseek → cerebras → ollama → lmstudio |
| **Embed** | gemini → openai → jina → openrouter → local_st |

Override: `NAMM_CHAT_PROVIDER`, `NAMM_EMBED_PROVIDER`, or flags `--provider`.

## Python API

```python
from namm.llm import chat, embed, get_client
from namm.metrics.live_embeddings import run_phase_lock_live_probe

vec = embed("typicality probe text")
reply = chat("Explain CNS", system="...", provider="groq")
probe = run_phase_lock_live_probe(skip_chat=True, embed_provider="openai")
```

## AMAT note

- Metric `d_med` = distance from **barycenter** \(B_*\) (typicality location), not coordinate median.
- Live probe lift `d_nd - d_mu` on prompt pairs is a **pilot witness**; full 030 loop remains synthetic until multi-turn live trajectories are wired.

## Free-tier candidates to add

| Provider | Env var | Role |
|----------|---------|------|
| Jina | `JINA_API_KEY` | 10M free embedding tokens |
| OpenRouter | `OPENROUTER_API_KEY` | free `:free` chat + embeddings router |
| Gemini | `GEMINI_API_KEY` | free tier (quota varies) |
| Groq | `GROQ_API_KEY` | fast chat, no embeddings |

Related: [`EXTERNAL_TOOLS.md`](EXTERNAL_TOOLS.md) (AI Scientist env vars).
