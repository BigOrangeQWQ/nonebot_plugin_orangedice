from re import findall


def get_attrs(msg: str) -> dict[str, int]:
    find: list[tuple[str, int]] = findall(r"(\D{2,4})(\d{1,3})", msg)
    attrs: dict[str, int] = {}
    for i in find:
        a, b = i
        attrs[str(a)] = int(b)
    return attrs