from engine.tokens import Token, TokenType
from rules.special_symbol import SpecialSymbolInsertionRule


def test_insert_hash_simple():
    rule = SpecialSymbolInsertionRule()

    tokens = [
        Token(TokenType.WORD, ["a", "b", "c", "d", "e"])
    ]

    encrypted = rule.encrypt(tokens)
    assert encrypted[0].symbols == ["a","b","c","#","d","e"]


def test_insert_hash_with_macro():
    rule = SpecialSymbolInsertionRule()

    tokens = [
        Token(TokenType.WORD, ["a", "{{101}}", "b", "c"])
    ]

    encrypted = rule.encrypt(tokens)
    assert encrypted[0].symbols == ["a","{{10#1}}","b","c","#"]

    decrypted = rule.decrypt(encrypted)
    assert decrypted[0].symbols == ["a","{{101}}","b","c"]


def test_multiple_hashes():
    rule = SpecialSymbolInsertionRule()

    tokens = [
        Token(TokenType.WORD, ["a","b","c","d","e","f","g"])
    ]

    encrypted = rule.encrypt(tokens)
    assert encrypted[0].symbols == ["a","b","c","#","d","e","f","#","g"]

    decrypted = rule.decrypt(encrypted)
    assert decrypted[0].symbols == ["a","b","c","d","e","f","g"]

