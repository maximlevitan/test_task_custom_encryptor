from typing import List
from engine.tokens import Token, TokenType
from .base import EncryptionRule


class SpecialSymbolInsertionRule(EncryptionRule):

    # Encrypt algorithm:
    #     - For each word:
    #         - Count letters and digits inside macros separately.
    #         - After every third counted symbol, insert a '#' symbol.
    #         - Digits inside macros may receive '#' inside the macro itself.
    #         - Spaces and other special symbols are preserved.
    def encrypt(self, tokens: List[Token]) -> List[Token]:
        return self._process(tokens, encode=True)

    # Decrypt algorithm:
    #     - For each word:
    #         - Remove all '#' symbols.
    #         - Digits inside macros are restored to their original form.
    #         - The original letter positions and macros remain unchanged.
    def decrypt(self, tokens: List[Token]) -> List[Token]:
        return self._process(tokens, encode=False)

    def _process(self, tokens: List[Token], encode: bool) -> List[Token]:
        result: List[Token] = []

        for token in tokens:
            if token.type != TokenType.WORD:
                result.append(token)
                continue

            new_symbols = []
            count = 0

            for sym in token.symbols:
                if isinstance(sym, str) and sym.startswith("{{") and sym.endswith("}}"):
                    digits = sym[2:-2]
                    new_macro = "{{"
                    for d in digits:
                        new_macro += d
                        count += 1
                        if encode and count % 3 == 0:
                            new_macro += "#"
                    new_macro += "}}"
                    new_symbols.append(new_macro)
                elif str(sym).isalpha():
                    new_symbols.append(sym)
                    count += 1
                    if encode and count % 3 == 0:
                        new_symbols.append("#")
                else:
                    new_symbols.append(sym)

            if not encode:
                cleaned = []
                for s in new_symbols:
                    if str(s).startswith("{{") and str(s).endswith("}}"):
                        content = s[2:-2].replace("#", "")
                        cleaned.append(f"{{{{{content}}}}}")
                    elif s == "#":
                        continue
                    else:
                        cleaned.append(s)
                new_symbols = cleaned

            result.append(Token(TokenType.WORD, new_symbols))

        return result
