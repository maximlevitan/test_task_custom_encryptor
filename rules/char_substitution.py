from typing import List
from engine.tokens import Token, TokenType
from .base import EncryptionRule
from .utils import is_vowel, shift_letter, unshift_letter


class CharacterSubstitutionRule(EncryptionRule):

    # Encrypt algorithm:
    #     - For each letter in a word:
    #         - If it is a vowel (a, e, i, o, u or uppercase), replace it with its ASCII code wrapped in a macro {{NNN}}.
    #         - If it is a consonant, shift it to the next letter in the alphabet (z->a, Z->A).
    #     - Non-letter symbols (punctuation, spaces) are left unchanged.
    def encrypt(self, tokens: List[Token]) -> List[Token]:
        result: List[Token] = []

        for token in tokens:
            if token.type != TokenType.WORD:
                result.append(token)
                continue

            new_symbols = []
            for sym in token.symbols:
                if isinstance(sym, str) and sym.startswith("{{"):
                    new_symbols.append(sym)
                    continue

                if isinstance(sym, str) and sym.isalpha():
                    if is_vowel(sym):
                        new_symbols.append(f"{{{{{ord(sym)}}}}}")
                    else:
                        new_symbols.append(shift_letter(sym))
                else:
                    new_symbols.append(sym)

            result.append(Token(TokenType.WORD, new_symbols))

        return result

    # Decrypt algorithm:
    #     - For each symbol in a word:
    #         - If it is a macro {{NNN}}, convert it back to the corresponding vowel character.
    #         - If it is a consonant, shift it back to the previous letter in the alphabet (a->z, A->Z).
    #     - Non-letter symbols are left unchanged.
    def decrypt(self, tokens: List[Token]) -> List[Token]:
        result: List[Token] = []

        for token in tokens:
            if token.type != TokenType.WORD:
                result.append(token)
                continue

            new_symbols = []
            for sym in token.symbols:
                if isinstance(sym, str) and sym.startswith("{{"):
                    code = int(sym[2:-2])
                    new_symbols.append(chr(code))
                    continue

                if isinstance(sym, str) and sym.isalpha():
                    new_symbols.append(unshift_letter(sym))
                else:
                    new_symbols.append(sym)

            result.append(Token(TokenType.WORD, new_symbols))

        return result
