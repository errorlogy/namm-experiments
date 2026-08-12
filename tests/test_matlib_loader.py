"""Tests for mathematics library base loader."""

from pathlib import Path

import pytest
import yaml

from namm.matlib import load_mathematics_sections
from namm.matlib.loader import default_mathematics_library_path


def test_load_mathematics_sections_returns_sections_list():
    data = load_mathematics_sections()
    assert isinstance(data, dict)
    assert "sections" in data
    assert isinstance(data["sections"], list)
    assert len(data["sections"]) >= 25


def test_each_section_has_required_fields():
    data = load_mathematics_sections()
    required = {"id", "name_ru", "name_en", "subfields", "python_libs", "namm_connected"}
    for section in data["sections"]:
        missing = required - set(section.keys())
        assert not missing, f"Section {section.get('id')} missing {missing}"


def test_default_path_points_to_existing_yaml():
    path = default_mathematics_library_path()
    assert path.is_file()
    assert path.name == "mathematics_library_base.yaml"
    with path.open(encoding="utf-8") as handle:
        parsed = yaml.safe_load(handle)
    assert parsed["schema_version"] == 1
