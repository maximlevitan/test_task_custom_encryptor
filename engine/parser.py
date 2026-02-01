from typing import List
from engine.tokens import Token, TokenType, Symbol
from engine.ascii_utils import is_letter_ascii, is_digit_token


class Parser:

    # Parsing for encryption:
    #         - Split input into WORD / NUMBER / SPACE / SYMBOL tokens
    #         - No macro restoration needed
    def parse_for_encrypt(self, text: str) -> List[Token]:
        return self._primary_parse(text)

    # Parsing for decryption:
    #         - First perform primary parsing
    #         - Then restore ASCII macros {{NNN}} inside WORD tokens
    def parse_for_decrypt(self, text: str) -> List[Token]:
        tokens = self._primary_parse(text)
        return Parser._restore_macros(tokens)

    def _primary_parse(self, text: str) -> List[Token]:
        tokens: List[Token] = []
        buffer = []
        current_type = None

        def flush():
            nonlocal buffer, current_type
            if not buffer:
                return
            tokens.append(Token(current_type, buffer.copy()))
            buffer.clear()
            current_type = None

        for ch in text:
            if ch == " ":
                flush()
                tokens.append(Token(TokenType.SPACE, [" "]))
            elif ch.isdigit():
                if current_type not in (TokenType.NUMBER, TokenType.WORD):
                    flush()
                    current_type = TokenType.NUMBER
                buffer.append(int(ch))
            elif ch.isalpha() or ch in "{}#":
                if current_type != TokenType.WORD:
                    flush()
                    current_type = TokenType.WORD
                buffer.append(ch)
            else:
                flush()
                tokens.append(Token(TokenType.SYMBOL, [ch]))

        flush()
        return tokens

    # Restore ASCII macros inside WORD tokens.
    #
    #         Example:
    #         symbols = ['I', 1, 0, '#', 2, 'o', 'p', '#', 1, 1, 5, '#']
    #         →
    #         ['I', '{{10#2}}', 'o', 'p', '#', '{{115}}', '#']
    def _restore_macros(tokens):
        for token in tokens:
            if token.type is not TokenType.WORD:
                continue

            src = token.symbols
            result: list[Symbol] = []

            i = 0
            n = len(src)

            while i < n:
                sym = src[i]

                if isinstance(sym, int):
                    buffer: list[Symbol] = []
                    digits_only: list[int] = []

                    while i < n and (
                            isinstance(src[i], int) or src[i] == "#"
                    ):
                        buffer.append(src[i])
                        if isinstance(src[i], int):
                            digits_only.append(src[i])
                        i += 1

                    ascii_code = Parser._try_restore_ascii(digits_only)

                    if ascii_code is not None:
                        macro_text = "".join(
                            str(x) if isinstance(x, int) else x
                            for x in buffer
                        )
                        result.append(f"{{{{{macro_text}}}}}")
                    else:
                        result.extend(buffer)

                else:
                    result.append(sym)
                    i += 1

            token.symbols = result

        return tokens

    # Try to restore ASCII code from digit characters.
    #         '#' symbols are already removed before calling this method.
    def _try_restore_ascii(digits):
        for length in (3, 2):
            if len(digits) >= length:
                code = int("".join(str(d) for d in digits[:length]))
                if is_letter_ascii(code):
                    return code
        return None
