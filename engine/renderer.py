from typing import List
from .tokens import Token, TokenType


def render(tokens: List[Token]) -> str:
    result = []

    for token in tokens:
        if token.type == TokenType.NUMBER:
            result.append("".join(str(d) for d in token.symbols))
        else:
            for sym in token.symbols:
                if isinstance(sym, str) and sym.startswith("{{") and sym.endswith("}}"):
                    result.append(sym[2:-2])  # {{101}} -> 101
                else:
                    result.append(str(sym))

    return "".join(result)
