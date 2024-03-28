# /utils/functions.py


def process_pascal_case(string: str) -> str:
    result: str = string[0]

    for char in string[1:]:
        result += f" {char}" if char.isupper() else char

    return result
