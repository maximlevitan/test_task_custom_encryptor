from typing import List
from engine.tokens import Token, TokenType
from .base import EncryptionRule


class IndexBasedEncodingRule(EncryptionRule):

    # Encrypt algorithm:
    #     - For each word, process symbols left to right.
    #     - Maintain an index counter (letters + digits in macros count as 1 each).
    #     - For letters:
    #         - Add the index to its ASCII code.
    #         - Wrap around alphabet if exceeding 'z' or 'Z'.
    #     - Non-letter symbols are ignored in indexing.
    def encrypt(self, tokens: List[Token]) -> List[Token]:
        return self._process(tokens, encode=True)

    # Decrypt algorithm:
    #     - For each word, process symbols left to right with the same indexing.
    #     - For letters:
    #         - Subtract the index from its ASCII code.
    #         - Wrap around alphabet if below 'a' or 'A'.
    #     - Non-letter symbols are ignored in indexing.
    def decrypt(self, tokens: List[Token]) -> List[Token]:
        return self._process(tokens, encode=False)

    def _process(self, tokens: List[Token], encode: bool) -> List[Token]:
        result: List[Token] = []

        for token in tokens:
            if token.type != TokenType.WORD:
                result.append(token)
                continue

            new_symbols = []
            index = 0

            for sym in token.symbols:
                if not self._is_letter_symbol(sym):
                    new_symbols.append(sym)
                    continue

                delta = index if encode else -index

                # MACRO {{NNN}}
                if isinstance(sym, str) and sym.startswith("{{"):
                    code = int(sym[2:-2])
                    new_code = code + delta
                    new_symbols.append(f"{{{{{new_code}}}}}")
                    index += 1
                    continue

                # LETTER
                if isinstance(sym, str) and sym.isalpha():
                    base = ord(sym)
                    new_code = base + delta

                    if "A" <= sym <= "Z" and new_code > ord("Z"):
                        new_code -= 26
                    elif "a" <= sym <= "z" and new_code > ord("z"):
                        new_code -= 26
                    elif "A" <= sym <= "Z" and new_code < ord("A"):
                        new_code += 26
                    elif "a" <= sym <= "z" and new_code < ord("a"):
                        new_code += 26

                    new_symbols.append(chr(new_code))
                    index += 1
                    continue

                new_symbols.append(sym)

            result.append(Token(TokenType.WORD, new_symbols))

        return result

    @staticmethod
    def _is_letter_symbol(sym) -> bool:
        if isinstance(sym, str):
            if sym.startswith("{{") and sym.endswith("}}"):
                return True
            return sym.isalpha()
        return False
