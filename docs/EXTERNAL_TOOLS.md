# External tools (vendored upstream)

NAMM keeps shallow Git clones of upstream research tooling under `external/`. These directories are **gitignored** in this repository; only this document is versioned. Re-clone after a fresh checkout.

## Layout

| Tool | Path | Upstream |
|------|------|----------|
| AI Scientist (v1) | `external/AI-Scientist/` | https://github.com/SakanaAI/AI-Scientist |
| AI Scientist v2 | `external/AI-Scientist-v2/` | https://github.com/SakanaAI/AI-Scientist-v2 |
| OpenEvolve | `external/openevolve/` | https://github.com/algorithmicsuperintelligence/openevolve |

## Shallow clone (retry / fresh machine)

From the NAMM repo root:

```powershell
git clone --depth 1 https://github.com/SakanaAI/AI-Scientist.git external/AI-Scientist
git clone --depth 1 https://github.com/SakanaAI/AI-Scientist-v2.git external/AI-Scientist-v2
git clone --depth 1 https://github.com/algorithmicsuperintelligence/openevolve.git external/openevolve
```

If a clone was interrupted (network abort), remove the partial directory and re-run the matching command.

## OpenEvolve — install notes

- **Python:** 3.10+ (see upstream `pyproject.toml`).
- **Recommended (editable, local venv):**

```powershell
cd external/openevolve
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
# optional dev extras: pip install -e ".[dev]"
```

- **PyPI alternative:** `pip install openevolve` (upstream README).
- **Runtime:** needs an OpenAI-compatible LLM API. Upstream often documents Gemini via the `OPENAI_API_KEY` env var (see `external/openevolve/README.md`).
- **Entrypoint:** `openevolve-run.py` and examples under `external/openevolve/examples/`.

NAMM workspace status (this machine): editable install in `external/openevolve/.venv` (`pip install -e .` succeeded).

## AI Scientist (v1) — install notes (document only)

Do **not** commit API keys. Install in an isolated environment when you are ready to run experiments.

```powershell
cd external/AI-Scientist
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**API keys / env vars** (from upstream README; set in your shell or `.env`, never in git):

| Provider | Environment variable |
|----------|----------------------|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` |
| AWS Bedrock | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION_NAME` |
| Semantic Scholar (optional) | `S2_API_KEY` |

**Entrypoint:** `launch_scientist.py`. Model list: upstream `ai_scientist/llm.py`.

Heavy dependencies include **PyTorch**, **transformers**, and **wandb**; expect a long install and GPU/sandbox planning before running generated code.

## AI Scientist v2 — install notes (document only)

Upstream recommends **Conda** and a **sandbox** (e.g. Docker) because the agent executes LLM-written code.

```powershell
# upstream README uses conda; equivalent venv sketch:
cd external/AI-Scientist-v2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**API keys / env vars:**

| Provider | Environment variable |
|----------|----------------------|
| OpenAI | `OPENAI_API_KEY` |
| Gemini (via OpenAI-compatible API) | `GEMINI_API_KEY` |
| AWS Bedrock | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION_NAME` |
| Semantic Scholar (optional) | `S2_API_KEY` |

**Entrypoint:** `launch_scientist_bfts.py`. Config: `bfts_config.yaml`.

## Pin snapshot (informational)

Recorded when this doc was written; shallow clones track upstream `main` tip:

| Repo | Branch | HEAD (short) |
|------|--------|----------------|
| AI-Scientist | main | `1de1dbc` |
| AI-Scientist-v2 | main | `96bd516` |
| openevolve | main | `411fb59` |

Re-run `git -C external/<name> rev-parse --short HEAD` after `git fetch --depth 1 origin` to refresh.