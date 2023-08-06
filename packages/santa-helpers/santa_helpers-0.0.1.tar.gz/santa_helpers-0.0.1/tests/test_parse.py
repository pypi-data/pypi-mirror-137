import pytest

from santa_helpers.parse import parse_grid_to_dict

EXAMPLES_PARSE_GRID_TO_DICT = (
    ('.', {(0, 0): '.'}),
    ('A', {(0, 0): 'A'}),
    ('.-#', {(0, 0): '.', (1, 0): '-', (2, 0): '#'}),
    ("""
12
34
""", {(0, 0): '1', (1, 0): '2', (0, 1): '3', (1, 1): '4'}),
)


@pytest.mark.parametrize('data,expected', EXAMPLES_PARSE_GRID_TO_DICT)
def test_parse_grid_to_dict(data, expected):
    assert parse_grid_to_dict(data) == expected
