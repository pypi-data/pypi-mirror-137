def parse_grid_to_dict(data: str) -> dict:
    """
    Parse grid given as a string to dictionary.
    k: coordinates (x, y)
    v: value

    Example:
        X.O    =>   { (0, 0): 'X', (1, 0): '.', (2, 0): 'O',
        ...           (0, 1): '.', (1, 1): '.', (2, 1): '.',
        ..O           (0, 2): '.', (1, 2): '.', (2, 2): 'O', }

    """
    return {
        (x, y): v
        for y, row in enumerate(data.strip().split('\n'))
        for x, v in enumerate(row.strip())
    }
