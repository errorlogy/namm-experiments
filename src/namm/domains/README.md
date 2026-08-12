# NAMM domain adapters

Permanent catalog: [`docs/NAMM_DOMAIN_UNIVERSE.md`](../../../docs/NAMM_DOMAIN_UNIVERSE.md)

Python modules here implement **domain adapters** — `(Σ, Eval, Cert)` for NAMM experiments. Each subdirectory maps to a `domain:` key in experiment `config.yaml`.

Registry: `DOMAIN_REGISTRY` in [`__init__.py`](__init__.py).

Install optional ND libraries (TDA, quantum):

```bash
pip install -e ".[dev,nd]"
```
