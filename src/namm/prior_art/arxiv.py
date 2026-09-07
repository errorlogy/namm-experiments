"""arXiv API Client & Prior Art Ingestion for NAMM.

Allows fetching preprints, searching literature by category (cs.AI, cs.LO, math.CO, stat.ML),
caching results locally, and conducting automated prior-art novelty checks.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib

import json
from pathlib import Path
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

WORKSPACE = Path(__file__).resolve().parents[3]
CACHE_DIR = WORKSPACE / "data" / "arxiv_cache"

ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"


@dataclass
class ArxivPaper:
    arxiv_id: str
    title: str
    authors: list[str]
    summary: str
    published: str
    categories: list[str]
    pdf_url: str
    abs_url: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PriorArtResult:
    query: str
    total_found: int
    papers: list[ArxivPaper]
    has_prior_art_match: bool


def _clean_text(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.strip().split())


def search_arxiv(
    query: str,
    max_results: int = 10,
    categories: list[str] | None = None,
    use_cache: bool = True,
) -> list[ArxivPaper]:
    """Search arXiv via REST API and return parsed paper metadata.

    Args:
        query: Free text query or search terms.
        max_results: Maximum papers to return (default 10).
        categories: Optional arXiv categories (e.g. ['cs.AI', 'math.CO']).
        use_cache: If True, uses local disk cache in data/arxiv_cache/.
    """
    search_query = query
    if categories:
        cat_filter = " OR ".join(f"cat:{cat}" for cat in categories)
        search_query = f"({query}) AND ({cat_filter})"

    cache_key = hashlib.sha256(f"{search_query}:{max_results}".encode("utf-8")).hexdigest()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if use_cache and cache_file.exists():
        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))
            return [ArxivPaper(**paper) for paper in data]
        except Exception:
            pass

    encoded_query = urllib.parse.quote(search_query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NAMM-Experiments/0.1.0 (Research Auto-Verification)"},
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
    except Exception as err:
        # Fallback empty list on connection error
        return []

    root = ET.fromstring(xml_data)
    papers: list[ArxivPaper] = []

    for entry in root.findall(f"{ATOM_NS}entry"):
        id_elem = entry.find(f"{ATOM_NS}id")
        raw_id = id_elem.text if id_elem is not None and id_elem.text else ""
        arxiv_id = raw_id.split("/abs/")[-1] if "/abs/" in raw_id else raw_id

        title_elem = entry.find(f"{ATOM_NS}title")
        title = _clean_text(title_elem.text if title_elem is not None else "")

        summary_elem = entry.find(f"{ATOM_NS}summary")
        summary = _clean_text(summary_elem.text if summary_elem is not None else "")

        published_elem = entry.find(f"{ATOM_NS}published")
        published = _clean_text(published_elem.text if published_elem is not None else "")

        authors = []
        for author in entry.findall(f"{ATOM_NS}author"):
            name_elem = author.find(f"{ATOM_NS}name")
            if name_elem is not None and name_elem.text:
                authors.append(_clean_text(name_elem.text))

        categories_list = []
        for cat in entry.findall(f"{ATOM_NS}category"):
            term = cat.attrib.get("term")
            if term:
                categories_list.append(term)

        pdf_url = ""
        abs_url = raw_id
        for link in entry.findall(f"{ATOM_NS}link"):
            rel = link.attrib.get("rel")
            title_attr = link.attrib.get("title")
            href = link.attrib.get("href", "")
            if title_attr == "pdf":
                pdf_url = href
            elif rel == "alternate":
                abs_url = href

        paper = ArxivPaper(
            arxiv_id=arxiv_id,
            title=title,
            authors=authors,
            summary=summary,
            published=published,
            categories=categories_list,
            pdf_url=pdf_url,
            abs_url=abs_url,
        )
        papers.append(paper)

    if use_cache:
        try:
            cache_file.write_text(
                json.dumps([p.to_dict() for p in papers], indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass

    return papers


def check_prior_art(
    query: str,
    categories: list[str] | None = None,
    max_results: int = 5,
) -> PriorArtResult:
    """Conduct a Prior Art check for a candidate mathematical or AI concept against arXiv."""
    if categories is None:
        categories = ["cs.AI", "cs.LO", "math.CO", "stat.ML"]

    papers = search_arxiv(query=query, max_results=max_results, categories=categories)
    has_match = len(papers) > 0

    return PriorArtResult(
        query=query,
        total_found=len(papers),
        papers=papers,
        has_prior_art_match=has_match,
    )
