from engine.tokens import Token, TokenType
from rules.index_encoding import IndexBasedEncodingRule


def test_simple_index_encoding():
    rule = IndexBasedEncodingRule()

    tokens = [
        Token(TokenType.WORD, ["a", "b", "c"])
    ]

    encrypted = rule.encrypt(tokens)
    assert encrypted[0].symbols == ["a", "c", "e"]

    decrypted = rule.decrypt(encrypted)
    assert decrypted[0].symbols == ["a", "b", "c"]


def test_macro_index_encoding():
    rule = IndexBasedEncodingRule()

    tokens = [
        Token(TokenType.WORD, ["{{101}}", "b", "{{111}}"])
    ]

    encrypted = rule.encrypt(tokens)
    assert encrypted[0].symbols == ["{{101}}", "c", "{{113}}"]

    decrypted = rule.decrypt(encrypted)
    assert decrypted[0].symbols == ["{{101}}", "b", "{{111}}"]


def test_index_resets_per_word():
    rule = IndexBasedEncodingRule()

    tokens = [
        Token(TokenType.WORD, ["a", "b"]),
        Token(TokenType.SPACE, [" "]),
        Token(TokenType.WORD, ["a", "b"]),
    ]

    encrypted = rule.encrypt(tokens)

    assert encrypted[0].symbols == ["a", "c"]
    assert encrypted[2].symbols == ["a", "c"]


def test_wraparound_uppercase():
    rule = IndexBasedEncodingRule()

    tokens = [
        Token(TokenType.WORD, ["Y", "Z"])
    ]

    encrypted = rule.encrypt(tokens)
    # Y + 0 = Y, Z + 1 = A
    assert encrypted[0].symbols == ["Y", "A"]

    decrypted = rule.decrypt(encrypted)
    assert decrypted[0].symbols == ["Y", "Z"]
