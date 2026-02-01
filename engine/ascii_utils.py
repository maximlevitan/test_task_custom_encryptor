# Check if code is a valid ASCII code for supported characters.
def is_letter_ascii(code: int) -> bool:
    return (
        65 <= code <= 90   # A-Z
        or 97 <= code <= 122  # a-z
    )


def is_digit_token(token):
    return isinstance(token, int) or str(token).isdigit()
