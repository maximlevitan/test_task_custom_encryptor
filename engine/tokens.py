from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class TokenType(Enum):
    WORD = "word"
    NUMBER = "number"
    SPACE = "space"
    SYMBOL = "symbol"


Symbol = Union[str, int]
# str: character letter, special symbol [!,.?...], macros "{{101}}", "#"
# int: digits (0–9)


@dataclass
class Token:
    type: TokenType
    symbols: List[Symbol]

    def __repr__(self) -> str:
        return f"Token(type={self.type.value}, symbols={self.symbols})"
