from engine.parser import Parser
from engine.renderer import render
from engine.tokens import TokenType


def test_parse_and_render_simple():
    text = "Hello 123"
    tokens = Parser().parse_for_encrypt(text)

    assert tokens[0].type == TokenType.WORD
    assert tokens[1].type == TokenType.SPACE
    assert tokens[2].type == TokenType.NUMBER

    assert render(tokens) == text
