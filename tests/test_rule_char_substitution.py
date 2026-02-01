from engine.tokens import Token, TokenType
from rules.char_substitution import CharacterSubstitutionRule


def test_encrypt_vowels_and_consonants():
    rule = CharacterSubstitutionRule()

    tokens = [
        Token(TokenType.WORD, ["H", "e", "l", "l", "o"])
    ]

    encrypted = rule.encrypt(tokens)

    assert encrypted[0].symbols == [
        "I", "{{101}}", "m", "m", "{{111}}"
    ]


def test_decrypt_vowels_and_consonants():
    rule = CharacterSubstitutionRule()

    tokens = [
        Token(TokenType.WORD, ["I", "{{101}}", "m", "m", "{{111}}"])
    ]

    decrypted = rule.decrypt(tokens)

    assert decrypted[0].symbols == ["H", "e", "l", "l", "o"]


def test_case_last_alpha():
    rule = CharacterSubstitutionRule()

    tokens = [
        Token(TokenType.WORD, ["Z", "z"])
    ]

    encrypted = rule.encrypt(tokens)
    assert encrypted[0].symbols == ["A", "a"]

    decrypted = rule.decrypt(encrypted)
    assert decrypted[0].symbols == ["Z", "z"]
