from typing import List
from engine.tokens import Token, TokenType
from .base import EncryptionRule


FLIP_MAP = {'6': '9', '9': '6'}


class NumberEncodingRule(EncryptionRule):

    # Encrypt algorithm:
    #     - For each number token:
    #         - Multiply each digit by 3 (numbers with multiple digits are treated per digit).
    #         - Apply vertical flip for digits: 6 ↔ 9.
    #         - Keep digits order unchanged.
    def encrypt(self, tokens: List[Token]) -> List[Token]:
        result: List[Token] = []

        for token in tokens:
            if token.type != TokenType.NUMBER or not token.symbols:
                result.append(token)
                continue

            digits = [int(d) for d in token.symbols]
            encrypted_digits = []

            for d in digits:
                n = d * 3
                for ch in str(n):
                    encrypted_digits.append(int(FLIP_MAP.get(ch, ch)))

            result.append(Token(TokenType.NUMBER, encrypted_digits))

        return result

    # Decrypt algorithm:
    #     - For each number token:
    #         - First, apply vertical flip back (6 ↔ 9) to all digits.
    #         - Then divide digits or combined digits by 3 to recover the original number.
    #         - If a digit cannot be divided by 3, combine it with the next digit and divide.
    def decrypt(self, tokens: List[Token]) -> List[Token]:
        result: List[Token] = []

        for token in tokens:
            if token.type != TokenType.NUMBER or not token.symbols:
                result.append(token)
                continue

            digits = token.symbols.copy()

            flipped = [int(FLIP_MAP.get(str(d), str(d))) for d in digits]

            original_digits = []
            i = 0
            while i < len(flipped):
                val = flipped[i]
                if val % 3 == 0:
                    original_digits.append(val // 3)
                    i += 1
                else:
                    if i + 1 < len(flipped):
                        combined = val * 10 + flipped[i + 1]
                        if combined % 3 != 0:
                            break
                        original_digits.append(combined // 3)
                        i += 2
                    else:
                        break
            if len(original_digits) > 0:
                result.append(Token(TokenType.NUMBER, original_digits))

        return result
