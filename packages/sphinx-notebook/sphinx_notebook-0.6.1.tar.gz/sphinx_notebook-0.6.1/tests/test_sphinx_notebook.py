#!/usr/bin/env python
"""Tests for `media_hoard_cli` package."""
# pylint: disable=redefined-outer-name

from sphinx_notebook import notebook


def test_parse_stem():
    """Test parse note stem."""

    stems = [
        'my_note', '0__my_note', 'checklist__my_note', 'checklist_0__my_note'
    ]

    expected = [None, None, 'checklist', 'checklist']

    results = [notebook._parse_stem(x) for x in stems]  # pylint: disable=protected-access

    assert expected == results
