def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def format_number(value):
    return f"{value:.2f}".rstrip("0").rstrip(".")