from engine.tokens import Token, TokenType
from rules.substring_rearrangement import SubstringRearrangementRule


def test_no_rearrangement_short_word():
    rule = SubstringRearrangementRule()

    tokens = [
        Token(TokenType.WORD, ["H", "e", "l", "l", "o"])
    ]

    result = rule.encrypt(tokens)
    assert result[0].symbols == ["H", "e", "l", "l", "o"]


def test_rearrangement_even_length():
    rule = SubstringRearrangementRule()

    tokens = [
        Token(TokenType.WORD, ["P", "y", "t", "h", "o", "n"])
    ]

    result = rule.encrypt(tokens)
    assert result[0].symbols == ["h", "o", "n", "P", "y", "t"]


def test_rearrangement_odd_length():
    rule = SubstringRearrangementRule()

    tokens = [
        Token(TokenType.WORD, ["A", "B", "C", "D", "E", "F", "G"])
    ]

    result = rule.encrypt(tokens)
    assert result[0].symbols == ["E", "F", "G", "A", "B", "C", "D"]


def test_macro_as_single_letter():
    rule = SubstringRearrangementRule()

    tokens = [
        Token(TokenType.WORD, ["A", "{{101}}", "B", "C", "D", "E"])
    ]

    result = rule.encrypt(tokens)

    # letters = [A, {{101}}, B, C, D, E]
    # mid = 3 → [A, {{101}}, B] | [C, D, E]
    assert result[0].symbols == ["C", "D", "E", "A", "{{101}}", "B"]


def test_decrypt_is_same_operation():
    rule = SubstringRearrangementRule()

    tokens = [
        Token(TokenType.WORD, ["h", "o", "n", "P", "y", "t"])
    ]

    decrypted = rule.decrypt(tokens)
    assert decrypted[0].symbols == ["P", "y", "t", "h", "o", "n"]
