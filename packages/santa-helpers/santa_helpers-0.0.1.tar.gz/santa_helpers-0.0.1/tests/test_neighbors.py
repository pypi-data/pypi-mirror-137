import pytest

from santa_helpers.neighbors import neighbors

EXAMPLES_PARSE_GRID_TO_DICT = (
    ((1, 1), 4, None, None, {(0, 1), (1, 0), (2, 1), (1, 2)}),
    ((0, 0), 4, (0, 0), None, {(0, 1), (1, 0)}),
    ((0, 0), 4, (0, 0), (0, 0), set()),
    ((0, 0), 8, None, None, {
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1,  1), (0,  1), (1,  1),
    }),
)


@pytest.mark.parametrize(
    'p,n,p_min,p_max,expected',
    EXAMPLES_PARSE_GRID_TO_DICT
)
def test_parse_grid_to_dict(p, n, p_min, p_max, expected):
    assert set(neighbors(p, n, p_min, p_max)) == expected
