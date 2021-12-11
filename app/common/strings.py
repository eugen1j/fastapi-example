def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False
