"""Prior-art checks: algebraic simplify and stub external queries."""

from namm.prior_art.arxiv import ArxivPaper, PriorArtResult, check_prior_art, search_arxiv
from namm.prior_art.simplify import check_simplification, simplifies_to_known_baseline

__all__ = [
    "check_simplification",
    "simplifies_to_known_baseline",
    "search_arxiv",
    "check_prior_art",
    "ArxivPaper",
    "PriorArtResult",
]

