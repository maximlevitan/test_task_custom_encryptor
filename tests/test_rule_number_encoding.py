from engine.tokens import Token, TokenType
from rules.number_encoding import NumberEncodingRule

def test_number_encoding_with_vertical_flip():
    rule = NumberEncodingRule()

    # простой пример
    tokens = [Token(TokenType.NUMBER, [1,2,6])]
    encrypted = rule.encrypt(tokens)
    print("Encrypted:", encrypted[0].symbols)  # ожидаем: [3,9,18] → цифры склеиваются как [3,9,1,8] или [3,9,1,8]

    decrypted = rule.decrypt(encrypted)
    print("Decrypted:", decrypted[0].symbols)
    assert decrypted[0].symbols == [1,2,6]

def test_single_digit_flip():
    rule = NumberEncodingRule()
    tokens = [Token(TokenType.NUMBER, [6])]
    encrypted = rule.encrypt(tokens)
    print("Encrypted:", encrypted[0].symbols)  # 6*3=18 → 1,8 → переворот → 1,8
    decrypted = rule.decrypt(encrypted)
    assert decrypted[0].symbols == [6]

def test_multiple_digits():
    rule = NumberEncodingRule()
    tokens = [Token(TokenType.NUMBER, [9,1,2])]
    encrypted = rule.encrypt(tokens)
    decrypted = rule.decrypt(encrypted)
    assert decrypted[0].symbols == [9,1,2]
