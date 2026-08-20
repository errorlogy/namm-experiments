"""Tests for arXiv Prior Art ingestion and search module."""

from unittest.mock import MagicMock, patch
from namm.prior_art.arxiv import ArxivPaper, check_prior_art, search_arxiv

MOCK_XML_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2401.00001v1</id>
    <title>Neural-Symbolic Invariant Search in Finite Graphs</title>
    <summary>We propose a machine-native search framework for graph invariants.</summary>
    <published>2024-01-01T00:00:00Z</published>
    <author><name>Alice Smith</name></author>
    <author><name>Bob Jones</name></author>
    <category term="cs.AI"/>
    <category term="math.CO"/>
    <link href="http://arxiv.org/abs/2401.00001v1" rel="alternate" type="text/html"/>
    <link href="http://arxiv.org/pdf/2401.00001v1" rel="shortcut icon" title="pdf"/>
  </entry>
</feed>
"""


def test_arxiv_paper_dataclass():
    paper = ArxivPaper(
        arxiv_id="2401.00001v1",
        title="Test Title",
        authors=["Alice Smith"],
        summary="Test Summary",
        published="2024-01-01",
        categories=["cs.AI"],
        pdf_url="http://arxiv.org/pdf/2401.00001v1",
        abs_url="http://arxiv.org/abs/2401.00001v1",
    )
    d = paper.to_dict()
    assert d["arxiv_id"] == "2401.00001v1"
    assert d["title"] == "Test Title"


@patch("urllib.request.urlopen")
def test_search_arxiv_mock(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = MOCK_XML_RESPONSE.encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    papers = search_arxiv("graph invariant", max_results=1, use_cache=False)
    assert len(papers) == 1
    p = papers[0]
    assert p.arxiv_id == "2401.00001v1"
    assert p.title == "Neural-Symbolic Invariant Search in Finite Graphs"
    assert "Alice Smith" in p.authors
    assert "cs.AI" in p.categories


@patch("urllib.request.urlopen")
def test_check_prior_art_mock(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = MOCK_XML_RESPONSE.encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    res = check_prior_art("graph invariant", max_results=1)
    assert res.has_prior_art_match is True
    assert res.total_found == 1
    assert len(res.papers) == 1
