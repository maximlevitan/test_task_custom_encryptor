from typing import List
from engine.tokens import Token, TokenType
from .base import EncryptionRule


class SubstringRearrangementRule(EncryptionRule):

    # Encrypt algorithm:
    #     - For each word with more than 5 letters:
    #         - Split the word into two halves.
    #             - If odd, the middle letter goes to the first half.
    #         - Swap the two halves.
    #     - Spaces and special characters are preserved at their positions.
    def encrypt(self, tokens: List[Token]) -> List[Token]:
        return self._process(tokens)

    # Decrypt algorithm:
    #     - For each word with more than 5 letters:
    #         - Split into two halves as done during encryption.
    #         - Swap the halves back to restore the original word.
    def decrypt(self, tokens: List[Token]) -> List[Token]:
        return self._process(tokens)

    def _process(self, tokens: List[Token]) -> List[Token]:
        result: List[Token] = []

        for token in tokens:
            if token.type != TokenType.WORD:
                result.append(token)
                continue

            symbols = token.symbols
            letter_positions = []
            letters = []

            for idx, sym in enumerate(symbols):
                if self._is_letter_symbol(sym):
                    letter_positions.append(idx)
                    letters.append(sym)

            length = len(letters)

            if length <= 5:
                result.append(token)
                continue

            mid = (length + 1) // 2
            first = letters[:mid]
            second = letters[mid:]

            rearranged = second + first

            new_symbols = list(symbols)
            for pos, new_sym in zip(letter_positions, rearranged):
                new_symbols[pos] = new_sym

            result.append(Token(TokenType.WORD, new_symbols))

        return result

    @staticmethod
    def _is_letter_symbol(sym) -> bool:
        if isinstance(sym, str):
            if sym.startswith("{{") and sym.endswith("}}"):
                return True
            return sym.isalpha()
        return False
