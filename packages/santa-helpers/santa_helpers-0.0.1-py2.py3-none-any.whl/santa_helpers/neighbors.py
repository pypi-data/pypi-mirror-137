NEIGHBORS_4 = [
           (0, -1),         # noqa
    (-1, 0),       (1, 0),  # noqa
           (0,  1),         # noqa
]

NEIGHBORS_8 = [
    (-1, -1), (0, -1), (1, -1),  # noqa
    (-1,  0),          (1,  0),  # noqa
    (-1,  1), (0,  1), (1,  1),  # noqa
]

NEIGHBORS_N = {
    4: NEIGHBORS_4,
    8: NEIGHBORS_8,
}


def is_point_in_range(p, p_min=None, p_max=None) -> bool:
    """Check if point lays between two other points.

    Args:
        p: tuple (x, y)
        p_min (optional): min border point
        p_max (optional): max border point

    Returns:
        True if p_max >= p >= p_min
    """
    if p_min is None and p_max is None:
        return True

    x, y = p
    if p_min:
        x_min, y_min = p_min
        if x < x_min or y < y_min:
            return False
    if p_max:
        x_max, y_max = p_max
        if x > x_max or y > y_max:
            return False

    return True


def neighbors(p, n=4, p_min=None, p_max=None):
    """Point neighbor generator.

    Args:
        p: tuple (x, y)
        n: int 4 (no diagonal) or 8 (with diagonal)
        p_min (optional): min grid point, if not given infinite
        p_max (optional): max grid point, if not given infinite

    Yields:
        point (x, y)
    """
    neighbor_points = NEIGHBORS_N[n]
    x, y = p
    for dx, dy in neighbor_points:
        new_p = (x + dx, y + dy)
        if is_point_in_range(new_p, p_min, p_max):
            yield new_p
