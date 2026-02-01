def is_vowel(ch: str) -> bool:
    return ch.lower() in {"a", "e", "i", "o", "u"}


def shift_letter(ch: str) -> str:
    if "a" <= ch <= "z":
        return chr(ord("a") + (ord(ch) - ord("a") + 1) % 26)
    if "A" <= ch <= "Z":
        return chr(ord("A") + (ord(ch) - ord("A") + 1) % 26)
    return ch


def unshift_letter(ch: str) -> str:
    if "a" <= ch <= "z":
        return chr(ord("a") + (ord(ch) - ord("a") - 1) % 26)
    if "A" <= ch <= "Z":
        return chr(ord("A") + (ord(ch) - ord("A") - 1) % 26)
    return ch
