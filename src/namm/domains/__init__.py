"""NAMM domain adapters — see docs/NAMM_DOMAIN_UNIVERSE.md."""

# domain_id → import path (module package under namm.domains)
DOMAIN_REGISTRY: dict[str, str] = {
    "finite_graphs": "namm.domains.graph",
    "program_ast": "namm.domains.program",
    "rewriting": "namm.domains.rewriting",
    "meta_evaluation": "namm.domains.meta",
    "open_problem_shadow": "namm.domains.open_problem",
    "tda_frame": "namm.domains.tda",
    "raw_tensor": "namm.domains.tensor",
    "config_shadow": "namm.domains.config_shadow",
    "quantum": "namm.domains.quantum",
    "category": "namm.domains.category",
}

__all__ = ["DOMAIN_REGISTRY"]
