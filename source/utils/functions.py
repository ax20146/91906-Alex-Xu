def rand_range(value: float, range: int) -> int:
    from random import randint

    return randint(round(value) - range, round(value) + range)
